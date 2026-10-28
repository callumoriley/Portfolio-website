### CNC Router

Even though I studied electrical engineering, I enjoy working on mechanical projects sometimes. Maybe it's because I find the mechanical aspects of projects more difficult

A big part of any mechanical project is how you produce parts for it. 3D printing has been quite popular over the last decade or so (I've personally used it for a bunch of projects), but I have always been more interested in other faster prototyping methodologies, like laser cutting or CNC routing.

So when a dilapidated Shapeoko 2 was offered to me after sitting unused in our design team workspace for several years, I couldn't pass up the opportunity to put a really capable machine to use.



The bones of the machine is a Shapeoko 2 CNC router. I'm not sure how or when my design team received this machine, but it was taking up a bunch of space and there wasn't anyone who was claiming it, so design team leadership offered it up and I took it home. In addition to the Shapeoko frame, the machine had all the NEMA17 stepper motors, a stepper driver board, and a vice for workholding.

The first thing I had to do was to get the axes moving. I downloaded Universal G-code Sender onto one of my Linux laptops, uploaded GRBL to an Arduino Uno and connected it to the stepper driver, powered it all with an ATX power supply that I had laying around, and it started moving immediately!

I then had to attach some kind of cutting tool to the machine. I chose a cheap Genmitsu router motor with an ER11 collet chuck and some router bits that I got off Amazon.

Previously, I had done all my 3D design work in SolidWorks as it was what I had access to through school, but this project prompted me to switch over to Fusion 360 for its integrated CAM software
