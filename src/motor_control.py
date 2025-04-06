import moteus
from controller import Controller
import asyncio
import math

# Make sure to run the following commands on Jetson Orin Nano so camfd works properly:
# https://github.com/mjbots/fdcanusb/blob/master/70-fdcanusb.rules

MAX_SPEED = 2
SERVO_IDS = [1]

async def init_motors() -> list[moteus.Controller]:
    print('[init_motors] create controller objects')
    qr = moteus.QueryResolution()
    qr.trajectory_complete = moteus.INT8
    controllers = []
    for id in SERVO_IDS:
        controllers.append(moteus.Controller(id, query_resolution=qr))
    print('[init_motors] set stop')
    for c in controllers:
        await c.set_stop()
    print('[init_motors] ready!')
    return controllers

async def update_motors(controller: Controller, controllers: list[moteus.Controller]):
    velocity = controller.velocity
    # Set Velocity
    for c in controllers:
        await c.set_position(position=math.nan, velocity=velocity, query=True)
    print(f'[update_motors] v: {velocity}')
    # Flush
    for c in controllers:
        await c.flush_transport()