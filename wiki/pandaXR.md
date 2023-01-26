Module pandaXR
==============

Classes
-------

`XRCamera(baseInput: direct.showbase.ShowBase.ShowBase, fovX: float = 69, fovY: float = 55)`
:   Class that stores all the messy setup for initial XR

    ### Methods

    `calculateRadialZ(self, x, y, z)`
    :   calculates Radial depth of a point from camera
        
        Args:
            x (float): x
            y (float): y
            z (float): z
        
        Returns:
            radial Z (float): _description_

    `updateCameraPose(self, rotation: panda3d.core.LQuaternionf, position: panda3d.core.LVector3f)`
    :

`XR_Anchor(base: direct.showbase.ShowBase.ShowBase, anchorName: str)`
:   an object that handles rendering of models in XR 
    
    _summary_
    
    Args:
        base (ShowBase): _description_
        anchorName (str): _description_

    ### Methods

    `IsInView(self, object)`
    :

    `addActor(self, modelPath: str, animPaths: str, pos=LVector3f(0, 0, 0), rot=LVector3f(0, 0, 0), scale=LVector3f(0, 0, 0))`
    :

    `addImage(self, texturePath: str, pos=LVector3f(0, 0, 0), rot=LVector3f(0, 0, 0), scale=LVector3f(0, 0, 0))`
    :   Adds Card object with a texture
        
        Args:
            texturePath (str): path to the texture that will be mapped to the card
            pos (_type_, optional): _description_. Defaults to Vec3(0,0,0).
            rot (_type_, optional): _description_. Defaults to Vec3(0,0,0).
            scale (_type_, optional): _description_. Defaults to Vec3(0,0,0).

    `addModel(self, modelPath: str, pos=LVector3f(0, 0, 0), rot=LVector3f(0, 0, 0), scale=LVector3f(0, 0, 0))`
    :   Adds model object
        
        Args:
            modelPath (str): _description_
            pos (_type_, optional): _description_. Defaults to Vec3(0,0,0).
            rot (_type_, optional): _description_. Defaults to Vec3(0,0,0).
            scale (_type_, optional): _description_. Defaults to Vec3(0,0,0).

    `addMovie(self, texturePath: str, pos=LVector3f(0, 0, 0), rot=LVector3f(0, 0, 0), scale=LVector3f(0, 0, 0))`
    :   Adds Card object with a texture
        
        Args:
            texturePath (str): path to the movie that will be mapped to the card
            pos (_type_, optional): _description_. Defaults to Vec3(0,0,0).
            rot (_type_, optional): _description_. Defaults to Vec3(0,0,0).
            scale (_type_, optional): _description_. Defaults to Vec3(0,0,0).

    `hideModels(self)`
    :

    `showModels(self)`
    :

`XR_AnchorManager(base: direct.showbase.ShowBase.ShowBase, anchorCount=0)`
:   

    ### Methods

    `addAnchor(self, name: str)`
    :

    `checkVisible(self)`
    :

    `clip(self, value, lower, upper)`
    :

    `lerp(self, A, B, t)`
    :