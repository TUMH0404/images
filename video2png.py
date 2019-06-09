# -*- coding: utf-8 -*-
import os.path
import sys
import cv2
import os
import numpy as np
import glob
import pickle
#動画ファイルを読み込む


def VIDEOtoPNG(dir_name,k):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    
    video = cv2.VideoCapture(k)
    ##
    f_fps = video.get(cv2.CAP_PROP_FPS)
    f_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    f_height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    f_width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    dat = {"f_fps":f_fps,"f_count":f_count,"f_height":f_height,"f_width":f_width}
    with open(f"./{dir_name}/info.pickle","wb") as d:
        pickle.dump(dat,d)
    ##
    for i in range(int(f_count)):

        _, frame=video.read()
        cv2.imwrite(f'./{dir_name}/r{i:06d}.png',frame)

        
def PNGtoVIDEO(dir_name,k,fps=30):
    
    files = glob.glob(dir_name+"/*.png")
    files.sort()
    
    ll = glob.glob(f"{dir_name}/*.pickle")
    if len(ll)==1:
        with open(f"{dir_name}/info.pickle","rb") as d:
            ab = pickle.load(d)
        
        w = int(ab["f_width"])
        h = int(ab["f_height"])
        fps = int(ab["f_fps"])
    
    else:
        h,w,_ = cv2.imread(files[0]).shape
        
    fourcc =cv2.VideoWriter_fourcc('m','p','4','v')
    video=cv2.VideoWriter(k,fourcc,int(fps),(w,h))


    for i in files:
        img=cv2.imread(i)
        video.write(img)

    video.release()
        
if __name__ == '__main__':
    args = sys.argv
    if args[1]=="VIDEOtoPNG":
        dname = args[2]
        kname = args[3]
        VIDEOtoPNG(dname,kname)
    elif args[1]=="PNGtoVIDEO":
        dname = args[2]
        kname = args[3]
        #FPS = args[4]
        PNGtoVIDEO(dname,kname)
    #print(args,dname,kname)