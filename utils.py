import cv2
import math
import numpy as np

# paths
path2 = r'./pictures/vinyl_overlay.png'


# Reading in images
image2 = cv2.imread(path2)



def easeOutQuad(x):
    return 1 - (1 - x) * (1 - x)

def easeOutCubic(x):
    return 1 - pow(1 - x, 3)

def calculate_rotation_increment_ease(video_len, fps, curr_amt):
    num_half_rotations = round(video_len / 15)
    num_degrees =  num_half_rotations * 180
    rot_amt = (num_degrees / video_len) / fps
    amt_to_reach = easeOutQuad((curr_amt + rot_amt)/num_degrees) * num_degrees
    return amt_to_reach

def calculate_rotation_increment(video_len, fps):
    num_half_rotations = round(video_len / 15)
    num_degrees =  num_half_rotations * 180
    return (num_degrees / video_len) / fps

    
def brighten(img, bvalue, svalue):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h, s, v = cv2.split(hsv)
    v = cv2.add(v,bvalue)
    v[v > 255] = 255
    v[v < 0] = 0

    s = cv2.add(s,svalue)
    s[s > 255] = 255
    s[s < 0] = 0

    final_hsv = cv2.merge((h, s, v))
    
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    return img

def get_alpha(img):
    h, w ,c = img.shape
    alpha = np.empty(img.shape)
    alpha.fill(1)
    for i in range(w):
        for j in range(h):
            if np. all((img[j][i] == 0)):
                alpha[j][i] = (0.0,0.0,0.0)
    

    return alpha

#Shifts the image over by the x and y values
def place(bgimg, overlay, x, y, alpha):
    h, w, c = overlay.shape
    bgh, bgw, bgc = bgimg.shape
    # print("bgh: {}".format(bgh))
    # print("bgw: {}".format(bgw))
    # print("x: {}".format(x))
    # print("y: {}".format(y))
    # print("h: {}".format(h))
    # print("w: {}".format(w))
    # print(bgimg[y:y+h,x:x+w].shape)
    a = np.multiply(alpha,overlay)
    b = np.multiply(1-alpha,bgimg[y:y+h,x:x+w])
    overlay_w_alpha = np.add(a,b)
    bgimg[y:y+h,x:x+w] = overlay_w_alpha
    # old looping to understand what above is doing
    # for i in range(w):
    #     for j in range(h):
    #             if x+i < bgw and y+j < bgh:
    #                 new_value = alpha[j][i][0]*overlay[j][i] + (1-alpha[j][i][0])*bgimg[y + j][x + i]
    #                 bgimg[y + j][x + i] = new_value
                # else:
                #     print("x + i : {}, y + j: {}".format(x+i, y +j))



#composites image over a background
def overlay(background, on_top, up_width, up_height, placey, alpha_channel):
    #resizing image
    up_points = (up_width, up_height)
    background_resized = cv2.resize(background, up_points, interpolation= cv2.INTER_LINEAR)

    w, h, c = on_top.shape

    #make vinyl transparent
    # black_mask = np.all(on_top == 0, axis=-1)
    # alpha = np.uint8(np.logical_not(black_mask)) * 255
    # bgra = np.dstack((on_top, alpha))
    # cv2.imwrite("rgba.png", bgra)

    # alpha_channel = bgra[:, :, 3] / 255

    x = ((up_width//2) - (w//2)) # = 710

    place(background_resized, on_top, x, placey, alpha_channel)


    return background_resized


#creates vinyl with chosen image, can set to any size
def make_vinyl(img, size):
    cover_resized = cv2.resize(img, (size, size))

    overlay = cv2.imread(path2, cv2.IMREAD_UNCHANGED)
    overlay = cv2.resize(overlay, (size,size))  # IMREAD_UNCHANGED => open image with the alpha channel
    alpha_channel = overlay[:, :, 3] / 255 # convert from 0-255 to 0.0-1.0
    vinyl_overlay_colors = overlay[:, :, :3]
    alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))
    h, w = overlay.shape[:2]
    background_subsection = cover_resized[0:h, 0:w]
    composite = background_subsection * (1 - alpha_mask) + vinyl_overlay_colors * alpha_mask
    cover_resized[0:h, 0:w] = composite

    height, width, channels = cover_resized.shape

    r = width/2

    for i in range(width):
        y = int(math.sqrt(r**2 - (i-r)**2))
        for j in range(height):
            if j > y+r or j < -y+r:
                cover_resized[i][j] = 0

    return cover_resized