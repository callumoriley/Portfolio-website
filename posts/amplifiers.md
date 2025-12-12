## Amplifier Projects

During my 3rd year, I took ELEC 301, which is our equivalent of Circuit Analysis III at UBC. The course mainly focused on analyzing BJT amplifiers, and by the end of it, I wanted to put what I had learned into action. I felt like designing and building an audio amplifier was somewhat of a rite of passage for an electrical engineer, but I also wanted a cheap but robust speaker that I could use for hosting events or general speaker needs.

While conceptualizing this project, I realized that I could fill both these goals better if I instead designed and built two devices: a fully-analog amplifier where I could fully simulate every part of it and learn a lot from building it (but not necessarily a very practical device), and a device built around a class D amplifier IC that prioritized portability and ease of use.

### Class A/AB Amplifier

Since this device was not intended to be very practical and was mostly an exercise in design, I made this a single-channel audio amplifier for simplicity. I decided on a class A preamplifier using a common-emitter topology, as it made the most intuitive sense to me and seems to be a very common analog preamplifier. I initially tried to use the techniques I had learned in ELEC 301 to choose the bias resistors for maximum gain and output swing empirically, but I realized that the assumptions behind those rules don't hold as well when aiming for larger output signals. I ended up running a bunch of simulations in LTSpice to determine the resistor values, which ended up working pretty well. I found some resistor values that gave me a large gain and a reasonable output swing with no clipping. One fact that I learned more intuitively with this project than I did during 301 is that the forward transconductance (and therefore gain) of a BJT is proportional to the collector current through the BJT, and in my pursuit of gain I ended up with a significant amount of power loss across my BJT. 

For the power amplifier, I chose a class AB power amplifier to minimize crossover distortion with my relatively low gain preamplifier. I used a complimentary pair of BJTs for the power amplifiers (TIP31C and TIP32C) and added some 1N4148s with 1k resistors to eliminate the crossover distortion that one would see if they used a class B power amplifier (which doesn't include diodes or resistors).

(include LTSpice picture here)

My design voltage was 12V, so my output range ended up being relatively small, so I chose a pretty small 3W speaker as my output. I soldered the amplifier onto a perfboard and tested it out, and surprisingly it worked first try! 

One issue that I experienced was that the power amplifier transistors would go into thermal runaway over a period of a couple of minutes, which increased the audio volume (by increasing their forward transconductance) but also got the transistors way too hot. I tried adding emitter resistors to the power output stage, but I found that while I could stop the thermal runaway, I incurred a severe volume penalty. Potentially a future version of this amplifier could include collector current control on the output stage to properly limit this issue, but I didn't end up testing this before shelving the project.

(include board picture here)

(video?)

### Class D Amplifier/Speaker

This project was more to build a practical speaker that I could use to listen to music on my own or play some music if I had some friends over. 

I was inspired by an [Afrotechmods video](https://www.youtube.com/watch?v=O1UagNkcxi4) to use the TPA3122, which is an all-in-one stereo class D audio amplifier chip from TI. I started this project during our 3rd year design project class, so I snuck the parts for this project onto one of our last-minute Digikey orders for parts that we desperately needed to get our project working (to save on shipping costs). Mainly following the suggested application circuit, I soldered all the parts onto a perfboard right the day after my last final exam while we still had access to our project lab. It didn't work the first try, and I had to move for an internship in Victoria, so I shelved the project for a little while, but I later realized that I had skipped some capacitors that weren't in the application schematic but turned out to be important. Using some speaker drivers that a friend picked up for me from Lee's Electronics (a local electronics shop in Vancouver), I was able to properly finish the project and built an enclosure for it using some plywood. It ended up sounding quite good! It's probably one of my most useful projects, as I still use it fairly often. One time, I had some friends over for dinner and they asked about playing music, and when I brought the speaker out they started laughing, but then they were pleasantly surprised by the sound quality! There's something to be said for having a speaker whose appearance sets low expectations and then rises above them in sound quality! 

(include board picture here)

(video?)

### Conclusion

These were both very fun projects, and I definitely learned a lot more about audio amplifiers than I expected to! I realized that a lot of my electronics projects have been pretty experimental and not super practical, so the class D amplifier is probably my most useful project to date.