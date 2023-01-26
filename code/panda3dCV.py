import cv2
from cv2 import Mat
import numpy as np
from panda3d.core import *
from cv2_tracking import *
import dai_getCalibration as calib
from math import sqrt, atan2, asin, pi
from direct.showbase.ShowBase import ShowBase
from pandaXR import XR_Anchor
from direct.interval.LerpInterval import *
import numba

INVERSE_MATRIX = [[1,  0,  0, 0 ],
                  [0,  0,  1, 0 ],
                  [0, -1,  0, 0 ],
                  [0,  0,  0, 0 ]]

class XR_arucoTracker() :
    def __init__(self, camera : NodePath, baseInput : ShowBase, intristics, distcoefficent):
        """Manages list of tracked ids with their respective models

        Args:
            intristics (_type_): _description_
            distcoefficent (_type_): _description_
        """
        self.baseInput = baseInput
        self.arucoTracker = ArucoTracker(intristics, distcoefficent)
        self.trackedNodes : list[XR_Anchor] = []
        self.params = self.arucoTracker.createParameters()
        self.dictionary = self.arucoTracker.getDictionary("DICT_ARUCO_ORIGINAL")
        self.cam = camera
        pass
    
    def registerNodePathToID(self, nodes):
        """_summary_

        Args:
            nodes (_type_): nodes to move using aruco poses
        """
        self.trackedNodes = nodes
    
    def calculateRadialZ(self, x, y, z):
        """
        calculates Radial depth of a point from camera

        Args:
            x (float): x
            y (float): y
            z (float): z

        Returns:
            radial Z (float): _description_
        """
        radialZ = sqrt(pow(x,2) + pow(y,2) + pow(z,2))
        return radialZ
    
    def updateTracker(self, render : NodePath,_camera : NodePath, cardDisplay : NodePath, frame):
        """
        finds aruco and recognizes markers on the frame and moves the subscribed 
        models to the calculated position

        Args:
            _camera (NodePath): scene camera object
            cardDisplay (NodePath): video display object
            frame : image frame to pass to the tracker
        """
        
        (corners, ids, _) = self.arucoTracker.detect(frame, self.dictionary, self.params)
        if ids is None:
                return
        ids = ids.flatten()
        
        # TODO : cleaning up for using this as a generic function
        print("marker ids : ", ids.flatten())
        self.arucoTracker.drawMarkers(frame, corners, ids)
        rvecs, tvecs = self.arucoTracker.getMarkersPoses(corners, ids)
        print(rvecs, tvecs)
        self.arucoTracker.drawPoseAxis(frame, ids, rvecs, tvecs)
        
        for _node in self.trackedNodes :
            _node.visible = False
        
        for i, m_id in enumerate(ids):
                
                try:
                    self.trackedNodes[m_id]
                except:
                    continue
                
                self.trackedNodes[m_id].visible = True
                
                node : XR_Anchor = self.trackedNodes[m_id].root
                print( "picked marker name : ", node.getPythonTag("name")," ", m_id, " ", m_id)
                m_pos, m_rot, m_hpr = self.arucoTracker.convertToPosRot(
                    i, rvecs, tvecs)
                m_x, m_y = self.arucoTracker.get2Dposition(i, corners)

                #TODO: instead of hardcoded X / Y there should be variables that are locked to the source image h / w
                p2d = Vec3(1 - (m_x / 640), m_y / 400, 0)
                z = self.calculateRadialZ(
                    m_pos[0], m_pos[1], m_pos[2])

                camPos: Vec3 = _camera.getPos(self.baseInput.render)
                
                # position
                # first XY on display
                node.setPos(cardDisplay, Vec3(
                    p2d.x,  # p3d.x,
                    0,  # p3d.z,
                    p2d.y  # p2d.y
                )
                )
                # then Z from camera to the 2d point using z from tracker
                #pos1 * (1 - x) + pos2 * x
                node.setPos(
                    camPos * (1-z) + node.getPos(self.baseInput.render) * z)
                
                #""" ROTATION
                r = self.rvecToQuat(rvecs, i)
                c = _camera.getQuat(render)
                q = node.getQuat(_camera)
                targetRot = slerp(q,r,0.05)
                node.setQuat( _camera ,q) 
                #"""
                print("node pos : ", node.getPos(self.baseInput.render), "node rot : ", node.getHpr(self.baseInput.render))
                
        return

    def rodrigues(self, r : np.ndarray):
        """
        This returns a 4x4 matrix, which you can apply to a NodePath with setMat(). If you really only want the hpr triple, you can then extract that again with nodePath.getHpr().

        David

        Args:
            r (_type_): rvecs

        Returns:
            Mat4 : panda3d matrix
        """
        
        theta = r.size
        if theta == 0:
            return Mat4.identMat()
        c = math.cos(theta)
        s = math.sin(theta)
        c1 = 1.0 - c

        rx = r[0] / theta
        ry = r[1] / theta
        rz = r[2] / theta

        I = Mat3.identMat()
        rrt = Mat3(rx*rx, rx*ry, rx*rz, rx*ry, ry*ry, ry*rz, rx*rz, ry*rz, rz*rz)
        _r_x_ = Mat3(0, -rz, ry, rz, 0, -rx, -ry, rx, 0)

        R = Mat3()
        for y in range(3):
            for x in range(3):
                R.setCell(y, x, I(y, x) * c + rrt(y, x) * (1.0 - c) + _r_x_(y, x) * s)
        R.transposeInPlace()
        return Mat4(R)
    
    def rvecToQuat(self, rvecs, m_id) :
        
        #float theta = (float)(Math.Sqrt(m.x*m.x + m.y*m.y + m.z*m.z)*180/Math.PI);
        #Vector3 axis = new Vector3 (m.x, -m.y, m.z);            //multiply m.y by -1 since in Unity y-axis points upward
        #Quaternion rot = Quaternion.AngleAxis (theta, axis);
        r = np.array(rvecs[m_id][0])
        #print("rot vector :  ", r)
        theta = sqrt(r[0]*r[0] + r[1]*r[1] + r[2]*r[2]) * 180/pi
        #print("THETA :  ", theta)
        axis = Vec3(r[0],r[2],-r[1])
        axis = axis.normalized()
        q = Quat()
        q.setFromAxisAngle(theta, axis)
        return q
    
    def convertRvecsToRot(self, rvecs, m_id):
        print("rotation vector : ", rvecs[m_id])
        rotMat = np.eye(4)
        rotMat[0:3, 0:3] = cv2.Rodrigues(rvecs[m_id][0])[0]
        print("rotation matrix : ", rotMat)
        rotMat = rotMat @ INVERSE_MATRIX

        mat3 = Mat3()
        mat3.set(rotMat[0][0], rotMat[0][1], rotMat[0][2], 
                 rotMat[1][0], rotMat[1][1], rotMat[1][2], 
                 rotMat[2][0], rotMat[2][1], rotMat[2][2])

        mat = Mat4(mat3)

        r = Quat()
        r.setFromMatrix(mat)
        r.normalize()

        q = Quat()
        q.setHpr(Vec3(0, 0, 0))
        r : Quat = r #* q
        return r