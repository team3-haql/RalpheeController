import moteus
import time
import math
import usb
import numpy as np

# Can bus id, bisit mjbots moteus repo for more info: https://github.com/mjbots/moteus
# center motor id should be in center.
LEFT_MOTOR_IDS  = [0, 5, 2]
RIGHT_MOTOR_IDS = [1, 4, 3]

async def init_motors() -> list[list[moteus.Controller]]:
    """
        Initializes moteus controllers!
        Return:
            Groups of moteus controllers! Each group has a different velocity sent to it.
    """
    print("[init_motors] resetting device file...")

    # Reset fdcamusb device
    # Without this step the program will get stuck at 'set_stop' on repeat runs.
    dev = usb.core.find(idVendor=0x0483, idProduct=0x5740)
    if dev is None:
        raise ValueError('Device not found')

    dev.reset()

    print("[init_motors] reset usb!")
    print('[init_motors] create controller objects')
    qr = moteus.QueryResolution()
    qr.trajectory_complete = moteus.INT8

    # Create Motor Objects
    left_controllers = []
    for id in LEFT_MOTOR_IDS:
        left_controllers.append(moteus.Controller(id, query_resolution=qr))
    right_controllers = []
    for id in RIGHT_MOTOR_IDS:
        right_controllers.append(moteus.Controller(id, query_resolution=qr))

    # Reset motors incase of inpropper shutdown.
    print('[init_motors] set stop')
    for c in left_controllers:
        await c.set_stop()
    for c in right_controllers:
        await c.set_stop()
    print('[init_motors] ready!')

    # Return groups
    return [left_controllers, right_controllers]

async def update_motors(left_velocity: float, right_velocity: float, controller_groups: list[list[moteus.Controller]]):
    """
        Updates motor velocities.
        Args:
            velocity:
                Speed that the rover itself will travel at.
            radius:
                length from turning point to center of body
            controller_groups:
                Controller groups to be set.
    """
    coroutines = []

    # Gets the velocity for both sides.


    LEFT_SIDE_INDEX  = 0
    RIGHT_SIDE_INDEX = 1

    # Start coroutines
    for i, c in enumerate(controller_groups[LEFT_SIDE_INDEX]):
        v = left_velocity
        coroutines.append(c.set_position(position=math.nan, velocity=v, query=True, watchdog_timeout=0.1))

    for i, c in enumerate(controller_groups[RIGHT_SIDE_INDEX]):
        v = right_velocity
        coroutines.append(c.set_position(position=math.nan, velocity=v, query=True, watchdog_timeout=0.1))

    # Await coroutines
    for coroutine in coroutines:
        await coroutine