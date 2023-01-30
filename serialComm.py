import serial
import io
import re
import lampState
import dummyLamp


class serialComm:
    """ A class handling the serial IO for the lamp"""
    def __init__(self,port):


        if port == 'test':
            self.sio = dummyLamp.dummyLamp()
        else:
            self.sio = serial.Serial(
                port=port,
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=5,
            )



    def togglePower(self,oldLampOn):
        if oldLampOn:
            self.closePower()
        else:
            self.openPower()
        return not oldLampOn    

    def openPower(self):
        self.sio.write(b'PW1\r\n')
        self.sio.flush()

        reply = self.sio.readline()
        if reply != b'OK\r\n':
            raise Exception('Unknown response form device' +reply.decode('utf_8'))

    def closePower(self):
        self.sio.write(b'PW0\r\n')
        self.sio.flush()

        reply = self.sio.readline()
        if reply != b'OK\r\n':
            raise Exception('Unknown response form device' +reply.decode('utf_8'))



    def toggleShutter(self,oldShutterOpen):
        if oldShutterOpen:
            self.closeShutter()
        else:
            self.openShutter()
        return not oldShutterOpen    


    def openShutter(self):
        self.sio.write(b'S1\r\n')
        self.sio.flush()

        reply = self.sio.readline()
        if reply != b'OK\r\n':
            raise Exception('Unknown response form device' +reply.decode('utf_8'))

    def closeShutter(self):
        self.sio.write(b'S0\r\n')
        self.sio.flush()

        reply = self.sio.readline()
        if reply != b'OK\r\n':
            raise Exception('Unknown response form device' +reply.decode('utf_8'))

    def setIntensity(self,intensity):
        self.sio.write(b'LI'+str(intensity).encode('utf_8')+b'\r\n')
        self.sio.flush
        reply = self.sio.readline()
        if reply != b'OK\r\n':
            raise Exception('Unknown response form device' +reply.decode('utf_8'))

    def endRemote(self):        
        self.sio.write(b'L\r\n')
        self.sio.flush()
        reply = self.sio.readline()
        if reply != b'OK\r\n':
            raise Exception('Unknown response form device' +reply.decode('utf_8'))

    def getLampState(self):

        self.sio.write(b'S?\r\n')
        self.sio.flush()

        reply = self.sio.readline()
        if reply == b'SHUTTER OPEN\r\n':
            shutter = True
        elif reply == b'SHUTTER CLOSE\r\n':
            shutter = False
        else:
            raise Exception('Unknown response form device' +reply.decode('utf_8'))

        self.sio.write(b'T?\r\n')
        self.sio.flush()

        reply = self.sio.readline()
        number = re.findall("\d+\.\d+",reply.decode('utf_8'))[0]
        timer =  float(number)
        
        self.sio.write(b'LI?\r\n')
        self.sio.flush()

        reply = self.sio.readline()
        number = re.findall("\d+",reply.decode('utf_8'))[0]
        intensity =  int(number)

        self.sio.write(b'PW?\r\n')
        self.sio.flush()

        reply = self.sio.readline()
        if reply == b'LAMP ON\r\n':
            lamp = True
        elif reply == b'LAMP OFF\r\n':
            lamp = False
        else:
            raise Exception('Unknown response form device' +reply.decode('utf_8'))

        self.sio.write(b'LIFE?\r\n')
        self.sio.flush()

        reply = self.sio.readline()
        number = re.findall("\d+\.\d+",reply.decode('utf_8'))[0]
        life =  float(number)


        self.sio.write(b'VER?\r\n')
        self.sio.flush()

        reply = self.sio.readline()
        version = reply.decode('utf_8')

        initialState = lampState.HAL320(shutter,timer,intensity,lamp,life,version)
        return initialState


        