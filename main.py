import matplotlib.pyplot as plt #pip install matplotlib
import pytesseract #pip install pytesseract
import cv2 #pip install opencv-python\
from datetime import datetime

def load_image(image_path):
    car_plate_image = cv2.imread(image_path)
    car_plate_image = cv2.cvtColor(car_plate_image, cv2.COLOR_BGR2RGB)
    return car_plate_image

def extract_car_plate(image, car_plate_haar_cascade):
    car_plate_rectangles = car_plate_haar_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)
    for x, y, w, h in car_plate_rectangles:
        car_plate_image = image[y + 15:y + h - 10, x + 15:x + w - 20]
    return car_plate_image

def resize_image(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    plt.axis('off')
    resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized_image

def check_car_plate(plate_number, filename='cars_plates.txt'):
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if plate_number.lower() in line.lower():
                return True
    return False

def add_plate_to_file(plate_info, filename='cars_time.txt'):
    with open(filename, 'a') as file:
        file.write(plate_info + '\n')

def authorized_action(detected_plate_number):
    print("Authorized action performed.")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_info = f"{current_time}: {detected_plate_number}"
    add_plate_to_file(full_info)
    
def main():
    # Загрузка изображения автомобильного номера
    car_plate_image_rgb = load_image(image_path=r'C:\Users\shara\Desktop\project_Cars\cars\3.jpg')

    # Загрузка каскада Хаара для обнаружения автомобильных номеров
    car_plate_haar_cascade = cv2.CascadeClassifier(r'C:\Users\shara\Desktop\project_Cars\haar_cascades\haarcascade_russian_plate_number.xml')

    # Извлечение изображения автомобильного номера с помощью каскада Хаара
    extracted_car_plate_image = extract_car_plate(car_plate_image_rgb, car_plate_haar_cascade)

    # Изменение размера изображения автомобильного номера
    extracted_car_plate_image = resize_image(extracted_car_plate_image, 150)

    # Преобразование изображения автомобильного номера в оттенки серого
    extracted_car_plate_image_gray = cv2.cvtColor(extracted_car_plate_image, cv2.COLOR_RGB2GRAY)

    # Отображение изображения автомобильного номера в оттенках серого
    plt.axis('off')
    plt.imshow(extracted_car_plate_image_gray, cmap='gray')
    plt.show()

    # Установка пути к Tesseract OCR
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Распознавание текста с изображения автомобильного номера с использованием Tesseract OCR
    detected_plate_number = pytesseract.image_to_string(
        extracted_car_plate_image_gray,
        config='--psm 6 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    )
    
    # Вывод распознанного номера автомобиля
    if check_car_plate(detected_plate_number):
        print(f"Car Plate Number {detected_plate_number} is authorized. Allowing the car to pass.")
        authorized_action(detected_plate_number)
    else:
        print(f"Car Plate Number {detected_plate_number} is not authorized. Denying access.")

main() # вызов функции

