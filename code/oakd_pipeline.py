#!/usr/bin/env python3
import depthai as dai
import math
import numpy
import cv2

from numpy import mat

from numpy import matrix 

class Oakd_pipeline() :
    """ 
        A oakd interface for multiple pipeline configurations
    """

    def __init__ (self,imuEnabled : bool = False, depthEnabled : bool = False, colorEnabled : bool = False, greyStereoEnabled : bool = False, trackColor : bool = False, trackGrayStereo : bool = False, fps : int = 30, downscaleColor : bool = True) :
        """
            Create new pipeline that requests the data from oakd device 
        """
        self.imuEnabled : bool = imuEnabled
        self.depthEnabled : bool = depthEnabled
        self.colorEnabled : bool = colorEnabled
        self.grayStereoEnabled : bool = greyStereoEnabled
        self.trackColorEnabled : bool = trackColor
        self.trackStereoEnabled : bool = trackGrayStereo
        
        self.inputFeatureTrackerConfigQueue = None
        self.featureTrackerConfig = None
        
        
        self.pipeline = None
        self.device = None
        
        self.latestPacket = {}
        
        # Create Oakd_pipeline.pipeline
        self.pipeline = dai.Pipeline()
        
        if(imuEnabled) :
            self.accOut = None
            self.rotVectorOut = None
    
            # Define sources and outputs
            imu = self.pipeline.create(dai.node.IMU)
            xlinkOut = self.pipeline.create(dai.node.XLinkOut)
            xlinkOut.setStreamName("imu")
            # enable ARVR_STABILIZED_GAME_ROTATION_VECTOR at 100 hz rate
            imu.enableIMUSensor([dai.IMUSensor.LINEAR_ACCELERATION, dai.IMUSensor.ARVR_STABILIZED_GAME_ROTATION_VECTOR], 100)
            # above this threshold packets will be sent in batch of X, if the host is not blocked and USB bandwidth is available
            imu.setBatchReportThreshold(1)
            # maximum number of IMU packets in a batch, if it's reached device will block sending until host can receive it
            # if lower or equal to batchReportThreshold then the sending is always blocking on device
            # useful to reduce device's CPU load  and number of lost packets, if CPU load is high on device side due to multiple nodes
            imu.setMaxBatchReports(28)
            # Link plugins IMU -> XLINK
            imu.out.link(xlinkOut.input)
        
        if(greyStereoEnabled) :
            monoResolution = dai.MonoCameraProperties.SensorResolution.THE_400_P
            # Create pipeline
            # Define sources and outputs
            left = self.pipeline.create(dai.node.MonoCamera)
            right = self.pipeline.create(dai.node.MonoCamera)

            leftOut = self.pipeline.create(dai.node.XLinkOut)
            rightOut = self.pipeline.create(dai.node.XLinkOut)

            leftOut.setStreamName("left")

            rightOut.setStreamName("right")

            # Properties
            left.setResolution(monoResolution)
            left.setBoardSocket(dai.CameraBoardSocket.LEFT)
            left.setFps(fps)

            right.setResolution(monoResolution)
            right.setBoardSocket(dai.CameraBoardSocket.RIGHT)
            right.setFps(fps)

            # Linking
            left.out.link(leftOut.input)
            right.out.link(rightOut.input)

            
        if(colorEnabled) :
            
            camRgb = self.pipeline.create(dai.node.ColorCamera)
            rgbOut = self.pipeline.create(dai.node.XLinkOut)

            rgbOut.setStreamName("rgb")
            
            camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
            camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
            camRgb.setFps(fps)
            # downscale color to fit the 800p mono
            if(downscaleColor) :
                camRgb.setIspScale(2,3)
        
            camRgb.isp.link(rgbOut.input)
        
        if(depthEnabled) :
            # check if we didn't enabled stereo cameras before
            if(greyStereoEnabled is not True) :
                monoResolution = dai.MonoCameraProperties.SensorResolution.THE_400_P
                left = self.pipeline.create(dai.node.MonoCamera)
                right = self.pipeline.create(dai.node.MonoCamera)

            self.stereo = self.pipeline.create(dai.node.StereoDepth)
            depthOut = self.pipeline.create(dai.node.XLinkOut)
            
            #"""
            left.setResolution(monoResolution)
            left.setBoardSocket(dai.CameraBoardSocket.LEFT)
            left.setFps(fps)
            right.setResolution(monoResolution)
            right.setBoardSocket(dai.CameraBoardSocket.RIGHT)
            right.setFps(fps)

            #"""
            self.stereo.initialConfig.setConfidenceThreshold(245)
            self.stereo.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_5x5)
            # LR-check is required for depth alignment
            self.stereo.setLeftRightCheck(True)
            
            # align to color if color is present
            if(colorEnabled) :
                self.stereo.setDepthAlign(dai.CameraBoardSocket.RGB)
            
            depthOut.setStreamName("depth")
            
            # linking
            left.out.link(self.stereo.left)
            right.out.link(self.stereo.right)
            self.stereo.disparity.link(depthOut.input)
            # end
        
        if(trackColor) :
            
            if(colorEnabled) :
                featureTrackerColor = self.pipeline.create(dai.node.FeatureTracker)
                xoutPassthroughFrameColor = self.pipeline.create(dai.node.XLinkOut)
                xoutTrackedFeaturesColor = self.pipeline.create(dai.node.XLinkOut)
                xinTrackedFeaturesConfig = self.pipeline.create(dai.node.XLinkIn)

                xoutPassthroughFrameColor.setStreamName("passthroughFrameColor")
                xoutTrackedFeaturesColor.setStreamName("trackedFeaturesColor")
                xinTrackedFeaturesConfig.setStreamName("trackedFeaturesConfig")
                
                if (downscaleColor) :
                    camRgb.video.link(featureTrackerColor.inputImage)
                else:
                    camRgb.isp.link(featureTrackerColor.inputImage)
                    
            numShaves = 2
            numMemorySlices = 2
            featureTrackerColor.setHardwareResources(numShaves, numMemorySlices)
            featureTrackerConfig = featureTrackerColor.initialConfig.get()
            
        if(trackGrayStereo) :
            if(greyStereoEnabled ) :
                featureTrackerLeft = self.pipeline.create(dai.node.FeatureTracker)
                featureTrackerRight = self.pipeline.create(dai.node.FeatureTracker)
                
                #xoutPassthroughFrameLeft  = self.pipeline.create(dai.node.XLinkOut)
                xoutTrackedFeaturesLeft   = self.pipeline.create(dai.node.XLinkOut)
                #xoutPassthroughFrameRight = self.pipeline.create(dai.node.XLinkOut)
                xoutTrackedFeaturesRight  = self.pipeline.create(dai.node.XLinkOut)
                xinTrackedFeaturesConfig  = self.pipeline.create(dai.node.XLinkIn)

                #xoutPassthroughFrameLeft.setStreamName("passthroughFrameLeft")
                xoutTrackedFeaturesLeft.setStreamName("trackedFeaturesLeft")
                #xoutPassthroughFrameRight.setStreamName("passthroughFrameRight")
                xoutTrackedFeaturesRight.setStreamName("trackedFeaturesRight")
                xinTrackedFeaturesConfig.setStreamName("trackedFeaturesConfig")

                left.out.link(featureTrackerLeft.inputImage)
                #featureTrackerLeft.passthroughInputImage.link(xoutPassthroughFrameLeft.input)
                featureTrackerLeft.outputFeatures.link(xoutTrackedFeaturesLeft.input)
                xinTrackedFeaturesConfig.out.link(featureTrackerLeft.inputConfig)

                right.out.link(featureTrackerRight.inputImage)
                #featureTrackerRight.passthroughInputImage.link(xoutPassthroughFrameRight.input)
                featureTrackerRight.outputFeatures.link(xoutTrackedFeaturesRight.input)
                xinTrackedFeaturesConfig.out.link(featureTrackerRight.inputConfig)
                
                numShaves = 2
                numMemorySlices = 2
                featureTrackerLeft.setHardwareResources(numShaves, numMemorySlices)
                featureTrackerRight.setHardwareResources(numShaves, numMemorySlices)

                self.featureTrackerConfig = featureTrackerRight.initialConfig.get()
            else :
                greyStereoEnabled = True
        # set the pipeline to the device 
        self.device = dai.Device(self.pipeline)
        print("USB SPEED : ", self.device.getUsbSpeed())
        #print(self.pipeline.getAllNodes)
        # Now we get ouput queues according to the streams
        if (greyStereoEnabled) :
            self.qLeft = self.device.getOutputQueue(name="left", maxSize=4, blocking=False)
            self.qRight= self.device.getOutputQueue(name="right", maxSize=4, blocking=False)
        
    def timeDeltaToMilliS(self, delta) -> float:
                return delta.total_seconds()*1000
    """
        Retrieves imu data in form of quaternion representing rotation vector
    """
    def getImuData(self) :
        
        if self.device is not None :
            if self.imuEnabled :
                # Output queue for imu bulk packets
                imuQueue = self.device.getOutputQueue(name="imu", maxSize=1, blocking=False)
                imuData = imuQueue.get()  # blocking call, will wait until a new data has arrived
                imuPackets = imuData.packets
                
                for imuPacket in imuPackets:
                    rotVector = imuPacket.rotationVector
                    rotVecTs = rotVector.timestamp.get()
                    self.rotVectorOut = [rotVector.real,rotVector.i,rotVector.j,rotVector.k]
                    
                return self.rotVectorOut
    """
        Retrieves pair of left right gray camera views 
    """
    def getGrayFrames(self) :
        
        if self.device is not None :
            if self.grayStereoEnabled :
                
                inLeft = self.qLeft.tryGet()
                inRight = self.qRight.tryGet()
                
                frameLeft = None
                frameRight = None

                if inLeft is not None:
                    frameLeft = inLeft.getCvFrame()

                if inRight is not None:
                    frameRight = inRight.getCvFrame()
                    
                if frameLeft is not None and frameRight is not None:
                    return [frameLeft, frameRight]
        """
        Gets color frame in CV2 format
        """
    def getColorFrames(self) :
        if self.device is not None :
            if self.colorEnabled :
                
                self.latestPacket["rgb"] = None
                colorFrame = None
                
                queueEvents =  self.device.getQueueEvents(("rgb"))
                for queueName in queueEvents:
                    packets =  self.device.getOutputQueue(queueName).tryGetAll()
                    if len(packets) > 0:
                        self.latestPacket[queueName] = packets[-1]
                if self.latestPacket["rgb"] is not None:
                    colorFrame = self.latestPacket["rgb"].getCvFrame()
                return colorFrame
        """
        Gets depth frame in CV2 format
        """
    def getDepthFrames(self) :
        """Gets depth from gray stereo stream

        Returns:
            CV frame: Depth frame 
        """
        if self.device is not None :
            if self.depthEnabled :
                
                self.latestPacket["depth"] = None
                depthFrame = None
                
                queueEvents =  self.device.getQueueEvents(("depth"))
                for queueName in queueEvents:
                    packets =  self.device.getOutputQueue(queueName).tryGetAll()
                    if len(packets) > 0:
                        self.latestPacket[queueName] = packets[-1]
                if self.latestPacket["depth"] is not None:
                    depthFrame = self.latestPacket["depth"].getCvFrame()
                return depthFrame
    
    def getStereoFeatures(self, getPassthroughFrames : bool = False) :
        """_summary_

        Args:
            drawPassthroughFrames (bool, optional): Additionally outputs left and right passthrough frame with features drawn onto them. Defaults to False.

        Returns:
            _type_: _description_
        """
        if self.device is not None :
            if self.trackStereoEnabled :
                
                self.outputFeaturesLeftQueue     = self.device.getOutputQueue("trackedFeaturesLeft", 8, False)
                self.outputFeaturesRightQueue    = self.device.getOutputQueue("trackedFeaturesRight", 8, False)
                
                self.inputFeatureTrackerConfigQueue = self.device.getInputQueue("trackedFeaturesConfig")
                leftKeyPoints, rightKeyPoints = None, None
                leftFrame, rightFrame = None, None
                
                leftKeyPoints = self.outputFeaturesLeftQueue.get().trackedFeatures
                rightKeyPoints = self.outputFeaturesRightQueue.get().trackedFeatures
        
                if getPassthroughFrames :
                    passthroughImageLeftQueue   = self.device.getOutputQueue("passthroughFrameLeft", 8, False)
                    passthroughImageRightQueue  = self.device.getOutputQueue("passthroughFrameRight", 8, False)
                    
                    inPassthroughFrameLeft = passthroughImageLeftQueue.tryGet()
                    inPassthroughFrameRight = passthroughImageRightQueue.tryGet()
                    
                    passthroughFrameLeft = inPassthroughFrameLeft.getFrame()
                    leftFrame = cv2.cvtColor(passthroughFrameLeft, cv2.COLOR_GRAY2BGR)
                    passthroughFrameRight = inPassthroughFrameRight.getFrame()
                    rightFrame = cv2.cvtColor(passthroughFrameRight, cv2.COLOR_GRAY2BGR)
                    
                    return leftKeyPoints, rightKeyPoints, leftFrame, rightFrame
                
                return leftKeyPoints, rightKeyPoints
            
    def setFeatureTrackingConfig(self, hwAccelerated : bool = False):
        """Sets the Config of feature tracking optical flow algorithm

        Args:
            hwAccelerated (bool, optional): Sets the optical flow to HW Accelerated algorithm. Defaults to False.
        """
        if hwAccelerated :
            self.featureTrackerConfig.motionEstimator.type = dai.FeatureTrackerConfig.MotionEstimator.Type.HW_MOTION_ESTIMATION
            print("Switching to hardware accelerated motion estimation")

        else :
            self.featureTrackerConfig.motionEstimator.type = dai.FeatureTrackerConfig.MotionEstimator.Type.LUCAS_KANADE_OPTICAL_FLOW
            print("Switching to Lucas-Kanade optical flow")
        
        cfg = dai.FeatureTrackerConfig()
        cfg.set(self.featureTrackerConfig)
        self.inputFeatureTrackerConfigQueue.send(cfg)