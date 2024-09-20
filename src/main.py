import cv2
from ultralytics import YOLO
import torch

def main():
    model = YOLO("yolov8s.pt")
    if (is_cuda_available()):
        model.to("cuda")
        print("model is processing on cuda")
    else:
        model.to("cpu")
        print("model is processing on cpu")
        
    camera_index = 1
    result = model.predict(source=camera_index, conf=.5, show=True, stream=True)
    
    for res in result:
        
        boxes = res.boxes
        classes = boxes.cls.tolist()
        conf = [round(v, 2) for v in boxes.conf.tolist()]
        xyxy = boxes.xyxy.tolist()
        origin_shape = tuple(boxes.orig_shape)
        xywh = boxes.xywh.tolist()
        xywhn = boxes.xywhn.tolist()
        xyxy = boxes.xyxy.tolist()
        xyxyn = boxes.xyxyn.tolist()
        
    
def is_cuda_available():
    return torch.cuda.is_available()
    
    
if __name__ == '__main__':
    main()