import control
from multiprocessing import Queue
from webserver import webserver
from subprocess import check_output


def server_stats():
    uptime_result=str(check_output("uptime -p",shell=1).rstrip())
    uptime_result=uptime_result[2:len(uptime_result)-1]
    stats = {
        "uptime":uptime_result,
        "led power":int(not con.safe_control.is_off),
        "brightness":con.safe_control.current_brightness,
        "current animation":con.animation.animation_instructions[0]
    }
    return stats


q = Queue()
con = control.control(q)

webserv = webserver(con.safe_control, server_stats)

print(server_stats())
con.thread.join()
webserv.thread.join()