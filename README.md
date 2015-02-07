MinePi
======

An internet of things project using:
- a raspberry pi running python scripts and a mosquitton MQTT server
- an arduino phone used as a camera mounted in a servo-controlled pan/tilt mechanism
- a Minecraft server plugin that acts as an MQTT client that talks to the MQTT client on the RPi
- a webpage (uses websockets) that also acts as an MQTT client that talks to the MQTT client on the RPi

Integration of Minecraft (or a web page) with real world events using GPIO on a Raspberry Pi, Python and MQTT

The basic idea is that the pan/tilt camera can be viewed and controlled from either a webpage or from Minecraft.

This all works but the code is very rough ...
I still need to include the Minecraft Server code here.

3D Printed Pan/Tilt Arm
=======================

The .scad and .stl files for the 3D printed parts are in the directory branch
'3DPrinter'.

The parts were printed with an infill of .8 (80%) with good results.
The pan/tilt arm uses two servo motors ... the initial prototype uses:
- 1x SG-5010 TowerPro servo
- 1x SM-S4303R (not sure of manufacturer)

These servos were used because they were available ... one of these servos is 
cpntinuous and one is not.  I would go with non-continuous servos for both 
motors ... the SG-5010 is non-continuous so I would go with two of 
these servos (or similar) moving forward.

There are also images in the 3DPrinter directory showing what the pan/tilt arm
looks like.

