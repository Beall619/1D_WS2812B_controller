from time import sleep as tsleep
from random import randint

def write_all(r,g,b,safe_control):
    for i in range(0,96):
        safe_control.buffer.append([i,r,g,b])
    safe_control.play_buffer()

def sleep(secs,kill):
    if(kill):
        exit()

    tsleep(secs)


class programmed_animation:
    def __init__(self, safe_control):
        self.safe_control = safe_control
        self.kill = False
    def stop(self):
        self.kill = True

class rainbow(programmed_animation):
    def run(self):
        sleeptime = .2

        red = 255
        green = 0
        blue = 0

        for i in range(1, 256):
            red -= 1
            green+=1
            sleep(sleeptime,self.kill)
            write_all(red,green,blue,self.safe_control)

        for i in range(1, 256):
            green -= 1
            blue += 1
            sleep(sleeptime,self.kill)
            write_all(red,green,blue,self.safe_control)

        for i in range(1, 256):
            blue -= 1
            red += 1
            sleep(sleeptime,self.kill)
            write_all(red,green,blue,self.safe_control)

class randomness(programmed_animation):
    def run(self):
        for i in range(0,randint(0,11)):
            self.safe_control.buffer.append([randint(0,95),randint(0,255),randint(0,255),randint(0,255)])
        self.safe_control.play_buffer()
        sleep(.1,self.kill)

class run_around(programmed_animation):
    def run(self):
        for i in range(0,96):
            write_all(0,0,0,self.safe_control)

            self.safe_control.buffer.append([i-2,255,255,255])
            self.safe_control.buffer.append([i-1,255,255,255])
            self.safe_control.buffer.append([i,255,255,255])

            self.safe_control.play_buffer()

class white_light(programmed_animation):
    def run(self):
        write_all(255,255,255, self.safe_control)