# Ralphee Controller
A program to interperate the inputs from a PS4 controller into motion for the Ralphee Rover.

## Setup
Install deps system wide
```bash
    pip install .
```
Install deps locally
```bash
    pip install -e .
```

## Run Controller
Run controller using:
```bash
    cd src/main.py
```

## Controls
### Startup Sequence
Inorder to enable the controller you need to enter the sequence:
```
    A -> X -> Y -> B
```
After start up max speed is zero. Use D-Pad to select max speed.
- Left D-Pad is a max speed of 0.5
- Down D-Pad is a max speed of 1
- Right D-Pad is a max speed of 2
- Up D-Pad is a max speed of 4
Max Speed can be changed at anytime.
### Moving
Left Joystick controls the servos and the motors.
### Disabling Controls
To disable the controller press the "Start" button on the controller.
