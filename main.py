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



def make_vinyl(img):
    cover_resized = cv2.resize(img, (1000, 1000))

    overlay = cv2.imread(path2, cv2.IMREAD_UNCHANGED)
    overlay = cv2.resize(overlay, (1000,1000))  # IMREAD_UNCHANGED => open image with the alpha channel
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
cv2.imshow(window_name, make_vinyl(image))

  
#waits for user to press any key 
#(this is necessary to avoid Python kernel form crashing)
cv2.waitKey(0) 
  
#closing all open windows 
cv2.destroyAllWindows() 