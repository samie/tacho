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

The Hz is calibrated to [specific hardware](http://biltema.se/sv/Bil---MC/Bil-tillbehor/Bil-el/Instrument/Varvraknare-32251/) using the calibration array in the beginning of the script. You probably need to adjust the numbers 
here to make it match your hardware. 

Operating modes
----

Run the script by giving the operating more as the first parameter:

- test - Goes trhough test cycle setting values from 1 to 8
- [value] - displays the given float value between 1-8
- cpu - displays CPU load percentage from 0 up to 80%
- network - displays network inbound traffic in MB/s.

Optional 'quiet' parameter disables the console output.

For example the following puts the script to refresh CPU on the background

    sudo ./tacho.py cpu quiet &

Note that because GPIO on RPi needs root access, so sudo is used.
