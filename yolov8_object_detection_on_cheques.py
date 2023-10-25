# -*- coding: utf-8 -*-
"""yolov8-object-detection-on-cheques.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wpwP4H_dlWq9yvMifYAX5D03mLM0EpCe
"""

!nvidia-smi

import os
HOME = os.getcwd()
print(HOME)

!pip install ultralytics==8.0.20

from IPython import display
display.clear_output()

import ultralytics
ultralytics.checks()

# Git clone method (for development)

# %cd {HOME}
# !git clone github.com/ultralytics/ultralytics
# %cd {HOME}/ultralytics
# !pip install -e .

# from IPython import display
# display.clear_output()

# import ultralytics
# ultralytics.checks()

from ultralytics import YOLO

from IPython.display import display, Image

"""yolo"""

# Commented out IPython magic to ensure Python compatibility.
!mkdir {HOME}/datasets
# %cd {HOME}/datasets

!pip install roboflow --quiet

from roboflow import Roboflow
rf = Roboflow(api_key="GqRnfdLze9mzBCO6Y4Ps")
project = rf.workspace("rmk-engineering-college").project("cheque-veket")
dataset = project.version(1).download("yolov8")

"""## Custom Training"""

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}

!yolo task=detect mode=train model=yolov8s.pt data={dataset.location}/data.yaml epochs=25 imgsz=800 plots=True

!ls {HOME}/runs/detect/train/

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}
Image(filename=f'{HOME}/runs/detect/train/confusion_matrix.png', width=600)

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}
Image(filename=f'{HOME}/runs/detect/train/results.png', width=600)

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}
Image(filename=f'{HOME}/runs/detect/train/val_batch0_pred.jpg', width=600)

"""## Validate Custom Model"""

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}

!yolo task=detect mode=val model={HOME}/runs/detect/train/weights/best.pt data={dataset.location}/data.yaml

"""## Inference with Custom Model"""

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}
!yolo task=detect mode=predict model={HOME}/runs/detect/train/weights/best.pt conf=0.06 source={dataset.location}/test/images save=True

import glob
from IPython.display import Image, display

for image_path in glob.glob(f'/content/runs/detect/predict/X_087_jpeg.rf.7a77dc782f5fe61125bfcd9718864db3.jpg')[:3]:
# for image_path in glob.glob(f'/content/cheque.png')[:3]:
      display(Image(filename=image_path, width=600))
      print("\n")

# project.version(dataset.version).deploy(model_type="yolov8", model_path=f"{HOME}/runs/detect/train/")

#While your deployment is processing, checkout the deployment docs to take your model to most destinations https://docs.roboflow.com/inference

#Run inference on your model on a persistant, auto-scaling, cloud API

#load model
model = project.version(dataset.version).model
import torch

# Assuming you have the 'model' object
torch.save(model, 'model.pth')
#choose random test set image
import os, random
# test_set_loc = dataset.location + "/content/datasets/cheque-1/test"
# random_test_image = random.choice(os.listdir(test_set_loc))
random_test_image = "/content/datasets/cheque-1/test/images/X_087_jpeg.rf.7a77dc782f5fe61125bfcd9718864db3.jpg"
print("running inference on " + random_test_image)
pred = model.predict(random_test_image, confidence=6, overlap=30).json()
pred

predictions = pred['predictions']

for prediction in predictions:
    x = prediction['x']
    y = prediction['y']
    width = prediction['width']
    height = prediction['height']
    class_label = prediction['class']
    confidence = prediction['confidence']

    x = int(x)
    y = int(y)
    width = int(width)
    height = int(height)

    print('Bounding Box:', (x, y, width, height))
    print('Confidence:', confidence)
    print('Class Label:', class_label)


    # print(f'x: {x}, y: {y}, width: {width}, height: {height}')

predictions = pred['predictions']

for prediction in predictions:
    x = prediction['x']
    y = prediction['y']
    width = prediction['width']
    height = prediction['height']
    class_label = prediction['class']
    confidence = prediction['confidence']

    x = int(x)
    y = int(y)
    width = int(width)
    height = int(height)

    print('Bounding Box:', (x, y, width, height))
    print('Confidence:', confidence)
    print('Class Label:', class_label)

    # Convert bounding box coordinates to (x1, y1, x2, y2) format
    bbox = xywh2xyxy(torch.tensor([x, y, width, height]))

    x1, y1, x2, y2 = bbox.tolist()

    # Draw bounding box on the image
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Write class label and confidence on the image
    label = f'{class_label}: {confidence:.2f}'
    cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

# Display the image with bounding boxes and labels
from google.colab.patches import cv2_imshow
cv2_imshow(img)
cv2.waitKey(0)
cv2.destroyAllWindows()

import cv2
import torch
import numpy as np
from google.colab.patches import cv2_imshow

def xywh2xyxy(x):
    # """
    # Convert bounding box coordinates from (x, y, width, height) format to (x1, y1, x2, y2) format where (x1, y1) is the
    # top-left corner and (x2, y2) is the bottom-right corner.

    # Args:
    #     x (np.ndarray | torch.Tensor): The input bounding box coordinates in (x, y, width, height) format.
    # Returns:
    #     y (np.ndarray | torch.Tensor): The bounding box coordinates in (x1, y1, x2, y2) format.
    # """
    y = x.clone() if isinstance(x, torch.Tensor) else np.copy(x)
    y[..., 0] = x[..., 0] - x[..., 2] / 2  # top left x
    y[..., 1] = x[..., 1] - x[..., 3] / 2  # top left y
    y[..., 2] = x[..., 0] + x[..., 2] / 2  # bottom right x
    y[..., 3] = x[..., 1] + x[..., 3] / 2  # bottom right y
    return y

predictions = pred['predictions']

for prediction in predictions:
    x = prediction['x']
    y = prediction['y']
    width = prediction['width']
    height = prediction['height']
    class_label = prediction['class']
    confidence = prediction['confidence']

    x = int(x)
    y = int(y)
    width = int(width)
    height = int(height)

    print('Bounding Box:', (x, y, width, height))
    print('Confidence:', confidence)
    print('Class Label:', class_label)

    # Convert bounding box coordinates to (x1, y1, x2, y2) format
    bbox = xywh2xyxy(torch.tensor([x, y, width, height]))

    x1, y1, x2, y2 = bbox.tolist()

    # Draw bounding box on the image
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Crop the bounding box region

    if(class_label == 'micr'):
      crop = img[y1:y2, x1:x2]

    # Display the cropped image
      cv2_imshow(crop)
      cv2.waitKey(0)
      cv2.destroyAllWindows()
      print(pytesseract.image_to_string(crop,lang='eng'))

    label = f'{class_label}: {confidence:.2f}'
    cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

# Display the image with bounding boxes and labels
print("")
cv2_imshow(img)
cv2.waitKey(0)
cv2.destroyAllWindows()

