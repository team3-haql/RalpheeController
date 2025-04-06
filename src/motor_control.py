import moteus
from controller import controller
import asyncio
import math

MAX_SPEED = 2
SERVO_IDS = [1]

async def init_motors():
    print('Init Motors')
    print('Init Controller')

    qr = moteus.QueryResolution()
    qr.trajectory_complete = moteus.INT8

    controllers = []
    for id in SERVO_IDS:
        controllers.append(moteus.Controller(id, query_resolution=qr))

    print('set stop')

    for c in controllers:
        await c.set_stop()

    print('ready!')
    return controllers

async def update_motors(controllers):
    velocity = controller.LeftJoystickY*MAX_SPEED
    if abs(controller.LeftJoystickY) < 0.1:
        velocity = 0
    for c in controllers:
        await c.set_position(position=math.nan, velocity=velocity, query=True)
    print(f'v: {velocity}')
    
    for c in controllers:
        await c.flush_transport()
    await asyncio.sleep(0.02)