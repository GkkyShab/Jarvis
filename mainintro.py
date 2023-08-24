from tkinter import *
import os
import cv2
import PIL.Image, PIL.ImageTk

root = Tk()
root.withdraw()
video_path = os.path.join('video', 'ai.mp4')
cap = cv2.VideoCapture(video_path)
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
root.deiconify()
root.geometry(f'{width}x{height}')
root.state('zoomed')
canvas = Canvas(root, width=width, height=height)
canvas.pack()
def run_ai():
    os.system('python Jarvis/main.py')

button = Button(root, text='Start', bg='white', fg='black', font=('Helvetica', 14, 'bold'), command=run_ai)
button.place(relx=0.5, rely=0.5, anchor=CENTER)

def update_video():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        canvas.create_image(0, 0, image=photo, anchor=NW)
        canvas.image = photo
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    root.after(int(1000 / fps), update_video)

update_video()
root.mainloop()
