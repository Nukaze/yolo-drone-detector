import cv2
from ultralytics import YOLO
import torch

def main():
    # Load the YOLO model
    model = YOLO("models/yolov8s.pt")
    
    # Check if CUDA is available and set the model to CUDA if it is
    if (is_cuda_available()):
        model.to("cuda")
        print("="*64)
        print("*** Model is processing on [CUDA] ***")
        print("="*64)
    else:
        model.to("cpu")
        print("="*64)
        print("*** Model is processing on [CPU] ***")
        print("="*64)
    
    # Set the source to the camera
    camera_index = 1
    
    # Start the AI model prediction
    result = model.predict(source=camera_index, conf=.5, show=True, stream=True)
    
    # Loop through the results for each frame
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
    # Check if CUDA is available
    return torch.cuda.is_available()
    


if __name__ == '__main__':
    main()