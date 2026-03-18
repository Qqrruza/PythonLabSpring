import tkinter as tk
import requests
from PIL import Image, ImageTk
from io import BytesIO
import time

def show_cat():
    try:
        url = "https://cataas.com/cat?type=small"
        
        r = requests.get(url, timeout=10)
        
        if r.status_code == 200:
            img = Image.open(BytesIO(r.content))
            img.thumbnail((550, 550))
            
            photo = ImageTk.PhotoImage(img)
            label.config(image=photo)
            label.image = photo
        else:
            label.config(text=f"ошибка {r.status_code}")
            
    except Exception as e:
        label.config(text="ошибка")

def next_cat():
    show_cat()

root = tk.Tk()
root.title("кот")
root.geometry("500x550")

btn = tk.Button(root, text="новый кот", command=next_cat)
btn.pack(pady=10, side="bottom")

label = tk.Label(root)
label.pack(expand=True)

show_cat()

root.mainloop()