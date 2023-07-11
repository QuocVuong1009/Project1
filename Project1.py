import cv2
import pytesseract
import string
import numpy as np
import json
import csv

#doc anh
img = cv2.imread("file_path_of_picture")
#chuyen anh sang mau xam
grimg = img.copy()
grimg = cv2.cvtColor(grimg, cv2.COLOR_BGR2GRAY)

#cac ham
def ToaDoYDau(x):
	for i in range(x, grimg.shape[0], 1):
		for j in range(grimg.shape[1]):
			#y truoc x sau(i la y chieu cao, j la x do dai)
			px = grimg[i][j]
			if (px > 80 and px < 120):
				return i #tra ve gia tri i tuc la gia tri cua toa do y sau khi bat dau phat hien chu
			if i == grimg.shape[0]:
				return t 
	#khi x vuot qua gio han thi se tra ve gia tri ngay tai do va ket thuc
	return grimg.shape[0]
			
def ToaDoYCuoi(y):
	for t in range(y, grimg.shape[0], 1): #y nghia vong lap la bat dau tu y den 399 moi lan tang 1 don vi
		count = 0
		for j in range(grimg.shape[1]):
			#y truoc x sau
			px1 = grimg[t][j] 
			if (px1 < 200):
				count += 1
		if count == 0:
			return t #tra ve gia tri cua t tuc la gia tri toa do y khi da biet hang nay khong co chu
		if t == grimg.shape[0]:
			return t 
	#khi x vuot qua gio han thi se tra ve gia tri ngay tai do va ket thuc
	return grimg.shape[0]

def ExtractTextStr(img):
	custom_config = r'--oem 3 --psm 6 tessedit_char_whitelist=0123456789'
	text = pytesseract.image_to_string(img, lang="vie", config = custom_config)
	#mo file text va luu vao duoi dang tieng Viet, co xuong hang
	cv2.imshow("subimage", img)
	with open("text.txt", "a", encoding="utf-8") as f:
		#ghi theo tung hang
		f.writelines(text)

#Ham thay the mot hang trong mot file
def replace_line(file_path, num_line, new_line):
	#Mo file va chay theo tung dong
	with open(file_path, "r+") as f:
		lines = f.readlines()
		#Thay the bang dong moi 
		lines[num_line] = new_line
	#Mo file de viet lai
	with open(file_path, "w") as f:
		f.writelines(lines)

def SavetoTxt(file_path):
	#mo file txt o che do doc
	with open("text.txt", "r+") as f:
		#doc theo hang
		lines = f.readlines()
		#o tung hang chuyen ky tu 000C sang khoang trang
		lines = [line.replace("\x0c", "") for line in lines]
		#xoa ky tu dac biet o moi hang
		lines = [line.translate(str.maketrans("", "", string.punctuation)) for line in lines]
		#chuyen con tro ve dau hang
		f.seek(0)
		#ghi lai van ban
		f.writelines(lines)
		#xoa khoang trang thua
		f.truncate()

def DeleteSpeCha(file_path):
	count = 0
	with open("text.txt", "r+") as f:
		#chay theo tung hang trong file
		for line in f:
			#lay gia tri do dai 
			length = len(line)
			#chay theo tung ky tu cua chuoi
			for c in range(length):
				#Lay gia tri cua bang ASCII
				value = ord(line[c])
				#Neu ky tuw la so 0123456789
				if (value > 47) and (value < 58):
					#Neu ky tu dang sau khong phai la so hoac khoang trag thi se cach ra
					if line[c+1] not in "0123456789 ":
						line = line[:c+1] + " " + line[c+1:]
						replace_line("text.txt", count, line)
					#Neu ky tu hien tai khong phai la ky tu dau va ky tu dang truoc khong phai la so hoac khoang trag thi se cach ra
					if c > 0 and line[c-1] not in "0123456789 ":
						line = line[:c] + " " + line[c:]
						replace_line("text.txt", count, line)
			count = count + 1	


def SavetoJson(file_path):
	try:
		with open("data.json", "r", encoding="utf-8") as file:
			data = json.load(file)
# Nếu chưa có data thì sẽ khởi tạo một data mới có hai theo format key là do_am và nhiet_do để chuẩn bị lưu vào file JSON
	except FileNotFoundError:
    		data = {
        		"so_thu_tu": [],
        		"ten_thuoc": [],
			"so_luong" : []
    			}

	with open(file_path, "r+") as f:
		for line in f:
			#Tach chu ra thanh tung tu rieng biet
			words = line.split()
			#Gom nhom cac chu theo thu tu va ghep lai
			chudau = words[0]
			haichucuoi = words[-2:]
			haichucuoitxt = " ".join(haichucuoi)
			chuconlai = words[1:-2]
			chuconlaitxt = " ".join(chuconlai)
			#Them cac tu dax taxh vao danh sach theo thu tu
			so_thu_tu_list = data.get("so_thu_tu", [])
			ten_thuoc_list = data.get("ten_thuoc", [])
			so_luong_list = data.get("so_luong", [])
			so_thu_tu_list.append(chudau)
			ten_thuoc_list.append(chuconlaitxt)
			so_luong_list.append(haichucuoitxt)
			#Cap nhat lai vao data
			data["so_thu_tu"] = so_thu_tu_list
			data["ten_thuoc"] = ten_thuoc_list
			data["so_luong"] = so_luong_list
			#Ghi dữ liệu mới vào file JSON
			with open("data.json", "w", encoding="utf-8") as file:
        			json.dump(data, file)

def SaveToCSV(file_path):
	with open(file_path, mode='r', encoding='utf-8-sig') as infile,open('text_new_2.csv', mode='w', newline='', encoding='utf-8-sig') as outfile:
    		# tao bien writer cua file CSV de ghi vao
    		writer = csv.writer(outfile, delimiter=',', lineterminator='\n')
    		# ghi dong header vao file CSV va bo qua dong dau tien vi no giong nhau
    		header = ['Số thứ tự', 'Tên thuốc', 'Số lượng', 'Đơn Vị']
    		writer.writerow(header)
    		next(infile)
    
    		# Doc lan luot tung hang cua file CSV
    		for line in infile:
        		# danh so tung cot tren 1 hang dua theo vi tri
        		columns = line.split()
        		#Cot dau tien la stt
        		number = columns[0]
        		#cac cot con lai se la ten thuoc, 
        		name = ' '.join(columns[1:-2])
        		#cot ke cuoi se la so luong
        		quantity = columns[-2]
        		#cot cuoi cung la don vi 
        		unit = columns[-1]
        		# ghi cac cot tren vao file CSV
        		writer.writerow([number, name, quantity, unit])


#Ham chinh
Pery1 = 0
Pery = 0
while (Pery1 < grimg.shape[0]):
	Pery = ToaDoYDau(Pery1)
	Pery1 = ToaDoYCuoi(Pery)
	#neu nhu vung co chu nho hon 10 pixel thi khong in ra
	if (Pery1 - Pery) > 10:
		#cat anh ra theo hai toa do va nang hai khoang bien len de cho de nhin
		subimg = grimg[Pery - 5: Pery1 + 5, 0: grimg.shape[1]]
		ExtractTextStr(subimg)
		cv2.waitKey()
SavetoTxt("text.txt")
DeleteSpeCha("text.txt")
SaveToCSV("text.txt")

