#-------LOAD THƯ VIỆN VÀ MODUL CẦN THIẾT--------------------------
import numpy as np
import cv2
import pytesseract
import matplotlib.pyplot as plt
from PIL import Image

#-------- ĐỌC HÌNH ẢNH - NHẬN DIỆN VÀ ĐÁNH DẤU ĐỐI TƯỢNG -------------
#Load image cv2.imread
img = cv2.imread('D:\\TT_ChuyenNganh\\HinhAnh\\xe7.jpg')
cv2.imshow('HINH ANH GOC', img)
#Chuyển về ảnh xám cv2.cvtColor
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#sử dụng adaptive threshold để làm nổi bật
#những phần mà ta muốn lấy(màu đen)
thresh = cv2.adaptiveThreshold(gray,255,
cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
#Dùng cv2.findContours để tạo các contours
#bao quanh các kí tự cũng như các nhiễu
contours,h = cv2.findContours(thresh,1,2)
largest_rectangle = [0,0]

#Vòng lặp for để đánh dấu đối tượng trên ảnh
for cnt in contours:
    #Tiếp theo ta tính chu vi của từng contour bẳng cv2.arcLength
    #sau đó dùng cv2.approxPolyDP để xấp xếp đa giác ở đây ta cần tìm
    #là hình chữ nhật nên ta chỉ giữ lại contour nào có 4 cạnh
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    if len(approx) == 4:
        area = cv2.contourArea(cnt)
        if area > largest_rectangle[0]:
            largest_rectangle = [cv2.contourArea(cnt), cnt, approx]
x,y,w,h = cv2.boundingRect(largest_rectangle[1])

image = img[y:y+h, x:x+w]
cv2.drawContours(img,[largest_rectangle[1]],0,(0,255,0),5)
#Đánh dấu viền đối tượng trên ảnh
cropped = img[y:y+h, x:x+w]
cv2.imshow('DANH DAU DOI TUONG', img)

cv2.drawContours(img,[largest_rectangle[1]],0,(255,255,255),18)

#------ TÁCH ĐỐI TƯỢNG VÀ ĐỌC NỘI DUNG HÌNH ẢNH CHUYỂN THÀNH DẠNG TEXT ---------------
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#Lọc nhiễu bằng cv2.GaussianBlur
blur = cv2.GaussianBlur(gray, (3,3), 0)
#Dùng thereshold OTSU đưa ảnh về trắng đen tách biệt background và region intersting
thresh = cv2.threshold(blur, 0, 255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU) [1]
#Hiển thị đối tượng được tách ra khỏi hình ảnh
cv2.imshow('CROP', thresh)

#Đọc thông tin hình ảnh chuyển về dạng text
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations = 1)
invert = 255 - opening
data = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')
print('THONG TIN NHAN DIEN:\n', data)
cv2.waitKey()
