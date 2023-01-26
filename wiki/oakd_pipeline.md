Module oakd_pipeline
====================

Classes
-------

`Oakd_pipeline(imuEnabled: bool = False, depthEnabled: bool = False, colorEnabled: bool = False, greyStereoEnabled: bool = False, trackColor: bool = False, trackGrayStereo: bool = False, fps: int = 30, downscaleColor: bool = True)`
:   A oakd interface for multiple pipeline configurations
    
    Create new pipeline that requests the data from oakd device 
    
    self.imuEnabled : bool = imuEnabled
    self.depthEnabled : bool = depthEnabled
    self.colorEnabled : bool = colorEnabled
    self.grayStereoEnabled : bool = greyStereoEnabled
    self.trackColorEnabled : bool = trackColor
    self.trackStereoEnabled : bool = trackGrayStereo

    ### Methods

    `getColorFrames(self)`
    :   Gets color frame in CV2 format
        
        Returns:
            ndarray : color frame

    `getDepthFrames(self)`
    :   Gets depth from gray stereo stream
        
        Returns:
            ndarray : Depth frame

    `getGrayFrames(self)`
    :   Retrieves pair of left right gray camera views 
        
        Returns:
            [ndarray , ndarray] : gray left frame, gray right frame

    `getImuData(self, getTimeStamp: bool = False)`
    :   Retrieves imu data in form of quaternion representing rotation vector
        
        Args:
            getTimeStamp (bool, optional): if true returns timestamp . Defaults to False.
        
        Returns:
                [float, float, float, float] : list in form of : real, i, j, k
        (optional):
                [float, float, float, float], float : list in form of : real, i, j, k , timestamp

    `getStereoFeatures(self, getPassthroughFrames: bool = False)`
    :   Gets feature tracking from stereo camera
        
        Args:
            drawPassthroughFrames (bool, optional): Additionally outputs left and right passthrough frame with features drawn onto them. Defaults to False.
        
        Returns:
            _type_: _description_

    `setFeatureTrackingConfig(self, hwAccelerated: bool = False)`
    :   Sets the Config of feature tracking optical flow algorithm
        
        Args:
            hwAccelerated (bool, optional): Sets the optical flow to HW Accelerated algorithm. Defaults to False.

    `timeDeltaToMilliS(self, delta) ‑> float`
    :