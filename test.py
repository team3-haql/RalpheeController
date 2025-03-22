import serial
import time
from inputs import get_gamepad
import math
import threading
import moteus
import asyncio

MAX_SPEED = 2
CONTROLLER_COUNT = 1

class Controller(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / Controller.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / Controller.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = event.state / Controller.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / Controller.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / Controller.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / Controller.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state #previously switched with X
                elif event.code == 'BTN_WEST':
                    self.X = event.state #previously switched with Y
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state

controller = Controller()

async def moteus_controller(): # return the buttons/triggers that you care about in this methode
    print('Init Controller')

    qr = moteus.QueryResolution()
    qr.trajectory_complete = moteus.INT8

    SERVO_IDS = [1]

    controllers = []
    for id in SERVO_IDS:
        controllers.append(moteus.Controller(id, query_resolution=qr))

    print('set stop')

    for c in controllers:
        await c.set_stop()

    print('ready!')

    while True:
        velocity = controller.LeftJoystickY*MAX_SPEED
        if abs(controller.LeftJoystickY) < 0.1:
            velocity = 0
        for c in controllers:
            await c.set_position(position=math.nan, velocity=velocity, query=True)
        # print(f'v: {velocity}')

        if controller.B == 1:
            break
        
        for c in controllers:
            await c.flush_transport()
        await asyncio.sleep(0.02)

def arduino():
    # print('arduino init')
    arduino = serial.Serial('/dev/ttyACM0', 9600)

    arduino.setDTR(False)
    time.sleep(1)
    arduino.flushInput()
    arduino.setDTR(True)
    time.sleep(2)

    while True:
        angle = controller.RightJoystickX
        if abs(controller.RightJoystickX) < 0.1:
            angle = 0
        arduino.write((str(angle) + '\n').encode())
        # print(f't: {angle}')

        if controller.B == 1:
            break

if __name__ == '__main__':
    # joy.arduino()
    # arduino_thread = threading.Thread(target=arduino)
    # arduino_thread.daemon = True
    # arduino_thread.start()
    asyncio.run(moteus_controller())