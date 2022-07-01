# rcj_soccer_player controller - ROBOT B1

# Feel free to import built-in libraries
import math  # noqa: F401
import time
# You can also import scripts that you put into the folder with controller
import utils
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP

class MyRobot1(RCJSoccerRobot):
    def run(self):
        kp = 10
        ki = 1.5
        kd = 0.65
       	t1 = time.time()

        while self.robot.step(TIME_STEP) != -1:

            if self.is_new_data():
                data = self.get_new_data()  # noqa: F841
                while self.is_new_team_data():
                    team_data = self.get_new_team_data()  # noqa: F841
                    # Do something with team data

                if self.is_new_ball_data():
                    ball_data = self.get_new_ball_data()
                else:
                    # If the robot does not see the ball, stop motors
                    self.left_motor.setVelocity(0)
                    self.right_motor.setVelocity(0)
                    continue

                # Get data from compass
                heading = self.get_compass_heading()  # noqa: F841

                # Get GPS coordinates of the robot
                robot_pos = self.get_gps_coordinates()  # noqa: F841

                # Get data from sonars
                sonar_values = self.get_sonar_values()  # noqa: F841

                
                print(robot_pos)
                x_coordinate = robot_pos[1]
                x_desired = -0.5		#this is the goal's x coordinate
                error =  x_coordinate - x_desired
                sum_error = 0
                error_back = 0
                sum_error += error*0.1 # 0.1 = sampling time
                error_d =(error - error_back)/0.1 # 0.1 = sampling time
                error_back = error
                u = kp*error + ki*sum_error + kd*error_d
                self.left_motor.setVelocity(u)
                self.right_motor.setVelocity(u)
                t2 = time.time()
                if t2-t1 <0.1:
                	time.sleep(0.1-(t2-t1)) 

                '''# Compute the speed for motors
                direction = utils.get_direction(ball_data["direction"])

                # If the robot has the ball right in front of it, go forward,
                # rotate otherwise
                if direction == 0:
                    left_speed = 7
                    right_speed = 7
                else:
                    left_speed = direction * 4
                    right_speed = direction * -4

                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)

                # Send message to team robots
                self.send_data_to_team(self.player_id)'''
