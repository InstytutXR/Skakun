#!/usr/bin/env python3

import depthai as dai
import numpy as np
import sys
from pathlib import Path

def exportCalibrationToJson(device : dai.Device):
    calibFile = str((Path(__file__).parent / Path(f"calib_{device.getMxId()}.json")).resolve().absolute())
    if len(sys.argv) > 1:
        calibFile = sys.argv[1]

    calibData = device.readCalibration()
    calibData.eepromToJsonFile(calibFile)

def getRGB_Intristics(device : dai.Device):
    calibData = device.readCalibration()
    M_rgb, width, height = calibData.getDefaultIntrinsics(dai.CameraBoardSocket.RGB)
    print("RGB Camera Default intrinsics...")
    print(M_rgb)
    print(width)
    print(height)
    M_rgb = np.array(M_rgb)
    return M_rgb

def getRGB_DistCoefficent(device : dai.Device):
    calibData = device.readCalibration()
    D_rgb = np.array(calibData.getDistortionCoefficients(dai.CameraBoardSocket.RGB)) 
    print("RGB Camera disort coefficents")
    print(D_rgb)
    return D_rgb
    
def getLMonoCameraIntristics(device : dai.Device, width : int = 1280, height : int = 720):
    calibData = device.readCalibration()
    M_left = np.array(calibData.getCameraIntrinsics(dai.CameraBoardSocket.LEFT, width, height))
    print("LEFT Camera resized intrinsics...")
    print(M_left)
    return(M_left)
    
def getLMonoCameraDistCoefficent(device : dai.Device):
    calibData = device.readCalibration()
    D_left = np.array(calibData.getDistortionCoefficients(dai.CameraBoardSocket.LEFT))
    print("LEFT Distortion Coefficients...")
    [print(name+": "+value) for (name, value) in zip(["k1","k2","p1","p2","k3","k4","k5","k6","s1","s2","s3","s4","τx","τy"],[str(data) for data in D_left])]
    return D_left

def getRMonoCameraIntristics(device : dai.Device, width : int = 1280, height : int = 720):
    calibData = device.readCalibration()
    M_right = np.array(calibData.getCameraIntrinsics(dai.CameraBoardSocket.RIGHT, width, height))
    print("RIGHT Camera resized intrinsics...")
    print(M_right)
    return(M_right)
    
def getRMonoCameraDistCoefficent(device : dai.Device):
    calibData = device.readCalibration()
    D_right = np.array(calibData.getDistortionCoefficients(dai.CameraBoardSocket.RIGHT))
    print("RIGHT Distortion Coefficients...")
    [print(name+": "+value) for (name, value) in zip(["k1","k2","p1","p2","k3","k4","k5","k6","s1","s2","s3","s4","τx","τy"],[str(data) for data in D_right])]
    return D_right

def getRGB_FOV(device : dai.Device):
    calibData = device.readCalibration()
    rgbFov = calibData.getFov(dai.CameraBoardSocket.RGB)
    print(f"RGB FOV {calibData.getFov(dai.CameraBoardSocket.RGB)}, Mono FOV {calibData.getFov(dai.CameraBoardSocket.LEFT)}")
    return rgbFov

def getMono_FOV(device : dai.Device):
    calibData = device.readCalibration()
    monoFov = calibData.getFov(dai.CameraBoardSocket.LEFT)
    return monoFov

#TODO : figure the rectification purposes and how to automate it properly

def get_R_StereoRectifiedRotation(device : dai.Device, width : int = 1280, height : int = 720):
    calibData = device.readCalibration()
    R1 = np.array(calibData.getStereoLeftRectificationRotation())
    R2 = np.array(calibData.getStereoRightRectificationRotation())
    
    #TODO : probably needs some resolution parameters probably in a way the THE_720P notation is made
    M_left = np.array(calibData.getCameraIntrinsics(calibData.getStereoLeftCameraId(), width, height))
    M_right = np.array(calibData.getCameraIntrinsics(calibData.getStereoRightCameraId(), width, height))

    H_left = np.matmul(np.matmul(M_left, R1), np.linalg.inv(M_left))
    print("LEFT Camera stereo rectification matrix...")
    print(H_left)

    H_right = np.matmul(np.matmul(M_right, R2), np.linalg.inv(M_right))
    print("RIGHT Camera stereo rectification matrix...")
    print(H_right)
    return H_left, H_right

def getLR_Extrinsics(device : dai.Device):
    calibData = device.readCalibration()
    lr_extrinsics = np.array(calibData.getCameraExtrinsics(dai.CameraBoardSocket.LEFT, dai.CameraBoardSocket.RIGHT))
    print("Transformation matrix of where left Camera is W.R.T right Camera's optical center")
    print(lr_extrinsics)
    return(lr_extrinsics)

def getLRGB_Extrinsics(device : dai.Device):
    calibData = device.readCalibration()
    l_rgb_extrinsics = np.array(calibData.getCameraExtrinsics(dai.CameraBoardSocket.LEFT, dai.CameraBoardSocket.RGB))
    print("Transformation matrix of where left Camera is W.R.T RGB Camera's optical center")
    print(l_rgb_extrinsics)
    return(l_rgb_extrinsics)
    