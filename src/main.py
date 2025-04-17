from motor_control import init_motors, update_motors
from servo_control import init_servos, update_servos
from controller import Controller, MAX_SPEEDS
import asyncio
import math

WHEEL_BASE  = 0.6858
TRACK_WIDTH = 0.5969

MAX_ANGLE = 0.75 * math.pi
MIN_ANGLE = 0.25 * math.pi

def inverse_lerp_angle(angle: float) -> float:
    """
        Translates angle to angle between -1 and 1
    """
    global MIN_ANGLE, MAX_ANGLE

    clamped_angle = max(min(angle, MAX_ANGLE), MIN_ANGLE)
    return (2.0*(clamped_angle - MIN_ANGLE)/(MAX_ANGLE - MIN_ANGLE)) - 1.0

async def main():
    controller = Controller()
    controllers = await init_motors()
    # arduino = await init_servos()

    while True:
        radius: float = WHEEL_BASE/(math.tan(inverse_lerp_angle(controller.angle)) * (TRACK_WIDTH/2))
        velocity: float = controller.velocity*MAX_SPEEDS[controller.max_speed_index]
        await update_motors(velocity, radius, controllers)
        # await update_servos(controller, arduino)

if __name__ == '__main__':
    asyncio.run(main())