import cv2
import cv2.aruco as aruco
import numpy as np

def load_fly_image():
    fly_img = cv2.imread('fly64.png', cv2.IMREAD_UNCHANGED)
    
    if fly_img is None:
        print("Ошибка: не удалось загрузить fly64.png")
        return None
    
    print(f"Изображение мухи загружено: {fly_img.shape[1]}x{fly_img.shape[0]}")
    return fly_img

def overlay_image_alpha(img, img_overlay, pos, overlay_size=None):
    if overlay_size is not None:
        img_overlay = cv2.resize(img_overlay, overlay_size, interpolation=cv2.INTER_AREA)
    
    h, w = img_overlay.shape[:2]
    
    x = int(pos[0] - w // 2)
    y = int(pos[1] - h // 2)
    
    if x < 0 or y < 0 or x + w > img.shape[1] or y + h > img.shape[0]:
        return img
    
    if img_overlay.shape[2] == 4:
        alpha = img_overlay[:, :, 3] / 255.0
        img_overlay_rgb = img_overlay[:, :, :3]
        
        for c in range(3):
            img[y:y+h, x:x+w, c] = (1 - alpha) * img[y:y+h, x:x+w, c] + alpha * img_overlay_rgb[:, :, c]
    else:
        img[y:y+h, x:x+w] = img_overlay
    
    return img

def track_marker_with_fly():
    fly_img = load_fly_image()
    if fly_img is None:
        return
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Ошибка: не удалось открыть камеру")
        return
    
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
    parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dict, parameters)
    
    fly_size = 80 
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        corners, ids, rejected = detector.detectMarkers(gray)
        
        if ids is not None:
            aruco.drawDetectedMarkers(frame, corners, ids)
            
            for i, marker_corners in enumerate(corners):
                marker_id = ids[i][0]
                corners_2d = marker_corners[0]
                
                center_x = int(np.mean(corners_2d[:, 0]))
                center_y = int(np.mean(corners_2d[:, 1]))
                
                frame = overlay_image_alpha(frame, fly_img, (center_x, center_y), 
                                            (fly_size, fly_size))
                
                cv2.circle(frame, (center_x, center_y), 1, (0, 0, 255), -1)
                
                cv2.putText(frame, f"ID: {marker_id}", 
                           (center_x - 20, center_y - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                cv2.putText(frame, f"X: {center_x}, Y: {center_y}", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.6, (0, 255, 0), 2)
        
        cv2.imshow('Marker Tracking with Fly', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    track_marker_with_fly()