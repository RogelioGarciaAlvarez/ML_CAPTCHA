import cv2
import matplotlib.path as mplPath
import numpy as np
import torch

ZONE = np.array([
    [521, 562],
    [1324, 505],
    [1891, 822],
    [679, 847],
]) 


def get_center(bbox):
    #xmin, ymin, xmax, ymax
    #0      1      2     3
    center = ((bbox[0] + bbox[2]) // 2, (bbox[1]+bbox[3]) // 2)
    return center
    
    
def load_model():
    
    model = torch.hub.load("ultralytics/yolov5", model="yolov5n", pretrained=True)
    return model

def get_bboxes(preds: object):
    #xmin, ymin, xmax, ymax
    df = preds.pandas().xyxy[0]
    df = df[df["confidence"]>=0.2]
    df = df[df["name"] == "car"]
    
    return df[["xmin", "ymin", "xmax", "ymax"]].values.astype(int)

def is_valid_detection(xc, yc):
    
    return mplPath.Path(ZONE).contains_point((xc,yc))

def detector (cap:object):
    
    model = load_model()
    
    while cap.isOpened():
        
        status, frame = cap.read()
        
        if not status:
            break
    
        preds = model(frame)
        bboxes = get_bboxes(preds)
        
        detections = 0
        for box in bboxes:
            xc, yc = get_center(box)
            
            if is_valid_detection(xc, yc):
                detections += 1
                
            cv2.circle(img=frame, center=(xc,yc), radius=2, color=(0,255,0), thickness=-1)
            cv2.rectangle(img=frame, pt1=(box[0], box[1]), pt2 = (box[2], box[3]), color = (255,0,0), thickness=1)
    
        cv2.putText(img=frame, text=f"Coches: {detections}", org=(150,100), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=3, color=(0,0,255), thickness=3)
        cv2.polylines(img=frame, pts=[ZONE], isClosed=True, color=(0,0,255), thickness=4)
        
        cv2.imshow("frame", frame)
    
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    
    cap.release()
    
if __name__ == '__main__':
        
    cap = cv2.VideoCapture("data/coches.mp4")
    
    detector(cap)
                               
