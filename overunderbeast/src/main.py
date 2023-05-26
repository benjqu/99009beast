#region VEXcode Generated Robot Configuration
from vex import *

# Brain should be defined by default
brain=Brain()

# Robot configuration code


# wait for rotation sensor to fully initialize
wait(30, MSEC)
#endregion VEXcode Generated Robot Configuration

leftmotor1 = Motor(Ports.PORT4, GearSetting.RATIO_6_1, True)
leftmotor2 = Motor(Ports.PORT11, GearSetting.RATIO_6_1, True)
leftmotor3 = Motor(Ports.PORT12, GearSetting.RATIO_6_1, False)
MotorGroupLeft = MotorGroup(leftmotor1, leftmotor2, leftmotor3)
rightmotor1 = Motor(Ports.PORT5, GearSetting.RATIO_6_1, False)
rightmotor2 = Motor(Ports.PORT19, GearSetting.RATIO_6_1, False)
rightmotor3 = Motor(Ports.PORT20, GearSetting.RATIO_6_1, True)
MotorGroupRight = MotorGroup(rightmotor1, rightmotor2, rightmotor3)
inertial = Inertial(Ports.PORT10)
controller_1 = Controller(PRIMARY)

drivetrainStop = False



def when_started1():
    brain.screen.print("Calibrating!")
    while inertial.is_calibrating():
       sleep(50)
    controller_1.rumble("---")

def driveFor_distance_speed(
    driveFor_distance_speed__distance, driveFor_distance_speed__speed
):
    MotorGroupLeft.set_velocity(driveFor_distance_speed__speed, PERCENT)
    MotorGroupRight.set_velocity(driveFor_distance_speed__speed, PERCENT)
    d = driveFor_distance_speed__distance / 12.56
    MotorGroupLeft.spin_for(FORWARD, -d, TURNS, wait=False)
    MotorGroupRight.spin_for(FORWARD, -d, TURNS, wait=True)

def turnFor_degree_speed(turnFor_degree_speed__degree, turnFor_degree_speed__speed):
    MotorGroupLeft.set_velocity(turnFor_degree_speed__speed, PERCENT)
    MotorGroupRight.set_velocity(turnFor_degree_speed__speed, PERCENT)
    d = turnFor_degree_speed__degree / 0.33
    MotorGroupLeft.spin_for(REVERSE, d, DEGREES, wait=False)
    MotorGroupRight.spin_for(REVERSE, (d * -1), DEGREES, wait=True)

def turnnorth():
    if inertial.heading(DEGREES) <= 180:
        turnFor_degree_speed(-inertial.heading(DEGREES), 50)
    else:
        turnFor_degree_speed(360 - inertial.heading(DEGREES), 50)

def turnsouth():
    turnFor_degree_speed(180 - inertial.heading(DEGREES), 50)

def turneast():
    if inertial.heading(DEGREES) > 270:
        turnFor_degree_speed(360 + 90 - inertial.heading(DEGREES), 50)
    else:
        turnFor_degree_speed(90 - inertial.heading(DEGREES), 50)

def turnwest():
    if inertial.heading(DEGREES) > 90:
        turnFor_degree_speed(270 - inertial.heading(DEGREES), 50)
    else:
        turnFor_degree_speed(-(inertial.heading(DEGREES) + 90), 50)

def ondriver_drivercontrol_2():
    global drivetrainStop
    while True:
        straight = -controller_1.axis3.position()
        turn = controller_1.axis1.position() / -2
        if straight == 0 and turn == 0:
            if drivetrainStop:
                MotorGroupLeft.stop()
                MotorGroupRight.stop()
                drivetrainStop = False
        else:
            MotorGroupLeft.set_velocity((straight + turn), PERCENT)
            MotorGroupRight.set_velocity((straight - turn), PERCENT)
            MotorGroupLeft.spin(FORWARD)
            MotorGroupRight.spin(FORWARD)
            drivetrainStop = True
        wait(5, MSEC)




def onevent_controller_1buttonB_pressed_0():
    MotorGroupLeft.set_stopping(HOLD)
    MotorGroupLeft.stop()
    MotorGroupRight.set_stopping(HOLD)
    MotorGroupRight.stop()


def test():
    brain.timer.clear()
    auton_started = True

    controller_1.screen.clear_row(1)
    controller_1.screen.set_cursor(1, 1)
    controller_1.screen.print(brain.timer.time)

def offensive():
    inertial.set_heading(270, DEGREES)

def defensive():
    inertial.set_heading(270, DEGREES)


current_auton_selection = 0
auton_started = False
def menu():
    global current_auton_selection, auton_started
    txt = ["offensive", "defensive"]
    auton_num = len(txt)
    brain.screen.set_font(FontType.MONO60)
    while auton_started == False:
        brain.screen.clear_screen()
        brain.screen.set_cursor(2,1)
        brain.screen.print(txt[current_auton_selection])
        controller_1.screen.clear_row(1)
        controller_1.screen.set_cursor(1, 1)
        controller_1.screen.print(txt[current_auton_selection] + "        ")
        if brain.screen.pressing():
            while brain.screen.pressing():
                pass
            current_auton_selection = (current_auton_selection + 1) % auton_num
            sleep(50)

def vexcode_auton_function():
    global current_auton_selection, auton_started
    MotorGroupLeft.set_stopping(BRAKE)
    MotorGroupRight.set_stopping(BRAKE)
    auton_started = True
    # Start the autonomous task
    if current_auton_selection == 0:
        offensive()
    elif current_auton_selection == 1:
        defensive()

def ondriver_drivercontrol_1():
    brain.timer.clear()
    while brain.timer.time(SECONDS) < 75:
        wait(5, MSEC)
    controller_1.rumble("---")

def vexcode_driver_function():
    driver_control_task_1 = Thread(ondriver_drivercontrol_1)
    driver_control_task_2 = Thread(ondriver_drivercontrol_2)
    MotorGroupLeft.set_stopping(BRAKE)
    MotorGroupRight.set_stopping(BRAKE)
    # wait for the driver control period to end
    while True:
        # wait 10 milliseconds before checking again
        wait(10, MSEC)

# system event handlers
controller_1.buttonB.pressed(onevent_controller_1buttonB_pressed_0)
controller_1.buttonRight.pressed(turneast)
controller_1.buttonDown.pressed(turnsouth)
controller_1.buttonLeft.pressed(turnwest)
controller_1.buttonUp.pressed(turnnorth)
controller_1.buttonX.pressed(test)

competition = Competition(vexcode_driver_function, vexcode_auton_function)

when_started1()
menu()
