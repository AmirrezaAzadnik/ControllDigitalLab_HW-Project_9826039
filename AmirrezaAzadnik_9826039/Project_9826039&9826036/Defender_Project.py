# rcj_soccer_player controller - ROBOT B1

# Feel free to import built-in libraries
import math  # noqa: F401
import time
# You can also import scripts that you put into the folder with controller
import utils
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP

class MyRobot1(RCJSoccerRobot):
    def run(self):
        t1=time.time()
        kp = 10
        ki = 1.5
        kd = 0.65
       	
        kp1 = 1
        ki1 = 0
        kd1 = 0
       	
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

                
                #print(robot_pos)                                                        #THIS ROBOT IS THE DEFENDER
                #heading=math.pi/2
                #robot_pos[1]=0.72
                
                
                
                
                
                
                
                
                
                x_coordinate = robot_pos[1]
                x_desired = 0.72		#this is the ball's y coordinate
                error1 = -x_desired +x_coordinate 
                print(error1)
                sum_error1 = 0
                error_back1 = 0
                sum_error1 += error1*0.1 # 0.1 = sampling time
                error_d1 =(error1 - error_back1)/0.1 # 0.1 = sampling time
                error_back1 = error1
                u1 = kp*error1 + ki*sum_error1 + kd*error_d1
                self.left_motor.setVelocity(u1)
                self.right_motor.setVelocity(u1)
                
                
                
                if abs(error1)<= 0.2:
                
                    phi_desired = 90         
                    heading_degrees = math.degrees(heading)
                    error3 = phi_desired - heading_degrees 
                    error2 = math.atan2(math.sin(error3*math.pi/180) , math.cos(error3*math.pi/180))
                    sum_error2 = 0
                    error_back2 = 0
                    sum_error2 += error2*0.1 # 0.1 = sampling time
                    error_d2 =(error2 - error_back2)/0.1 # 0.1 = sampling time
                    error_back2 = error2
                    v = 0
                    w = kp1*error2 + ki1*sum_error2 + kd1*error_d2
                    R = 0.02
                    L = 0.08
                    vr = (2*v - L*w)/(2*R) 
                    vl = (2*v + L*w)/(2*R) 
                    self.left_motor.setVelocity(vl)
                    self.right_motor.setVelocity(vr)
                    
                    '''if error2 <= 1:
                        ball_direction=ball_data.get('direction','not found')
                        y_desired = 0
                        y_coordinate = robot_pos[0]
                        error4 = y_desired - y_coordinate 
                        sum_error3 = 0
                        error_back3 = 0
                        sum_error3 += error4*0.1 # 0.1 = sampling time
                        error_d3 =(error4 - error_back3)/0.1 # 0.1 = sampling time                            
                        error_back3 = error4
                        u2 = kp*error4 + ki*sum_error3 + kd*error_d3
                        self.left_motor.setVelocity(u2)                            
                        self.right_motor.setVelocity(u2)'''
                        
                    if abs(error2)<=0.1:    
                        #while(y_desired<= 0.18 and y_desired >=-0.18) :
                            ball_direction=ball_data.get('direction','not found')
                            y_coordinate = robot_pos[0]
                            y_desired = ball_direction[0]		#this is the ball's y coordinate
                            error4 = y_desired - y_coordinate 
                            sum_error3 = 0
                            error_back3 = 0
                            sum_error3 += error4*0.1 # 0.1 = sampling time
                            error_d3 =(error4 - error_back3)/0.1 # 0.1 = sampling time
                            error_back3 = error4
                            u2 = kp*error4 + ki*sum_error3 + kd*error_d3
                            self.left_motor.setVelocity(u2)
                            self.right_motor.setVelocity(u2)
                    else:
                            continue    
                    #else:
                    #   continue
                                
                else:
                    continue
                    
                
                
                
                
                
                
                
                
                t2=time.time()
                
                if t2-t1 <0.1:
                	time.sleep(0.1-(t2-t1)) 
