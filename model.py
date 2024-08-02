from ultralytics import YOLO
import cv2

model = YOLO('yolov8.yaml')

model.train(data="/Users/danielletran/Downloads/boxing.v1i.yolov8/data.yaml", epochs=1)
print('ran')
model.save("/Users/danielletran/Downloads/boxing.v1i.yolov8/trained_data.pt",)

print('successfully completed training')
