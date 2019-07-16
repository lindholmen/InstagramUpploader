from watchdog.events import FileSystemEventHandler
import os
import json
from threading import Thread
from queue import Queue



def reconstruct_json():
    folder_path = os.getcwd() + "/published_pool"
    all_posts_in_pool = []

    for filename in os.listdir(folder_path):
        if filename != '.DS_Store':
            all_posts_in_pool.append(
                {'image': filename, 'description': 'des3', 'post_date': '20190103', 'has_been_posted': True})

    with open('posts.json', mode='w', encoding="utf-8") as json_file:
        json.dump(all_posts_in_pool, json_file)


class MyHandler(FileSystemEventHandler):
    def __init__(self,func):
        self.q = Queue()
        self.worker = func
        t = Thread(target= self.worker, args=(self.q,))
        t.daemon = True
        t.start()

        self.feeds = []
        with open('posts.json', mode='w', encoding="utf-8") as json_file:
            json.dump(self.feeds, json_file)


    def on_any_event(self, event):
        #print(event)
        pass

    # new_description = ''
    def on_created(self, event):
        print("created file with path:",event._src_path)
        file_name = event._src_path
        self.q.put(file_name)


    def on_deleted(self, event):
        print("deleted!")
        reconstruct_json()

