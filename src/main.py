from motor_control import init_motors, update_motors
from servo_control import init_servos, update_servos
from controller import Controller
import asyncio

async def main():
    controller = Controller()
    controllers, arduino = await asyncio.gather(init_motors(), init_servos())

    while True:
        motor_update_promise = update_motors(controller, controllers)
        servo_update_promise = update_servos(controller, arduino)

        asyncio.gather(motor_update_promise, servo_update_promise)

if __name__ == '__main__':
    asyncio.run(main())