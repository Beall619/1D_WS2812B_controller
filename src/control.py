from threading import Thread
from multiprocessing import Queue
from time import sleep

import json

import board, neopixel

import animation

class safe_control:
    def __init__(self, control_obj):
        self.buffer = []
        self.max_brightness = .7
        self.current_brightness = .4
        
        self.is_off = False
   
        self.control_obj = control_obj

        self.num_leds = 96

        self.leds = neopixel.NeoPixel(board.D12, self.num_leds, auto_write=False, brightness=self.current_brightness)

    def calc_brightness(self, wanted_brightness):
        res = (self.max_brightness)*(wanted_brightness)
        if res>self.max_brightness:
            res = self.max_brightness
        return res

    def play_buffer(self):
        if(self.is_off):
            self.buffer=[]
            return None
        for l in self.buffer:
            	self.leds[l[0]] = l[1:len(l)]   
        self.buffer = []
        self.leds.write()

    def set_brightness(self, brightness):
        brightness = self.calc_brightness(brightness)
        self.leds.brightness = brightness
        self.current_brightness = brightness

    def turn_off(self):
        for i in range(0, self.num_leds):
            self.buffer.append([i,0,0,0])
        self.play_buffer()
        self.is_off = True

    def turn_on(self):
        self.is_off = False

class control:
    def __init__(self, main_queue):
        self.queue = Queue()
        self.main_queue = main_queue
        self.safe_control = safe_control(self)
        self.is_interupt = False

        self.thread = Thread()
        self.thread.run = self.thread_run

        self.animation_iter = 0
        self.change_animation_set()

        self.start_new_animation()

        self.thread.start()

    def change_animation_set(self, a_set=None):
        if(a_set is None):
            with open("data/current_set.json") as file:
                self.animation_set = json.load(file)
        else:
            self.animation_set = a_set


    def start_new_animation(self, a=None):
        if(a==None):
            self.animation = animation.animation(self.safe_control, self.animation_set[self.animation_iter])
            self.animation_iter += 1
            if(self.animation_iter > len(self.animation_set)-1):
                self.animation_iter = 0
        else:
            self.animation = animation.animation(self.safe_control, a)

    def thread_run(self):
        while 1:
            if(self.is_interupt and not self.animation.is_done):
                sleep(.1)
                continue
            if(self.animation.is_done):
                self.start_new_animation()
            
            #self.check_interupts()
            sleep(.1)
