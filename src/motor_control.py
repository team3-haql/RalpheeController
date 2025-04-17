import moteus
from controller import Controller, MAX_SPEEDS
import time
import math
import usb

# Make sure to run the following commands on Jetson Orin Nano so camfd works properly:
# https://github.com/mjbots/fdcanusb/blob/master/70-fdcanusb.rules

LEFT_SERVO_IDS = [3, 4, 5]
RIGHT_SERVO_IDS = [0, 1, 2]

async def init_motors() -> list[list[moteus.Controller]]:
    print("[init_motors] resetting device file...")

    dev = usb.core.find(idVendor=0x0483, idProduct=0x5740)
    if dev is None:
        raise ValueError('Device not found')

    dev.reset()

    print("[init_motors] reset usb!")
    print('[init_motors] create controller objects')
    qr = moteus.QueryResolution()
    qr.trajectory_complete = moteus.INT8
    left_controllers = []
    for id in LEFT_SERVO_IDS:
        left_controllers.append(moteus.Controller(id, query_resolution=qr))
    right_controllers = []
    for id in RIGHT_SERVO_IDS:
        right_controllers.append(moteus.Controller(id, query_resolution=qr))
    print('[init_motors] set stop')
    for c in left_controllers:
        await c.set_stop()
    for c in right_controllers:
        await c.set_stop()
    print('[init_motors] ready!')
    return [left_controllers, right_controllers]

async def update_motors(controller: Controller, controller_groups: list[list[moteus.Controller]]):
    velocity = controller.velocity*MAX_SPEEDS[controller.max_speed_index]
    # Set Velocity
    coroutines = []
    for c in controller_groups[0]:
        coroutines.append(c.set_position(position=math.nan, velocity=velocity, query=True, watchdog_timeout=0.1))
    for c in controller_groups[1]:
        coroutines.append(c.set_position(position=math.nan, velocity=(-velocity), query=True, watchdog_timeout=0.1))
    print(f'[update_motors] v: {velocity}')
    for coroutine in coroutines:
        await coroutine