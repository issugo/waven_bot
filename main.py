import cv2 as cv
import numpy as np

isle_screen_img = cv.imread('isle_screen.PNG', cv.IMREAD_UNCHANGED)
png_to_speak_img = cv.imread('png_to_speak.PNG', 0)

img_rgb = np.array(isle_screen_img)
img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)


# get matching template result
result = cv.matchTemplate(img_gray, png_to_speak_img, cv.TM_CCOEFF_NORMED)

cv.imshow('Result', result)
cv.waitKey()

# get position of best match in template
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

print('Best match top left position: %s' % str(max_loc))
print('Best match confidence: %s' % max_val)

treshold = 0.9
if max_val < treshold:
    print('pnj not found')
    exit(1)

# get dimensions of pnj
top_left = max_loc
bottom_right = (top_left[0] + png_to_speak_img.shape[1], top_left[1] + png_to_speak_img.shape[0])

cv.rectangle(isle_screen_img, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)
cv.imshow('Result', isle_screen_img)
cv.waitKey()