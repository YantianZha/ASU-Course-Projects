#!/usr/bin/env python

import time

## Define a static Pomodoro timer.
def Countdown():
        p = 2.00
        alarm = time.time() + p
        while True: ## Loop infinitely
            n = time.time()
            if n < alarm:
 #               print(round(alarm - n))
            else:
                print("Time's up!")
                break

Countdown()
