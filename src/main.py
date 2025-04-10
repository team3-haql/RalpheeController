from motor_control import init_motors, update_motors
from servo_control import init_servos, update_servos
from controller import Controller
import asyncio

async def main():
    controller = Controller()
    controllers = await init_motors()
    # arduino = await init_servos()

    while True:
        # await update_motors(controller, controllers)
        print(controller.velocity)
        # await update_servos(controller, arduino)
        # servo_update_promise = update_servos(controller, arduino)

        # asyncio.gather(motor_update_promise)

if __name__ == '__main__':
    asyncio.run(main())