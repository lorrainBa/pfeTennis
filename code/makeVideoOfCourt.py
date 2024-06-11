import cv2
from moviepy.editor import VideoFileClip, CompositeVideoClip
from associateCoordToRectangle import processFieldAndCoordonate, getImageImpact
from PIL import Image
import numpy as np
import os
import re

def merge_videos(video_path, output_video_path, overlay_video_path):
    if not os.path.exists(overlay_video_path):
        return

    main_clip = VideoFileClip(video_path)
    overlay_clip = VideoFileClip(overlay_video_path)
    overlay_clip = overlay_clip.resize(height=int(main_clip.h / 4))
    overlay_clip = overlay_clip.set_position(("right", "bottom"))
    final_clip = CompositeVideoClip([main_clip, overlay_clip])
    final_clip.write_videofile(output_video_path, codec="libx264", audio_codec="aac")

def get_frame_count_and_fps(video_path):
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        return None

    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)
    video.release()
    return frame_count, fps

def save_images(frames, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for i, frame in enumerate(frames):
        cv2.imwrite(os.path.join(folder_path, f"{i}.png"), frame)

def create_video_from_images(image_folder, output_path, fps):
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    images.sort(key=lambda x: int(re.findall(r'\d+', x)[0]))
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))
    
    cv2.destroyAllWindows()
    video.release()

def generateVideoOfCourt(video_path, dictionnaryCoords, treeCoords, allAnnotedCoords, processedCoordonateData, rebound_positionsFrame, decalageX, decalageY):
    imageWithImpact = Image.open("data/terrain.png")
    numberOfFrame, fpsVideo = get_frame_count_and_fps(video_path)

    xList = processedCoordonateData[0]
    yList = processedCoordonateData[1]
    frameList = processedCoordonateData[2]

    generated_frames = []

    for frameNumber in range(numberOfFrame):
        if frameNumber in rebound_positionsFrame:
            impactX = rebound_positionsFrame[frameNumber][0]
            impactY = rebound_positionsFrame[frameNumber][1]
            imageWithImpact = getImageImpact(imageWithImpact, dictionnaryCoords, treeCoords, allAnnotedCoords, (impactX, impactY), (0, 255, 0))
        
        if frameNumber in frameList:
            indexFrame = np.where(frameList == frameNumber)[0]
            impactX = xList[indexFrame][0] - decalageX
            impactY = yList[indexFrame][0] - decalageY
            imageWithImpactAndCurrentBall = getImageImpact(imageWithImpact, dictionnaryCoords, treeCoords, allAnnotedCoords, (impactX, impactY), (255, 0, 0))
        
        else:
            imageWithImpactAndCurrentBall = imageWithImpact
        
        open_cv_image = cv2.cvtColor(np.array(imageWithImpactAndCurrentBall), cv2.COLOR_RGB2BGR)
        generated_frames.append(open_cv_image)

    video_name = os.path.basename(video_path)
    video_name_without_extension = os.path.splitext(video_name)[0]
    output_dir = f"output/{video_name_without_extension}"
    output_folder = f"{output_dir}/temp_frames"
    output_video_path = f"{output_dir}/{video_name_without_extension}OUTPUTmap.mp4"
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    save_images(generated_frames, output_folder)
    
    if not os.path.exists(os.path.dirname(output_video_path)):
        os.makedirs(os.path.dirname(output_video_path))
    create_video_from_images(output_folder, output_video_path, fpsVideo)
    
    final_output_path = f"{output_dir}/{video_name_without_extension}FINALoutput.mp4"
    if not os.path.exists(os.path.dirname(final_output_path)):
        os.makedirs(os.path.dirname(final_output_path))
    merge_videos(video_path, final_output_path, output_video_path)
