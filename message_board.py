import time
from matrix import dispMatrix
import requests
from random import randint
from _thread import start_new_thread

class MessageB(object):
    def __init__(self):
        self.ip_address = '192.168.1.10'
        self.df = dispMatrix(1,0)
        self.txt = [30,0,0]
        self.fg = [0,0,0]
        start_new_thread(self.display,())

    def display(self):
        data = []

        r = requests.get("http://%s/?r%sg%sb%s&%s?" % (self.ip_address,str(self.fg[0]),str(self.fg[1]),str(self.fg[2]),"99"))
        try:
            while True:
                data = self.df.frame()
                s_data = [str(x) for x in data]
                res = '-'.join(s_data)
                #print(res)
                if len(res) == 0:
                    r = requests.get("http://%s/?r%sg%sb%s&%s?" % (self.ip_address,str(self.fg[0]),str(self.fg[1]),str(self.fg[2]),""))
                else:
                    r = requests.get("http://%s/?r%sg%sb%s&%s?" % (self.ip_address,str(self.txt[0]),str(self.txt[1]),str(self.txt[2]),res))
                time.sleep(0.1)
        except KeyboardInterrupt:
            r = requests.get("http://%s/?r%sg%sb%s&%s?" % (self.ip_address,"0","0","0","99"))
            r = requests.get("http://%s/?r%sg%sb%s&%s?" % (self.ip_address,"0","0","0"," "))

    def message(self,msg):
        self.df.generate_message(msg)