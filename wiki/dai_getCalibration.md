Module dai_getCalibration
=========================

Functions
---------

    
`exportCalibrationToJson(device: depthai.Device)`
:   exports calibration data from device formatted as json file
    
    Args:
        device (dai.Device): device to extract the calibration data from

    
`getLMonoCameraDistCoefficent(device: depthai.Device)`
:   _summary_
    
    Args:
        device (dai.Device): _description_
    
    Returns:
        ndarray: right mono camera distortion coefficent

    
`getLMonoCameraIntristics(device: depthai.Device, width: int = 1280, height: int = 720)`
:   Gets left camera intristics
    
    Args:
        device (dai.Device): device to extract the data from
        width (int, optional): frame width. Defaults to 1280. 
        height (int, optional): frame height. Defaults to 720.

    
`getLRGB_Extrinsics(device: depthai.Device)`
:   _summary_
    
    Args:
        device (dai.Device): _description_
    
    Returns:
        ndarray : Transformation matrix of where left Camera is W.R.T RGB Camera's optical center

    
`getLR_Extrinsics(device: depthai.Device)`
:   _summary_
    
    Args:
        device (dai.Device): _description_
    
    Returns:
        ndarray : Transformation matrix of where left Camera is W.R.T right Camera's optical center

    
`getMono_FOV(device: depthai.Device)`
:   _summary_
    
    Args:
        device (dai.Device): _description_
    
    Returns:
        float : monocular field of view

    
`getRGB_DistCoefficent(device: depthai.Device)`
:   _summary_
    
    Args:
        device (dai.Device): _description_
    
    Returns:
        _type_: _description_

    
`getRGB_FOV(device: depthai.Device)`
:   _summary_
    
    Args:
        device (dai.Device): _description_
    
    Returns:
        float : rgb field of view

    
`getRGB_Intristics(device: depthai.Device)`
:   Gets central rgb camera intristics
    
    Args:
        device (dai.Device): device to extract the data from
        
    Returns:
        ndarray : rgb camera intristics

    
`getRMonoCameraDistCoefficent(device: depthai.Device)`
:   _summary_
    
    Args:
        device (dai.Device): _description_
    
    Returns:
        ndarray : right mono camera distortion coefficent

    
`getRMonoCameraIntristics(device: depthai.Device, width: int = 1280, height: int = 720)`
:   Gets right camera intristics
    
    Args:
        device (dai.Device): device to extract the data from
        width (int, optional): frame width. Defaults to 1280. 
        height (int, optional): frame height. Defaults to 720.
    
    Returns:
        ndarray : right mono camera intristics

    
`get_R_StereoRectifiedRotation(device: depthai.Device, width: int = 1280, height: int = 720)`
:   _summary_
    
    Args:
        device (dai.Device): _description_
        width (int, optional): _description_. Defaults to 1280.
        height (int, optional): _description_. Defaults to 720.
    
    Returns:
        mat, mat : left rectification matrix, right rectification matrix