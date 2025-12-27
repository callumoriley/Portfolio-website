### Quadcopter Drone

This is a project that I've wanted to do for about a decade and had on the backburner for almost 5 years! It's a 5-inch quadcopter drone. I finally got the chance to complete it a little while ago, to the point where I can fly it around in a controlled way.

I watched a lot of FliteTest when I was younger, and I always wanted to get into RC stuff, but it was always a little out of reach. I always wanted to build a quadcopter because they're probably the most versatile RC vehicle you can build. In July 2020, I finally had the money and time (in the summer of COVID, after I had graduated high school) to work on it, so I decided to dive in and make it happen!

In hindsight, my choice of parts was very much informed from what I learned from FliteTest several years earlier and whatever I could find for cheap on eBay at the time:
- Motors and ESCs: I chose discrete ESCs running BLHeli instead of a single combined ESC board. Came in a pack with 2206 ____kV BLDC motors, which meant that I didn't have to search for matching motors.
- Flight controller: I chose a CC3D running LibrePilot, which was already obsolete when I bought it and is even more obsolete now. It works OK, but getting something that runs more modern firmware (like BetaFlight) and has enough memory for position hold would probably have been a better choice.
- TX/RX: I chose a Flysky FS-i6 as the transmitter and a compatible Flysky receiver, which is a more generic RC transmitter/receiver combo than a lot of the ELRS solutions that I see a lot of newer drones use.
- Frame: Just chose a cheap 5 inch frame.
- Battery: 3S LiPo from a local hobby shop.

Once everything arrived, I started assembling all the parts. It was pretty simple to assemble everything from some tutorials online, and pretty soon I had a fully assembled drone!

My first tests in 2020 did not go very well, as the default PID values led to oscillations and a general lack of control authority (I think I also had it in rate mode instead of attitude mode, which was a poor idea for a first flight). I ended up having a landing where it got dirt in the motors, which seized them up, leading me to shelve the project for years.

#### Picking up the project again

When I picked up the project again last summer, I tried cleaning the motors but realized they were too far gone. I bought a new set of motors and ESCs on eBay, and this time I soldered the motors in with bullet connectors so I could swap them out or easily clean them if needed. I also replaced the receiver as I had used the original receiver for another project. I designed and 3D printed a proper receiver mount and changed to the PPM communication protocol rather than have a ton of wires connected between the receiver and flight controller.

I started tuning again this time taking a more systematic approach where I recorded my findings and PID values, but a crash broke the receiver mount and I shelved the project again (life started getting busy again by this point).

Earlier this year, one of my friends showed me his DJI Mini 3, and that inspired me to finish the project and get it flying. I asked another friend to 3D print me a new strengthened receiver mount using a Bambu Lab printer.

I brought it out to a small field and started tuning it. I had documented my tuning process from the previous summer already, so I used that as a starting point and continued from there, and I got it working quite well!

After flying it a couple more times, it became apparent that FPV was a near requirement for a drone like this, so later in the summer I used my newfound access to 3D printers at work to print some landing legs and an FPV mount, and I ordered an FPV camera, a 5V buck converter, and a FPV monitor. I assembled it all and did some brief bench testing to ensure that the camera and monitor worked, and then I took it to a field to test it. I had a lot of fun testing it, although by the time I got off work and got to the field it was a bit too dark for the camera to see much. Still, it was a lot of fun, and I noted down a bunch of things that I can improve for the next flight!


#### Conclusion

This is a project that I want to come back to in the near future and continue optimizing, so stay tuned!