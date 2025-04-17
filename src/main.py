from motor_control import init_motors, update_motors
from servo_control import init_servos, update_servos
from controller import Controller
import asyncio

async def main():
    controller = Controller()
    controllers = await init_motors()
    arduino = await init_servos()

    while True:
        await update_motors(controller, controllers)
        await update_servos(controller, arduino)

if __name__ == '__main__':
    asyncio.run(main())