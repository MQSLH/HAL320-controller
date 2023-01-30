import lampState
import re
import random
import time

class dummyLamp:
    """A class for a virtual lamp for testing"""
    def __init__(self):
        self.state = lampState.HAL320(False,10.0,50,False,134.2,'API test dummy')
        self.nextReply = b''

    def write(self,lineIn):
        if lineIn == b'S0\r\n':
            self.state.shutterOpen = False
            self.nextReply = b'OK\r\n'

        elif lineIn == b'S1\r\n':
            self.state.shutterOpen = True
            self.nextReply = b'OK\r\n'

        elif lineIn == b'S?\r\n':
            if self.state.shutterOpen:
                self.nextReply = b'SHUTTER OPEN\r\n'
            else:
                self.nextReply = b'SHUTTER CLOSE\r\n'

        elif lineIn == b'TS\r\n':
            self.nextReply = b'OK\r\n' 

        elif lineIn == b'TP\r\n':
            self.nextReply = b'OK\r\n'

        elif lineIn == b'T?\r\n':
            self.nextReply = b'T'+str(self.state.timer).encode('utf_8') + b'\r\n'

        elif lineIn == b'LIFE?\r\n':
            self.nextReply = b'LF' + str(self.state.life).encode('utf_8') + b'\r\n'

        elif lineIn[0:2] == b'LI':
            if lineIn == b'LI?\r\n':
                self.nextReply = b'LI'+str(self.state.intensity).encode('utf_8') + b'\r\n'
            else:
                self.state.intensity = int(lineIn[2:-2])
                self.nextReply = b'OK\r\n'

        elif lineIn == b'PW1\r\n':
            self.state.lampOn = True
            self.nextReply = b'OK\r\n'

        elif lineIn == b'PW0\r\n':
            self.state.lampOn = False
            self.nextReply = b'OK\r\n'

        elif lineIn == b'PW?\r\n':
            if self.state.lampOn:
                self.nextReply = b'LAMP ON\r\n'
            else:
                self.nextReply = b'LAMP OFF\r\n'

        elif lineIn == b'L\r\n':
            self.nextReply = b'OK\r\n'


        elif lineIn == b'VER?\r\n':
            self.nextReply = b'API test dummy\r\n' 
    
    def readline(self):
        time.sleep(random.random() * 0.1)
        return self.nextReply


    def flush(self):
        pass