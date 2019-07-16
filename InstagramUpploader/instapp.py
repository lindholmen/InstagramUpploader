from instapy_cli import client
import time
import os
from watchdog.observers import Observer
from eventhandler import MyHandler
from tkinter import *
from tkinter import messagebox


user_name = "xxx" # account name of Insta
pwd = "xxx" # password
to_be_published_list = []



def worker(q):
    while True:
        item = q.get()
        if item:
            print("get the message:", item)
            to_be_published_list.append(item)
        time.sleep(1)

path = os.getcwd() + "/published_pool"
event_handler = MyHandler(func=worker)
observer = Observer()
observer.schedule(event_handler, path, recursive=False)
observer.start()

try:
    while True:

        for image_name in to_be_published_list:
            window = Tk()
            window.title("Picture of " + image_name.split("/")[-1])
            window.geometry('460x100')
            lbl = Label(window, text="Input description:")
            lbl.grid(column=0, row=0)
            txt = Entry(window, width=50)
            txt.grid(column=0, row=1)

            def clicked():
                des = txt.get()
                print(image_name," with ", des)
                with client(user_name, pwd) as cli:
                    cli.upload(image_name, des)
                    pass
                messagebox.showinfo('Message title', 'Upload done!')


            btn = Button(window, text="Post it to Instagram!", command=clicked)
            btn.grid(column=0, row=5)

            window.mainloop()

        to_be_published_list.clear()


        time.sleep(15)
except KeyboardInterrupt:
    observer.stop()

observer.join()

