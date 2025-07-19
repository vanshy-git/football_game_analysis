from ultralytics import YOLO
import supervision as sv
import pickle
import os

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