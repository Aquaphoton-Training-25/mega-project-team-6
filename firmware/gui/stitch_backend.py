
import cv2
import numpy as np
from multiprocessing import Pool
from PyQt6.QtWidgets import QApplication, QFileDialog



class StitchBackend:
    def stitch_videos(self):
        leftVideo, _ = QFileDialog.getOpenFileName(None,"left vid")
        rightVideo, _ = QFileDialog.getOpenFileName(None,"right vid")
        if leftVideo and rightVideo:
            output_path = "outputStitched_new.mp4"
            target_width = 1300
            target_height = 700
            self.combineVideo(leftVideo, rightVideo, output_path, target_width, target_height)

    def loadVideo(self, video_path):
        capture = cv2.VideoCapture(video_path)
        if not capture.isOpened():
            print('video not opened')
            return None
        return capture

    def STITCH(self, leftFrame, rightFrame):
        stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)
        status, stitched = stitcher.stitch([leftFrame, rightFrame])
        if status != cv2.Stitcher_OK:
            print('error status number :', status)
            return None
        return stitched

    def resize_frame(self, frame, width, height):
        return cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

    def stitch_frame_pair(self, args):
        leftFrame, RightFrame, target_width, target_height = args
        StitchedFrame = self.STITCH(leftFrame, RightFrame)
        if StitchedFrame is not None:
            return self.resize_frame(StitchedFrame, target_width, target_height)
        else:
            return None

    def combineVideo(self, leftVideo, rightVideo, output_path, target_width, target_height):
        leftCapture = self.loadVideo(leftVideo)
        rightCapture = self.loadVideo(rightVideo)

        if leftCapture is None or rightCapture is None:
            return 0

        FPS = int(leftCapture.get(cv2.CAP_PROP_FPS))
        Vidformat = cv2.VideoWriter_fourcc(*'mp4v')
        output = cv2.VideoWriter(output_path, Vidformat, FPS, (target_width, target_height))
        frame_pairs = []

        while True:
            ret_left, frame_left = leftCapture.read()
            ret_right, frame_right = rightCapture.read()
            if not ret_left or not ret_right:
                break
            frame_pairs.append((frame_left, frame_right, target_width, target_height))

        with Pool() as pool:
            stitchedFrames = pool.map(self.stitch_frame_pair, frame_pairs)

        for frame in stitchedFrames:
            if frame is not None:
                output.write(frame)
        leftCapture.release()
        rightCapture.release()
        output.release()

        self.displayVideos(output_path)

    def displayVideos(self, output_path):
        print(f"saved as{output_path}")