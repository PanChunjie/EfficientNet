import tkinter as tk
import cv2 as cv
from PIL import Image, ImageTk
from tkinter import messagebox, ttk
import time
import random
import os
import sys
class Application(tk.Frame):
    def __init__(self, master = None):

        super().__init__(master)

        self.master = master
        self.pack()
        self.photo_index = 0  # the index of photo in snapshot folder
        self.sw = self.winfo_screenwidth()
        self.sh = self.winfo_screenheight()

        self.wx = 800
        self.wh = 600
        self.window_geo()
        self.creat_widgets()

        self.capture = VideoCapture(0)
        #self.master.mainloop()

    def window_geo(self):
        self.master.geometry("%dx%d+%d+%d" % (self.wx, self.wh, (self.sw - self.wx) / 2, (self.sh - self.wh) / 2 - 100))
        #self.master.geometry("800x600")

    def creat_widgets(self):
        self.tab = ttk.Notebook(self.master)
        self.tab_home = ttk.Frame(self.tab)
        self.tab_photo = ttk.Frame(self.tab)
        self.tab.add(self.tab_home, text = 'Home')
        self.tab.add(self.tab_photo, text= 'Album')
        self.tab.pack(expand = 1, fill = 'both')
        ###### widgets in first tab ######
        self.canvas = tk.Canvas(self.tab_home, bg='black', height=self.wh*0.9, width=self.wx*0.8)
        self.canvas.pack(anchor = 'n')
        self.creat_snapshot_btn()
        ###### widgets in second tab ######
        self.label = tk.Label(self.tab_photo, height = int(self.wh*0.9), width=int(self.wx*0.8))
        self.label.pack()
        self.creat_album_btn()
        self.tab.bind("<<NotebookTabChanged>>", lambda event:self.show_photos(event, index=0))



    def show_video(self):
        ret, frame = self.capture.get_frame()
        if not ret:
            raise ValueError('video read frame error')
            return
        frame = cv.flip(frame, 1)
        cv2image = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        self.image_file = ImageTk.PhotoImage(img, width=self.canvas.winfo_width(), height=self.canvas.winfo_height())
        self.canvas.create_image(self.canvas.winfo_width()/2, self.canvas.winfo_height()/2, anchor='center', image=self.image_file,)
        self.canvas.after(1, self.show_video)

    def creat_snapshot_btn(self):
        self.snapshot_btn = tk.Button(self.tab_home, text='shot', width = int(self.wx*0.2/10), height = int(self.wh*0.1/10),
                                       bg = 'green',command = lambda:self.snapShot())
        # print(int(self.wx*0.2), int(self.wh*0.1))
        self.snapshot_btn.pack()
        #button3 = tk.Button(self, text="Button3", width=16, height=60)
        #button3.pack()

    def creat_album_btn(self):
        self.album_frame = tk.Frame(self.tab_photo, height = int(self.wh*0.1))
        self.album_frame.pack(fill='x', side = 'top')

        self.album_pre_btn = tk.Button(self.album_frame, text='Previous',  width = int(self.wx*0.2/10), height = int(self.wh*0.1/10),
                                      command = lambda:self.show_photos(index = -1))
        self.album_next_btn = tk.Button(self.album_frame, text='Next', width=int(self.wx * 0.2 / 10), height=int(self.wh * 0.1 / 10),
                                      command=lambda: self.show_photos(index = 1))
        col, row = self.album_frame.grid_size()
        print('col:',col, 'row', row)
        self.album_pre_btn.pack(side = 'left', padx = int(self.wh * 0.2))
        self.album_next_btn.pack(side = 'right', padx = int(self.wh * 0.2))
        #self.album_pre_btn.grid(row = 0, column = 0,  sticky = 'n', padx = int(self.wh * 0.2))
        #root.grid_columnconfigure(col, minsize=20)
        #self.album_next_btn.grid(row = 0, column = 1,  stick = 'n', padx = int(self.wh * 0.2))

    def show_photos(self, event = None, index = 0):
        index = self.photo_index + index
        file_path = os.getcwd() + '\\snapshot'
        if not os.path.isdir(file_path):
            os.mkdir(file_path)
        if len(os.listdir(file_path)) == 0:
            self.label['text'] = 'Album is empty'
            self.album_pre_btn['state'] = 'disabled'
            self.album_next_btn['state'] = 'disabled'
            return
        else:
            self.photo_index = index
            self.album_pre_btn['state'] = 'normal'
            self.album_next_btn['state'] = 'normal'
            if index == 0:
                self.album_pre_btn['state'] = 'disable'
            if index == len(os.listdir(file_path))-1:
                self.album_next_btn['state'] = 'disable'
            imglist = [image for image in os.listdir(file_path)]
            print('state1: ', self.album_pre_btn['state'])
            print('state2: ', self.album_pre_btn['state'])
            print(imglist, ',', index)
            image = Image.open(os.path.join(file_path, imglist[index]))
            image = ImageTk.PhotoImage(image)
            self.label['image'] = image
            self.label.photo = image

    def creat_file_name(self, prefix = 'Driver2.0', suffix = None):
        secondsSinceEpoch = time.time()
        localTime = time.localtime(secondsSinceEpoch)
        random.seed(secondsSinceEpoch)
        return prefix + ('_%d%d%d%d%d%d'%(localTime.tm_year, localTime.tm_mon, localTime.tm_mday,
                                                   localTime.tm_hour, localTime.tm_min, localTime.tm_sec))\
               +str(random.randint(1000,9999)) + '.' + suffix

    def snapShot(self):
        ret, frame = self.capture.get_frame()
        if not ret:
            raise ValueError('video read frame error')
            return
        frame = cv.flip(frame, 1)
        file_name = self.creat_file_name(prefix='snapshot', suffix = 'jpg')
        file_path = os.getcwd() + '\\snapshot'
        if not os.path.isdir(file_path):
            os.mkdir(file_path)
        save_status = cv.imwrite(os.path.join(file_path, file_name), frame)
        if not save_status:
            self.creat_messagebox('Save Photo', 'Fail to save')
        self.creat_messagebox('Save Photo', 'Save successfully')


    def creat_messagebox(self, title = None, message = None):
        self.master.messagebox = tk.messagebox.showinfo(title,message)


class VideoCapture:
    def __init__(self, video_id=0):
        self.vid = cv.VideoCapture(video_id)
        if not self.vid.isOpened():
            raise ValueError('Unable to open video source', video_id)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return ret, frame
            else:
                return ret, None

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


root = tk.Tk()
app = Application(master = root)
app.show_video()
app.mainloop()


#
#
# t = threading.Thread(target=show_video())
# t.start()



cv.destroyAllWindows()