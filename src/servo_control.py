import serial
import time
from controller import Controller

async def init_servos() -> serial.Serial:
    print('[init_servos] create arduino object')
    # Creates arduino object
    # try:
    #     arduino = serial.Serial('/dev/ttyACM0', 9600)
    # except():
    arduino = serial.Serial('/dev/ttyACM1', 9600)

    print('[init_servos] setup serial port for arduino')
    arduino.setDTR(False)
    time.sleep(0.1) # Initially set to 1
    arduino.flushInput()
    arduino.setDTR(True)
    time.sleep(0.1) # Initially set to 2
    print('[init_servos] arduino ready!')
    return arduino

async def update_servos(controller: Controller, arduino: serial.Serial):
    angle = controller.angle
    arduino.write((str(angle) + '\r').encode())
    print(f'[update_servos] t: {angle}')