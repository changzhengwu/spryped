import pybullet as p
import time
import pybullet_data
GRAVITY = -9.81
dt = 1e-3
iters = 2000

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.resetSimulation()
planeID = p.loadURDF("plane.urdf")
robotStartOrientation = p.getQuaternionFromEuler([0,0,0])
robot = p.loadURDF("Desktop/spryped rev03/urdf/spryped rev03.urdf", [0,0,0.8], robotStartOrientation, useFixedBase=0)

p.setGravity(0,0, GRAVITY)
p.setTimeStep(dt)

def moveLeg( subject=None, id=0, position=0, force=10  ):
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

pixelWidth = 1000
pixelHeight = 1000
camTargetPos = [0,0,0]
camDistance = 0.5
pitch = -10.0
roll=0
upAxisIndex = 2
yaw = 0

viewMatrix = p.computeViewMatrixFromYawPitchRoll(camTargetPos, camDistance, yaw, pitch, roll, upAxisIndex)

toggle = 1000
#enableJointForceTorqueSensor(robot,3,1)
p.setRealTimeSimulation(1)
for i in range (10000):
    #p.stepSimulation()

    moveLeg( subject=robot, id=0,  position= toggle * 1 ) #LEFT_FEMUR
    moveLeg( subject=robot, id=1,  position= toggle * 1 ) #LEFT_TIBIOTARSUS
    moveLeg( subject=robot, id=2,  position= toggle * 1 ) #LEFT_TARSOMETATARSUS
    moveLeg( subject=robot, id=3,  position= toggle * 1 ) #LEFT_TOE

    moveLeg( subject=robot, id=4,  position= toggle * 1 ) #RIGHT_FEMUR
    moveLeg( subject=robot, id=5,  position= toggle * 1 ) #RIGHT_TIBIOTARSUS
    moveLeg( subject=robot, id=6,  position= toggle * 1 ) #RIGHT_TARSOMETATARSUS
    moveLeg( subject=robot, id=7,  position= toggle * 1 ) #RIGHT_TOE
    #time.sleep(1./140.)g
    #time.sleep(0.01)
    #pront=p.getJointInfo(robot,3)
    #pront=[j[0] for j in p.getJointStates(robot,range(7))]
    pront=p.getJointState(robot,3)
    prunt='%s' % float('%.1g' % pront[3])
    print(prunt)
    time.sleep(1)

    toggle = toggle * -1

#maxForce = 5000
#p.setJointMotorControl2(robot, jointIndex=1, controlMode=p.POSITION_CONTROL, targetPosition = 2)
#p.setJointMotorControlArray(robot, range(7), p.POSITION_CONTROL,targetPositions=[1.5]*7)
#for _ in range(10000):
#	p.stepSimulation()
#	time.sleep(1./240.)
#time.sleep(10000)

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








