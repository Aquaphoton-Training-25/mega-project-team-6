#required pipelines

# 1. Calibration:
# 1. You need to compare each two images of the same scenario and select a set of matching
# features. You can use any inbuilt function for feature matching (SIFT and corner detection)
# 2. Then you need the estimate the Fundamental matrix using the features obtained, you can use
# inbuilt SVD function to solve for the fundamental matrix. You can use RANSAC method or the
# straight least square method to estimate the fundamental matrix.
# 3. From the fundamental matrix you need the Estimate Essential matrix by accounting for the
# calibration parameters. You can use the built-in functions or implement your own to estimate
# the Essential matrix and to recover the rotation/translational matrices.
# 4. Decompose the essential matrix into a translation and rotation.

# 2. Rectification:
# 1. Apply perspective transformation to make sure that the epipolar lines are horizontal for both
# the images. (Use the built-in functions for this purpose)
# 2. Print the homography matrices for both left and right images that will rectify the images.
# 3. Plot (Show) the epipolar lines on both images along with feature points.


# 3. Correspondence:
# 1. For each epipolar line, apply the matching windows concept (such as SSD or Cross correlation).
# 2. Calculate Disparity
# 3. Rescale the disparity to be from 0-255 and save the resulting image.
# 4. You need to save the disparity as a gray scale and color image using heat map conversion.


# 4. Compute Depth Image:
# 1. Using the disparity information obtained above, compute the depth information for each pixel
# image. The resulting depth image has the same dimensions of the disparity image, but it has
# depth information instead.
# 2. You need to save the depth image as a gray scale and color image using heat map conversion.

import cv2
import numpy as np

img1 = cv2.imread('im11.png', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('im00.png', cv2.IMREAD_GRAYSCALE)

# 1-Calibration

# 1:feature matching using SIFT
sift= cv2.SIFT_create()            #SIFT for feature matching and keypoints detection
keypoints_1 , desipator1= sift.detectAndCompute(img1,None)
keypoints_2 , desipator2=sift.detectAndCompute(img2,None)

#flann matcher  (to match keypoints on img)
index_params= dict(algorithm=1,trees=5)
search_params= dict(checks=50)
flann = cv2.FlannBasedMatcher(index_params,search_params)
matches =flann.knnMatch( desipator1 ,desipator2,k=2)

#lowes ratio test to compute the matches between the different features
good_matches =[]
for m, n in matches:
    if m.distance < 0.6 * n.distance:   #0.7 el match ratio
        good_matches.append(m)

# Draw matches
img_matches = cv2.drawMatches(img1, keypoints_1, img2, keypoints_2, good_matches, None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
cv2.imshow('matches',cv2.resize(img_matches,(1024,512)))
cv2.waitKey(0)
cv2.destroyAllWindows()

#fundamental Matrix ->show epipolar geometryy
#we get fund matrix from the keypoints coordinates using findFundamentalMat()
pts1= np.float32([keypoints_1[i.queryIdx].pt for i in good_matches])    #key points coordinates
pts2= np.float32([keypoints_2[i.trainIdx].pt for i in good_matches])

fundMatrix , mask = cv2.findFundamentalMat(pts1 ,pts2,cv2.FM_RANSAC)
pts1= pts1[mask.ravel()== 1]
pts2= pts2[mask.ravel()== 1]

#ESSENTIAL mat to encode the rotation and translation between cam0 and cam1
cam0= np.array([[5299.313,0, 1263.818],[0,5299.313,977.763] ,[0,0,1]])  #assume focal length and principal points
cam1= np.array([[5299.313,0, 1438.004],[0,5299.313,977.763] ,[0,0,1]])

#essential mat= cam1(transpose) * fundmental mat * cam0
essentialMatrix= cam1.T @ fundMatrix @ cam0

#decompose essential mat. to get rotation and translation using recoverPose()
x,rotationalMat ,transformMat,y = cv2.recoverPose(essentialMatrix,pts1,pts2,cam0)
print("rotation matrix: \n ", rotationalMat)
print("translation matrix: \n", transformMat)


#2-rectification -> to align image and make epi. lines parallel(on same horiontal line)
#rectify the images using fundamental mat with stereoRectifyUncalibrated() take 4 inputs->image points and fund matrix
rect_done,homographyMat_1,homographyMat_2= cv2.stereoRectifyUncalibrated(pts1,pts2,fundMatrix,img1.shape[:2])

if rect_done:  #warpperspective()-> change the perspective of all the image
      img1_rectified= cv2.warpPerspective(img1,homographyMat_1,img1.shape[:2][::-1])
      img2_rectified= cv2.warpPerspective(img2, homographyMat_2,img2.shape[:2][::-1])

      img_stack = np.hstack((img1_rectified, img2_rectified))
      cv2.imshow('rectified left image', cv2.resize(img1_rectified,(600,512)))
      cv2.imshow('rectified right image', cv2.resize(img2_rectified,(600,512)))
      cv2.waitKey(0)
      cv2.destroyAllWindows()
else:
 print("error in rectification")


print("left imagE homography matrix:\n", homographyMat_1)
print("right image homography matrix:\n", homographyMat_2)

def epipolarLines(img1, img2,lines1, lines2, pts1, pts2):
    r1, c1 = img1.shape
    r2, c2 = img2.shape
    img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
    img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)

#left image
    for r1, pt1 in zip(lines1, pts1):
        color = tuple(np.random.randint(0, 255, 3).tolist())
        x0, y0 = map(int, [0, -r1[2] / r1[1]])
        x1, y1 = map(int, [c1, -(r1[2] + r1[0] * c1) / r1[1]])
        img1 = cv2.line(img1, (x0, y0), (x1, y1), color,1)
        img1 = cv2.circle(img1, tuple(map(int, pt1)), 5, color,-1)
#right image
    for r2, pt2 in zip(lines2, pts2):
        color = tuple(np.random.randint(0, 255, 3).tolist())
        x0, y0 = map(int, [0, -r2[2] / r2[1]])
        x1, y1 = map(int, [c2, -(r2[2] + r2[0] * c2) / r2[1]])
        img2 = cv2.line(img2, (x0, y0), (x1, y1), color,1)
        img2 = cv2.circle(img2, tuple(map(int, pt2)),5, color, -1)

    return img1,img2

lines1 = cv2.computeCorrespondEpilines(pts2.reshape(-1, 1, 2), 2, fundMatrix)
lines1 = lines1.reshape(-1, 3)
lines2 = cv2.computeCorrespondEpilines(pts1.reshape(-1, 1, 2), 1, fundMatrix)
lines2 = lines2.reshape(-1, 3)

ep_imgLeft,ep_imgRight =epipolarLines(img1, img2, lines1, lines2, pts1, pts2)

cv2.imshow('left epipolar lines',cv2.resize(ep_imgLeft,(650,512)))
cv2.imshow('right epiolar lines', cv2.resize(ep_imgRight,(650,512)))
cv2.waitKey(0)
cv2.destroyAllWindows()
#3-correspondence
#disparity using StereoBM
stereo = cv2.StereoBM_create(numDisparities=128, blockSize=7) #block matching   #16,15
disparity = stereo.compute(img1_rectified, img2_rectified)
# Normalize disparity for visualization
disparity = cv2.normalize(disparity, disparity, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
disparity = np.uint8(disparity)
cv2.imshow('Disparity', cv2.resize(disparity,(1024,1024)))
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('disparity_grayscale.png', disparity)


#heatmap
disparity_color = cv2.applyColorMap(disparity, cv2.COLORMAP_JET)
cv2.imwrite('disparity_heatmap.png', disparity_color)
cv2.imshow('',disparity_color)
#4-depth image
# get depth using disparity
focal_length =1.0 #random value
baseline = 0.1   #random value(m)
depth= (focal_length*baseline)/ (disparity + 1e-6)
depth_grayscale = (depth - depth.min()) / (depth.max() - depth.min())#-->grayscale
depth_grayscale= (depth_grayscale * 255).astype(np.uint8)
cv2.imshow('Depth Map', cv2.resize(depth_grayscale, (1024, 512)))
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('depth_grayscale.png', depth_grayscale)
#heatmap
depth_color = cv2.applyColorMap(depth_grayscale, cv2.COLORMAP_JET)
cv2.imshow('depth_heatmap.png', depth_color)


