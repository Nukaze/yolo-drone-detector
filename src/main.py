import threading
import time
import cv2
import ultralytics
from ultralytics import YOLO

import torch

def main() -> None:
    # Check the version of the ultralytics
    ultralytics.checks()
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
        
    stop_trobber_event = threading.Event()    
    throbber_thread = threading.Thread(target=throbber_animation, args=(stop_trobber_event,))
    throbber_thread.start()
    
    
    # Set the source to the camera
    camera_index = 2
    
    try:
        # Start the AI model prediction
        result = model.track(
            source=camera_index,
            classes=[4,],
            show_labels=True,
            show_conf=True,
            conf=0.5,
            show=True,
            stream=True,
            verbose=False
            save_txt=True,
        )
        
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
    
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt detected. Stopping the throbber and exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Stop the throbber animation
        stop_trobber_event.set()
        throbber_thread.join()
        print("Program exited")
        
def is_cuda_available() -> bool:
    # Check if CUDA is available
    return torch.cuda.is_available()
    
def throbber_animation(stop_event) -> None:
    throbber = ["|", "/", "-", "\\"]
    count = 0
    while not stop_event.is_set():
        print("AI Tracking " + throbber[count % len(throbber)], end="\r")
        count += 1
        time.sleep(0.1)
        
    print("throbber animation stopped")

if __name__ == '__main__':
    main()