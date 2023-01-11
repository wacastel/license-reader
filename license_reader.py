# Tutorial - Detect and Recognize Car License Plates Using Python
#
# First, you need to install Tesseract OCR on your Mac or PC
# On Mac: brew install tesseract
#
# Path to tesseract on Mac:
# /opt/homebrew/Cellar/tesseract/5.3.0/bin/tesseract
#
# pip install OpenCV-Python
# You will use this library for preprocessing the input image and displaying various output images.
#
# pip install imutils
# You will use this library to crop the original input image to a desired width.
#
# pip install pytesseract
# You will use this library to extract the characters of the license plate and convert them into strings.

# Import the libraries
import cv2
import imutils
import pytesseract

# Point pytesseract to the location where the Tesseract engine is installed
# Replace the string with the path to the tesseract executable on the Mac
# pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/Cellar/tesseract/5.3.0/bin/tesseract'

# Read in the input image
IMAGE_1 = 'image1.jpeg'
IMAGE_2 = 'image2.jpeg'
IMAGE_3 = 'image3.jpeg'
IMAGE = 'image'
SUFFIX = '.jpeg'
DIR = 'img/'
X = 1
IMAGE_NAME = IMAGE + str(X) + SUFFIX
print(IMAGE_NAME)
FILE_PATH = DIR + IMAGE_NAME
print(FILE_PATH)
original_image = cv2.imread(FILE_PATH)

# Preprocess the image
# Resize the image width to 500 pixels. 
# Then convert the image to grayscale as the canny edge detection function only works with grayscale images. 
# Finally, call the bilateralFilter function to reduce the noise in the image.
original_image = imutils.resize(original_image, width=500 )
gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY) 
gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)

# Perform edge detection
edged_image = cv2.Canny(gray_image, 30, 200)

# Find the contours
contours, new = cv2.findContours(edged_image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
img1 = original_image.copy()
cv2.drawContours(img1, contours, -1, (0, 255, 0), 3)
cv2.imshow("img1", img1)

# Sort the contours
# contours = sorted(contours, key = cv2.contourArea, reverse = True)[:30]
contours = sorted(contours, key = cv2.contourArea, reverse = True)[:100]

# stores the license plate contour
screenCnt = None
img2 = original_image.copy()

# draws top 30 contours
cv2.drawContours(img2, contours, -1, (0, 255, 0), 3)
cv2.imshow("img2", img2)

# Loop over the top 30 contours
count = 0
idx = 7

for c in contours:
    # approximate the license plate contour
    contour_perimeter = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.018 * contour_perimeter, True)

    # Look for contours with 4 corners
    if len(approx) == 4:
        screenCnt = approx

        # find the coordinates of the license plate contour
        x, y, w, h = cv2.boundingRect(c)
        new_img = original_image [ y: y + h, x: x + w]

        # stores the new image
        cv2.imwrite('./'+str(idx)+'.png',new_img)
        idx += 1
        break

# draws the license plate contour on original image
cv2.drawContours(original_image , [screenCnt], -1, (0, 255, 0), 3)
cv2.imshow("detected license plate", original_image )

# Convert the characters in the new image to a string
# filename of the cropped license plate image
cropped_License_Plate = './7.png'
cv2.imshow("cropped license plate", cv2.imread(cropped_License_Plate))

# converts the license plate characters to string
text = pytesseract.image_to_string(cropped_License_Plate, lang='eng') 

# Display the output
print("License plate is: ", text)
cv2.waitKey(0)
cv2.destroyAllWindows()
