import multiprocessing
from time import sleep
import os

pause = False

def printing(rep):
    global pause
    for i in range(0,rep):
        print("Printing: " + str(i) + " of " + str(rep) + ", PID: " + str(os.getpid()))
        x = 0
        while x<1000000:
            x+=1
        print pause
        while pause == True:
            print("paused")
            sleep(.001)

if __name__ == '__main__':
    repsIn = input("Number of reps: ")
    p = multiprocessing.Process(target=printing, args=(repsIn,))
    p.start()
    while p.is_alive():
        raw_input("")
        print("changing")
        if pause == True:
            pause = False
        else:
            pause = True
        print(pause)
        #print("Waiting for print, PID: " + str(os.getpid()))
        #x = 0
        #while x<1000000:
        #    x+=1
    print("Print complete!")

