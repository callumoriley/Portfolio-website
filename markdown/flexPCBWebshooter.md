### Flex PCB Webshooter

I'm excited to finally share a project I've had on the backburner for a couple years. This is a wrist-wearable device built around a flex PCB. Its main features, which are accessed through a capacitive touch sensor that extends into the palm, are some white LEDs for illumination and an IR blaster that can send arbitrary IR commands to nearby devices. It is heavily inspired by the webshooters from the Spider-Man comics and movies.

(insert video embed here)

#### Idea and Project Concept

In June 2023, I watched Spider-Man: Across the Spider-Verse, and I absolutely loved it. I loved the characters, the animation, the story, everything about it. One of the ways that I like to engage with pop culture is by building projects based on it, so as I was walking out of the theater, I knew I had to make some kind of webshooter.

After some more thinking, I decided that I wanted to implement this project using a flex PCB, and that I wanted it to have a couple specific features. I chose LED illumination because it is relatively simple to implement, and I chose the IR blaster because it's quite a bit more interesting, I had done some experiments with receiving/transmitting IR codes previously, and it fits the formfactor of a webshooter well (because you can point your wrist at a TV and turn it off/on). I chose to interact with the device through capacitive touch sensing to be true to the comics, and because I didn't want to deal with the forces required for a pushbutton.

(insert comic book panel here)

So to recap, here are the high-level requirements for this project:
- Built on a flex PCB
- Interact with it through a capacitive touch sensor
- Has white LEDs for illumination
- Can send IR commands to an IR device

#### Hardware

(insert Altium screenshot here?)

The requirements for this project required some technologies and skills that I previously hadn't worked with:
- Flex PCB design
- Embedding a microcontroller with oscillator onto a flex PCB
- Capacitive touch sensing

The main flex PCB takes the shape of a wristband with a projection coming out from it to act as the capacitive touch sensor in the palm. I added steel stiffeners behind areas where components are placed to prevent stress on the solder joints of the components (flex PCBs can easily rip at solder joints because of how thin they are). To clasp the device around your wrist, there are holes through the PCB and the stiffeners to put a pin through with a stopper on the other end (like the kind used for making enamel pins).

I chose to use a PIC microcontroller for this project, as the behaviour I wanted to implement was pretty simple and it didn't sit right with me to have a really overkill microcontroller. I specifically chose the PIC16F18425 for is capacitive touch sensing capability and its forgiving SOIC-14 package. To program the PIC without putting too much strain on the board from unplugging/plugging it in, I added 5 pads in a line for the programming signals and soldered an adapter between the PICKit3 and some pogo pins that could interface with those pads. The only downside to this is that I had to hold the adapter down on the board with one hand while stepping through code with my other hand, so maybe creating a programming jig is another task for a version 3.

The white LEDs are placed on the wristband with stiffeners behind them. They’re all driven by a single MOSFET. In hindsight, it would have been neat to make them addressable to do something a bit more interesting with them, maybe an idea for version 3! IR communications are done by 3 wide-beamwidth IR LEDs, also driven by a single MOSFET. The component selection and schematic design for these was taken from the Flipper Zero’s schematics, as it’s a proven device with the functionality I wanted, and it’s open-source!

I assembled the board by hand (placing parts manually and using a reflow oven at school) so I wasn't constrained with JLCPCB's part selection, and to save money. The layout wasn't super dense, so I could make do with 0805 passives to make that easier on myself.

Every hardware project requires at least two revisions, and this is no exception. The first revision largely worked, but I had to make some minor changes to some footprints and the capacitive touch sensor line to decrease spurious detections.

(insert assembly pictures here)

#### Firmware

(insert hall debugging image here)

I generally prefer hardware to firmware, so when writing the firmware, I just wanted to get it done as fast as possible to get the device working. This meant that I was leaning heavily on Microchip’s libraries and code generation features. This came back to bite me later on, and I learned some valuable lessons that I’ve carried into more recent projects.

Since I’m using a PIC, the firmware is programmed using the MPLAB IDE and programmed using a PICKit3. 

The behaviour I decided upon implementing was to send an IR command with a single tap, then toggle the illumination LED state with a double tap. This is pretty simple behaviour to implement.

I used the mTouch library to implement the capacitive touch sensor, which I found to be a super easy way to implement capacitive touch. One fun feature of this library is the sensor thresholds are adjusted on the fly, so it even works when you have the sensor right next to your skin (which adds a bunch of extra capacitance). If I had to do this project over again, I probably would have tried to write the capacitive sensing code on my own, for reasons discussed later. 

I used a bunch of hardware timers for generating the timeout, for generating the 38kHz IR LED modulation, and for timing the IR LED pulse periods.

Getting the IR communication code to work was the most difficult part of the project. I was having a lot of issues with the pulse periods being longer and having more timing variance than the periods I specified, which I initially thought were inefficiencies in my code. I did a ton of rounds of optimization, which I systematically recorded and analyzed in a Jupyter Notebook, trying things like optimizing my timer interrupt code, trying O3 optimization (which Microchip paywalls with a free trial, by the way), and pre-generating the timer reloads so I didn't have to do 16-bit math on the fly. I ended up realizing that my system clock was not fast enough and that I could boost my 8MHz external clock to a 32MHz system clock using the PLL inside the microcontroller. After adjusting all my timers so that everything worked with the faster system clock, it worked!

I definitely dragged my feet a lot on the firmware portion of this project, although I learned a lot of really important lessons that I can apply in future projects. The biggest thing I learned was that you have to fully understand your entire firmware codebase, because when things start to go south and you need to debug them, you will have to understand everything that's going on to effectively debug it. Early on, I leaned a lot on MPLAB's code configurator for generating timer interrupts, which made development quick at the start but allowed me to get quite far without actually understanding how the PIC platform implements timer interrupts, so when things started not working, I had to learn all that from scratch anyways after spending time trying to make it work through MCC. Code generators also tend to pave over your code if you make edits outside of the very limiting barriers that they put in the code, so I couldn't really use MCC past a certain point anyways. Another good example is the mTouch library, which while working quite well, I didn't have a good understanding of what it was doing and therefore couldn't optimize that much, I think it was generating interrupts while I was sending IR codes, contributing a bit to the timing variance I was seeing.

I also felt like I was running up against the limitations of the PIC platform. If I did this project again, I would probably use a more powerful platform like the STM32, as these days you can get some lower-capability versions that blow the 8-bit PIC I was using out of the water while being cheaper (for example the STM32C011J4M6, which is half the price of my PIC16F18425). There is something to be said for writing optimized code that fits your platform very well, and I think that's an important skill, just for my personal projects where I'm more interested in getting something that works, I would rather give myself more performance headroom to begin with than run up against the limitations of my platform and have to spin a new revision with a new microcontroller. I was also running into some headaches with MPLAB, such as O3 optimization being paywalled and my PICKit3 being obsoleted in the newest version. I use the STM32 platform a lot at my current job, and I find it a much better experience overall, which counts for a lot.

Ultimately, I ended up with working firmware that taught me a lot and I'm still pretty proud of, even though it's very simple from a high level. I'll be able to take the things I've learned and apply them in many different projects in the future.


#### Conclusion

This was a really neat project to work on, and I learned a ton from it! It definitely took a lot longer to finish than it needed to (started in summer 2023 and finally finished in fall 2025), but I ended up being quite busy during my last couple years of school and didn’t have much time to work on it. Overall, this project was a success. The hardware portion of this project was relatively straightforward, so I gained a lot of confidence with the design risks that I took there. The firmware portion was a huge learning experience, and I learned a lot of hard lessons about hardware limitations and leaning on code you don’t understand. At the end of it all, I designed, built, programmed, and debugged a really cool device that, while not being super useful, looks really cool and meets all my requirements perfectly! I’m really looking forward to building some more projects with the learnings gained from this project!