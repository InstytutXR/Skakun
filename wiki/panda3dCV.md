Module panda3dCV
================

Classes
-------

`XR_arucoTracker(camera: panda3d.core.NodePath, baseInput: direct.showbase.ShowBase.ShowBase, intristics, distcoefficent)`
:   Manages list of tracked ids with their respective models
    
    Args:
        intristics (_type_): _description_
        distcoefficent (_type_): _description_

    ### Methods

    `calculateRadialZ(self, x, y, z)`
    :   calculates Radial depth of a point from camera
        
        Args:
            x (float): x
            y (float): y
            z (float): z
        
        Returns:
            radial Z (float): _description_

    `convertRvecsToRot(self, rvecs, m_id)`
    :

    `registerNodePathToID(self, nodes)`
    :   _summary_
        
        Args:
            nodes (_type_): nodes to move using aruco poses

    `rodrigues(self, r: numpy.ndarray)`
    :   This returns a 4x4 matrix, which you can apply to a NodePath with setMat(). If you really only want the hpr triple, you can then extract that again with nodePath.getHpr().
        
        David
        
        Args:
            r (_type_): rvecs
        
        Returns:
            Mat4 : panda3d matrix

    `rvecToQuat(self, rvecs, m_id)`
    :

    `updateTracker(self, render: panda3d.core.NodePath, _camera: panda3d.core.NodePath, cardDisplay: panda3d.core.NodePath, frame)`
    :   finds aruco and recognizes markers on the frame and moves the subscribed 
        models to the calculated position
        
        Args:
            _camera (NodePath): scene camera object
            cardDisplay (NodePath): video display object
            frame : image frame to pass to the tracker