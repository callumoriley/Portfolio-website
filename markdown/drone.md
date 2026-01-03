### Quadcopter Drone

This is a project that I've wanted to do for about a decade and had on the backburner for almost 5 years! It's a 5-inch quadcopter drone. I finally got the chance to complete it a little while ago, to the point where I can fly it around in a controlled way.

I watched a lot of FliteTest on YouTube when I was younger, and I always wanted to get into RC stuff, but it was always a little out of reach. I always wanted to build a quadcopter because I figured they would maximize my return on investment as they're probably the most versatile RC vehicle you can build. In July of 2020, I finally had the money and time (in the summer of COVID, after I had graduated high school) to work on it, so I decided to dive in and make it happen!

### Initial work

In hindsight, my choice of parts was very much informed from what I learned from FliteTest several years earlier and whatever I could find for cheap on eBay at the time:
- Motors and ESCs: I chose discrete ESCs running BLHeli instead of a single combined ESC board. Came in a pack with 2206 ____kV BLDC motors, which meant that I didn't have to search for matching motors.
- Flight controller: I chose a CC3D flight controller running LibrePilot, which was already obsolete when I bought it and is even more obsolete now. It works OK, but getting something that runs more modern firmware (like BetaFlight) and has enough memory for position hold would probably have been a better choice.
- TX/RX: I chose a Flysky FS-i6 as the transmitter and a compatible Flysky receiver, which is a more generic RC transmitter/receiver combo than a lot of the ELRS solutions that I see a lot of newer drones use.
- Frame: Just chose a cheap 5 inch frame.
- Battery: 3S LiPo from a local hobby shop.

Once everything arrived, I started assembling all the parts. It was pretty simple to assemble everything from some tutorials online, and pretty soon I had a fully assembled drone!

My first tests in 2020 did not go very well, as the default PID values led to oscillations and a general lack of control authority (I think I also had it in rate mode instead of attitude mode, which was a poor idea for a first flight). I ended up having a landing where it got dirt in the motors, which seized them up, leading me to shelve the project. The shelving of this project also happened at about the same time I started university, which kept this project on the backburner for years.

#### Picking up the project again

When I picked up the project again in the summer of 2024, I tried cleaning the motors but realized they were too far gone (I also lost some of the C-clips that hold the rotors on and they were soldered directly to the ESCs, which made cleaning tough). I bought a new set of motors and ESCs on eBay, and this time I soldered the motors in with bullet connectors so I could swap them out or easily clean them if needed. I also replaced the receiver as I had salvaged the original receiver for another project. I designed and 3D printed a proper receiver mount and changed to the PPM communication protocol rather than have a ton of wires connected between the receiver and flight controller.

I started tuning again this time taking a more systematic approach where I recorded my findings and PID values and made changes based on those, and I got it working quite well! I'm not much of a pilot, so it's still in attitude mode, but I can take off, land, and fly it around in a controlled way without crashing (mostly), which is honestly all I really need this project to be.

After flying it a couple of times, it became apparent that FPV was a near requirement for a drone like this, so this past summer (in 2025) I used my newfound access to 3D printers at work to print some landing legs and an FPV mount, and I ordered an FPV camera, a 5V buck converter, and a FPV monitor. I assembled it all and did some brief bench testing to ensure that the camera and monitor worked, and then I took it to a field to test it. I had a lot of fun testing it, although by the time I got off work and got to the field it was a bit too dark for the camera to see much. Still, it was a lot of fun, and I noted down a bunch of things that I can improve for the next flight!


#### Conclusion

Although I didn't feel like I learned a huge amount from this project beyond getting experience with building a drone and using components intended for the RC ecosystem, this project ended up being pretty cool! I also enjoyed having a project that I shelved and then picked up again, as sometimes I find that the shame of shelving a project is somewhat of a barrier to picking it up again, which I want to avoid as much as possible because then I miss out on finishing off projects and enjoying the cool results of them. There are a lot of things that I would do differently if I could do this project again, and I may end up getting the chance to do some of those things if I decide to build a new drone with more modern hardware. In the meantime, I plan on doing some further tuning and optimizing so that I can maximize my learning from this project.