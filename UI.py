
# importing required packages
from ctypes import resize
from pickle import FALSE
import tkinter as tk
from tkinter.messagebox import showinfo
from turtle import back
from PIL import ImageTk, Image
from tkinter import Label, filedialog
import main
import subprocess
import os


currentdir='/'
finaldir = ''

song = ''
vinylpic = ''
backgroundpic = ''
save_file_dir = ''



def run():
    if song:
        main.main(vinylpic, backgroundpic, finaldir)
        subprocess.run(["ffmpeg", "-y", "-i", str(song), "-i", "{0}/video_no_audio.mp4".format(finaldir), str(save_file_dir)])
        subprocess.run(["rm", "{0}/video_no_audio.mp4".format(finaldir)])

def select_vinyl():
    filetypes = (
        ('png files', '*.png'),
        ('jpeg files', '*.jpeg')
    )

    global vinylpic
    global currentdir

    vinylpic = filedialog.askopenfilename(
        title='Open a file',
        initialdir=currentdir,
        filetypes=filetypes)
    
    currentdir = vinylpic

    showinfo(
        title='Selected File',
        message=vinylpic
    )

def select_bg():
    filetypes = (
        ('png files', '*.png'),
        ('jpeg files', '*.jpeg')
    )

    global backgroundpic
    global currentdir

    backgroundpic = filedialog.askopenfilename(
        title='Open a file',
        initialdir=currentdir,
        filetypes=filetypes)

    currentdir = backgroundpic

    showinfo(
        title='Selected File',
        message=backgroundpic
    )

def select_song():
    filetypes = (
        ('mp3 files', '*.mp3'),
        ('wav files', '*.wav')
    )

    global song
    global currentdir

    song = filedialog.askopenfilename(
        title='Open a file',
        initialdir=currentdir,
        filetypes=filetypes)
    
    currentdir = song

    showinfo(
        title='Selected File',
        message=song
    )

def save_file():
    global save_file_dir
    global currentdir
    global finaldir
    save_file_dir = filedialog.asksaveasfilename(
        defaultextension=".mp4",
        initialdir=currentdir,
        initialfile="Untitled.mp4",
        title="Save File"
        )

    currentdir = save_file_dir
    finaldir = os.path.dirname(save_file_dir)



# creating main window
root = tk.Tk()

root.title("Supa Sounds video generator")
root.geometry("1000x600")
root.configure(bg="black")
root.resizable(False, False)

# canvas = tk.Canvas(root,width=1000, height= 600)
# canvas.grid(columnspan=3)
# canvas.configure(bg="black")

  
pic = Image.open("./pictures/logo.png")
resized = pic.resize((1280,853))
logo = ImageTk.PhotoImage(resized)
label1 = tk.Label(root, image= logo)
label1.configure(bg="black")
label1.place(x=-400,y=-150)


#Get the Vinyl picture
VinylText = Label(root, text = 'Choose Vinyl Picture')
VinylText.place(x=650,y=125)
VinylText.configure(bg="black")

chooseVinyl = tk.Button(root, bg='white', text='Open file', command=lambda:select_vinyl(), border=-2, width=15)
chooseVinyl.place(x=630,y=150)


#Get the background picture
BgText = Label(root, text = 'Choose Background Picture')
BgText.place(x=630,y=225)
BgText.configure(bg="black")

chooseBg = tk.Button(root, bg='white', text='Open file', command=lambda:select_bg(), border=-2, width=15)
chooseBg.place(x=630,y=250)


#Get the song
SongText = Label(root, text = 'Choose song')
SongText.place(x=670,y=325)
SongText.configure(bg="black")

chooseSong = tk.Button(root, bg='white', text='Open file', command=lambda:select_song(), border=-2, width=15)
chooseSong.place(x=630,y=350)



#Choose directory
DirText = Label(root, text = 'Choose directory')
DirText.place(x=660,y=425)
DirText.configure(bg="black")

RunProgram = tk.Button(root, bg='black', text='Open Directory', command=lambda:save_file(), border=-2, width=15)
RunProgram.place(x=630,y=450)

#Run the program
RunProgram = tk.Button(root, bg='black', text='Run', command=lambda:run(), border=-2, width=20)
RunProgram.place(x=150,y=450)


  
# running the application
root.mainloop()