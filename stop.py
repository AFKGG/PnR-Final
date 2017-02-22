from gopigo import *
import time

# KEEP THIS APP READY TO CALL IN CASE YOUR ROBOT GOES ON A RAMPAGE

for x in range(5):
    stop()
    time.sleep(.1)

disable_servo()