Module cv2_tracking
===================

Functions
---------

    
`slerp(q1, q2, t)`
:   

Classes
-------

`ArucoTracker(mtx, dst, interOcularyDistance: float = 0.75, aruco_marker_side_Length: float = 0.07)`
:   Generic tracker for aruco markers
    
    _summary_
    
    Args:
        mtx (nparray): camera matrix
        dst (nparray): distortion coefficient
        interOcularyDistance (float, optional): distance between cameras. Defaults to 0.75.
        aruco_marker_side_Length (float, optional): size of aruco marker. Defaults to 0.07.

    ### Class variables

    `FastICPOdometry`
    :

    ### Methods

    `convertToPosRot(self, marker_id, rvecs, tvecs)`
    :

    `createParameters(self)`
    :   creates aruco parameters
        
        Returns:
            _type_: aruco parameters

    `detect(self, image, dictionary, params)`
    :   Detects aruco marker
        
        Args:
            image (_type_): image to detect the marker on
            dictionary (_type_): aruco dictionary
            params (_type_): aruco parameters
            mtx (_type_): camera matrix
            dst (_type_): camera distortion coefficent
        
        Returns:
            corners, ids, rejected (_type_): returns detected corners of markers and their respective ids

    `drawMarkers(self, image, corners, ids)`
    :   Draws markers on provided frame
        
        Args:
            image (input array): image to draw on
            corners (_type_): detected corners
            ids (_type_): ids of detected markers

    `drawPoseAxis(self, image, ids, rvecs, tvecs)`
    :

    `euler_from_quaternion(self, x, y, z, w)`
    :   Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)

    `get2Dposition(self, marker_id, corners)`
    :   Converts 
        
        Args:
            marker_id (_type_): _description_
            corners (_type_): _description_
        
        Returns:
            _type_: _description_

    `getDictionary(self, desired_aruco_dictionary: str)`
    :   creates aruco dictionary  
        
        Args:
            desired_aruco_dictionary (str): _description_
        
        Returns:
            _type_: _description_

    `getMarkersPoses(self, corners, ids, markerLength: float = 0.07)`
    :   Gets poses of markers from provided corners and ids
        
        Args:
            image (_type_): image to paint the 
            corners (_type_): _description_
            ids (_type_): _description_
            markerLength (int): _description_