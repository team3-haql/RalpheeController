from inputs import get_gamepad
import threading
import math
from enum import IntEnum

class ControllerState(IntEnum):
    DISABLED = 0
    ENABLED  = 1

class Actions(IntEnum):
    NONE = 0
    A = 1
    B = 2
    X = 3
    Y = 4

ACTIVATION_CODE = [Actions.A, Actions.X, Actions.Y, Actions.B]
SIN_PI_OVER_4 = math.sin(math.pi/4)
DEADZONE = 0.1
DEADZONE_INV = 1-DEADZONE

# Used as reference
# https://stackoverflow.com/questions/46506850/how-can-i-get-input-from-an-xbox-one-controller-in-python
class Controller(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):
        self.activation_index: int = 0
        self.state: ControllerState = ControllerState.DISABLED
        self.velocity: float = 0.0
        self.angle: float = math.nan

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / Controller.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / Controller.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = event.state / Controller.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / Controller.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / Controller.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / Controller.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state #previously switched with X
                elif event.code == 'BTN_WEST':
                    self.X = event.state #previously switched with Y
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state

            self.update_state()
            if self.state == ControllerState.ENABLED:
                self.update_velocity()
                self.update_angle()
            else:
                self.velocity = 0.0
                self.angle = math.nan
           
    def update_state(self):
        # Deactivate
        if self.Start == 1 and self.state == ControllerState.ENABLED:
            self.velocity = 0
            self.angle = 0
            self.state = ControllerState.DISABLED
            return
        if self.state == ControllerState.DISABLED and sum([self.A, self.B, self.X, self.Y] == 1):
            # Activate
            recent_action = Actions.NONE # Get Action
            if self.A == 1:
                recent_action = Actions.A
            elif self.B == 1:
                recent_action = Actions.B
            elif self.X == 1:
                recent_action = Actions.X
            elif self.Y == 1:
                recent_action = Actions.Y

            if recent_action == Actions.NONE: # No Input
                return
            if recent_action == ACTIVATION_CODE[self.activation_index]: # Valid
                self.activation_index += 1
                if self.activation_index == len(ACTIVATION_CODE):
                    self.state = ControllerState.ENABLED
                    self.activation_index = 0
            else: # Invalid
                self.activation_index = 0

    def update_velocity(self):
        # Equation https://www.desmos.com/calculator/721p4tkigr

        if abs(self.LeftJoystickY) < DEADZONE:
            self.velocity = 0.0
            return
        # Keeps joystick in 'square' zone
        sign = abs(self.LeftJoystickY)/self.LeftJoystickY
        vel = (self.LeftJoystickY-DEADZONE*sign) / (SIN_PI_OVER_4*DEADZONE_INV)
        self.velocity = max(-1, min(1, vel))

    def update_angle(self):
        # Equation https://www.desmos.com/calculator/721p4tkigr
        
        if abs(self.LeftJoystickX) < DEADZONE:
            self.angle = 0.0
            return
        # Keeps joystick in 'square' zone
        sign = abs(self.LeftJoystickX)/self.LeftJoystickX
        vel = (self.LeftJoystickX - DEADZONE*sign) / (SIN_PI_OVER_4*DEADZONE_INV)
        self.angle = max(-1, min(1, vel))