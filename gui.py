import os
import time
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sounddevice as sd
import wavio as wv
from asrecognition import ASREngine

asr = ASREngine("en", model_path="jonatasgrosman/wav2vec2-large-xlsr-53-english")

index = 0

imgs = []

def getImgs():
    print("Get images...")
    return [im.split(".")[0] for im in os.listdir("./imgs/512/")]

imgs = getImgs()

img_path = "./imgs/512/" + imgs[0] + ".png"
print(imgs)

audio_paths = ["temp_rec.wav"]
 
root = Tk()
root.title("Demo ASR - Yanis Labrak")
root.geometry("700x700")
root.maxsize(700, 700)
root.config(bg="#6FAFE7")
 
login = Label(root, text="Reconnaissance de la parole", bg="#2176C1", fg='white', relief=RAISED)
login.pack(ipady=5, fill='x')
login.config(font=("Font", 30)) # change font and size of label
 
# Main Image
image = PhotoImage(file=img_path)
img_resize = image.subsample(1,1)
img_label = Label(root, image=img_resize, bg="white", relief=SUNKEN)
img_label.pack(pady=5)

# Transcription
txt_transcript = StringVar()
label_transcript = Label(root, textvariable=txt_transcript, relief=SUNKEN)
label_transcript.pack(pady=5)
last_transcription = ""

def speech_to_text():
    global label_transcript, last_transcription
    print("ASR")
    last_transcription = asr.transcribe(audio_paths)[0]["transcription"].lower()
    txt_transcript.set(last_transcription)
    print("last_transcription: ",last_transcription)

def record():
    freq = 44100
    duration = 1
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)
    sd.wait()
    wv.write("temp_rec.wav", recording, freq, sampwidth=1)

def changeImg():
    global img_label

    print("Use: ", index)
    img_path = "./imgs/512/" + imgs[index] + ".png"
    print(img_path)

    image = PhotoImage(file=img_path)
    img_resize = image.subsample(1,1)
    img_label.configure(image=img_resize)
    img_label.image=img_resize

def nextPage():
    global index, speech_button

    print("Inside Next Page")

    print(last_transcription, " <=> ", imgs[index])

    if last_transcription in imgs[index]:
        print("Inside")
    else:
        print("Not inside")
        return

    print(index)
    print(len(imgs) - 1)
    print(index >= len(imgs) - 1)

    if index >= len(imgs) - 1:
        print("Finished")
        messagebox.showinfo('Bravo!', 'Bravo, tu as fini le défi!')
        index = 0
        return
    else:
        index += 1

    txt_transcript.set("")
    changeImg()

def help():
    print("Help")

    print("Use: ", index)
    img_path = "./imgs/512+text/" + imgs[index] + ".png"
    print(img_path)

    image = PhotoImage(file=img_path)
    img_resize = image.subsample(1,1)
    img_label.configure(image=img_resize)
    img_label.image=img_resize

def speech():
    record()
    print("Save recording...")
    speech_to_text()
    speech_button.after(2000, nextPage)

speech_button = Button(root, text="Parler!", command=speech, bg="#6FAFE7", width=15)
# speech_button.after(8500, nextPage)
speech_button.pack(pady=5)

help_button = Button(root, text="Help!", command=help, bg="#6FAFE7", width=15)
help_button.pack(pady=5)

root.mainloop()