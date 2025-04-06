import serial
import time
from controller import controller

async def init_servos():
    print('arduino init')
    arduino = serial.Serial('/dev/ttyACM0', 9600)

    arduino.setDTR(False)
    time.sleep(0.2)
    arduino.flushInput()
    arduino.setDTR(True)
    time.sleep(0.2)

    print('arduino ready!')
    return arduino

async def update_servos(arduino):
    angle = controller.RightJoystickX
    if abs(controller.RightJoystickX) < 0.1:
        angle = 0
    arduino.write((str(angle) + '\n').encode())
    print(f't: {angle}')