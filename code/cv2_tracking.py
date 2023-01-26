import math
import numpy as np
from scipy.spatial.transform import Rotation as R
import cv2


class ArucoTracker():
    """
    Generic tracker for aruco markers

    """

    def __init__(self, mtx, dst, interOcularyDistance:float=0.75, aruco_marker_side_Length: float = 0.07):
        """Aruco tracker

        Args:
            mtx (_type_): camera matrix
            dst (_type_): distortion coefficient
        """
        self.matrix = mtx
        self.distortion = dst
        self.sideLength = aruco_marker_side_Length
        self.rvecs = None
        self.tvecs = None

        self.ARUCO_DICT = {
            "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
            "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
            "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
            "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
            "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
            "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
            "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
            "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
            "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
            "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
            "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
            "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
            "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
            "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
            "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
            "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
            "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
            "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
            "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
            "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11,
            "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL
        }

    def createParameters(self):
        """creates aruco parameters

        Returns:
            _type_: aruco parameters
        """
        params = cv2.aruco.DetectorParameters_create()
        return params

    def getDictionary(self, desired_aruco_dictionary: str):
        """
        creates aruco dictionary  

        Args:
            desired_aruco_dictionary (str): _description_

        Returns:
            _type_: _description_
        """
        dictionary = cv2.aruco.Dictionary_get(
            self.ARUCO_DICT[desired_aruco_dictionary])
        return dictionary

    def detect(self, image, dictionary, params):
        """
        Detects aruco marker

        Args:
            image (_type_): image to detect the marker on
            dictionary (_type_): aruco dictionary
            params (_type_): aruco parameters
            mtx (_type_): camera matrix
            dst (_type_): camera distortion coefficent

        Returns:
            corners, ids, rejected (_type_): returns detected corners of markers and their respective ids
        """
        if image is not None:
            (corners, ids, rejected) = cv2.aruco.detectMarkers(
                image, dictionary, parameters=params, cameraMatrix=self.matrix, distCoeff=self.distortion)
            return (corners, ids, rejected)

    def drawMarkers(self, image, corners, ids):
        """
        Draws markers on provided frame

        Args:
            image (input array): image to draw on
            corners (_type_): detected corners
            ids (_type_): ids of detected markers
        """
        if len(corners) > 0:
            # Flatten the ArUco IDs list
            ids = ids.flatten()

            # Loop over the detected ArUco corners
            for (marker_corner, marker_id) in zip(corners, ids):
                # Extract the marker corners
                corners = marker_corner.reshape((4, 2))
                (top_left, top_right, bottom_right, bottom_left) = corners

                # Convert the (x,y) coordinate pairs to integers
                top_right = (int(top_right[0]), int(top_right[1]))
                bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
                bottom_left = (int(bottom_left[0]), int(bottom_left[1]))
                top_left = (int(top_left[0]), int(top_left[1]))

                # Draw the bounding box of the ArUco detection
                cv2.line(image, top_left, top_right, (0, 255, 0), 2)
                cv2.line(image, top_right, bottom_right, (0, 255, 0), 2)
                cv2.line(image, bottom_right, bottom_left, (0, 255, 0), 2)
                cv2.line(image, bottom_left, top_left, (0, 255, 0), 2)

                # Calculate and draw the center of the ArUco marker
                center_x = int((top_left[0] + bottom_right[0]) / 2.0)
                center_y = int((top_left[1] + bottom_right[1]) / 2.0)
                cv2.circle(image, (center_x, center_y), 4, (0, 0, 255), -1)

                # Draw the ArUco marker ID on the video frame
                # The ID is always located at the top_left of the ArUco marker
                cv2.putText(image, str(marker_id),
                            (top_left[0], top_left[1] - 15),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 255, 0), 2)

    def getMarkersPoses(self, corners, ids, markerLength: float = 0.07):
        """
        Gets poses of markers from provided corners and ids

        Args:
            image (_type_): image to paint the 
            corners (_type_): _description_
            ids (_type_): _description_
            markerLength (int): _description_
        """
        if len(corners) > 0:
            rvecs, tvecs, obj_points = cv2.aruco.estimatePoseSingleMarkers(
                corners,
                markerLength,
                self.matrix,
                self.distortion)

            return(rvecs, tvecs)

    def euler_from_quaternion(self,x, y, z, w):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)
     
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)
     
        return roll_x, pitch_y, yaw_z # in radians

    def convertToPosRot(self, marker_id, rvecs, tvecs):
        # Return the detected markers along with their respective ids
        # Print the pose for the ArUco marker
        # The pose of the marker is with respect to the camera lens frame.
        # Imagine you are looking through the camera viewfinder,
        # the camera lens frame's:
        # x-axis points to the right
        # y-axis points straight down towards your toes
        # z-axis points straight ahead away from your eye, out of the camera

        # Store the translation (i.e. position) information
        i = marker_id
        transform_translation_x = tvecs[i][0][0]
        transform_translation_y = tvecs[i][0][1]
        transform_translation_z = tvecs[i][0][2]

        # Store the rotation information
        rotation_matrix = np.eye(4)
        rotation_matrix[0:3, 0:3] = cv2.Rodrigues(
            np.array(rvecs[i][0]))[0]
        rotation_matrix = cv2.transpose(rotation_matrix)
        _, rotation_matrix = cv2.invert(rotation_matrix)
        r = R.from_matrix(rotation_matrix[0:3, 0:3])
        quat = r.as_quat()

        # Quaternion format
        transform_rotation_x = quat[0]
        transform_rotation_y = quat[1]
        transform_rotation_z = quat[2]
        transform_rotation_w = quat[3]

        # Euler angle format in radians
        roll_x, pitch_y, yaw_z = self.euler_from_quaternion(transform_rotation_x,
                                                            transform_rotation_y,
                                                            transform_rotation_z,
                                                            transform_rotation_w)

        roll_x = math.degrees(roll_x)
        pitch_y = math.degrees(pitch_y)
        yaw_z = math.degrees(yaw_z)

        pos = [transform_translation_x,
               transform_translation_y, transform_translation_z]
        rot = [transform_rotation_x, transform_rotation_y,
               transform_rotation_z, transform_rotation_w]
        hpr = [roll_x, pitch_y, yaw_z]
        return (pos, rot, hpr)

    def get2Dposition(self, marker_id, corners ):
        i = marker_id
        x = (corners[i][0][0][0] + corners[i][0][1][0] +
             corners[i][0][2][0] + corners[i][0][3][0]) / 4
        y = (corners[i][0][0][1] + corners[i][0][1][1] +
             corners[i][0][2][1] + corners[i][0][3][1]) / 4
        return (x, y)

    def drawPoseAxis(self, image, ids, rvecs, tvecs):
        # Draws axis of the given detected markers on given image
        ids = ids.flatten()
        # ids present two values : index and marker_id
        for i, marker_id in enumerate(ids):
            cv2.aruco.drawAxis(image, self.matrix,
                               self.distortion, rvecs[i], tvecs[i], 0.05)
    

# TODO : Establish odometry tracking
    class FastICPOdometry():
        def FastICPOdometry_create(cameraMatrix):
            fastICPOdometer = rgbd.FastICPOdometry_create(cameraMatrix)
            return fastICPOdometer

def slerp(q1, q2, t):
        costheta = q1.dot(q2)
        if costheta < 0.0:
            costheta = -costheta
            q1 = q1.conjugate()
        elif costheta > 1.0:
            costheta = 1.0

        theta = math.acos(costheta)
        if abs(theta) < 0.01:
            return q2

        sintheta = math.sqrt(1.0 - costheta * costheta)
        if abs(sintheta) < 0.01:
            return (q1+q2)*0.5

        r1 = math.sin((1.0 - t) * theta) / sintheta
        r2 = math.sin(t * theta) / sintheta
        return (q1*r1) + (q2*r2)
