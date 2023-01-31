from panda3d.core import loadPrcFileData
import gltf
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.interval.IntervalGlobal import *
from panda3d.core import *
from panda3d.core import GraphicsOutput
from panda3d.core import StereoDisplayRegion
import pandaXR as xr
import oakd_pipeline
import dai_getCalibration as calib
import cv2
import numpy as np
import panda3dCV
import tkinter as tk
from PIL import Image, ImageDraw
# Config for Virtual Reality
configVar = """
show-frame-rate-meter 1
side-by-side-stereo 1
win-size 1920 1080 
fullscreen #t
default-iod 0.75
textures-power-2 none
want-pstats 1
"""
loadPrcFileData('', configVar)
WIDTH = 640
HEIGHT = 400
WIDTHRATIO = 1
#HEIGHTRATIO_RGB = 720/1280
HEIGHTRATIO = HEIGHT/WIDTH
CAMDISTANCE = 1
IOD = .75
CONVERGENCE = 35 # Where both images are identical ie max depth distance
DEPTH = 1
SCALE = 2.3

sensor = oakd_pipeline.Oakd_pipeline(True, False, True, True, False, False, 30)

device = sensor.device
I_rgb = calib.getRGB_Intristics(device)
D_rgb = calib.getRGB_DistCoefficent(device)
I_Lmono = calib.getLMonoCameraIntristics(device, WIDTH, HEIGHT)
D_Lmono = calib.getLMonoCameraDistCoefficent(device)


class Skakun(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        # setup debug values
        self.hor: float = 0
        self.ver: float = 0
        self.lat: float = 0
        # setup debug cam
        print('MxId:',device.getDeviceInfo().getMxId())

        self.accept("q", self.oobe)

        # setup XR camera
        self.xr_Cam = xr.XRCamera(self)
        self.xr_Cam.lens.setInterocularDistance(IOD)
        self.xr_Cam.lens.setConvergenceDistance(CONVERGENCE)
        #self.xr_Cam.VRRig.setPos(0, 0, 8)

        # tasks to run dynamically
        self.taskMgr.add(self.updateCameraTask,
                         "updateCameraTask", priority=0, sort = 49)
        self.taskMgr.add(self.updateArucoTask,
                         "updateArucoTask", priority=1, sort = 48)
        # setup background cards
        # set up a texture for (h by w) rgb image
        self.transTex = Texture()
        self.grayStereoTex_l = Texture()
        self.grayStereoTex_r = Texture()
        self.grayStereoTex_l.setup2dTexture(
            WIDTH, HEIGHT, Texture.T_unsigned_byte, Texture.F_rgba8)
        self.grayStereoTex_r.setup2dTexture(
            WIDTH, HEIGHT, Texture.T_unsigned_byte, Texture.F_rgba8)
        # has to be set up after setup2dTexture because setup2dtexture resets multiview to 1
        self.grayStereoTex_l.setNumViews(2)
        self.grayStereoTex_r.setNumViews(2)

        #self.leftTex.setup2dTexture(640, 400, Texture.T_unsigned_byte, Texture.F_luminance)
        #self.rightTex.setup2dTexture(640, 400, Texture.T_unsigned_byte, Texture.F_luminance)

        # set up a stereo cards to apply the numpy texture
        # """
        cm = CardMaker('cardMaker')
        self.background = NodePath("background")
        # generate cards and attach them to the background node
        self.background.setPos(self.xr_Cam.Head.getPos())
        
        self.card_L: NodePath = self.background.attachNewNode(cm.generate())
        self.card_R: NodePath = self.background.attachNewNode(cm.generate())
        self.card_C: NodePath = self.background.attachNewNode(cm.generate())  
        # transparent center card for disparity
        self.card_L.setTransparency(TransparencyAttrib.M_alpha)
        self.card_R.setTransparency(TransparencyAttrib.M_alpha)
        # Set streams  to render in respective camera views

        self.background.reparentTo(self.xr_Cam.Head)

        # create alpha transparent image to use in the dual textures
        #self.transparent_img = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)
        img = Image.new('RGBA', (WIDTH, HEIGHT), (255, 0, 0, 0))
        self.transparent_img = np.array(img)
        #cv2.cvtColor(self.transparent_img,cv2.COLOR_BGRA2RGBA)
        # self.transTex.setRamImage(self.transparent_img)

        # cardL is square, rescale to the original image aspect ratio
        cardScale = Vec3(WIDTHRATIO * CAMDISTANCE * SCALE,
                         DEPTH, HEIGHTRATIO * CAMDISTANCE * SCALE)
        cardPos = Vec3(-WIDTHRATIO/2 * CAMDISTANCE * SCALE,
                       CAMDISTANCE, -HEIGHTRATIO/2 * CAMDISTANCE * SCALE)

        self.card_L.setScale(cardScale)
        self.card_R.setScale(cardScale)
        self.card_C.setScale(cardScale)
        # bring it to center, put it in front of camera add half 
        # inter oculary distance for eye distance
        self.card_L.setPos(cardPos + Vec3(IOD/2, 0, 0))
        self.card_R.setPos(cardPos - Vec3(IOD/2, 0, 0))
        self.card_C.setPos(cardPos)
        #
        self.card_C.hide()
        #"""
        self.card_L.setBin("background", 20)
        self.card_L.setDepthTest(False)
        self.card_L.setDepthWrite(False)

        self.card_R.setBin("background", 20)
        self.card_R.setDepthTest(False)
        self.card_R.setDepthWrite(False)
        #"""
        q = Quat()
        q.setHpr(Vec3(0,0,180))
        self.background.setQuat(self.xr_Cam.Head.getQuat(self.render) * q)
        # """
        self.gray = None
        #self.card_C.setTexture(self.transTex)
        self.aruco = panda3dCV.XR_arucoTracker(
            self.xr_Cam.cam, self, I_Lmono, D_Lmono)
        # setup the XR world
        # Todo : Convert to scene loader // additional class for aruco markers
        #"""
        
        #""" 
        # Map Loading 
        self.anchorManager = xr.XR_AnchorManager(self, 10)
        michal = self.anchorManager.anchors[1].addModel("gfx/3d/korzenie.glb",Vec3.zero(),Vec3(0,0,0),Vec3(1,1,1))
        maciej = self.anchorManager.anchors[2].addModel("gfx/3d/metakosmos/spacehulk.glb",Vec3.zero(),Vec3(0,0,0),Vec3(.1,.1,.1))
        marzena = self.anchorManager.anchors[3].addModel("gfx/3d/metakosmos/marzenaKolarz.glb",Vec3.zero(),Vec3(0,0,0),Vec3(1,1,1))
        tv = self.anchorManager.anchors[4].addModel("gfx/3d/metakosmos/tv.glb",Vec3.zero(),Vec3(0,0,0),Vec3(.001,.001,.001))
        natalia = self.anchorManager.anchors[5].addModel("gfx/3d/metakosmos/nataliaNowosinska.glb",Vec3.zero(),Vec3(0,0,0),Vec3(1,1,1))
        julia : NodePath = self.anchorManager.anchors[6].addModel("gfx/3d/metakosmos/juliaWierenko.glb",Vec3(0,1,0),Vec3(0,0,0),Vec3(1,1,1))
        ewaD = self.anchorManager.anchors[7].addModel("gfx/3d/metakosmos/ewa_doroszenko.glb",Vec3.zero(),Vec3(0,0,0),Vec3(1,1,1))
        #town = self.anchorManager.anchors[8].addModel("gfx/3d/metakosmos/townScan.glb",Vec3.zero(),Vec3(0,0,0),Vec3(1,1,1))
        #self.anchorManager.anchors[11].addModel("gfx/3d/marker.glb",Vec3.zero(),Vec3(90,90,0),Vec3(.1,.1,.1))
        #self.anchorManager.anchors[8].addMovie("gfx/2d/eye_video_4_3.mp4",Vec3.zero(),Vec3(90,0,0),Vec3(1.6,0.9,1))
        #jacekD = self.anchorManager.anchors[10].addMovie("gfx/2d/Jacek Doroszenko Kernel-1.mp4",Vec3.zero(),Vec3(90,0,0),Vec3(1.6,0.9,1))
        #kuba = self.anchorManager.anchors[5].addMovie("gfx/2d/Kuba Metakosmos_hd_2.mp4",Vec3.zero(),Vec3(90,0,0),Vec3(1.6,0.9,1))
        self.aruco.registerNodePathToID(self.anchorManager.anchors)
        posInterval1 = julia.posInterval(3,Point3(0, 0, -1),startPos=Point3(0, 0, 1))
        posInterval2 = julia.posInterval(3,Point3(0, 0, 1),startPos=Point3(0, 0, -1))
        oscillate = Sequence(posInterval1,posInterval2,name="oscillate")
        oscillate.loop()
        print(julia)
        #"""
        # Stereo Camera texture setup
        self.card_L.setTexture(self.grayStereoTex_l)
        self.card_R.setTexture(self.grayStereoTex_r)

    def updateCameraTask(self, task):
        # Draws passthrough
        if sensor.device is not None:
                # updates imu
            imu = sensor.getImuData()
            # print(imu)
            #"""
            
            offset = Quat()
            offset.setHpr(Vec3(90,90,180)) # compensation for whatever the coordinate system is in depth ai
            q = Quat(imu[0], imu[1], imu[2], imu[3])
            self.xr_Cam.Head.setQuat(offset*q)
            """
            print("head rot : ", self.xr_Cam.Head.getHpr(self.render))
            print("camera rot : ", self.camera.getHpr(self.render))
            #"""
            #rgb = sensor.getColorFrames()
            #rgb_flipped = cv2.flip(rgb, 1)
            # if rgb is not None:
            # self.tex.setRamImage(rgb_flipped)
            self.gray = sensor.getGrayFrames()
            if self.gray is not None:

                left = self.gray[0]
                right = self.gray[1]
                # mistakes were made - dont relate to cam bc its going to fuck u up
                """
                self.aruco.updateTracker(
                    self.render,
                    self.xr_Cam.Head, 
                    self.card_C, left)  # the actual tracking
                
                self.anchorManager.checkVisible()
                #"""
                # convert bw to color with alpha and set alpha to 0
                left = cv2.cvtColor(left, cv2.COLOR_GRAY2RGBA)
                right = cv2.cvtColor(right,cv2.COLOR_GRAY2RGBA)
                
                left = cv2.flip(left, 1)
                right = cv2.flip(right, 1)
                
                left_image = bytes(left) + bytes(self.transparent_img)
                right_image = bytes(self.transparent_img) + bytes(right)

                # set the streams to  the textures
                self.grayStereoTex_l.setRamImage(left_image)
                self.grayStereoTex_r.setRamImage(right_image)
                
                #print("frame updated" )
        else:
            print("sensor lost, please check connection")
        return Task.cont

    def updateArucoTask(self, task):
         # Draws passthrough
        if sensor.device is not None:
            #rgb = sensor.getColorFrames()
            #rgb_flipped = cv2.flip(rgb, 1)
            # if rgb is not None:
            # self.tex.setRamImage(rgb_flipped)
            #self.gray = sensor.getGrayFrames()
            if self.gray is not None:

                left = self.gray[0]
                right = self.gray[1]
                # mistakes were made - dont relate to cam bc its going to fuck u up
                self.aruco.updateTracker(
                    self.render,
                    self.xr_Cam.Head, 
                    self.card_C, left)  # the actual tracking
                
                self.anchorManager.checkVisible()
                # convert bw to color with alpha and set alpha to 0
                """
                left = cv2.cvtColor(left, cv2.COLOR_GRAY2RGBA)
                right = cv2.cvtColor(right,cv2.COLOR_GRAY2RGBA)
                
                left = cv2.flip(left, 1)
                right = cv2.flip(right, 1)
                
                left_image = bytes(left) + bytes(self.transparent_img)
                right_image = bytes(self.transparent_img) + bytes(right)

                # set the streams to  the textures
                self.grayStereoTex_l.setRamImage(left_image)
                self.grayStereoTex_r.setRamImage(right_image)
                #"""
        return Task.cont

app = Skakun()
app.run()
