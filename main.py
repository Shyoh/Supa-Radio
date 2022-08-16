from turtle import back
import cv2 
import math
import numpy as np
  
# paths
path = r'./pictures/mercury.jpeg'
path2 = r'./pictures/vinyl_overlay.png'
path3 = r'./pictures/bgimg.jpeg'
  
# Reading in images
image = cv2.imread(path)
image2 = cv2.imread(path2)
image3 = cv2.imread(path3)

#Shifts the image over by the x and y values
def place(bgimg, overlay, x, y, alpha):
    h, w, c = overlay.shape
    for i in range(w):
        for j in range(h):
            if alpha[i][j] == 1:
                bgimg[x + i][y + j] = overlay[i][j]
            
    


def vinyl_over_bg(background, vinyl):
    #resizing image
    up_width = 1920
    up_height = 1080
    up_points = (up_width, up_height)
    background_resized = cv2.resize(background, up_points, interpolation= cv2.INTER_LINEAR)

    w, h, c = vinyl.shape

    #make vinyl transparent
    tmp = cv2.cvtColor(vinyl, cv2.COLOR_BGR2GRAY)
    _,alpha = cv2.threshold(tmp,0,255,cv2.THRESH_BINARY)
    b, g, r = cv2.split(vinyl)
    rgba = [b,g,r, alpha]
    dst = cv2.merge(rgba,4)
    cv2.imwrite("test.png", dst)

    #shifting x nd y values for vinyl
    alpha_channel = dst[:, :, 3] / 255
    x = ((up_width/2) - (w/2)) # = 710
    place(background_resized, vinyl, 200, 710, alpha_channel)

    #displaying vinyl over bg
    # alpha_channel = dst[:, :, 3] / 255 # convert from 0-255 to 0.0-1.0
    # vinyl_overlay_colors = dst[:, :, :3]
    # alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))
    # h, w = dst.shape[:2]
    # background_subsection = background_resized[0:h, 0:w]
    # composite = background_subsection * (1 - alpha_mask) + vinyl_overlay_colors * alpha_mask
    # background_resized[0:h, 0:w] = composite




    return background_resized


def make_vinyl(img):
    size = 500

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



#img = cv2.addWeighted(vinyl_overlay,1,cover_resized,.2,.5)
            

# Window name in which image is displayed
window_name = 'image'
  
# Using cv2.imshow() method 
# Displaying the image 
cv2.imshow(window_name, vinyl_over_bg(image3, make_vinyl(image)))

  
#waits for user to press any key 
#(this is necessary to avoid Python kernel form crashing)
cv2.waitKey(0) 
  
#closing all open windows 
cv2.destroyAllWindows() 