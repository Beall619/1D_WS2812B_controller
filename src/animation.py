from threading import Thread
from multiprocessing import Queue
from datetime import datetime, timedelta
from time import sleep
import json
import sys
sys.path.append("data/animations")
programmed_animations = __import__("programmed_animations")

class animation:
    def __init__(self, safe_control, animation_instructions):
        self.safe_control = safe_control
        self.animation_instructions = animation_instructions

        self.thread = Thread()

        if(self.get_type(animation_instructions[0]) == "frames"):
            self.thread.run = self.thread_mapped_run
        else:
            self.thread.run = self.thread_programmed_run

        self.is_done = False

        self.thread.start()
    
    def thread_programmed_run(self):
        anim_code = self.load_programmed_animation(self.animation_instructions[0])

        anim_thread = Thread()

        anim_thread.run = anim_code.run

        times_to_repeat, end_time = self.get_timeout_info()

        repeated_times = 0

        anim_thread.start()

        while(repeated_times < times_to_repeat and not datetime.now() > end_time):
            sleep(.1)
            if(not anim_thread.isAlive()):
                repeated_times += 1
                #do it again, have to re-create Thread() object
                anim_thread = Thread()
                anim_thread.run = anim_code.run
                anim_thread.start()
        
        anim_code.stop()
        anim_thread.join()

        self.is_done = True

    def get_timeout_info(self):
        if(self.animation_instructions[1][0] == "repeat"):
            times_to_repeat = self.animation_instructions[1][1]
            end_time = datetime.now()+timedelta(weeks=999)
        else:
            times_to_repeat = float("inf")
            end_time = datetime.now()+timedelta(seconds=self.animation_instructions[1][1])

        return times_to_repeat, end_time

    def thread_mapped_run(self):
        times_to_repeat, end_time = self.get_timeout_info()

        animation_frames = self.load_mapped_animation(self.animation_instructions[0])
        repeated_times = 0
        frame = 0
        while(repeated_times < times_to_repeat and not end_time>datetime.now()):
            if(frame > len(animation_frames)-1):
                frame = 0
                repeated_times += 1
            if(animation_frames[frame] == "sleep"):
                sleep(animation_frames[frame][1])
                frame+=1
                continue
            for led in animation_frames[frame]:
                self.safe_control.buffer.append(led)
            frame+=1
            self.safe_control.play_buffer()
        self.is_done = True

    def load_mapped_animation(self, animation_name):
        with open("data/animations/%s.anim"%(animation_name)) as file:
            return json.load(file)
    
    def load_programmed_animation(self, animation_name):
        return getattr(programmed_animations, animation_name)(self.safe_control)

    def get_type(self, animation_name):
        with open("data/types.json") as file:
            data = json.load(file)
        return data[animation_name]