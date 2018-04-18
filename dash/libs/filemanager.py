#!/usr/bin/env python
#   Program:
#       Functions to monitor files and folders
#   Author:
#       Wen-Chih, MosQuito, Lo
#   Date:
#       2017.4.18

import os
import sys

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError:
        print >> sys.stderr, 'Folder %s already exsits.' % path
        pass


def clean_exsited_files(tmp_path, output_path, seg_id):
    # Remove files at first
    try:
        rm_temp_mp4 = tmp_path + "temp_" + str(seg_id) + ".mp4" 
        os.remove(rm_temp_mp4)
    except OSError:
        print >> sys.stderr, 'File %s do not exsit.' % rm_temp_mp4
        pass

    try:
        rm_temp_hvc = tmp_path + "temp_" + str(seg_id) + "_track1.hvc"
        os.remove(rm_temp_hvc)
    except OSError:
        print >> sys.stderr, 'File %s do not exsit.' % rm_temp_hvc
        pass 

    try:
        rm_output = output_path + "output_" + str(seg_id) + ".mp4"
        os.remove(rm_output)
    except OSError:
        print >> sys.stderr, 'File %s do not exsit.' % rm_output
        pass
