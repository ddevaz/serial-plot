serial-plot
===========

Plot serial data as a scrolling graph in (almost) real-time.


Plots a data stream coming in on a serial (COM) port. The data should
be floats or integers seperated by spaces and terminated by a newline \n, 
eg. 1023.6 28 126

Installation:
     -- TO DO --

Usage:
     -- TO DO --

Args:
     -- TO DO --
  
  -h, --help            show this help message and exit
  -p PORT, --port PORT  COM port to use. Defaults to 'COM1' eg. --port 'COM1'.
  -b BAUD, --baud BAUD  Baudrate in bits per second. Default is 115200.
  -s SIGNALS [SIGNALS ...], --signals SIGNALS [SIGNALS ...]
                        Indeces of signals to plot seperated by spaces. Zero
                        indexed. eg. To plot the 1st and 3rd variables:
                        --signals 0 2
  --xmax XMAX           Specifies the time window to use for the plot in
                        seconds.
  --ymax YMAX           Specifies the range of the window to use for the plot.
  -l, --list            Lists available ports
  --log LOG             Log the serial port to stdout
