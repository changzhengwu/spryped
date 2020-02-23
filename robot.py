# Copyright 2020 Benjamin Bokser

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import numpy as np
import math
import csv

values = []
with open('spryped_urdf_rev05/urdf/spryped_urdf_rev05.csv', 'r') as csvfile:
    data = csv.reader(csvfile, delimiter=',') 
    next(data) # skip headers
    values = list(zip(*(row for row in data))) # transpose rows to columns
    values = np.array(values) # convert list of nested lists to array

comx = values[1].astype(np.float)
comy = values[2].astype(np.float)
comz = values[3].astype(np.float)

mass = values[7].astype(np.float)
ixx = values[8].astype(np.float)
ixy = values[9].astype(np.float)
ixz = values[10].astype(np.float)
iyy = values[11].astype(np.float)
iyz = values[12].astype(np.float)
izz = values[13].astype(np.float)

ox = values[38].astype(np.float)
oy = values[39].astype(np.float)
oz = values[40].astype(np.float)

coml = []
for j in range(9):
    comlen = math.sqrt((comx[j]**2)+(comz[j]**2)) # joint origin to COM ignoring y axis
    #comlen = math.sqrt((comx[j]**2)+(comy[j]**2)+(comz[j]**2)) # joint origin to COM length
    coml.append(comlen)
#print(coml[1])

# estimating init link angles
#p = 4
#dist = math.sqrt((ox[p]**2)+(oz[p]**2))
#angle = np.degrees(math.atan(oz[p]/dist))
#print("dist = ", dist)
#print("angle p = ", angle)
               
# link masses
if mass[1]!=mass[5]:
    print("WARNING: femur L/R masses unequal, check CAD")
if mass[2]!=mass[6]:
    print("WARNING: tibiotarsus L/R masses unequal, check CAD")
if mass[3]!=mass[7]:
    print("WARNING: tarsometatarsus L/R masses unequal, check CAD")
if mass[4]!=mass[8]:
    print("WARNING: toe L/R masses unequal, check CAD")

# link lengths must be manually updated
L0 = 0.1 # body
L1 = 0.1 # femur left
L2 = 0.199 # tibiotarsus left
L3 = 0.5 # tarsometatarsus left
L4 = 0.061 # toe left
L = np.array([L0, L1, L2, L3, L4, L1, L2, L3, L4])

class Robot:

    def __init__(self, q=np.zeros(9), dq=np.zeros(9),
                 init_q=[0, np.pi/4, -np.pi*40.3/180, np.pi*84.629/180,-np.pi*44.329/180,
                         np.pi/4, -np.pi*40.3/180, np.pi*84.629/180, -np.pi*44.329/180.],
                 init_dq=[0., 0., 0., 0., 0., 0., 0.], singularity_thresh=.00025, **kwargs):

        # mass matrices
        self.MM = []
        for i in range(9):
            M = np.zeros((6, 6))
            M[0:3, 0:3] = np.eye(3)*float(mass[i])
            M[3, 3] = ixx[i]
            M[3, 4] = ixy[i]
            M[3, 5] = ixz[i]
            M[4, 3] = ixy[i]
            M[4, 4] = iyy[i]
            M[4, 5] = iyz[i]
            M[5, 3] = ixz[i]
            M[5, 4] = iyz[i]
            M[5, 5] = izz[i]
            #self.MM.insert(i,M)
            self.MM.append(M)

    def gen_jacCOM1(self, q=None):
        """Generates the Jacobian from the COM of the first
        link to the origin frame"""
        q = self.q if q is None else q
        q1 = q[1]
    
        JCOM1 = np.zeros((6, 4))
        JCOM1[1, 0] = -L[1]*np.sin(q1) - 2*coml[1]*np.sin(2*q1)
        JCOM1[2, 0] = L[1]*np.cos(q1) + 2*coml[1]*np.cos(2*q1)
        JCOM1[3, :] = 1

        return JCOM1
    
    def gen_jacCOM2(self, q=None):
        """Generates the Jacobian from the COM of the second
        link to the origin frame"""
        q = self.q if q is None else q
        q1 = q[1]
        q2 = q[2]
        
        JCOM2 = np.zeros((6, 4))
        JCOM2[0, 1] = L[2]*np.cos(q2)
        JCOM2[1, 0] = -(L[1]+L[2]*np.cos(q2)+coml[2])*np.sin(q1)
        JCOM2[1, 1] = -L[2]*np.sin(q2)*np.cos(q1)
        JCOM2[2, 0] = (L[1]+L[2]*np.cos(q2)+coml[2])*np.cos(q1)
        JCOM2[2, 1] = -L[2]*np.sin(q1)*np.sin(q2)
        JCOM2[5, :] = 1

        return JCOM2
    
    def gen_jacCOM3(self, q=None):
        """Generates the Jacobian from the COM of the third
        link to the origin frame"""
        q = self.q if q is None else q
        q1 = q[1]
        q2 = q[2]
        q3 = q[3]
        
        JCOM3 = np.zeros((6, 4))
        JCOM3[0, 0] = (L[1]+coml[3]*np.cos(q3))*np.sin(q1)*np.sin(q2+q3)
        JCOM3[0, 1] = -L[1]*np.cos(q1)*np.cos(q2+q3)\
            + L[2]*np.cos(q2-q3) - coml[3]*np.sin(q3)*np.sin(q2+q3)\
            - coml[3]*np.cos(q1)*np.cos(q3)*np.cos(q2+q3)
        JCOM3[0, 2] = -L[1]*np.cos(q1)*np.cos(q2 + q3) - L[2]*np.cos(q2 - q3)\
            + L[3]*np.cos(q3) + coml[3]*np.sin(q3)*np.sin(q2 + q3)*np.cos(q1)\
            - coml[3]*np.sin(q3)*np.sin(q2 + q3)\
            - coml[3]*np.cos(q1)*np.cos(q3)*np.cos(q2 + q3)\
            + coml[3]*np.cos(q3)*np.cos(q2 + q3)
        JCOM3[1, 0] = -(L[1]+coml[3]*np.cos(q3))*np.sin(q1)*np.cos(q2+q3)
        JCOM3[1, 1] = -L[1]*np.sin(q2+q3)*np.cos(q1) - L[2]*np.sin(q2-q3)\
            + coml[3]*np.sin(q3)*np.cos(q2+q3)\
            - coml[3]*np.sin(q2+q3)*np.cos(q1)*np.cos(q3)
        JCOM3[1, 2] = -L[1]*np.sin(q2 + q3)*np.cos(q1) + L[2]*np.sin(q2 - q3)\
            - L[3]*np.sin(q3) - coml[3]*np.sin(q3)*np.cos(q1)*np.cos(q2 + q3)\
            + coml[3]*np.sin(q3)*np.cos(q2 + q3)\
            - coml[3]*np.sin(q2 + q3)*np.cos(q1)*np.cos(q3)\
            + coml[3]*np.sin(q2 + q3)*np.cos(q3)
        JCOM3[2, 0] = (L[1]+coml[3]*np.cos(q3))*np.cos(q1)
        JCOM3[2, 2] = -coml[3]*np.sin(q1)*np.sin(q3)
        JCOM3[5, :] = 1

        return JCOM3
    
    def gen_jacCOM4(self, q=None):
        """Generates the Jacobian from the COM of the fourth
        link to the origin frame"""
        q = self.q if q is None else q
        q1 = q[1]
        q2 = q[2]
        q3 = q[3]
        q4 = q[4]
        
        JCOM4 = np.zeros((6, 4))
        JCOM4[0, 0] = (L[1] + coml[4]*np.cos(q4))*np.sin(q1)*np.sin(q2 + q3 + q4)
        JCOM4[0, 1] = -L[1]*np.cos(q1)*np.cos(q2 + q3 + q4)\
            + L[2]*np.cos(-q2 + q3 + q4) - coml[4]*np.sin(q4)*np.sin(q2 + q3 + q4)\
            - coml[4]*np.cos(q1)*np.cos(q4)*np.cos(q2 + q3 + q4)
        JCOM4[0, 2] = -L[1]*np.cos(q1)*np.cos(q2 + q3 + q4)\
            - L[2]*np.cos(-q2 + q3 + q4) + L[3]*np.cos(q3 - q4)\
            - coml[4]*np.sin(q4)*np.sin(q2 + q3 + q4)\
            - coml[4]*np.cos(q1)*np.cos(q4)*np.cos(q2 + q3 + q4)
        JCOM4[0, 3] = -L[1]*np.cos(q1)*np.cos(q2 + q3 + q4)\
            - L[2]*np.cos(-q2 + q3 + q4) - L[3]*np.cos(q3 - q4) + L[4]*np.cos(q4)\
            + coml[4]*np.sin(q4)*np.sin(q2 + q3 + q4)*np.cos(q1)\
            - coml[4]*np.sin(q4)*np.sin(q2 + q3 + q4)\
            - coml[4]*np.cos(q1)*np.cos(q4)*np.cos(q2 + q3 + q4)\
            + coml[4]*np.cos(q4)*np.cos(q2 + q3 + q4)
        JCOM4[1, 0] = -(L[1] + coml[4]*np.cos(q4))*np.sin(q1)*np.cos(q2 + q3 + q4)
        JCOM4[1, 1] = -L[1]*np.sin(q2 + q3 + q4)*np.cos(q1)\
            + L[2]*np.sin(-q2 + q3 + q4) + coml[4]*np.sin(q4)*np.cos(q2 + q3 + q4)\
            - coml[4]*np.sin(q2 + q3 + q4)*np.cos(q1)*np.cos(q4)
        JCOM4[1, 2] = -L[1]*np.sin(q2 + q3 + q4)*np.cos(q1)\
            - L[2]*np.sin(-q2 + q3 + q4) - L[3]*np.sin(q3 - q4)\
            + coml[4]*np.sin(q4)*np.cos(q2 + q3 + q4)\
            - coml[4]*np.sin(q2 + q3 + q4)*np.cos(q1)*np.cos(q4)
        JCOM4[1, 3] = -L[1]*np.sin(q2 + q3 + q4)*np.cos(q1)\
            - L[2]*np.sin(-q2 + q3 + q4) + L[3]*np.sin(q3 - q4) - L[4]*np.sin(q4)\
            - coml[4]*np.sin(q4)*np.cos(q1)*np.cos(q2 + q3 + q4)\
            + coml[4]*np.sin(q4)*np.cos(q2 + q3 + q4)\
            - coml[4]*np.sin(q2 + q3 + q4)*np.cos(q1)*np.cos(q4)\
            + coml[4]*np.sin(q2 + q3 + q4)*np.cos(q4)
        JCOM4[2, 0] = (L[1] + coml[4]*np.cos(q4))*np.cos(q1)
        JCOM4[2, 3] = -coml[4]*np.sin(q1)*np.sin(q4)
        JCOM4[5, :] = 1
        
        return JCOM4

    def gen_jacEE(self, q=None):
        """Generates the Jacobian from the end effector to the origin frame"""
        q = self.q if q is None else q
        q1 = q[1]
        q2 = q[2]
        q3 = q[3]
        q4 = q[4]
        
        JEE = np.zeros((3, 4)) # Only x, y, z forces controlled, others dropped
        JEE[0, 0] = L[4]*np.sin(q1)*np.sin(q2 + q3 + q4)*np.cos(q4)
        JEE[0, 1] = -L[4]*(np.sin(q4)*np.sin(q2 + q3 + q4)\
            + np.cos(q1)*np.cos(q4)*np.cos(q2 + q3 + q4))
        JEE[0, 2] = JEE[0, 1]
        JEE[0, 3] = L[4]*(np.cos(q2 + q3 + 2*q4)\
            - np.cos(-q1 + q2 + q3 + 2*q4)/2 - np.cos(q1 + q2 + q3 + 2*q4)/2)
        JEE[1, 0] = -L[4]*np.sin(q1)*np.cos(q4)*np.cos(q2 + q3 + q4)
        JEE[1, 1] = L[4]*(np.sin(q4)*np.cos(q2 + q3 + q4)\
            - np.sin(q2 + q3 + q4)*np.cos(q1)*np.cos(q4))
        JEE[1, 2] = JEE[1, 1]
        JEE[1, 3] = L[4]*(np.sin(q2 + q3 + 2*q4)\
            - np.sin(-q1 + q2 + q3 + 2*q4)/2 - np.sin(q1 + q2 + q3 + 2*q4)/2)
        JEE[2, 0] = L[4]*np.cos(q1)*np.cos(q4)
        JEE[2, 3] = -L[4]*np.sin(q1)*np.sin(q4)

        return JEE
    
    def gen_Mx(self, JEE = None, q=None, **kwargs):
        # Mass matrix
        M1 = self.MM[1]
        M2 = self.MM[2]
        M3 = self.MM[3]
        
        JCOM1 = self.gen_jacCOM1(q=q)
        JCOM2 = self.gen_jacCOM2(q=q)
        JCOM3 = self.gen_jacCOM3(q=q)
        JCOM4 = self.gen_jacCOM3(q=q)
        
        Mq = (np.dot(JCOM1.T, np.dot(M1, JCOM1)) +
              np.dot(JCOM2.T, np.dot(M2, JCOM2)) +
              np.dot(JCOM3.T, np.dot(M3, JCOM3)) +
              np.dot(JCOM4.T, np.dot(M4, JCOM4)))

        if JEE is None:
            JEE = self.gen_jacEE(q=q)
        Mx_inv = np.dot(JEE, np.dot(np.linalg.inv(Mq), JEE.T))
        u, s, v = np.linalg.svd(Mx_inv)
        # cut off any singular values that could cause control problems
        for i in range(len(s)):
            s[i] = 0 if s[i] < singularity_thresh else 1./float(s[i])
        # numpy returns U,S,V.T, so have to transpose both here
        Mx = np.dot(v.T, np.dot(np.diag(s), u.T))

        return Mx

        # calculate force
        Fx = np.dot(Mx, x_des)
        self.u = (np.dot(JEE.T, Fx).reshape(-1,) -
                  np.dot(Mq, self.kv * arm.dq))

        return self.u
    
robert = Robot()
#print(robert.MM[7])
print(robert.gen_Mx())
