# Deepfake Detection

This repository contains the source code of the website developed to commercialize our research on deepfake detection using deep learning. Our research paper detailing this work is currently under peer-review at the 22nd International ISCISC Conference.

## Model Results

| Model                | Train Dataset | Test Dataset | AUC  |
|-----------------------|---------------|--------------|------|
| SBI (FFraw)           | FF++          | CDF-Test     | 93.83|
| SBI (FFc23)            | FF++          | CDF-Test     | 92.92|
| LAA-Net         | FF++          | CDF-Test     | 94.03|
| Fine-Tuned SBI (ours) | CDF-Train     | CDF-Test     | 99.87|
| Fine-Tuned LAA-Net (ours) | CDF-Train     | CDF-Test     | 99.94|

## Notes
- The weights of our models and the training source code are not publicly available at this time. If you need access, please send a request to [morteza24mail@protonmail.com](mailto:morteza24mail@protonmail.com).
