'''
Copyright (C) 2020 Benjamin Bokser

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import pybullet as p
import time
import pybullet_data
GRAVITY = -9.81
dt = 1e-3

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.resetSimulation()
planeID = p.loadURDF("plane.urdf")
robotStartOrientation = p.getQuaternionFromEuler([0,0,0])
robot = p.loadURDF("spryped_urdf_rev05/urdf/spryped_urdf_rev05.urdf", [0,0,0.8], robotStartOrientation, useFixedBase=0)

p.setGravity(0,0, GRAVITY)
p.setTimeStep(dt)

def moveLeg( subject=None, id=0, position=0, force=500 ):
    if(robot is None):
        return;
    p.setJointMotorControl2(
        robot,
        id,
        p.POSITION_CONTROL,
        targetPosition=position,
        force=force,
        maxVelocity=5
    )

def moveLegVel( subject=None, id=0, vel=0, force=100  ):
    if(robot is None):
        return;
    p.setJointMotorControl2(
        robot,
        id,
        p.VELOCITY_CONTROL,
        targetVelocity=vel,
        force=force,
        maxVelocity=50
    )

#enableJointForceTorqueSensor(robot,3,1)

useRealTime = 0

#p.setRealTimeSimulation(useRealTime)

#for i in range(p.getNumJoints(robot)):
#  p.setJointMotorControl2(robot, i, p.POSITION_CONTROL, targetPosition=0, force=500)

while(1):
    time.sleep(dt)
    moveLeg( subject=robot, id=0,  position= toggle ) #LEFT_FEMUR
    moveLeg( subject=robot, id=1,  position= toggle ) #LEFT_TIBIOTARSUS
    moveLeg( subject=robot, id=2,  position= toggle ) #LEFT_TARSOMETATARSUS
    moveLeg( subject=robot, id=3,  position= toggle ) #LEFT_TOE

    moveLeg( subject=robot, id=4,  position= toggle ) #RIGHT_FEMUR
    moveLeg( subject=robot, id=5,  position= toggle ) #RIGHT_TIBIOTARSUS
    moveLeg( subject=robot, id=6,  position= toggle ) #RIGHT_TARSOMETATARSUS
    moveLeg( subject=robot, id=7,  position= toggle ) #RIGHT_TOE
    
    pront=p.getJointInfo(robot,3)
    pront=[j[0] for j in p.getJointStates(robot,range(7))]
    pront=p.getJointState(robot,3)
    prunt='%s' % float('%.1g' % pront[3])
    print(prunt)
    

    toggle = toggle * -1
    if (useRealTime == 0):
        p.stepSimulation()
#maxForce = 5000
#p.setJointMotorControl2(robot, jointIndex=1, controlMode=p.POSITION_CONTROL, targetPosition = 2)
#p.setJointMotorControlArray(robot, range(7), p.POSITION_CONTROL,targetPositions=[1.5]*7)
#for _ in range(10000):
#	p.stepSimulation()
#	time.sleep(1./240.)

time.sleep(10000)

#robot = model[0]
#ordered_joints = []
#ordered_joint_indices = []

#parser = argparse.ArgumentParser()
#parser.add_argument('--profile')

#jdict = {}
#for j in range(p.getNumJoints(robot)):
#  info = p.getJointInfo(robot, j)
#  link_name = info[12].decode("ascii")
#  ordered_joint_indices.append(j)
#  if info[2] != p.JOINT_REVOLUTE: continue
#  jname = info[1].decode("ascii")
#  jdict[jname] = j
#  p.setJointMotorControl2(robot, j, controlMode=p.VELOCITY_CONTROL, force=0)

#motor_names = ["motor1", "motor2", "motor3", "motor4"]
#motor_power = [100, 100, 100, 100]
#motor_names += ["motor5", "motor6", "motor7", "motor8"]
#motor_power += [100, 100, 100, 100]
#motors = [jdict[n] for n in motor_names]








