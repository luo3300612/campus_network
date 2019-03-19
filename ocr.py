import pytesseract
import cv2

img = cv2.imread('valcode.png')

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

print(img_gray.shape)

result = pytesseract.image_to_string(img_gray)

print("before:",result)

result = "".join([c for c in result if c.isalnum()])

print("after:",result)

cv2.waitKey(0)
