#!/usr/bin/env python3
import sched
import time

scheduler = sched.scheduler(time.time, time.sleep)

def print_event(name):
    print('EVENT:', time.time(), name)

now = time.time()
print( 'START:', now)
scheduler.enterabs(now+2, 2, print_event, ('first',))
scheduler.enterabs(now+2, 1, print_event, ('second',))
scheduler.enterabs(now+3, 1, print_event, ('third',))
scheduler.enterabs(now+4, 1, print_event, ('fourth',))
scheduler.enterabs(now+5, 1, print_event, ('fifth',))
scheduler.run()