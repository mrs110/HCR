#!/usr/bin/env python
import roslib; roslib.load_manifest('ros_speech_engine')
import rospy
from std_msgs.msg import String

class Utterance:

    text = "NULL"

    def __init__(self, text):
        self.text = text

    def containsName(self):
        return self.extractWord('names.txt') != "NULL"

    def containsLocation(self):
        return self.extractWord('locations.txt') != "NULL"

    def containsYes(self):
        return self.extractWord('yes.txt') != "NULL"

    def containsNo(self):
        return self.extractWord('no.txt') != "NULL"

    def getName(self):
        return self.extractWord('names.txt')

    def extractWord(self, fname):
        words = self.text.split()
        temp = "/home/chris/ros_workspace/sandbox/ros_speech_engine/src/" + fname

        for word in words:
            if word in open(temp).read():
                return word
    
        return "NULL"

class PocketSphinx:

    def start(self):
        # Will eventually start recogniser
        print "Started PocketSphinx node"
        return True

    def stop(self):
        # Will eventually stop recogniser
        print "Stopped PocketSphinx node"
        return True

    def listen(self):
        # Will eventually listen to mic
        return raw_input('Input: ')

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

    ps = PocketSphinx()
    ss = SpeechSynthesis('TTS')

    # If the service is started
    if True:

        ps.start()
        ss.start()

        state = "ASK_NAME"
        name = "NULL"

        # While we have user's attention
        while True:

            if state == "ASK_NAME":

                ss.speak("Hello, what is your name?")
                name = "NULL"
                state = "RECOG_NAME"

            elif state == "RECOG_NAME":
               
                name = Utterance(ps.listen()).getName()
 
                if name != "NULL" :
                    state = "ASK_INTERESTED"
                else:
                    state = "ERROR"

            elif state == "ASK_INTERESTED":

                ss.speak("Hello " + name + ", would you be interested in finding out more about this experiment?")
                state = "RECOG_INTERESTED"

            elif state == "RECOG_INTERESTED":

                response = Utterance(ps.listen())

                if response.containsYes():
                    print "SUCCESS: Ticket printed"
                    state = "ASK_NAME"
                elif response.containsNo():
                    print "SUCCESS: Ticket not printed"
                    state = "ASK_NAME"
                else:
                    state = "ERROR"

            elif state == "ERROR":
                print "Error state"
                break
        
        ps.stop()
        ss.stop()

