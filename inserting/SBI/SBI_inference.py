import cv2
import torch
import torchvision
import numpy as np
from inserting.SBI.model import Detector
from retinaface.pre_trained_models import get_model
from inserting.SBI.preprocess import extract_face, extract_frames


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = Detector()
model = model.to(device)
if torch.cuda.is_available():
	cnn_sd = torch.load("inserting/SBI/w.tar")["model"]
else:
	cnn_sd = torch.load("inserting/SBI/w.tar", map_location='cpu')["model"]
model.load_state_dict(cnn_sd)
model.eval()
vid_face_detector = get_model("resnet50_2020-07-20", max_size=2048,device=device)
vid_face_detector.eval()


def SBI_video(video):
	face_list, idx_list = extract_frames(video, 32, vid_face_detector)
	with torch.no_grad():
		img = torch.tensor(face_list).to(device).float()/255
		pred=model(img).softmax(1)[:,1]
	pred_list = []
	idx_img = -1
	for i in range(len(pred)):
		if idx_list[i] != idx_img:
			pred_list.append([])
			idx_img = idx_list[i]
		pred_list[-1].append(pred[i].item())
	pred_res = np.zeros(len(pred_list))
	for i in range(len(pred_res)):
		pred_res[i] = max(pred_list[i])
	pred = pred_res.mean()
	return round(pred*100)


def SBI_image(image):
	frame = cv2.imread(image)
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	face_detector = get_model("resnet50_2020-07-20", max_size=max(frame.shape),device=device)
	face_detector.eval()
	face_list = extract_face(frame,face_detector)
	with torch.no_grad():
		img = torch.tensor(face_list).to(device).float()/255
		torchvision.utils.save_image(img, f'test.png', nrow=8, normalize=False)#, range=(0, 1))
		pred = model(img).softmax(1)[:,1].cpu().data.numpy().tolist()
	return round(max(pred)*100)
