import cv2
import os

def convert_to_grayscale():
 
    image_path = f'C:/Users/Anna/Desktop/lab8/variant-1.jpg'
    
    img = cv2.imread(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    output_path = f'variant-1_grayscale.jpg'
    cv2.imwrite(output_path, gray)


if __name__ == '__main__':
    convert_to_grayscale()