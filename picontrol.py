
"""Written by Saravanan 
   Visit Blog at http://mypiprojects.blogspot.in/2013/12/controlling-raspberry-pi-gpio-using.html"""

from tweepy import *
import tweepy
import RPi.GPIO as gpio
import pickle as pkl
import time

#import RPi.GPIO as gpio
last_id = '0'
ledstat = False
gpio.cleanup()
gpio.setmode(gpio.BOARD)
gpio.setup(7,gpio.OUT)
gpio.output(7,ledstat)

def authenticate():
    
    consumer_token = "xxxxxxxx...xxxxxxxxxx"#put your credentials here
    consumer_secret = "xxxxxxxxxxxxxxxx...xxxxxxxxxxxxxxxx"#

    auth = tweepy.OAuthHandler(consumer_token,consumer_secret)

    access_token = "xxxxxxxxxxxxxxx.........xxxxxxxxxxx"#
    access_token_secret = "xxxxxxxxxx...............xxxxxxxxxxxxxx"#

    auth.set_access_token(access_token,access_token_secret)

    api = tweepy.API(auth)

    return api


def check_new_DM(api):

    global last_id
    
    DMstatus = api.direct_messages(since_id = last_id,count = 1)

    if len(DMstatus)>0:
        
        last_id = DMstatus[0].id_str
        
        if (DMstatus[0].sender_screen_name == '___________'):#replace _______ with the account from which you want to control
            return DMstatus[0]

    print "\nNo new DM found"
    
    return None


def action(api,newDM):
    
    global ledstat

    DM = "Hi,\n"
    
    if newDM.text  == "ON":
        if ledstat == False:
            ledstat = True
            gpio.output(7,ledstat)
            DM = DM + "LED Turned ON\n"#+"DM id : "+newDM.id_str
            print "LED ON"
        else:
            DM = DM + "LED Already ON\n"#+"DM id : "+newDM.id_str
            print "LED Uneffected"

    elif newDM.text == "OFF":
        if ledstat==True:
            ledstat = False
            gpio.output(7,ledstat)
            DM = DM + "LED Turned OFF\n"#+"DM id : "+newDM.id_str
            print "LED OFF"

        else:
            DM = DM + "LED Already OFF\n"#+"DM id : "+newDM.id_str
            print "LED Uneffected"
	
    else:
        DM = DM + " Invalid Command : " + newDM.text
        
    return_DM(api,DM)
    
    return None


def return_DM(api,DM):

    api.send_direct_message(user = '___________',text = DM) # controlling account screen name as in line 42
    print "DM sent"
    return None
    

if __name__ == '__main__':

    print "Authenticating ...."
    api = authenticate()
    print "\nComplete."

    try:
        while(True):

            print "\nChecking for new DM..."
            DMstat = check_new_DM(api)
            if not(DMstat == None) :
                action(api,DMstat)
            for i in range(0,8):
                checktime = 240 - i*30
                print "Checking for new DM in " + str(checktime) + " s....."
                time.sleep(30)
        
    except KeyboardInterrupt:
        gpio.cleanup()

    finally:
        gpio.cleanup()

