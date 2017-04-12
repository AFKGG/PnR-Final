# STUDENTS SHOULD NOT EDIT THIS FILE. IT WILL MAKE UPDATING MORE DIFFICULT

from gopigo import *
import time

##########################################################
#################### PIGO PARENT CLASS
#### (students will make their own class & inherit this)


class Pigo(object):

    def __init__(self):

        self.MIDPOINT = 90
        self.STOP_DIST = 17
        self.RIGHT_SPEED = 200
        self.LEFT_SPEED = 200
        self.scan = [None] * 180

        # this makes sure the parent handler doesn't take over student's
        if __name__ == "__main__":
            print('-----------------------')
            print('------- PARENT --------')
            print('-----------------------')
            # let's use an event-driven model, make a handler of sorts to listen for "events"
            self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)
            while True:
                self.stop()
                self.handler()

    ########################################
    #### FUNCTIONS REPLACED IN CHILD CHILD
    #Parent's handler is replaced by child's
    def handler(self):
        menu = {"n": ("Navigate forward", self.nav),
                "d": ("Dance", self.dance),
                "c": ("Calibrate", self.calibrate),
                "o": ("Open House Demo", self.openHouse),
                "q": ("Quit", quit)
                }
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])

        ans = raw_input("Your selection: ")
        menu.get(ans, [None, error])[1]()

    def openHouse(self):
        choice = raw_input("1) Shy;  2) Spin.. ")
        if choice == "1":
            while True:
                if not self.is_clear():
                    self.beShy()
        else:
            while True:
                if not self.is_clear():
                    for x in range(5):
                        self.encR(2)
                        self.encL(2)
                    self.encR(15)

    def beShy(self):
        self.set_speed(80, 80)
        self.encB(5)
        for x in range(3):
            servo(20)
            time.sleep(.1)
            servo(120)
            time.sleep(.1)
        self.encL(2)
        self.encR(2)
        self.encF(5)

    #Explain the purpose of the method
    #Central logic loop of my navigation
    def nav(self):
        print("Parent nav")


    ##DANCING IS FOR THE CHILD CLASS
    def dance(self):
        print('Parent dance is lame.')



    ##############################################
    ##### FUNCTIONS NOT INTENDED TO BE OVERWRITTEN
    def set_speed(self, left, right):
        set_left_speed(left)
        set_right_speed(right)
        self.LEFT_SPEED = left
        self.RIGHT_SPEED = right
        print('Left speed set to: '+str(left)+' // Right set to: '+str(right))

    def fwd(self):
        fwd()

    def encF(self, enc):
        print('Moving '+str((enc/18))+' rotation(s) forward')
        enc_tgt(1, 1, enc)
        fwd()
        time.sleep(1 * (enc / 18)+.4)

    def encR(self, enc):
        print('Moving '+str((enc/18))+' rotation(s) right')
        enc_tgt(1, 1, enc)
        right_rot()
        time.sleep(1 * (enc / 18)+.4)

    def encL(self, enc):
        print('Moving '+str((enc/18))+' rotation(s) left')
        enc_tgt(1, 1, enc)
        left_rot()
        time.sleep(1*(enc/18)+.4)


    def encB(self, enc):
        print('Moving '+str((enc/18))+ ' rotations(s) backwards')
        enc_tgt(1, 1, enc)
        bwd()
        time.sleep(1 * (enc / 18)+.4)

    def servo(self, val):
        print('Moving servo to ' + str(val) + 'deg')
        servo(val)
        time.sleep(.1)

    def dist(self):
        measurement = us_dist(15)
        time.sleep(.05)
        print('I see something ' + str(measurement) + "cm away")
        return measurement
    # DUMP ALL VALUES IN THE SCAN ARRAY
    def flush_scan(self):
        self.scan = [None]*180

    # SEARCH 120 DEGREES COUNTING BY 2's
    def wide_scan(self):
        #dump all values
        self.flush_scan()
        for x in range(self.MIDPOINT-60, self.MIDPOINT+60, +2):
            servo(x)
            time.sleep(.1)
            scan1 = us_dist(15)
            time.sleep(.1)
            #double check the distance
            scan2 = us_dist(15)
            #if I found a different distance the second time....
            if abs(scan1 - scan2) > 2:
                scan3 = us_dist(15)
                time.sleep(.1)
                #take another scan and average the three together
                scan1 = (scan1+scan2+scan3)/3
            self.scan[x] = scan1
            print("Degree: "+str(x)+", distance: "+str(scan1))
            time.sleep(.01)

    def is_clear(self):
        print("Running the is_clear method.")
        for x in range((self.MIDPOINT - 25), (self.MIDPOINT + 25), 6):
            servo(x)
            time.sleep(.1)
            scan1 = us_dist(12)
            time.sleep(.1)
            # double check the distance
            scan2 = us_dist(12)
            time.sleep(.1)
            # if I found a different distance the second time....
            if abs(scan1 - scan2) > 2:
                scan3 = us_dist(12)
                time.sleep(.1)
                # take another scan and average the three together
                scan1 = (scan1 + scan2 + scan3) / 3
            self.scan[x] = scan1
            print("Degree: " + str(x) + ", distance: " + str(scan1))
            if scan1 < self.STOP_DIST:
                print("Doesn't look clear to me")
                return False
        return True

    # DECIDE WHICH WAY TO TURN
    def choose_path(self):
        print('Considering options...')
        if self.is_clear():
            return "fwd"
        else:
            self.wide_scan()
        avgRight = 0
        avgLeft = 0
        for x in range(self.MIDPOINT-60, self.MIDPOINT):
            if self.scan[x]:
                avgRight += self.scan[x]
        avgRight /= 60
        print('The average dist on the right is '+str(avgRight)+'cm')
        for x in range(self.MIDPOINT, self.MIDPOINT+60):
            if self.scan[x]:
                avgLeft += self.scan[x]
        avgLeft /= 60
        print('The average dist on the left is ' + str(avgLeft) + 'cm')
        if avgRight > avgLeft:
            return "right"
        else:
            return "left"

    def stop(self):
        print('All stop.')
        for x in range(3):
            stop()
        servo(self.MIDPOINT)
        time.sleep(0.05)
        disable_servo()

    def calibrate(self):
        print("Calibrating...")
        servo(self.MIDPOINT)
        response = raw_input("Am I looking straight ahead? (y/n): ")
        if response == 'n':
            while True:
                response = raw_input("Turn right, left, or am I done? (r/l/d): ")
                if response == "r":
                    self.MIDPOINT += 1
                    print("Midpoint: " + str(self.MIDPOINT))
                    servo(self.MIDPOINT)
                    time.sleep(.01)
                elif response == "l":
                    self.MIDPOINT -= 1
                    print("Midpoint: " + str(self.MIDPOINT))
                    servo(self.MIDPOINT)
                    time.sleep(.01)
                else:
                    print("Midpoint now saved to: " + str(self.MIDPOINT))
                    break
        response = raw_input("Do you want to check if I'm driving straight? (y/n)")
        if response == 'y':
            while True:
                set_left_speed(self.LEFT_SPEED)
                set_right_speed(self.RIGHT_SPEED)
                print("Left: " + str(self.LEFT_SPEED) + "//  Right: " + str(self.RIGHT_SPEED))
                self.encF(18)
                response = raw_input("Reduce left, reduce right or drive? (l/r/d): ")
                if response == 'l':
                    self.LEFT_SPEED -= 10
                elif response == 'r':
                    self.RIGHT_SPEED -= 10
                elif response == 'd':
                    self.encF(18)
                else:
                    break
    
    # PRINTS THE CURRENT STATUS OF THE ROBOT
    def status(self):
        print("My power is at "+ str(volt()) + " volts")
        print('Left speed set to: '+str(self.LEFT_SPEED)+' // Right set to: '+str(self.RIGHT_SPEED))
        print('My MIDPOINT is set to: '+ str(self.MIDPOINT))
        print('I get scared when things are closer than '+str(self.STOP_DIST)+'cm')


########################
#### STATIC FUNCTIONS

def error():
    print('Error in input')


def quit():
    raise SystemExit


p = Pigo()