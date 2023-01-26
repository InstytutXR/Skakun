from pydoc import visiblename
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Shader
from panda3d.core import *
from direct.filter.FilterManager import FilterManager
from panda3d.core import GraphicsOutput
from panda3d.core import StereoDisplayRegion
from math import sqrt
from direct.interval.LerpInterval import LerpScaleInterval
import sys

# Config for Virtual Reality
configVar = """
show-frame-rate-meter 1

"""
class XRCamera():
    """
    Class that stores all the messy setup for initial XR 

    """
    def __init__(self, baseInput : ShowBase, fovX : float = 69, fovY : float = 55):
        # Exit on pressing the escape button.
        baseInput.accept('escape', sys.exit)
        
        baseInput.disableMouse()
        self.window: GraphicsWindow = baseInput.win
        self.cam: NodePath = baseInput.cam
        self.sdr: StereoDisplayRegion = self.window.getDisplayRegion(5)
        self.lens : Lens = self.sdr.camera.node().getLens()
        baseInput.setBackgroundColor(0,0,0)
        # XR Barrel Distortion post processing
        baseInput.win.setClearDepth(1)
        baseInput.win.setClearDepthActive(True)
        
        manager = FilterManager(baseInput.win, baseInput.cam)
        
        shader = Shader.load(Shader.SL_GLSL,
                     vertex="gfx/shader/barrel.vert",
                     fragment="gfx/shader/barrel.frag")
        #"""
        tex = Texture()
        quad = manager.renderSceneInto(colortex=tex)
        quad.setShader(shader)
        quad.setShaderInput("HmdWarpParam", Vec4(.5,.5,.1,.1))
        quad.setShaderInput("LensCenter", Vec2(0.5,0.5))
        quad.setShaderInput("ScreenCenter", Vec2(.5,.5))
        quad.setShaderInput("Scale", Vec2(1,1))
        quad.setShaderInput("ScaleIn", Vec2(.85,1.5))
        quad.setShaderInput("tex", tex)
        
        self.sdr = manager.buffers[0].getDisplayRegion(3)
        
        #lens.setAspectRatio(800.0 / 300.0)
        
        self.sdr.camera.node().getLens().setNearFar(.1,10000)
        leftEye: DisplayRegion  = self.sdr.getLeftEye()
        rightEye: DisplayRegion = self.sdr.getRightEye()
        leftEye.setClearDepth(1)
        leftEye.setClearDepthActive(True)
        leftEye.camera.node().getLens().setNearFar(.1,10000)
        leftEye.camera.node().getLens().setAspectRatio(640.0 / 400.0)
        leftEye.camera.node().getLens().setFov(fovX,fovY)
        leftEye.camera.node().setCameraMask(BitMask32.bit(0))
        rightEye.setClearDepth(1)
        rightEye.setClearDepthActive(True)
        rightEye.camera.node().getLens().setNearFar(.1,10000)
        rightEye.camera.node().getLens().setAspectRatio(640.0 / 400.0) # change to init var
        rightEye.camera.node().getLens().setFov(fovX,fovY) # change to init var
        rightEye.camera.node().setCameraMask(BitMask32.bit(1)) # change to init var
        #"""
            
        # 
        self.VRRig = NodePath("VRRig")
        self.Head = NodePath("Head")
        self.VRRig.reparentTo(baseInput.render)
        self.Head.reparentTo(self.VRRig)
        
        # Camera setup
        baseInput.cam.node().getLens().setAspectRatio(640.0 / 400.0)
        baseInput.cam.node().getLens().setFov(fovX,fovY)
        baseInput.cam.node().getLens().setNearFar(.1, 10000)
        baseInput.camera.reparentTo(self.Head)
        """
        q = Quat()
        q.setHpr(Vec3(90,90, 180))
        baseInput.camera.set_quat(q)
        #self.Head.setPos(0, 0, 2)
        """
        
        
        # Synchronisation with pose provider 
    def updateCameraPose(self, rotation : Quat, position : Vec3):
        r = rotation
        p = position
        
        gyrRot = Quat(r[0],r[1],r[2],r[3])
        pos = Vec3(p[0],p[1],p[2])
        self.Head.set_quat(gyrRot)
        self.Head.setPos(pos)
    
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
    
class XR_Anchor():
    """
    an object that handles rendering of models in XR 
    """
    def __init__(self, base : ShowBase,  anchorName : str ):
        """_summary_

        Args:
            base (ShowBase): _description_
            anchorName (str): _description_
        """
        
        #self.setPythonTag("name", anchorName)
        self.base = base
        self.visible = False
        self.render = base.render
        self.root = NodePath("root")
        self.root.reparentTo(base.render)
        self.models : list[NodePath] = []
        
    def addModel(self,modelPath : str, pos = Vec3(0,0,0), rot = Vec3(0,0,0), scale = Vec3(0,0,0)):
        """Adds model object

        Args:
            modelPath (str): _description_
            pos (_type_, optional): _description_. Defaults to Vec3(0,0,0).
            rot (_type_, optional): _description_. Defaults to Vec3(0,0,0).
            scale (_type_, optional): _description_. Defaults to Vec3(0,0,0).
        """
        _model : NodePath = self.base.loader.loadModel(modelPath)
        _model.setPosHprScale(pos,rot,scale)
        _model.reparentTo(self.root)
        self.models.append(_model)
        return _model
    
    def addActor(self,modelPath : str, animPaths : str, pos = Vec3(0,0,0), rot = Vec3(0,0,0), scale = Vec3(0,0,0)):
        assembleActor = Actor(modelPath,animPaths)
        _model : NodePath = self.root.attachNewNode(assembleActor)
        _model.setPosHprScale(pos,rot,scale)
        _model.reparentTo(self.root)
        self.models.append(_model)
        return _model
    
    def addImage(self, texturePath : str, pos = Vec3(0,0,0), rot = Vec3(0,0,0), scale = Vec3(0,0,0)):
        """
        Adds Card object with a texture

        Args:
            texturePath (str): path to the texture that will be mapped to the card
            pos (_type_, optional): _description_. Defaults to Vec3(0,0,0).
            rot (_type_, optional): _description_. Defaults to Vec3(0,0,0).
            scale (_type_, optional): _description_. Defaults to Vec3(0,0,0).
        """
        cm = CardMaker('CardMaker')
        _card : NodePath = self.root.attachNewNode(cm.generate())
        _tex = self.base.loader.loadTexture(texturePath)
        _card.setTexture(_tex)
        _card.setPosHprScale(pos,rot,scale)
        self.models.append(_card)
        return _card
        
    def addMovie(self, texturePath : str, pos = Vec3(0,0,0), rot = Vec3(0,0,0), scale = Vec3(0,0,0)):
        """
        Adds Card object with a texture

        Args:
            texturePath (str): path to the movie that will be mapped to the card
            pos (_type_, optional): _description_. Defaults to Vec3(0,0,0).
            rot (_type_, optional): _description_. Defaults to Vec3(0,0,0).
            scale (_type_, optional): _description_. Defaults to Vec3(0,0,0).
        """
        cm = CardMaker('CardMaker')
        _card : NodePath = self.root.attachNewNode(cm.generate())
        self.movie : MovieTexture = self.base.loader.loadTexture(texturePath)
        _card.setTexture(self.movie)
        _card.setPosHprScale(pos,rot,scale)
        self.movie.play()
        self.movie.setLoop(True)
        self.models.append(_card)
        
    def IsInView(self, object):
        lensBounds = self.base.cam.makeBounds()
        bounds = object.getBounds()
        bounds.xform(object.getParent().getMat( self.base.cam))
        return lensBounds.contains(bounds)
    
    def hideModels(self) :
        #todo : create a logic of hiding models when they are not seen
        for _m in self.models :
            _model : NodePath = _m
            _model.hide()
        
    def showModels(self) :
        #todo : create a logic of hiding models when they are not seen
        for _m in self.models :
            _model : NodePath = _m
            _model.show()
            
class XR_AnchorManager() :
    def __init__(self, base : ShowBase, anchorCount = 0) :
        self.base = base
        self.anchors : list[XR_Anchor] = []
        if anchorCount > 0 :
            for i in range(anchorCount) :
                self.addAnchor(i)
            
    def addAnchor(self, name : str) :
        _anchor = XR_Anchor(self.base, name)
        self.anchors.append(_anchor)
        _anchor.root.setPythonTag("name", name)
        
    def clip(self, value, lower, upper):
        return lower if value < lower else upper if value > upper else value
    
    def lerp(self , A, B, t):
        value = (t * A) + ((1-t) * B)
        return value
    
    def checkVisible(self):
        for _anchor in self.anchors :
            #s : Vec3 = _anchor.root.getScale()
            #dt = globalClock.dt
            if not _anchor.visible :
                #print("invisible")
                #s = self.lerp(s,Vec3.zero,Vec3(.1,.1,.1))
                #_anchor.root.setScale(s)
                LerpScaleInterval(_anchor.root, 1, 0, None, None, 'easeInOut').start()
            else :
                #print("visible")
                #s = self.lerp(s,Vec3(1,1,1),Vec3(.1,.1,.1))
                #_anchor.root.setScale(s)
                LerpScaleInterval(_anchor.root, 1, 1, None, None, 'easeInOut').start()
                