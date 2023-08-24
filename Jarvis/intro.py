# perfect
from tkinter import *
import os
import cv2
import PIL.Image, PIL.ImageTk
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio
import subprocess

root = Tk()
root.withdraw()
video_path = os.path.join('video', 'ai.mp4')
cap = cv2.VideoCapture(video_path)
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Extract audio from video
audio = AudioSegment.from_file(video_path, format="mp4").set_channels(1)
audio -= 15

# Play audio in the background
def play_audio():
    global audio_player
    audio_player = _play_with_simpleaudio(audio)
play_audio()

root.deiconify()
root.geometry(f'{width}x{height}')
root.state('zoomed')
canvas = Canvas(root, width=width, height=height)
canvas.pack()

def run_ai():
    # Run the main.py script in a separate process
    subprocess.Popen(['python', 'Jarvis/main.py'])

# Bind the <Return> key to the run_ai function
root.bind('<Return>', lambda event: run_ai())

def restart_video():
    global cap, audio_player
    # Stop the audio player
    audio_player.stop()
    # Reset the video to the beginning
    cap.release()
    cap = cv2.VideoCapture(video_path)
    # Extract the audio again from the beginning of the video
    global audio
    audio = AudioSegment.from_file(video_path, format="mp4").set_channels(1)
    # Play the audio in the background again
    play_audio()

# Bind the spacebar key to the restart_video function
root.bind('<space>', lambda event: restart_video())

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

cap.release()
cv2.destroyAllWindows()
