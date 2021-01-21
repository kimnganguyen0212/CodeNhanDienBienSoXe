#-------LOAD THƯ VIỆN VÀ MODUL CẦN THIẾT--------------------------
import numpy as np
import cv2
import pytesseract
import matplotlib.pyplot as plt
from PIL import Image

#------DEMO CHƯƠNG TRÌNH NHỎ LOAD HÌNH ẢNH------------------------ 
img = cv2.imread('D:\\TT_ChuyenNganh\\HinhAnh\\opencv.jpg')
cv2.imshow('Load Img', img)
