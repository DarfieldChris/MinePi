//////////////////////////////////////////////////////////////
///
///  PanTiltArm - Servo-controlled pan/tilt arm for a USB or
///               web cam
///
///               This mount is modified from: 
///                http://www.thingiverse.com/thing:302741
///               This project uses the original scad file from
///               the above project and modifies it.
///
//////////////////////////////////////////////////////////////
///
///	 2014-09-18	Chris Newton, Canada			Created
///
///  released under Creative Commons - Attribution - Share Alike licence
//////////////////////////////////////////////////////////////

// include methods from "http://www.thingiverse.com/thing:302741"
use <PanTilt_Servo.scad>

// Modified version of the original method base_v1()
// Only difference is length is passed as parameter
module base_v1(length=30)
{
   difference()
   {
      union()
      {
         cube([length,30,5],center=true);
         translate([-length/2,0,0]) cylinder(5,15,15,center=true,$fn=60);
      }
      translate([-15,0,0]) holer_f();
   }
}

// Modified version of the original method holer_m()
// Only difference is length and width are passed as parameters
module holer_m(length=40, width=20)
{
   cube([length,width,5.2],center=true);
   for(x = [length/2+4,-length/2-4])
      for(y = [5,-5])
         translate([x,y,0]) cylinder(5.2,1.5,1.5,center=true,$fn=60);
}

// Modified version of the original method brace_1()
// Only difference is length is passed as parameter
module brace_1(length=30)
{
   difference()
   {
      cube([10,length,10],center=true);
      translate([5,0,5]) rotate([90,0,0]) cylinder(length + 0.2,9.9,9.9,center=true,$fn=60);
   }
}

// Modified version of the original method base_v2
// This method now creates a holder for an android phone
module base_v2_android()
{
   difference()
   {
      union()
      {
         cube([70,23,5],center=true);
         translate([35,0,0]) cylinder(5,23/2,23/2,center=true,$fn=60);

		// ADDED - CN
		translate([0,9,12]) cube([70,5,20], center=true);
		translate([0,-9,12]) cube([70,5,20], center=true);
		translate([30,-9,25]) cube([10,5,50], center=true);
		translate([30,9,25]) cube([10,5,50], center=true);
      }
      translate([4,0,0]) cube([50,6,5.2],center=true);
   }
}

// Modified version of the original method base_v()
// that will work for an android phone
module base_v_android_phone()
{
   union()
   {
      rotate([0,90,0]) { translate ([-10,0,0] ) base_v1(length=50); }
      translate([37.5,0,-12.5]) base_v2_android();
      translate([ 7.5,0, -5  ]) brace_1(length=23);
   }
}

module pantilt_android()
{
   // Vertical base 
   translate([0,0,32.5]) base_v_android_phone();
   // Horizontal base
   //rotate([0,270,0])
   translate([-15,0,20]) base_h();
   // Fixed base
   translate([15,0,-30]) base_f();
}

// uncomment this line if you want to draw all of the original pan/tilt parts
//pantilt();

// uncomment this line if you want to draw the modified android pan/tilt parts
pantilt_android();

// UNCOMMENT TO JUST PRINT THE VERTICAL BASE
//base_v_android_phone();

// UNCOMMENT TO JUST PRINT THE HORIZONTAL BASE
//rotate([0,270,0])
//base_h();

// UNCOMMENT TO JUST PRINT THE FIXED BASE
//base_f();
