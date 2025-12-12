## Quadcopter Drone

This is a project that I've wanted to do for about a decade and had on the backburner for almost 5 years! It's a 5-inch quadcopter drone. I finally got the chance to complete it a couple weeks ago, to the point where I can fly it around in a controlled way.

I watched a lot of FliteTest when I was younger, and I always wanted to get into RC stuff, but it was always a little out of reach. 

In July 2020, I finally had the money and time (in the summer of COVID, after I had graduated high school) to work on it.

In hindsight, my choice of parts was very much informed from what I gained from FliteTest and whatever I could find for cheap. I chose to go with 4 discrete BLHeli ESCs instead of a single combined ESC. I also chose a CC3D running LibrePilot, which was already obsolete when I bought it and is even more obsolete now (but it works).

My first tests in 2020 did not go very well, as the default PID values led to oscillations and a general lack of control authority (I think I also had it in rate mode instead of attitude mode, which was a poor idea for a first flight). I ended up having a landing where it got dirt in the motors, which siezed them up, leading me to shelve the project for years.

When I picked up the project again last summer, I tried cleaning the motors but realized they were too far gone. I bought a new set of motors and ESCs on eBay, and this time I soldered the motors in with bullet connectors so I could swap them out or easily clean them if needed. I also replaced the receiver as I had used the original receiver for another project. I designed and 3D printed a receiver mount and changed to the PPM communication protocol rather than have a ton of wires connected between the receiver and flight controller.

I started tuning again, but a crash broke the receiver mount and I shelved the project again (life got busy again by this point).

One of my friends showed me his DJI Mini 3, and that inspired me to finish the project and get it flying. I asked another friend to 3D print me a new strengthened receiver mount using a Bambu Lab printer.

I brought it out to a small field and started tuning it. I had documented my tuning process from the previous summer already, so I used that as a starting point and continued from there, and I got it working quite well!