from utils import read_video, save_video
from trackers.tracker import Tracker






def main():
    video_frames = read_video("C:/Users/Vansh/OneDrive/Desktop/football_analysis/input_videos/08fd33_4.mp4")

    tracker=Tracker("C:/Users/Vansh/OneDrive/Desktop/football_analysis/models/best.pt")
    tracks=tracker.get_object_tracks(video_frames,
                                     read_from_snub=True,
                                     stub_path="C:/Users/Vansh/OneDrive/Desktop/football_analysis/stubs/tracks.pkl")
                                     
    save_video(video_frames, "C:/Users/Vansh/OneDrive/Desktop/football_analysis/output_videos/output.mp4")


if __name__=="__main__":
    main()