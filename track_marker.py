import cv2
import numpy as np

template = cv2.imread('ref-point.jpg')
h, w = template.shape[:2]

fly = cv2.imread('fly64.png', cv2.IMREAD_UNCHANGED)
fly_h, fly_w = fly.shape[:2]
fly_rgb = fly[:,:,:3]
fly_mask = fly[:,:,3] / 255.0 if fly.shape[2] == 4 else np.ones((fly_h, fly_w))

cam = cv2.VideoCapture(0)

while True:
    flag, frame = cam.read()
    if not flag: break
    
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(frame_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    
    if max_val >= 0.6:
        x, y = max_loc
        center_x, center_y = x + w//2, y + h//2
        
        # Отрисовка метки
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
        cv2.circle(frame, (center_x, center_y), 5, (0,0,255), -1)
        
        # Вывод координат (левый верхний угол)
        cv2.putText(frame, f"Center: ({center_x}, {center_y})", (10,30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        
        # Наложение мухи
        fly_x, fly_y = center_x - fly_w//2, center_y - fly_h//2
        roi = frame[fly_y:fly_y+fly_h, fly_x:fly_x+fly_w]
        for c in range(3):
            roi[:,:,c] = (roi[:,:,c] * (1-fly_mask) + fly_rgb[:,:,c] * fly_mask).astype(np.uint8)
    else:
        cv2.putText(frame, "Marker not found", (10,30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
    
    cv2.imshow('Tracking', frame)
    if cv2.waitKey(1) == ord('q'): break

cam.release()
cv2.destroyAllWindows()