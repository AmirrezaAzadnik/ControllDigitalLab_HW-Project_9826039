# rcj_soccer_player controller - ROBOT B2

# Feel free to import built-in libraries
import math  # noqa: F401
import time
# You can also import scripts that you put into the folder with controller
import utils
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP


class MyRobot2(RCJSoccerRobot):
    def run(self):
        kp1 = 5
        ki1 = 0
        kd1 = 0
        
        kp2 = 5
        ki2 = 5
        kd2 = 3
       	
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

                # Compute the speed for motors
                direction = utils.get_direction(ball_data["direction"])

                
                ball_direction=ball_data.get('direction','not found')
                #print(ball_direction[0])
                x_coordinate = robot_pos[1]
                y_coordinate = robot_pos[0]
                x_desired = ball_direction[1]		#this is the goal's x coordinate
                y_desired = ball_direction[0]		#this is the goal's y coordinate
             
                error1 = x_desired - x_coordinate 
                error2 = y_desired - y_coordinate  
                distance_error = math.sqrt(error1**2 + error2**2)
                #print(distance_error)
                phi_desired = 180 - math.degrees(math.atan2(error2,error1))         
                heading_degrees = math.degrees(heading)
                error4 = phi_desired - heading_degrees 
                error3 = math.atan2(math.sin(error4*math.pi/180) , math.cos(error4*math.pi/180))
                sum_error1 = 0
                sum_error2 = 0
                error_back1 = 0
                error_back2 = 0
                sum_error1 += distance_error*0.1 # 0.1 = sampling time
                sum_error2 += error3*0.1 # 0.1 = sampling time
                error_d1 =(distance_error - error_back1)/0.1 # 0.1 = sampling time
                error_d2 =(error3 - error_back2)/0.1 # 0.1 = sampling time
                error_back1 = distance_error
                error_back1 = error3
                v = 0
                w = kp2*error3 + ki2*sum_error2 + kd2*error_d2
                R = 0.02
                L = 0.08
                u = kp1*distance_error + ki1*sum_error1 + kd1*error_d1
                vr = (2*v - L*w)/(2*R) + u
                vl = (2*v + L*w)/(2*R) + u
                self.left_motor.setVelocity(vl)
                self.right_motor.setVelocity(vr)
                if abs(distance_error) <= 0.001:
                    while(abs(distance_error) <= 0.001):
                        ball_direction=ball_data.get('direction','not found')
                        #print(ball_direction[0])
                        x_coordinate = robot_pos[1]
                        y_coordinate = robot_pos[0]
                        x_desired = -0.66		#this is the goal's x coordinate
                        y_desired = 0		#this is the goal's y coordinate
                    
                        error1 = x_desired - x_coordinate 
                        error2 = y_desired - y_coordinate  
                        distance_error = math.sqrt(error1**2 + error2**2)
                        #print(distance_error)
                        phi_desired = 180 - math.degrees(math.atan2(error2,error1))         
                        heading_degrees = math.degrees(heading)
                        error4 = phi_desired - heading_degrees 
                        error3 = math.atan2(math.sin(error4*math.pi/180) , math.cos(error4*math.pi/180))
                        sum_error1 = 0
                        sum_error2 = 0
                        error_back1 = 0
                        error_back2 = 0
                        sum_error1 += distance_error*0.1 # 0.1 = sampling time
                        sum_error2 += error3*0.1 # 0.1 = sampling time
                        error_d1 =(distance_error - error_back1)/0.1 # 0.1 = sampling time
                        error_d2 =(error3 - error_back2)/0.1 # 0.1 = sampling time
                        error_back1 = distance_error
                        error_back1 = error3
                        v = 0
                        w = kp2*error3 + ki2*sum_error2 + kd2*error_d2
                        R = 0.02
                        L = 0.08
                        u = kp1*distance_error + ki1*sum_error1 + kd1*error_d1
                        vr = (2*v - L*w)/(2*R) + u
                        vl = (2*v + L*w)/(2*R) + u
                        self.left_motor.setVelocity(vl)
                        self.right_motor.setVelocity(vr) 
                else:
                    continue
                        
                t2 = time.time()
                if t2-t1 <0.1:
                	time.sleep(0.1-(t2-t1))