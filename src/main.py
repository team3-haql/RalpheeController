from motor_control import init_motors, update_motors
from servo_control import init_servos, update_servos
from controller import Controller
import asyncio
import math
import os.path

WHEEL_BASE  = 0.6858
TRACK_WIDTH = 0.5969

MAX_ANGLE = 0.25 * math.pi
MIN_ANGLE = -0.25 * math.pi

def lerp_angle(angle: float) -> float:
    """
        Translates angle to 1, -1
    """
    global MIN_ANGLE, MAX_ANGLE

    clamped_angle = max(min(angle, 1), -1)
    translated_angle = (clamped_angle + 1.0)/2.0
    return MIN_ANGLE + translated_angle*(MAX_ANGLE-MIN_ANGLE)

def get_velocity_and_radius(controller: Controller) -> tuple[float, float]:
    global WHEEL_BASE, TRACK_WIDTH

    angle_interpolated = lerp_angle(controller.angle)
    denominator = math.tan(angle_interpolated)
    offset = TRACK_WIDTH/2 if controller.angle >= 0 else -TRACK_WIDTH/2
    radius = (WHEEL_BASE/denominator) + offset
    velocity = controller.velocity
    return velocity, radius

async def main():
    # Initialize controller
    controller = Controller()
    # Initialize motors and arduino
    motors  = await init_motors()
    arduino = await init_servos()

    while True:
        # Calculate velocity, and radius.
        velocity, radius = get_velocity_and_radius(controller)
        await update_motors(velocity, radius, motors)
        await update_servos(controller.angle, arduino)

if __name__ == '__main__':
    asyncio.run(main())