import os
import numpy
import math
import subprocess
import cv2

PIXEL_MAX = 255.0
NUM_POINTS = 655362

def SPsnrCalc(video, user_id, seg_id, bitrate, mode):
    global tmp_path
    tmp_path = "./tmp_"+ video + '_user' + user_id + '_' + str(seg_id) + '_' + bitrate + '_' + mode + '/'

    global output_path
    output_path = "./output_" + video + '_user' + user_id + '_' + str(seg_id) + '_' + bitrate + '_' + mode + '/'

    global frame
    frame_path = "./frame_" + video + '_user' + user_id + '_' + str(seg_id) + '_' + bitrate + '_' + mode + '/'

    # reconstruct yuv
    mp4_path = "output_" + video + '_user' + user_id + '_' + str(seg_id) + '_' + bitrate + "_TR.mp4"
    yuv_path = "rec_output_" + video + '_user' + user_id + '_' + str(seg_id) + '_' + bitrate + "_TR.yuv"
    conv2yuv = "ffmpeg -y -i " + output_path + mp4_path + " -c:v rawvideo -pix_fmt yuv420p " + output_path + yuv_path
    subprocess.call(conv2yuv, shell=True)

    # get the video infos
    vidcap = cv2.VideoCapture(output_path + mp4_path)
    if vidcap.isOpened():
        # get vidcap property 
        width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))    # get width 
        height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # get height
        fps = int(vidcap.get(cv2.CAP_PROP_FPS))              # get fps
        length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))   # get length

    depth = 3
    ratio = 2 # YUV420: (4Y+1Cb+1Cr) = 12 bits per pixel
    frame_size = int(width * height * depth / ratio) # bytes per frame

    # original yuv
    ori_path = "ori_output_" + video + '_user' + user_id + '_' + str(seg_id) + '_' + bitrate + "_TR.yuv"
    with open("./360videos_60s/" + video + "_equir.yuv", 'rb') as vid_in:
        vid_in.seek( (int(seg_id) - 1) * 64 * frame_size )
        for i in range(0, length):
            # read data from yuv file
            frame_data = vid_in.read(frame_size)
            output_frame = open(output_path + ori_path, "a")
            output_frame.write(frame_data)

    calSPsnr =  "TApp360ConvertStatic --InputFile=" + output_path + ori_path + " --InputBitDepth=8 --SourceWidth=" + str(width) + " --SourceHeight=" + str(height) + " --FrameRate=" + str(fps) + ' --InputGeometryType=0 --SourceFPStructure="1 1   0 0" --InternalBitDepth=8 --OutputBitDepth=8 --FrameSkip=0 --FramesToBeEncoded=' + str(length) + " --OutputFile=" + output_path + ori_path + " --CodingGeometryType=0 --CodingFaceWidth=" + str(width) + " --CodingFaceHeight=" + str(height) + ' --CodingFPStructure="1 1   0 0" --RefFile=' + output_path + yuv_path + " --ReferenceBitDepth=8 --ReferenceFaceWidth=" + str(width) + " --ReferenceFaceHeight=" + str(height) + " --ReferenceGeometryType=0 --SphFile=./metrics/sphere_655362.txt" + " 2>&1 | tee -a " + "./PSNR/psnr_" + video +'_user'+ user_id + '_' + str(seg_id) + '_' + bitrate + "_TR.csv"
    subprocess.call(calSPsnr, shell=True)

    ## If file exists, delete it ##
    if os.path.isfile(output_path + yuv_path):
        os.remove(output_path + yuv_path)

    ## If file exists, delete it ##
    if os.path.isfile(output_path + ori_path):
        os.remove(output_path + ori_path)
