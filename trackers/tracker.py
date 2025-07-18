from ultralytics import YOLO
import supervision as sv
import pickle
import os
import cv2
import sys
import os
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import get_center_of_bbox, get_bbox_width


class Tracker:
    def __init__(self, model_path):
        self.model = YOLO(model_path) 
        self.tracker = sv.ByteTrack()

    def detect_frames(self, frames):
        batch_size=20 
        detections = [] 
        for i in range(0,len(frames),batch_size):
            detections_batch = self.model.predict(frames[i:i+batch_size],conf=0.1)
            detections += detections_batch
        
        return detections    
    

    def  get_object_tracks(self, frames,read_from_snub=False,stub_path=None):


        if read_from_snub and stub_path is not None and os .path.exists(stub_path):
            with open(stub_path, 'rb') as f:
                tracks = pickle.load(f)
            return tracks

        detections = self.detect_frames(frames)
        tracks={
            "players": [],
            "ball": [],
            "referees": [],
        }



        for frame_num, detection in enumerate(detections):
            cls_names= detection.names
            cls_names_inv = {v.lower(): k for k, v in cls_names.items()}

            print(cls_names)
            #convert supervision to detection format
            detection_supervision = sv.Detections.from_ultralytics(detection)


           
            


            #convert goalkeeper to player
            for object_ind, class_id in enumerate(detection_supervision.class_id):
             if cls_names[class_id].lower() == "goalkeeper":


                    detection_supervision.class_id[object_ind] = cls_names_inv["player"]

            #track the objects
            detection_with_tracks = self.tracker.update_with_detections(detection_supervision)



            tracks["players"].append({})
            tracks["ball"].append({})
            tracks["referees"].append({})

            for frame_detection in detection_with_tracks:
                bbox=frame_detection[0].tolist()
                class_id=frame_detection[3]
                track_id=frame_detection[4]
                   
                if class_id== cls_names_inv["player"]:
                    tracks["players"][frame_num][track_id] = bbox

                if class_id== cls_names_inv["ball"]:
                    tracks["ball"][frame_num][track_id] = bbox

                if class_id== cls_names_inv["referee"]:
                    tracks["referees"][frame_num][track_id] = bbox     

            for frame_detection in detection_supervision:
                bbox=frame_detection[0].tolist()
                class_id=frame_detection[3]
                
                if class_id== cls_names_inv["ball"]:
                    tracks["ball"][frame_num][0] = bbox

                       


        if stub_path is not None:
            
            with open(stub_path, 'wb') as f:
                pickle.dump(tracks, f)
            
        return tracks
    
    def draw_ellipse(self, frame, bbox, color, track_id=None):
        y2 = int(bbox[3])
        x_center, _ = get_center_of_bbox(bbox)
        x_center = int(x_center)  
        width = int(get_bbox_width(bbox))  

        cv2.ellipse(
        frame,
        center=(x_center, y2),
        axes=(width, int(0.35 * width)),
        angle=0.0,
        startAngle=-45,
        endAngle=235,
        color=color,
        thickness=2,
        lineType=cv2.LINE_4
    )
        
        rectangle_width = 40
        rectangle_height=20
        x1_rect = x_center - rectangle_width//2
        x2_rect = x_center + rectangle_width//2
        y1_rect = (y2- rectangle_height//2) +15
        y2_rect = (y2+ rectangle_height//2) +15

        if track_id is not None:
            cv2.rectangle(frame,
                          (int(x1_rect),int(y1_rect) ),
                          (int(x2_rect),int(y2_rect)),
                          color,
                          cv2.FILLED)
            
            x1_text = x1_rect+12
            if track_id > 99:
                x1_text -=10
            
            cv2.putText(
                frame,
                f"{track_id}",
                (int(x1_text),int(y1_rect+15)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,0,0),
                2
            )
        return frame
    
    def draw_traingle(self,frame,bbox,color):
        y= int(bbox[1])
        x,_ = get_center_of_bbox(bbox)

        triangle_points = np.array([
    [x, y],
    [x - 10, y - 20],
    [x + 10, y - 20],
], dtype=np.int32)

        cv2.drawContours(frame, [triangle_points],0,color, cv2.FILLED)
        cv2.drawContours(frame, [triangle_points],0,(0,0,0), 2)

        return frame





    def draw_annotations(self,video_frames, tracks):
        output_video_frames= []
        for frame_num, frame in enumerate(video_frames):
            frame = frame.copy()

            player_dict = tracks["players"][frame_num]
            ball_dict = tracks["ball"][frame_num]
            referee_dict = tracks["referees"][frame_num]

            # Draw Players
            for track_id, player in player_dict.items():
                color = (255, 0, 255)
                frame = self.draw_ellipse(frame, player, color, track_id)
            #draw referee
            for track_id, referee in referee_dict.items():
                color = (0,255, 255)
                frame = self.draw_ellipse(frame, referee, color, track_id)

            #draw ball
            for track_id, ball in ball_dict.items():
                color=(0,55,25)
                frame = self.draw_traingle(frame, ball, color)

            output_video_frames.append(frame)

        return output_video_frames    