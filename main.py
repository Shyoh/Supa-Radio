from turtle import back
import cv2 
import math
import numpy as np
from scipy.ndimage import rotate
import utils

# helpful constants
all_white = np.full((1080, 1920, 3), 255)


# video setings
fps = 24
video_len = 30

def blur(img, size):
    # generating the kernel
    img = np.zeros((size, size))
    img[int((size-1)/2), :] = np.ones(size)
    img = img / size

def main():

    # resize background image
    utils.image3 = cv2.resize(utils.image3,(1920,1080), interpolation= cv2.INTER_LINEAR)
    utils.place(utils.image3,all_white,0,0,np.full((1080, 1920, 3), .3))

    blur = 13
    vinyl_size = 517
    vinyl_center_y = 400
    # making alpha channel for glow
    glow = utils.make_vinyl(utils.image, vinyl_size)
    glow = cv2.copyMakeBorder(glow, blur, blur, blur, blur, cv2.BORDER_CONSTANT)
    glow_alpha = utils.get_alpha(glow)
    glow_alpha = cv2.blur(glow_alpha, (blur,blur))
    # change glow back to full image, not circle cropped
    glow = cv2.resize(utils.image,(vinyl_size,vinyl_size))
    glow = cv2.copyMakeBorder(glow, blur, blur, blur, blur, cv2.BORDER_REFLECT)
    glow = cv2.blur(glow, (blur,blur))
    glow = utils.brighten(glow, 40, 40)

    

    
    vinyl = utils.make_vinyl(utils.image, 500)

    vinyl_with_glow = utils.overlay(glow, vinyl, vinyl_size,vinyl_size,10, utils.get_alpha(vinyl))
    vinyl_with_glow = cv2.copyMakeBorder(vinyl_with_glow, blur, blur, blur, blur, cv2.BORDER_REFLECT)
    # 

            

    # Window name in which image is displayed
    window_name = 'image'
    size = (1920,1080)

    rot = vinyl_with_glow
    out = cv2.VideoWriter('bahbahbahbah.mp4',cv2.VideoWriter_fourcc(*'DIVX'), 24, size)
    
    rotamt = 0
    grow = 1

    res_vinyl = cv2.resize(vinyl_with_glow, (1,1), interpolation=cv2.INTER_AREA)
    res_alpha = cv2.resize(glow_alpha, (1,1),interpolation=cv2.INTER_AREA)


    vidcap = cv2.VideoCapture('./videos/animation.mp4')
    res_animation_frame = None

    for i in range(video_len * fps):
        print("frame:", i)
        success, next_animation_frame = vidcap.read()
        if success:
            res_animation_frame = next_animation_frame

        rotamt -= .5
        res_vinyl = rotate(vinyl_with_glow, rotamt, reshape=False)
        res_alpha = glow_alpha
        if i <= 24:
            res_vinyl = cv2.resize(res_vinyl,(1,1),interpolation=cv2.INTER_AREA)
            res_alpha = cv2.resize(glow_alpha, (1,1),interpolation=cv2.INTER_AREA)

        if i > 24 and grow <= vinyl_with_glow.shape[0]:
            eased_size = 1 + round(utils.easeOutCubic(grow/vinyl_with_glow.shape[0]) * vinyl_with_glow.shape[0])
            res_vinyl = cv2.resize(res_vinyl,(eased_size, eased_size),interpolation = cv2.INTER_CUBIC)
            res_alpha = cv2.resize(glow_alpha, (eased_size, eased_size),interpolation = cv2.INTER_CUBIC)
            grow += 6
        dist_from_top = vinyl_center_y - round(res_vinyl.shape[0]/2)
        print("center pixel:", dist_from_top + round(res_vinyl.shape[0]/2))
        composite = utils.overlay(utils.image3, res_vinyl, 1920,1080,dist_from_top, res_alpha)
        utils.place(composite, all_white, 0, 0, np.divide(res_animation_frame,all_white))
        out.write(composite)
    out.release 
    # cv2.destroyAllWindows()
    # composite = overlay(image3, composite, 1920, 1080, 200)
    # cv2.imshow(window_name, composite)
    # cv2.waitKey(0)
    #     #closing all open windows 
    # cv2.destroyAllWindows() 

main()