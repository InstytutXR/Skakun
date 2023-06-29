# XRometr
---
### OAK-D based Mixed reality construction kit

![Photo of a assembled Skakun XR Moduel](/img/s_1.jpg)

---



XRometr is a fully open source modular mixed reality solution. It is made with researchers, artists and developers in mind. Project provides a base for further incorporation of external sensors and libraries. 
Current version uses inertial sensor for head tracking and aruco library for anchoring digital content to the physical world.  

## Hardware
---

- Depth AI OAK-D depth camera with neural processing unit (Series 1 )
- Chuwi LarkBox Pro micro PC 
- Powerbank Battery capable of providing at least 90 w of power (12v and 3a) for mobile version and 12v 1.5 a for headless mode.
- powerbank starter module set for requesting 12v, reference units would be PD2721/IP2721 chip or ZY12PDN mulitester
- 5.5 inch fullhd hdmi screen from DFRobot
- 3D printed cover for computer unit and the screen
- bluetooth controller pad ( optionally )

## Printables
--- 
![screenshot of enclosure in 3mf format](/img/enclosure_2.png)
![screenshot of enclosure in 3mf format](/img/xconnector_2.png)
- Screen and sensor enclosure 
- x-connector attaching screen and sensor to the enclosure
- additionally the 5x20 any metal screw is needed to secure x-connector

## Power for standalone and mobile setup
--- 

- XR and mobile needs powerbank with the following specs :
  - 12v and 3a minimum 
  - adapter with starter module for requesting precise 12v for Chuwi Larkbox Pro (may vary depending on what type the computing unit is being used)
- Headless setup, without display powered from the same source can work with lower tier powerbank that can provide 12v and 1.5 - 2a .
- Standalone will work with powerbrick  

## Software
---
Current version runs on Python backend and is rendered using Panda3D engine.
Additional libraries used for image processing and marker detection are Opencv-contrib with Aruco module. Numpy and Scipy for mathematical backend. 

# PRINCIPLES OF SUSTAINABILITY 
---
## 3D printing matherials:

We use biodegradable filament: 
B2A-834A1 | F3D FILAMENT Bioflex - 1,75mm 
or  F3D FILAMENT PLA 1,75MM

## Printing and packaging:

We print only with with eco-responsible produced EBS-260 hand printer our no-waste box for Xrometr

Certificates below: 

- [Eco responsibility](http://www.instytutxr.tk/XRometer/certyfikat/Deklaracja_EBS_260a.pdf)
- [ISO9001_2015_TUV Material utilization](http://www.instytutxr.tk/XRometer/certyfikat/Certyfikat_ISO9001_2015_TUV.pdf)

# Links 
---

- [Documentation](https://instytutxr.github.io/XRometer/index.html)
- [Release page](https://github.com/InstytutXR/XRometer/releases)
- [github page](https://github.com/InstytutXR/XRometer)
- [Collegium XR page](https://instytutxr.github.io/XRometer/index.html)

---
![sticker with affiliates logos](/img/afiliates.png)
