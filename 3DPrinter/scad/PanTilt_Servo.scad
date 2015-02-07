// NOTE: THIS FILE COPIED FROM http://www.thingiverse.com/thing:302741
// Not sure if there are any copyright issues with re-using it ...
// I have included it just so that the project has a complete file set ...
// THIS IS NOT MY WORK!!!

/*---------------------------------------------------------\
|     From: Ekobots Innovation Ltda - www.ekobots.com      |
|       by: Juan Sirgado y Antico - www.jsya.com.br        |
|----------------------------------------------------------|
|     Program Camera Rotate & Tilt Servo - 2014/04/12      |
|               All rights reserved 2014                   |
|---------------------------------------------------------*/
pantilt();
//---------------------------------------------------------|
module pantilt()
{
   // Micro camera for reference
   translate([35,0,55]) camera_m();
   // Vertical base 
   translate([0,0,32.5]) base_v();
   // Horizontal base
   //rotate([0,270,0])
   translate([-15,0,20]) base_h();
   // Fixed base
   translate([15,0,-30]) base_f();
}
//---------------------------------------------------------|
module camera_m()
{
   // Micro camera for reference
   difference()
   {
      union()
      {
         cube([36,16,36],center=true);
         rotate([90,0,0]) 
            translate([0,0,16]) cylinder(16,8,8,center=true,$fn=60);
      }
      translate([-35,0,-29]) cylinder(10,3,3,center=true,$fn=60);
   }
}
//---------------------------------------------------------|
module base_v()
{
   // Vertical base 
   union()
   {
      rotate([0,90,0]) base_v1();
      translate([22.5,0,-12.5]) base_v2();
      translate([ 7.5,0, -5  ]) brace_1();
   }
}
//---------------------------------------------------------|
module base_h()
{
   // Horizontal base
   union()
   {
      rotate([0,90,0]) base_h1();
      translate([17.5,0,-32.5]) base_h2();
      translate([ 7.5,0,-25  ]) brace_1();
   }
}
//---------------------------------------------------------|
module base_f()
{
   // Fixed base
   difference()
   {
      union()
      {
         cube([60,30,5],center=true);
         translate([ 30,0,0]) cylinder(5,15,15,center=true,$fn=60);
         translate([-30,0,0]) cylinder(5,15,15,center=true,$fn=60);
      }
      translate([-10,0,0]) holer_m();
      translate([ 30,0,0]) cylinder(5.2,3,3,center=true,$fn=60);
   }
}
//---------------------------------------------------------|
module base_v1()
{
   difference()
   {
      union()
      {
         cube([30,30,5],center=true);
         translate([-15,0,0]) cylinder(5,15,15,center=true,$fn=60);
      }
      translate([-15,0,0]) holer_f();
   }
}
//---------------------------------------------------------|
module base_v2()
{
   difference()
   {
      union()
      {
         cube([40,30,5],center=true);
         translate([20,0,0]) cylinder(5,15,15,center=true,$fn=60);
      }
      translate([10,0,0]) cube([30,3,5.2],center=true);
   }
}
//---------------------------------------------------------|
module base_h1()
{
   difference()
   {
      union()
      {
         cube([70,30,5],center=true);
         translate([-35,0,0]) cylinder(5,15,15,center=true,$fn=60);
      }
      translate([-15,0,0]) holer_m();
   }
}
//---------------------------------------------------------|
module base_h2()
{
   difference()
   {
      union()
      {
         cube([30,30,5],center=true);
         translate([15,0,0]) cylinder(5,15,15,center=true,$fn=60);
      }
      translate([15,0,0]) holer_f();
   }
}
//---------------------------------------------------------|
module holer_m()
{
   cube([40,20,5.2],center=true);
   for(x = [24,-24])
      for(y = [5,-5])
         translate([x,y,0]) cylinder(5.2,1.5,1.5,center=true,$fn=60);
}
//---------------------------------------------------------|
module holer_f()
{
   cylinder(5.2,4,4,center=true,$fn=60);
   for(r = [45,135,225,315])
      rotate([0,0,r]) translate([10,0,0]) 
         cylinder(5.2,1.5,1.5,center=true,$fn=60);
}
//---------------------------------------------------------|
module brace_1()
{
   difference()
   {
      cube([10,30,10],center=true);
      translate([5,0,5]) rotate([90,0,0]) cylinder(30.2,9.9,9.9,center=true,$fn=60);
   }
}
//---------------------------------------------------------|

