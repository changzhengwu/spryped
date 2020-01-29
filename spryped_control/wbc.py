# Copyright 2020 Benjamin Bokser

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Credit: Travis DeWolf

import numpy as np

class Control(control.Control):
    # a (whole body)/(operational space)/(task space) controller.

    def control(self, robot, x_des=None):
        # generates the control signal. 
        # x_des = desired task-space force. self.target if None
        
        # calculate desired end-effector acceleration
        if x_des is None:
            self.x = robot.x
            x_des = self.kp * (self.target - self.x)

        # generate mass matrix in end-effector space
        Mq = robot.gen_Mq()
        Mx = robot.gen_Mx()

        # calculate force
        Fx = np.dot(Mx, x_des)

        # calculate the Jacobian
        JEE = arm.gen_jacEE()
        self.u = 
		
