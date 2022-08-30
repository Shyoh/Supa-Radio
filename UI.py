
# importing required packages
from ctypes import resize
from pickle import FALSE
import tkinter as tk
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image
from tkinter import Label, filedialog
import main
import subprocess


def run():
    main.main()
    subprocess.run(["ffmpeg", "-y", "-i", "mercury.mp3", "-i", "video_no_audio.mp4", "final_video.mp4"])
    subprocess.run(["rm", "video_no_audio.mp4"])

def select_picture():
    filetypes = (
        ('png files', '*.png'),
        ('jpeg files', '*.jpeg')
    )

    filename = filedialog.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    # showinfo(
    #     title='Selected File',
    #     message=filename
    # )

    return filename

    


def select_song():
    filetypes = (
        ('mp3 files', '*.mp3'),
        ('wav files', '*.wav')
    )

    filename = filedialog.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    showinfo(
        title='Selected File',
        message=filename
    )

    return filename

def UploadAction(event=None):
    filename = filedialog.askopenfilename(filetypes=[("*.png")])
    print('Selected:', filename)

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

vinylpic = select_picture
chooseVinyl = tk.Button(root, bg='white', text='Open file', command=vinylpic, border=-2, width=15)
chooseVinyl.place(x=630,y=150)


#Get the background picture
VinylText = Label(root, text = 'Choose Background Picture')
VinylText.place(x=630,y=225)
VinylText.configure(bg="black")

backgroundpic = select_picture
chooseBg = tk.Button(root, bg='white', text='Open file', command=backgroundpic, border=-2, width=15)
chooseBg.place(x=630,y=250)


#Get the song
VinylText = Label(root, text = 'Choose song')
VinylText.place(x=670,y=325)
VinylText.configure(bg="black",)

song = select_song
chooseSong = tk.Button(root, bg='white', text='Open file', command=song, border=-2, width=15)
chooseSong.place(x=630,y=350)


#Choose directory
VinylText = Label(root, text = 'Choose directory')
VinylText.place(x=660,y=425)
VinylText.configure(bg="black",)

path =  filedialog.askdirectory
RunProgram = tk.Button(root, bg='black', text='Open Directory', command=path, border=-2, width=15)
RunProgram.place(x=630,y=450)

#Run the program
RunProgram = tk.Button(root, bg='black', text='Run', command=lambda:run(), border=-2, width=20)
RunProgram.place(x=150,y=450)


  
# running the application
root.mainloop()