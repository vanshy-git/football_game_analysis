from utils import read_video, save_video
from trackers.tracker import Tracker
import cv2
from team_assigner import TeamAssigner
from player_ball_assigner import PlayerBallAssigner
import numpy as np







def main():
    video_frames = read_video("C:/Users/Vansh/OneDrive/Desktop/football_analysis/input_videos/08fd33_4.mp4")

    tracker=Tracker("C:/Users/Vansh/OneDrive/Desktop/football_analysis/models/best.pt")
    tracks=tracker.get_object_tracks(video_frames,
                                     read_from_snub=True,
                                     stub_path="C:/Users/Vansh/OneDrive/Desktop/football_analysis/stubs/tracks.pkl")
    
    tracks["ball"] = tracker.interpolate_ball_positions(tracks["ball"])
    

    team_assigner = TeamAssigner()
    team_assigner.assign_team_color(video_frames[0], 
                                    tracks['players'][0])
    
    for frame_num, player_track in enumerate(tracks['players']):
        for player_id, track in player_track.items():
            team_assigner.team_colors[team_assigner.get_player_team(video_frames[frame_num],   
                                                 track,
                                                 player_id)]
            

        # Assign Ball Aquisition
    player_assigner =PlayerBallAssigner()
    team_ball_control= []
    for frame_num, player_track in enumerate(tracks['players']):
        ball_bbox = tracks['ball'][frame_num][1]['bbox']
        assigned_player = player_assigner.assign_ball_to_player(player_track, ball_bbox)

        if assigned_player != -1:
            tracks['players'][frame_num][assigned_player]['has_ball'] = True
          
            
            


    for track_id, player in tracks['players'][0].items():
         bbox = player
         frame =video_frames[0]
         cropped_image = frame[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]
         cv2.imwrite(f"C:/Users/Vansh/OneDrive/Desktop/football_analysis/output_videos/cropped_image.jpg", cropped_image)
        
         break

    #draw object track
    output_video_frames= tracker.draw_annotations(video_frames,tracks)






    save_video(output_video_frames, "C:/Users/Vansh/OneDrive/Desktop/football_analysis/output_videos/output.mp4")


if __name__=="__main__":
    main()