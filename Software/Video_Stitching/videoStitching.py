import cv2
import numpy as np
from multiprocessing import Pool   ## used pool for parallel cpu and multiframe processing (faster)
from PyQt6.QtWidgets import QApplication, QFileDialog

def loadVideo(video_path):         ## get vid from path
    capture= cv2.VideoCapture(video_path)  ## read frames using videocapture()
    if not  capture.isOpened():
     print('video not opened')
     return None
    return capture

def STITCH(leftFrame , RightFrame):      ## stitching proccess begins
    stitcher= cv2.Stitcher_create(cv2.Stitcher_PANORAMA)        ##use panorama stitching algorithm to combine every frame to form output fram
    status ,stitched= stitcher.stitch([leftFrame, RightFrame])
    if status !=cv2.Stitcher_OK:        # check status of stitching proccess
          print('frame processing error status number:',status)
          return None
    return stitched   ## o/p stitched image frames

# EL STATUS NUMBER ERRORS ELLY MOMKEN TZHARR :

# cv2.Stitcher_ERR_NEED_MORE_IMG: 0
# cv2.Stitcher_ERR_HOMOGRAPHY_EST_FAIL: 1
# cv2.Stitcher_ERR_CAMERA_PARAMS_ADJUST_FAIL: 2
# cv2.Stitcher_ERR_FEATURE_FIND_FAIL: 3
# cv2.Stitcher_ERR_FEATURE_MATCH_FAIL: 4
# cv2.Stitcher_ERR_PANO_CONFlict: 5
# cv2.Stitcher_ERR_IMAGE_REGISTRATION_FAIL: 6
# cv2.Stitcher_ERR_NEED_MORE_IMG_ERROR: -1
# cv2.Stitcher_ERR_HOMOGRAPHY_EST_FAIL_ERROR: -2
# cv2.Stitcher_ERR_CAMERA_PARAMS_ADJUST_FAIL_ERROR: -3

##  frame resizing :
def resize_frame(frame, width, height):
    return cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

def stitch_frame_pair(args):
    leftFrame ,RightFrame ,target_width , target_height= args
    StitchedFrame = STITCH(leftFrame, RightFrame)
    if not StitchedFrame is None:
        return resize_frame(StitchedFrame, target_width, target_height)
    else:
        return None

def combineVideo(leftVideo,rightVideo , output_path ,target_width ,target_height):
    leftCapture =loadVideo(leftVideo)
    rightCapture =loadVideo(rightVideo)

    if leftCapture is None or rightCapture is None:
        return 0
    FPS= int(leftCapture.get(cv2.CAP_PROP_FPS))
    Vidformat= cv2.VideoWriter_fourcc(*'mp4v')    #o/p vid format
    output =cv2.VideoWriter(output_path, Vidformat, FPS, (target_width, target_height))
    frame_pairs =[]
    while True:
        ret_left, frame_left = leftCapture.read()    ##read each left video frame
        ret_right, frame_right = rightCapture.read()   ## same for right video
        if not ret_left or not ret_right:
            break
        frame_pairs.append((frame_left, frame_right, target_width, target_height))

    with Pool() as pool:    ## use of paralel cpu processing of frames
        stitchedFrames = pool.map(stitch_frame_pair, frame_pairs)

    for frame in stitchedFrames:
        if frame is not None:
            output.write(frame)
    leftCapture.release()
    rightCapture.release()
    output.release()
    displayVideos(leftVideo, rightVideo, output_path)

def displayVideos(leftVideo, rightVideo, output_path):
    while True:
        leftCapture = cv2.VideoCapture(leftVideo)
        rightCapture = cv2.VideoCapture(rightVideo)
        stitchedCapture = cv2.VideoCapture(output_path)

        while True:   ###loop aslong as code running
            ret_left, leftFrame = leftCapture.read()
            ret_right, rightFrame = rightCapture.read()
            ret_stitched, stitchedFrame = stitchedCapture.read()

            if not ret_left or not ret_right or not ret_stitched:
                break
            res_LeftFrame = resize_frame(leftFrame, 640, 360)   ## res ->resize
            res_RightFrame = resize_frame(rightFrame, 640, 360)
            frame_stitched_resized = resize_frame(stitchedFrame, 1280, 360)

            combined_top = np.hstack((res_LeftFrame,res_RightFrame))     # l/r vid horizontal
            combined_video= np.vstack((combined_top,frame_stitched_resized))   #o/p  vertical

            cv2.imshow('Stitched Video Output',combined_video)

# reset if q pressedd  / close window
            if cv2.waitKey(1) & 0xFF == ord('q'):
             break
        leftCapture.release()
        rightCapture.release()
        stitchedCapture.release()

        if cv2.waitKey(1) & 0xFF == ord('q'):
               break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    app =QApplication([])
    leftVideo ,x =QFileDialog.getOpenFileName(None,"LEFT VIDEO" )
    rightVideo ,Y =QFileDialog.getOpenFileName(None,"RIGHT VIDEO ")
    output_path= "outputStitched_new.mp4"
    target_width= 1300
    target_height= 700

    if leftVideo and rightVideo:
        combineVideo(leftVideo, rightVideo, output_path, target_width,target_height)