import tkinter as tk
import cv2 as cv
from PIL import Image, ImageTk
from tkinter import messagebox
import time
import random
import os
import sys
class Application(tk.Frame):
    def __init__(self, master = None):

        super().__init__(master)

        self.master = master
        self.pack()

        self.sw = self.winfo_screenwidth()
        self.sh = self.winfo_screenheight()

        self.wx = 800
        self.wh = 600
        self.window_geo()
        self.creat_widgets()
        self.creat_snapshot_btn()
        self.capture = VideoCapture(0)
        #self.master.mainloop()

    def window_geo(self):
        self.master.geometry("%dx%d+%d+%d" % (self.wx, self.wh, (self.sw - self.wx) / 2, (self.sh - self.wh) / 2 - 100))

    def creat_widgets(self):
        self.canvas = tk.Canvas(self, bg='black', height=self.wh*0.9, width=self.wx*0.8)
        self.canvas.pack(anchor = 'nw')

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
        self.snapshot_btn = tk.Button(self, text='shot', width = int(self.wx*0.2/10), height = int(self.wh*0.1/10),
                                       bg = 'green',command = lambda:self.snapShot()) #
        # print(int(self.wx*0.2), int(self.wh*0.1))
        self.snapshot_btn.pack()
        #button3 = tk.Button(self, text="Button3", width=16, height=60)
        #button3.pack()

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
        #self.creat_messagebox('Save Photo', 'Save successfully')
        myDiag = MyDialog(window=self, title='test', message='test message')
        myDiag.popup_diag()
    def creat_messagebox(self, title = None, message = None):
        self.messagebox = tk.messagebox.showinfo(title,message)

class MyDialog:
    def __init__(self, window, title = 'My Dialog', message = 'Message'):
        self.window = window
        self.title = title
        self.message = message

    def button_func(self, option):
        if option == 'cancel':
            print('cancel')
        else:
            print('ok')

    def popup_diag(self):
        tl = tk.Toplevel(master=self.window)
        tl.title(self.title)
        frame = tk.Frame(tl)
        frame.grid()

        canvas = tk.Canvas(frame, width=self.window.wx/3/10, height = self.window.wh/3./10)
        canvas.grid(row = 1, column = 0)
        # canvas.grid(row=1, column=0)
        # imgvar = PhotoImage(file="pyrocket.png")
        # canvas.create_image(50, 70, image=imgvar)
        # canvas.image = imgvar

        msgbody1 = tk.Label(frame, text="The", font=("Times New Roman", 10, "bold"))
        msgbody1.grid(row=1, column=1, sticky='n')
        # lang = tk.Label(frame, text="language(s)", font=("Times New Roman", 10, "bold"), fg='blue')
        # lang.grid(row=1, column=2, sticky='n')
        # msgbody2 = tk.Label(frame, text="of this country is: Arabic", font=("Times New Roman", 20, "bold"))
        # msgbody2.grid(row=1, column=3, sticky='n')
        # cancelbttn = tk.Button(frame, text="Cancel", command=lambda: self.button_func("cancel"), width=10)
        # cancelbttn.grid(row=2, column=3)

        okbttn = tk.Button(frame, text="OK", command=lambda: self.button_func("ok"), width=10)
        okbttn.grid(row=2, column=4)

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