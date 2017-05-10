import pigo
import time
import random
import logging
'''
MR. A's Final Project Student Helper
'''

class GoPiggy(pigo.Pigo):

    ########################
    ### CONTSTRUCTOR - this special method auto-runs when we instantiate a class
    #### (your constructor lasted about 9 months)
    ########################

    def __init__(self):
        LOG_LEVEL = logging.INFO
        # LOG_LEVEL = logging.DEBUG
        LOG_FILE = "/home/pi/PnR-Final/log_robot.log"
        LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
        logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)
        print("Your piggy has be instantiated!")
        # Our servo turns the sensor. What angle of the servo( ) method sets it straight?
        self.MIDPOINT = 85
        # YOU DECIDE: How close can an object get (cm) before we have to stop?
        self.STOP_DIST = 23
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.LEFT_SPEED = 130
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.RIGHT_SPEED = 140
        # This one isn't capitalized because it changes during runtime, the others don't
        self.turn_track = 0
        # Our scan list! The index will be the degree and it will store distance
        self.scan = [None] * 180
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        while True:
            self.stop()
            self.menu()


    ########################
    ### CLASS METHODS - these are the actions that your object can run
    #### (they can take parameters can return stuff to you, too)
    #### (they all take self as a param because they're not static methods)
    ########################


    ##### DISPLAY THE MENU, CALL METHODS BASED ON RESPONSE
    def menu(self):
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like to add an experimental method
        menu = {"n": ("Navigate forward", self.nav),
                "d": ("Dance", self.dance),
                "c": ("Calibrate", self.calibrate),
                "t": ("Turn test", self.turn_test),
                "s": ("Check status", self.status),
                "o": ("Count Obstacles", self.count_obstacle),
                "r": ("Total Obstacles", self.total_obstacles),
                "q": ("Quit", quit)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = raw_input("Your selection: ")
        # activate the item selected
        menu.get(ans, [None, error])[1]()

    def count_obstacle(self):
        self.wide_scan()
        # count how many obstacles I've found
        counter = 0
        found_something = False
        # loop through all my scan data
        for x in self.scan:
            # if x is not None and really close
            if x and x <= self.STOP_DIST:
                # if I've already found something
                if found_something:
                    print("obstacle continues")
                # if this is a new obstacles
                else:
                    # switch my tracker
                    found_something = True
                    print("start of new obstacle")
            # if my data show safe distances...
            if x and x > self.STOP_DIST:
                # if my tracker is been triggered
                if found_something:
                    print("end of obstacle")
                    # reset tracker
                    found_something = False
                    # increase count of obstacles
                    counter += 1
        print('Total number of obstacles in this scan: ' + str(counter))
        return counter



    def turn_test(self):
        while True:
            ans = raw_input('Turn right, left or stop? (r/l/s): ')
            if ans == 'r':
                val = int(raw_input('/nBy how much?: '))
                self.encR(val)
            elif ans == 'l':
                val = int(raw_input('/nBy how much?: '))
                self.encL(val)
            else:
                break
        self.restore_heading()

    def total_obstacles(self):
        counter = 0
        for x in range(4):
            counter += self.count_obstacle()
            self.encR(7)
        print('Total number of obstacles in this scan: ' + str(counter))

    def restore_heading(self):
        print("Now I will turn back to the starting position.")
        if self.turn_track > 0:
            self.encL(abs(self.turn_track))
        elif self.turn_track < 0:
            self.encR(abs(self.turn_track))

    def sweep(self):
        for x in range(self.MIDPOINT - 60, self.MIDPOINT + 60, 2):
            self.servo(x)
            self.scan[x] = self.dist()
        print("Here's what I saw")
        print(self.scan)
        print("Here's how I usually print this:")
        for x in self.scan:
            print(x)

    def safety_dance(self):
        for y in range(3):
            for x in range(self.MIDPOINT - 60, self.MIDPOINT + 60, 2):
                self.servo(x)
                if self.dist() < 30:
                    print("AAAAAAAHHHHHH")
                    return
            self.encR(7)
        self.dance()


    # YOU DECIDE: How does your GoPiggy dance?
    def dance(self):
        print("Piggy dance")
        ##### WRITE YOUR FIRST PROJECT HERE
        for x in range(3):
            self.shimmy()
            #self.cool()

    def head(self):
        for x in range(2):
            self.servo(20)
            self.servo(160)
            self.servo(80)
            self.servo(90)
        self.servo(self.MIDPOINT)

    def shimmy(self):
        self.servo(135)
        self.encR(7)
        self.encF(10)
        self.servo(35)
        self.encL(7)
        self.encB(10)
        self.encR(7)
        self.encF(10)
        self.encL(20)
        self.servo(10)
        self.encF(5)
        self.encB(5)
        self.head()
        for x in range(2):
            self.encF(10)
            self.encB(10)

    def cool(self):
        self.encR(30)
        self.encL(30)
        self.servo(80)
        self.servo(90)
        self.encF(50)
        self.encL(36)
        for x in range(160, 80, -10):
            self.servo(160)
        for x in range(20, 80, 10):
            self.servo(20)


    ######################### ### MAIN LOGIC LOOP - the core algorithm of my navigation
    ### (kind of a big deal###    ########################

    def nav(self):
        logging.debug("Starting the nav method")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("[ Press CTRL + C to stop me, then run stop.py ]\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        # this is the loop part of the "main logic loop"
        count = 0
        while True:
            if self.is_clear():
                print("Looks clear, pulsing forward")
                self.encF(15)
                # Avoid being stuck at the corner
                count += 1
                if count >= 4 and self.turn_track != 0:
                    logging.info("Count is now " + str(count) + ", restoring heading")
                    print("Count is now " + str(count) + ", restoring heading")
                    # Moving forward before restore heading which creates distance from the previous obstacle
                    self.restore_heading()
                    count = 0
            # Choose path
            answer = self.choose_path()
            logging.info("Choose path has told me to go: " + answer)
            print("Choose path has told me to go: " + answer)
            if answer == "left":
                self.encL(5)
                self.encF(2)
                self.maneuver()
            elif answer == "right":
                self.encR(5)
                self.encF(2)
                self.maneuver()

    def maneuver(self):
        # I need to check my left side
        if self.turn_track > 0:
            while self.is_clear():
                self.encF(10)
                self.servo(self.MIDPOINT + 60)
                # Restore heading if clear
                if self.dist() > self.STOP_DIST + 20:
                    self.encF(5)
                    self.restore_heading()
                    logging.info("")
                    return
                self.servo(self.MIDPOINT)
        # Check left side
        else:
            while self.is_clear():
                self.encF(10)
                self.servo(self.MIDPOINT - 60)
                # Restore heading if clear
                if self.dist() > self.STOP_DIST + 20:
                    self.encF(5)
                    self.restore_heading()
                    return
                self.servo(self.MIDPOINT)


    def encR(self, enc):
        pigo.Pigo.encR(self, enc)
        self.turn_track += enc

    def encL(self, enc):
        pigo.Pigo.encL(self, enc)
        self.turn_track -= enc

####################################################
############### STATIC FUNCTIONS ###################

def error():
    print('Error in input')


def quit():
    raise SystemExit

##################################################################
######## The app starts right here when we instantiate our GoPiggy

try:
    g = GoPiggy()
except (KeyboardInterrupt, SystemExit):
    from gopigo import *
    stop()
except Exception as ee:
    logging.error(ee.__str__())