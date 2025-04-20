from motor_control import init_motors, update_motors
from servo_control import init_servos, update_servos
from controller import Controller, MAX_SPEEDS
import asyncio
import math
import os.path

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

def get_velocity_and_radius(controller: Controller) -> tuple[float, float]:
    global WHEEL_BASE, TRACK_WIDTH

    angle_interpolated = inverse_lerp_angle(controller.angle)
    denominator = math.tan(angle_interpolated) * (TRACK_WIDTH/2)
    radius = WHEEL_BASE/denominator
    velocity = controller.velocity
    return velocity, radius

async def main():
    # Initialize controller
    controller = Controller()
    # Initialize motors and arduino
    motors  = await init_motors()
    arduino = await init_servos()

    while True:
        # Update controller
        input_coroutine = controller.update_inputs()

        # Check if arduino or canbus are unplugged while running
        if arduino is not None and not os.path.exists('/dev/arduino'):
            print('[main] arduino was unplugged!')
            arduino = None
        if motors is not None and not os.path.exists('/dev/fdcanusb'):
            print('[main] canbus was unplugged!')
            motors = None

        # Wait for input to be complete before continuing
        await input_coroutine

        motor_coroutine, arduino_coroutine = None, None
        
        # If motors not plugged in program will continue to run until they are plugged in.
        if motors is None:
            motor_coroutine = init_motors()
        else:
            # Calculate velocity, and radius.
            velocity, radius = get_velocity_and_radius(controller)
            motor_coroutine = update_motors(velocity, radius, motors)

        # If arduino not plugged in program will continue to run until they are plugged in.
        if arduino is None:
            arduino_coroutine = init_servos()
        else:
            arduino_coroutine = update_servos(controller.angle, arduino)

        # gather motor coroutine
        if motors is None:
            motors = await motor_coroutine
        else:
            await motor_coroutine
        # gather arduino coroutine
        if arduino is None:
            arduino = await arduino_coroutine
        else:
            await arduino_coroutine

if __name__ == '__main__':
    asyncio.run(main())