import time
start_time = time.time()
import argparse
import os
import sys
import os.path
import cv2
import extracting_candidate_frames
import clustering_with_hdbscan
# from multiprocessing import Pool, Process, cpu_count
import logging


logging.basicConfig(filename='./logs/key_frames.log',format='%(asctime)s  %(levelname)s:%(message)s',level=logging.DEBUG)
logging.info('---------------------------------------------------------------------------------------------------------')


def main(argv):
    input_videos = argv[1]
    output_folder_video_image = "candidate_frames_and_their_cluster_folder"
    output_folder_video_final_image = "final_images"

    logging.info('file execution started for input video {}'.format(input_videos))
    vd = extracting_candidate_frames.FrameExtractor()
    if not os.path.isdir(input_videos.rsplit( ".", 1 )[ 0 ]):
        os.makedirs(input_videos.rsplit( ".", 1 )[ 0 ] + '/' + output_folder_video_image)
        os.makedirs(input_videos.rsplit( ".", 1 )[ 0 ] + '/' + output_folder_video_final_image)
    fps, imgs=vd.extract_candidate_frames(input_videos)
    """
    for counter, img in enumerate(imgs):
        _i, img = img[1], img[0]
        vd.save_frame_to_disk(
            img,
            file_path=os.path.join(input_videos.rsplit( ".", 1 )[ 0 ],output_folder_video_image),
            file_name=str(_i)+"_" + str(counter),
            file_ext=".jpeg",
        )
    """
    final_images = clustering_with_hdbscan.ImageSelector()
    imgs_final = final_images.select_best_frames(imgs,os.path.join(input_videos.rsplit( ".", 1 )[ 0 ],output_folder_video_image))
    #for counter, i, k in enumerate(imgs_final):
    for counter, i in enumerate(imgs_final):
        vd.save_frame_to_disk(
            i[0],
            file_path=os.path.join(input_videos.rsplit( ".", 1 )[ 0 ],output_folder_video_final_image),
            #file_name=argv[1].split(".")[0]+"_"+str(duration)+"_"+str(len(imgs)+1)+"_" + str(i[1])+"_"+str(duration*int(i[1])/(len(imgs)+1)),
            file_name=argv[1].split(".")[0]+"_"+str(float(i[2])/fps),
            file_ext=".jpeg",
        )

if __name__ == "__main__":
    main(sys.argv)
