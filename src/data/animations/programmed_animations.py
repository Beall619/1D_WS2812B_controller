from time import sleep as tsleep
from random import randint

def write_all(r,g,b,safe_control_queue):
    for i in range(0,90):
        safe_control_queue.put(["u",i,r,g,b])
    safe_control_queue.put(["p"])

def sleep(secs,kill):
    if(kill):
        exit()

    tsleep(secs)
class rainbow:
    def __init__(self, safe_control_queue):
        self.safe_control_queue = safe_control_queue
        self.kill = False
    def stop(self):
        self.kill = True
    def run(self):
        sleeptime = .2

        red = 255
        green = 0
        blue = 0

        for i in range(1, 256):
            red -= 1
            green+=1
            sleep(sleeptime,self.kill)
            write_all(red,green,blue,self.safe_control_queue)

        for i in range(1, 256):
            green -= 1
            blue += 1
            sleep(sleeptime,self.kill)
            write_all(red,green,blue,self.safe_control_queue)

        for i in range(1, 256):
            blue -= 1
            red += 1
            sleep(sleeptime,self.kill)
            write_all(red,green,blue,self.safe_control_queue)

class randomness:
    def __init__(self, safe_control_queue):
        self.safe_control_queue = safe_control_queue
        self.kill = False
    def stop(self):
        self.kill = True
    def run(self):
        for i in range(0,randint(0,11)):
            self.safe_control_queue.put(["u",randint(0,90),randint(0,255),randint(0,255),randint(0,255)])
        self.safe_control_queue.put(["p"])
        sleep(.1,self.kill)
