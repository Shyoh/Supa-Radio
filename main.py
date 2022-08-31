
import cv2 
import numpy as np
from scipy.ndimage import rotate
import utils
import subprocess


# helpful constants
all_white = np.full((1080, 1920, 3), 255)



# video setings
fps = 24
video_len = 10 # video length in seconds
rotate_increment = utils.calculate_rotation_increment(video_len, fps)


def blur(img, size):
    # generating the kernel
    img = np.zeros((size, size))
    img[int((size-1)/2), :] = np.ones(size)
    img = img / size

def main(vimg, bgimg, dir):
    image = cv2.imread(r'{0}'.format(vimg))
    image3 = cv2.imread(r'{0}'.format(bgimg))



    # resize background image
    image3 = cv2.resize(image3,(1920,1080), interpolation= cv2.INTER_LINEAR)
    utils.place(image3,all_white,0,0,np.full((1080, 1920, 3), .3))

    blur = 13
    vinyl_size = 517
    vinyl_center_y = 400
    # making alpha channel for glow
    glow = utils.make_vinyl(image, vinyl_size)
    glow = cv2.copyMakeBorder(glow, blur, blur, blur, blur, cv2.BORDER_CONSTANT)
    glow_alpha = utils.get_alpha(glow)
    glow_alpha = cv2.blur(glow_alpha, (blur,blur))
    # change glow back to full image, not circle cropped
    glow = cv2.resize(image,(vinyl_size,vinyl_size))
    glow = cv2.copyMakeBorder(glow, blur, blur, blur, blur, cv2.BORDER_REFLECT)
    glow = cv2.blur(glow, (blur,blur))
    glow = utils.brighten(glow, 60, 40)

    

    
    vinyl = utils.make_vinyl(image, 500)

    vinyl_with_glow = utils.overlay(glow, vinyl, vinyl_size,vinyl_size,10, utils.get_alpha(vinyl))
    vinyl_with_glow = cv2.copyMakeBorder(vinyl_with_glow, blur, blur, blur, blur, cv2.BORDER_REFLECT)
    # 

            

    # Window name in which image is displayed
    window_name = 'image'
    size = (1920,1080)

    rot = vinyl_with_glow
    out = cv2.VideoWriter("{0}/video_no_audio.mp4".format(dir),cv2.VideoWriter_fourcc(*'DIVX'), 24, size)
    
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

        rotamt += rotate_increment
        rot_ease_amt = utils.calculate_rotation_increment_ease(video_len, fps, rotamt)
        res_vinyl = rotate(vinyl_with_glow, -rot_ease_amt, reshape=False)
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
        # print("center pixel:", dist_from_top + round(res_vinyl.shape[0]/2))
        composite = utils.overlay(image3, res_vinyl, 1920,1080,dist_from_top, res_alpha)
        utils.place(composite, all_white, 0, 0, np.divide(res_animation_frame,all_white))
        out.write(composite)
    out.release 

    

    # videoclip = VideoFileClip("bahbahbahbah.mp4")
    # audioclip = AudioFileClip("./videos/mercury.mp3")

    # new_audioclip = CompositeAudioClip([audioclip])
    # videoclip.audio = new_audioclip
    # videoclip.write_videofile("finished_video.mp4")






# main()

# subprocess.run(["ffmpeg", "-y", "-i", "mercury.mp3", "-i", "bahbahbahbah.mp4", "final_video.mp4"])

# subprocess.run(["rm", "bahbahbahbah.mp4"])