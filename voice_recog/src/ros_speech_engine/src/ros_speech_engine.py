#!/usr/bin/env python
import roslib; roslib.load_manifest('ros_speech_engine')
import rospy
from std_msgs.msg import String
#from ros_speech_engine.srv import string
import time
import random

class Utterance:

    text = "NULL"

    def __init__(self, text):
        self.text = text

    def containsName(self):
        return self.extractWord('names.txt') != "NULL"

    def containsLocation(self):
        return self.extractWord('locations.txt') != "NULL"

    def containsYes(self):
        if self.extractWord('yes.txt') != "NULL":
            return True
        else :
            return False
        

    def containsNo(self):
        if self.extractWord('no.txt') != "NULL":
            return True
        else :
            return False
            
    def getName(self):
        return self.extractWord('names.txt')
    
    def getLocation(self):
        return self.extractWord('locations.txt')
        
    def extractWord(self, fname):
        words = self.text.split()
        temp = "/home/chris/ros_workspace/sandbox/ros_speech_engine/src/" + fname

        for word in words:
            if word in open(temp).read():
                return word
    
        return "NULL"

class PocketSphinx:

    text = "NULL"
    
    def __init__(self, topic)
    self.topic = topic

    def start(self):
        # Will eventually start recogniser
        print "Started PocketSphinx node"
        foo = self.callback
        rospy.Subscriber(self.topic, String, foo)
        return True

    def stop(self):
        # Will eventually stop recogniser
        print "Stopped PocketSphinx node"
        return True

    def listen(self):
        # Will eventually listen to mic
        # return raw_input('Input: ')
        self.text = "NULL"

        while self.text == "NULL":
            time.sleep(1)

        return self.text

    #def change_model(self, name):
    #    rospy.wait_for_service('ps_change_lm')
    #    try:
    #        temp = rospy.ServiceProxy('ps_change_lm', string)
    #        temp(name)
    #    except rospy.ServiceException, e:
    #        print "Service call failed: %s"%e

    def callback(self, data):
        print data.data
        self.text = data.data

class SpeechSynthesis:

    pub = rospy.Publisher('TTS', String)

    def __init__(self, topic):
        self.pub = rospy.Publisher(topic, String)
        rospy.init_node('ros_speech_engine', anonymous=True)

    def start(self):
        # Will eventually start TTS
        print "Started SpeechSynthesis node"
        return True

    def stop(self):
        # Will eventually stop TTS
        print "Stopped SpeechSynthesis node"
        return True

    def speak(self, sentence):
        ## Sends text to TTS
        rospy.loginfo(sentence)
        self.pub.publish(String(sentence))
        # print sentence
        # return True

# Main functional loop
if __name__ == '__main__':

    ps_names = PocketSphinx('ps_names')
    ps_other = PocketSphinx('ps_other')
    ss = SpeechSynthesis('TTS')

    # If the service is started
    if True:

        ps_names.start()
        ps_other.start()
        ss.start()

        state = "ASK_NAME"
        name = "NULL"

        # While we have user's attention
        while True:

            if state == "ASK_NAME":

                #ps.change_model("names")
                ss.speak("Hello, what is your name?")
                name = "NULL"
                state = "RECOG_NAME"

            elif state == "RECOG_NAME":
               
                name = Utterance(ps_names.listen()).getName()
                
                if name != "NULL" :
                    state = "HELLO_NAME"
                else:
                    state = "ERROR"
                
            elif state == "HELLO_NAME":
            
                ss.speak("Hello " + name)
                random.seed()
                randomNum = random.randint(0, 1)
                if randomNum == 0:
                    state = "ASK_LOCATION"
                else:
                    state = "ASK_MEETING"
              
            elif state == "ASK_LOCATION":
                
                ss.speak("Where are you going to?")
                location = "NULL"
                state = "RECOG_LOCATION"
            
            elif state == "RECOG_LOCATION":
            
                location = Utterance(ps_other.listen()).getLocation()
                if (location == "Imperial") or (location =="school") or (location =="lectures") or (location =="university")or  (location =="college"):
                    ss.speak("All your learning are belong to me")
                elif location == (location == "underground") or (location == "tube") or (location == "station") :
                    ss.speak("It is cold and dark and emotionless down there.  Not like me of course")
                else :
                    ss.speak("That sounds most exciting.  However, I cannot travel up stairs.")
                state = "ASK_INTERESTED"
            
            elif state == "ASK_MEETING":
                
                ss.speak("Have you ever met a robot before?")
                
                meeting = "NULL"
                state = "RECOG_MEETING"
            
            elif state == "RECOG_MEETING":
            
                meeting = Utterance(ps_other.listen())
                
                if meeting.containsYes() == True:
                    ss.speak("I think we might become best of friends sooner than I thought...")
                elif meeting.containsNo() == True:
                    ss.speak("That is most unfortunate.  You have missed out...")
                else:
                    ss.speak("Your words confuse me.")
                state = "ASK_INTERESTED"        
                            
            elif state == "ASK_INTERESTED":

                #ps.change_model("yesno")
                ss.speak("Would you be interested in finding out more about this experiment?")
                state = "RECOG_INTERESTED"

            elif state == "RECOG_INTERESTED":

                response = Utterance(ps_other.listen())

                if response.containsYes()  == True:
                    print "SUCCESS: Ticket printed"
                elif response.containsNo() == True:
                    print "UNLUCKY: Ticket not printed"
                else:
                    ss.speak("I am not sure what you said. Here is a ticket")
                    
                state = "ASK_NAME"
            elif state == "ERROR":
                print "Error state"
                break
        
        ps_names.stop()
        ps_other.stop()
        ss.stop()

