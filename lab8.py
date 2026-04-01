import cv2
import os

def convert_to_grayscale():
 
    image_path = f'C:/Users/Anna/Desktop/lab8/variant-1.jpg'
    
    if not os.path.exists(image_path):
        print(f"Ошибка: файл {image_path} не найден!")
        return
    
    img = cv2.imread(image_path)
    
    if img is None:
        print(f"Ошибка: не удалось загрузить изображение {image_path}")
        return
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    output_path = f'variant-1_grayscale.jpg'
    cv2.imwrite(output_path, gray)
    print(f"Полутоновое изображение сохранено: {output_path}")


if __name__ == '__main__':
    convert_to_grayscale()