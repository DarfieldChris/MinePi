MinePi
======

Integration of Minecraft with real world events using GPIO on a Raspberry Pi, Python and MQTT

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

