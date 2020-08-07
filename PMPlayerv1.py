from tkinter import ttk, messagebox, filedialog
from tkinter import *
import os
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
import pygame
from pygame import mixer
import time
import threading

root = Tk()
root.title("PMPlayer")


#################   Functions   ###############
def funcexit():
    confirmation = messagebox.askquestion("Exit", "Are you sure to exit?", icon='warning')
    if confirmation:
        pygame.mixer.music.stop()
        pygame.quit()
        root.destroy()


# This function is used to confirm the exit by the red button in upright corner and quits the program
# This function is used to save the data storage by quitting the pygame module and ending the music.

def ask_quit():
    confirmation = messagebox.askokcancel('Quit', 'Exit PMPlayer')
    if confirmation:
        pygame.mixer.music.stop()
        pygame.quit()
        root.destroy()


# same function but for in menu exit button with different confirmation

def showInfo():
    messagebox.showinfo(title='INFO', message='This MP3 Player is brought to you by PM')


# Message to pop up when about button is picked.

realnames = []
listofsongs = []
currentSong = 0
fullInfo = []
total_length = 0
paused = False
prev_volume = 0.5


def addMedia():
    directory = filedialog.askdirectory(title='Please select a directory')
    os.chdir(directory)
    for files in os.listdir(directory):
        if files.endswith('.mp3'):
            realdir = os.path.realpath(files)
            audio = ID3(realdir)
            realnames.append(audio['TIT2'].text[0])
            listofsongs.append(files)
            add_Titles(realnames)


# function to add media to media library

def playFile():
    global realnames, listofsongs
    song = filedialog.askopenfilename(parent=root, title='Select a File')
    path1 = os.path.realpath(song)
    listofsongs.append(song)
    songaudio = ID3(path1)
    realnames.append(songaudio['TIT2'].text[0])
    listofsongs.append(song)
    add_Titles(realnames)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    songInfo()


# playing a single file and adding to media library

def add_Titles(r):
    index = 0
    while index < len(r):
        title.insert(END, r[index])
        r.pop(index)
        index += 1


# function to add original titles of song to the list


def pauseandplay():
    if pauseButton.image == pauseIcon:
        pauseFunc()
        pauseButton.config(image=playIcon)
        pauseButton.image = playIcon
    else:
        playFunc()
        pauseButton.config(image=pauseIcon)
        pauseButton.image = pauseIcon


# function to change image of button

def pauseFunc():
    global paused
    pygame.mixer.music.pause()
    paused = True


# pause function

def playFunc():
    global paused
    if paused:
        mixer.music.unpause()
        paused = False
    else:
        playtime = slider_value.get()
        playtime = int(playtime)
        global currentSong
        try:
            currentSong = title.curselection()
            currentSong = int(currentSong[0])
            pygame.mixer.init()
            pygame.mixer.music.load(listofsongs[currentSong])
            pygame.mixer.music.play(playtime)
            songInfo()
        except:
            currentSong = 0
            pygame.init()
            pygame.mixer.music.load(listofsongs[currentSong])
            pygame.mixer.music.play(playtime)
            songInfo()
        TrackPlay(playtime)


# play function used to play and loading file's metadata in the player

def handler(event):
    global currentSong, listofsongs
    currentSong = event.widget.curselection()[0]
    pygame.init()
    pygame.mixer.music.load(listofsongs[currentSong])
    pygame.mixer.music.play()
    songInfo()


# function to handle curser selection

def nextfunc():
    global currentSong
    currentSong += 1
    pygame.mixer.music.load(listofsongs[currentSong])
    pygame.mixer.music.play()
    pauseButton.config(image=pauseIcon)
    pauseButton.image = pauseIcon
    songInfo()


# next button function

def prevfunc():
    global currentSong
    currentSong -= 1
    pygame.mixer.music.load(listofsongs[currentSong])
    pygame.mixer.music.play()
    pauseButton.config(image=pauseIcon)
    pauseButton.image = pauseIcon
    songInfo()


# prev button function


def playfolder():
    addMedia()
    global currentSong
    if currentSong <= len(listofsongs):
        pygame.mixer.music.load(listofsongs[currentSong])
        pygame.mixer.music.play()
        songInfo()


# function to play folder from 1st song

def songInfo():
    try:
        fullInfo = MP3(listofsongs[currentSong])
    except:
        fullInfo = MP3(song)
    # print(fullInfo.pprint())
    global total_length
    total_length = fullInfo.info.length
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d} : {:02d}'.format(mins, secs)
    fullTime['text'] = timeformat
    songtitle = fullInfo['TIT2']
    artist = fullInfo['TPE1']
    genre = fullInfo['TALB']
    year = fullInfo['TDRC']
    songName['text'] = songtitle
    songArtist['text'] = artist
    songGenre['text'] = genre
    songYear['text'] = year
    thread1 = threading.Thread(target=startcount, args=(total_length,))
    thread1.start()
    albumart()


# metadata collector function

def startcount(t):
    x = 0
    p = t
    global paused
    try:
        while x <= t and pygame.mixer.music.get_busy():
            if paused:
                continue
            else:
                if p == t:
                    mins, secs = divmod(x, 60)
                    mins = round(mins)
                    secs = round(secs)
                    timeformat = '{:02d} : {:02d}'.format(mins, secs)
                    curTime['text'] = timeformat
                    time.sleep(1)
                    x += 1
    except:
        pass


# function for calculating time lapsed during a song play

def albumart():
    audio = ID3(listofsongs[currentSong])
    img2 = audio.get(BitmapImage('APIC'))
    albumIcon.configure(image=img2)
    albumIcon.image = img2


# not working will update
# function to import albumart from metadata

def set_vol(event):
    volume = volumeBar.get()
    pygame.init()
    pygame.mixer.music.set_volume(1 - (volume / 100))
    global prev_volume
    prev_volume = pygame.mixer.music.get_volume()
    if prev_volume != 0:
        volumeButton.config(image=volumeOn)
        volumeButton.image = volumeOn


# function to handle user input of volume control

def mutefunc():
    global prev_volume
    if volumeButton.image == volumeOn:
        prev_volume = pygame.mixer.music.get_volume()
        pygame.mixer.music.set_volume(0)
        volumeButton.config(image=volumeOff)
        volumeButton.image = volumeOff
    else:
        pygame.mixer.music.set_volume(prev_volume)
        volumeButton.config(image=volumeOn)
        volumeButton.image = volumeOn


# function to handle mute button

def volUp():
    volume = pygame.mixer.music.get_volume()
    volume += 0.1
    pygame.mixer.music.set_volume(volume)


# volume up function from Play drop down

def volDown():
    volume = pygame.mixer.music.get_volume()
    volume -= 0.1
    pygame.mixer.music.set_volume(volume)


# volume down function from Play drop down

loop1 = []


def TrackPlay(playtime):
    if pygame.mixer.music.get_busy():
        global loop1
        slider_value.set(playtime)
        playtime += 1.0
        print(playtime)
        current = pygame.mixer.music.get_pos()  # .get_pos() returns integer in milliseconds
        slider_value.set(current / 1000)  # .set_pos() works in seconds
        root.after(1000, lambda: TrackPlay(playtime))  # Loop every sec
    else:
        print("Track Stopped")


# function to adjust the playtime in scrollbar

def Updatetrackbar(value):
    if pygame.mixer.music.get_busy() and not paused:
        global loop1
        after_cancel(loop1)  # Cancel PlayTrack loop
        slider_value.set(value)  # Move slider to new position
        playFunc()
    else:
        print("Track Not Playing")
        slider_value.set(value)


# function to update scrollbar
# not working properly.

#############Tkinter###############################
menuBar = Menu(root)
root.config(menu=menuBar)
file = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label='File', menu=file)
file.add_command(label='Play File', command=playFile)
file.add_command(label='Play Folder', command=playfolder)
file.add_separator()
file.add_command(label='Open Playlist')
file.add_command(label='Save Playlist')
file.add_separator()
file.add_command(label='Add Media to Library', command=addMedia)
file.add_separator()
# file widgets
file.add_command(label='Exit', command=funcexit)

play = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label='Play', menu=play)
play.add_command(label='Previous', command=prevfunc)
play.add_command(label='Play', command=playFunc)
play.add_command(label='Pause', command=pauseFunc)
play.add_command(label='Next', command=nextfunc)

play.add_separator()
play.add_command(label='Volume Up', command=volUp)
play.add_command(label='Volume Down', command=volDown)
# play widgets


about = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label='About', menu=about)
about.add_command(label='About PMPlayer', command=showInfo)
# abot drop down menu
left = Frame(root, relief=SUNKEN, height=650, width=250, borderwidth=2)
right = Frame(root, relief=RAISED, height=650, width=550, borderwidth=2)
# frames to contain different tkinter widgets
# widgets..........................
infoIcon = PhotoImage(file='icons/info/infoicon1.png')
info = Button(left, image=infoIcon, width=30, height=30, relief=FLAT, command=songInfo)
info.place(x=290, y=0)

pauseIcon = PhotoImage(file='icons/pausePlay/pause.png')
playIcon = PhotoImage(file='icons/pausePlay/play.png')
pauseButton = Button(left, image=playIcon, width=40, height=40, relief=FLAT, command=pauseandplay)
pauseButton.image = playIcon
pauseButton.place(x=110, y=275)

nextIcon = PhotoImage(file='icons/nextandprevious/next.png')
nextButton = Button(left, image=nextIcon, width=40, height=40, relief=FLAT, command=nextfunc)
nextButton.place(x=160, y=275)

prevIcon = PhotoImage(file='icons/nextandprevious/previous.png')
prevButton = Button(left, image=prevIcon, width=40, height=40, relief=FLAT, command=prevfunc)
prevButton.place(x=60, y=275)

volumeOn = PhotoImage(file='icons/volume/volumeon.png')
volumeOff = PhotoImage(file='icons/volume/volumeoff.png')
volumeButton = Button(left, image=volumeOn, width=40, height=40, relief=FLAT, command=mutefunc)
volumeButton.image = volumeOff
volumeButton.place(x=275, y=275)

curTime = Label(left, text='-:--', width=5, fg='black')
curTime.place(x=0, y=250)

slider_value = DoubleVar()
trackBar = ttk.Scale(left, to=total_length, orient=HORIZONTAL, length=175,
                     variable=slider_value, command=Updatetrackbar)
trackBar.place(x=40, y=250)

fullTime = Label(left, text='-:--', width=5)
fullTime.place(x=225, y=250)

songName = Label(left, text='---', width=25)
songName.place(x=35, y=225)

songArtist = Label(left, text='----', width=30)
songArtist.place(x=0, y=320)

songGenre = Label(left, text='-----', width=30)
songGenre.place(x=0, y=340)

songYear = Label(left, text='-----', width=30)
songYear.place(x=0, y=360)

default_img = PhotoImage(file='icons/favorite/outline_favorite_black_18dp.png')
albumIcon = Label(left, image=default_img, width=100, height=95, relief=SUNKEN)
albumIcon.place(x=100, y=3)
left.pack(side="left", expand=True, fill="both")
right.pack(side="right", expand=True, fill="both")

volumeBar = ttk.Scale(left, orient=VERTICAL, from_=0, to=100, command=set_vol)
volumeBar.set(50)
volumeBar.place(x=283, y=160)

# widgets in Listbox frame

title = Listbox(right, height=24, width=35)
title.pack()
title.bind('<Double-Button-1>', handler)

root.protocol("WM_DELETE_WINDOW", ask_quit)
root.geometry('650x400')
root.mainloop()
