# tacho
Python script to drive a tachometer on Raspberry Pi GPIO using PWM

![Screenshot](/tacho-network.jpg?raw=true "Network traffic MB/s")

 Required hardware and schematics
 ----

 The components needed to drive a standard automotive RPM gauge are
 pretty simple. You need:

   - 12V power source (or battery)
   - Optocoupler 4N25
   - 200 Ohm resistor for input
   - 20kOhm resistor for pull-down for gauge signal

The script assumes BCM GPIO 4 (Pin 7 in Rasperry Pi) to be used for
driving the gauge. Pin 9 is used for the ground. Opto-isolator acts like
normal led, so putting a small ~200 Ohm resistor makes it ok with 3.3V.

Operating modes
----

First parameter specifies the operating mode:

- test - Goes trhough test cycle setting values from 1 to 8
- <value> - sets the given value between 1-8
- cpu - displays CPU load percentage from 0 up to 80%
- network - displays network inbound traffic in MB/s.

Optional 'quiet' parameter disables the console output.

For example the following puts the script to refresh CPU on the background

sudo ./tacho.py cpu quiet &

Note that because GPIO on RPi needs root access, so sudo is used.
