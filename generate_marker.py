import cv2
import cv2.aruco as aruco
import numpy as np

def generate_and_save_marker():
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
    
    marker_id = 1
    marker_size = 300
    
    marker_img = aruco.generateImageMarker(aruco_dict, marker_id, marker_size)
    
    cv2.imwrite('aruco_marker.png', marker_img)
    print("ArUco маркер сохранен как 'aruco_marker.png'")
    
    cv2.imshow('ArUco Marker', marker_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    generate_and_save_marker()