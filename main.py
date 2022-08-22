from turtle import back
import cv2 
import math
import numpy as np
from scipy.ndimage import rotate
  
# paths
path = r'./pictures/mercury.jpeg'
path2 = r'./pictures/vinyl_overlay.png'
path3 = r'./pictures/bgimg.jpeg'
  
# Reading in images
image = cv2.imread(path)
image2 = cv2.imread(path2)
image3 = cv2.imread(path3)

# video setings
fps = 24
video_len = 30

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
    print("bgh: {}".format(bgh))
    print("bgw: {}".format(bgw))
    print("x: {}".format(x))
    print("y: {}".format(y))
    print("h: {}".format(h))
    print("w: {}".format(w))
    
    for i in range(w):
        for j in range(h):
                if x+i < bgw and y+j < bgh:
                    new_value = alpha[j][i][0]*overlay[j][i] + (1-alpha[j][i][0])*bgimg[y + j][x + i]
                    bgimg[y + j][x + i] = new_value
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



def main():
    #adding glow to the vinyl
    glow = make_vinyl(image, 520)
    glow_alpha = get_alpha(glow)
    glow_alpha = cv2.blur(glow_alpha, (15,15))

    glow = cv2.blur(glow, (15,15))
    vinyl = make_vinyl(image, 500)

    composite = overlay(image3, glow, 1920,1080,200, glow_alpha)
    composite = overlay(composite, vinyl, 1920,1080,200, get_alpha(vinyl))

            

    # Window name in which image is displayed
    window_name = 'image'
    # for i in range(video_len * fps):
        #rotate - .5
        # rot = rotate(rot, -30, reshape=False)
        # cv2.imshow(window_name, overlay(image3, rot, 1920, 1080, 200))
        # cv2.waitKey(0)
        #waits for user to press any key 
        #(this is necessary to avoid Python kernel form crashing)
    # composite = overlay(image3, composite, 1920, 1080, 200)
    cv2.imshow(window_name, composite)#make_vinyl(image, 500), 1920, 1080, 200
    cv2.waitKey(0)
        #closing all open windows 
    cv2.destroyAllWindows() 

main()
# Using cv2.imshow() method 
# Displaying the image 
# cv2.imshow(window_name, overlay(image3, make_vinyl(image)))

  
#waits for user to press any key 
#(this is necessary to avoid Python kernel form crashing)
# cv2.waitKey(0) 
  
# #closing all open windows 
# cv2.destroyAllWindows() 