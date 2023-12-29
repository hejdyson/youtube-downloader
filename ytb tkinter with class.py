from tkinter import *
from pytube import YouTube
from pytube.exceptions import RegexMatchError
import os
from pathlib import Path


class Youtube_class():
    def __init__(self):
        self.yt = None
        self.itag = None
        self.resolution_table = ['144p', '360p', '720p', 'audio']


def download(yt_info):
    # downloading file
    if yt_info.yt is not None and yt_info.itag is not None:
        download_path = str(os.path.join(Path.home(), 'Downloads'))

        stream = yt_info.yt.streams.get_by_itag(yt_info.itag)
        stream.download(download_path)


def show_error_message():
    feedback_label['text'] = 'Fill in missing information or enter valid link'
    feedback_label['fg'] = 'red'


def convert(yt_info):

    url = url_value.get()
    resolution = var.get()
    print('1 url', url)

    if url and resolution:

        # DOWNLOAD ITAG CODES
        # https://gist.github.com/sidneys/7095afe4da4ae58694d128b1034e01e2
        if resolution == 1:
            yt_info.itag = 17
        elif resolution == 2:
            yt_info.itag = 18
        elif resolution == 3:
            yt_info.itag = 22
        elif resolution == 4:
            yt_info.itag = 140

        # updating feedback label with title of video
        if yt_info.itag is not None:
            feedback_label['text'] = ''
            try:
                print('2 url', url)
                yt_info.yt = YouTube(url)
                feedback_label['text'] = 'File to download is: ' + yt_info.yt.title + '. ' + '(' + yt_info.resolution_table[resolution-1] + ')'
                feedback_label['fg'] = 'darkgreen'

                # make download button available
                b2['state'] = NORMAL
                b2['bg'] = 'lightgreen'
            except RegexMatchError:
                show_error_message()
                b2['state'] = DISABLED
                b2['bg'] = 'lightgrey'

            # help print of available streams
            # print(yt_info.yt.streams)

        else:
            show_error_message()


    else:
        show_error_message()
        b2['state'] = DISABLED
        b2['bg'] = 'lightgrey'


# create instance of a class
yt_info = Youtube_class()


# create a GUI window
window = Tk()
window.title('Youtube Downloader')
window.geometry('400x200')

px = 20
py = 20

frame = Frame(window)

# create labels
l1 = Label(window, text='Enter URL adress: ', padx=5)
url_value = StringVar()
l2 = Entry(window, textvariable=url_value)
l3 = Label(window, text='Select resolution: ', padx=5)
l4 = Label(window, text='144p')
l5 = Label(window, text='360p')
l6 = Label(window, text='720p', padx=20)
l7 = Label(window, text='audio', padx=20)

feedback_label = Label(window, text='', padx=0)

# create radio buttons
var = IntVar()
r4 = Radiobutton(window, variable=var, value=1)
r5 = Radiobutton(window, variable=var, value=2)
r6 = Radiobutton(window, variable=var, value=3)
r7 = Radiobutton(window, variable=var, value=4)

# create convert button
# TODO command function
b1 = Button(window, text='Convert', command=lambda: convert(yt_info))
b2 = Button(window, text='Download', command=lambda: download(yt_info), state=DISABLED, bg='lightgrey', pady=5, padx=5)

# column nad row configurations
window.rowconfigure(0, weight=2)
window.rowconfigure(5, weight=2)

# placing elements onto a grid
l1.grid(row=0, column=0)
l2.grid(row=0, column=1, columnspan=3, sticky='ew')
l3.grid(row=1, column=0)
l4.grid(row=2, column=0)
l5.grid(row=2, column=1)
l6.grid(row=2, column=2)
l7.grid(row=2, column=3)


r4.grid(row=3, column=0)
r5.grid(row=3, column=1)
r6.grid(row=3, column=2)
r7.grid(row=3, column=3)

b1.grid(row=4, column=1)
b2.grid(row=6, column=1)


feedback_label.grid(row=5, column=0, columnspan=4, sticky='w', padx=5)


window.mainloop()
