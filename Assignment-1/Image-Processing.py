import cv2
import numpy as num

image= cv2.imread("C:\\Users\\Dell\\Downloads\\free-nature-images.jpg")
print(image.shape)
print(image[2][3])

blue_channel=image[:,:,0]
green_channel=image[:,:,1]
red_channel=image[:,:,2]

shape= image.shape

z=num.zeros((image.shape[0],image.shape[1]))
image[:,:,0]=z
image[:,:,2]=z


sub_image=image[0:75,0:50,:]
image[100:175,51:101,:]=sub_image
cv2.imshow("sub_image",image[100:175,51:101,:])

cv2.waitKey(0)
