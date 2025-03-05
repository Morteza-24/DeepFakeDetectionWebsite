import os
import sys
if not os.getcwd() in sys.path:
    sys.path.append(os.getcwd())
import cv2
import random
import torch
import torch.nn as nn
import numpy as np
from retinaface.pre_trained_models import get_model
from inserting.ai.package_utils.transform import final_transform, get_center_scale, get_affine_transform
from inserting.ai.configs.get_config import load_config
from inserting.ai.models import *
from inserting.ai.package_utils.image_utils import crop_by_margin
from inserting.ai.losses.losses import _sigmoid
# from inserting.ai.package_utils.utils import vis_heatmap


IMAGE_H, IMAGE_W= 256, 256
PADDING = 0.25
cfg = "inserting/ai/configs/my_single_test_efn4_fpn_sbi_adv.yaml"
cfg = load_config(cfg)
seed = cfg.SEED
random.seed(seed)
torch.manual_seed(seed)
np.random.seed(seed)
torch.cuda.manual_seed(seed)
task = cfg.TEST.subtask
flip_test = cfg.TEST.flip_test
device_count = torch.cuda.device_count()
model = build_model(cfg.MODEL, MODELS).to(torch.float64)
model = load_pretrained(model, cfg.TEST.pretrained)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
resnet_model = get_model("resnet50_2020-07-20", max_size=2048, device=device)
resnet_model.eval()
if device_count >= 1:
    model = nn.DataParallel(model, device_ids=cfg.TEST.gpus).cuda()
#else:
#    model = model.cuda()
test_file = cfg.TEST.test_file
video_level = cfg.TEST.video_level
aspect_ratio = cfg.DATASET.IMAGE_SIZE[1]*1.0 / cfg.DATASET.IMAGE_SIZE[0]
pixel_std = 200
rot = 0
transforms = final_transform(cfg.DATASET)
metrics_base = cfg.METRICS_BASE
model.eval()


def infer_image(image):
	image = cv2.imread(image)
	height, width = image.shape[:-1]
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	faces = resnet_model.predict_jsons(image)
	if len(faces) == 0:
		return "no face"
	for face_idx in range(len(faces)):
		x0, y0, x1, y1 = faces[face_idx]['bbox']
		face_w = x1 - x0
		face_h = y1 - y0
		f_c_x0 = max(0, x0 - int(face_w*PADDING))
		f_c_x1 = min(width, x1 + int(face_w*PADDING))
		f_c_y0 = max(0, y0 - int(face_h*PADDING))
		f_c_y1 = min(height, y1 + int(face_h*PADDING))
		face_crop = image[f_c_y0:f_c_y1, f_c_x0:f_c_x1, :]
	face_crop = cv2.resize(face_crop, (IMAGE_H, IMAGE_W), interpolation=cv2.INTER_LINEAR)
	img = crop_by_margin(face_crop, margin=[5, 5])
	c, s = get_center_scale(img.shape[:2], aspect_ratio, pixel_std=pixel_std)
	trans = get_affine_transform(c, s, rot, cfg.DATASET.IMAGE_SIZE, pixel_std=pixel_std)
	input = cv2.warpAffine(img,
							trans,
							(int(cfg.DATASET.IMAGE_SIZE[0]), int(cfg.DATASET.IMAGE_SIZE[1])),
							flags=cv2.INTER_LINEAR,
							)
	with torch.no_grad():
		img_trans = transforms(input/255)#.to(torch.float64)
		img_trans = torch.unsqueeze(img_trans, 0)
		if device_count > 0:
			img_trans = img_trans.cuda(non_blocking=True)
		outputs = model(img_trans)
		cls_outputs = outputs[0]['cls']
		# hm_outputs = outputs[0]['hm']
		# hm_preds = _sigmoid(hm_outputs).cpu().numpy()
		# if cfg.TEST.vis_hm:
		# 	print(f'Heatmap max value --- {hm_preds.max()}')
		# 	vis_heatmap(img, hm_preds[0], 'output_pred.jpg')
		label_pred = _sigmoid(cls_outputs).cpu().numpy()
	return f'{round(label_pred[0][-1]*100)}%'


def infer_video(video):
	cap = cv2.VideoCapture(video)
	frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	frame_idxs = np.linspace(0, frame_count - 1, 32, endpoint=True, dtype=np.int64)
	images = []
	for frame_idx in frame_idxs:
		cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
		ret, frame = cap.read()
		height, width = frame.shape[:-1]
		if not ret:
			print("frame read error")
			continue
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		faces = resnet_model.predict_jsons(frame)
		if len(faces) == 0:
			return "no face"
		face_s_max = -1
		score_max = -1
		for face_idx in range(len(faces)):
			x0, y0, x1, y1 = faces[face_idx]['bbox']
			face_w = x1 - x0
			face_h = y1 - y0
			face_s = face_w * face_h
			score = faces[face_idx]['score']
			if face_s > face_s_max and score > score_max:
				f_c_x0 = max(0, x0 - int(face_w*PADDING))
				f_c_x1 = min(width, x1 + int(face_w*PADDING))
				f_c_y0 = max(0, y0 - int(face_h*PADDING))
				f_c_y1 = min(height, y1 + int(face_h*PADDING))
				face_crop = frame[f_c_y0:f_c_y1, f_c_x0:f_c_x1, :]
				face_s_max = face_s
				score_max = score
		face_crop = cv2.resize(face_crop, (IMAGE_H, IMAGE_W), interpolation=cv2.INTER_LINEAR)
		img = crop_by_margin(face_crop, margin=[5, 5])
		c, s = get_center_scale(img.shape[:2], aspect_ratio, pixel_std=pixel_std)
		trans = get_affine_transform(c, s, rot, cfg.DATASET.IMAGE_SIZE, pixel_std=pixel_std)
		input = cv2.warpAffine(img,
								trans,
								(int(cfg.DATASET.IMAGE_SIZE[0]), int(cfg.DATASET.IMAGE_SIZE[1])),
								flags=cv2.INTER_LINEAR,
								)
		with torch.no_grad():
			img_trans = transforms(input/255)#.to(torch.float64)
			if device_count > 0:
				img_trans = img_trans.cuda(non_blocking=True)
			images.append(img_trans)
	cat_outputs = torch.tensor([])
	bs = cfg.TRAIN.batch_size * len(cfg.TRAIN.gpus)
	for i in range(0, 32, bs):
		with torch.no_grad():
			outputs = model(torch.stack(images[i:i+bs], dim=0))
			cls_outputs = outputs[0]['cls']
			cat_outputs = torch.cat([cat_outputs, cls_outputs])
			# hm_outputs = outputs[0]['hm']
			# hm_preds = _sigmoid(hm_outputs).cpu().numpy()
			# if cfg.TEST.vis_hm:
			# 	print(f'Heatmap max value --- {hm_preds.max()}')
			# 	vis_heatmap(img, hm_preds[0], 'output_pred.jpg')
	label_pred = _sigmoid(cat_outputs.mean()).cpu().numpy()
	return f'{round(label_pred*100)}%'
