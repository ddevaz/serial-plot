#!/usr/bin/env python
"""
serial_plotter.py
 
Display serial data as scrolling plot.

Author: Dmitri De Vaz

"""

import sys, serial, argparse

# Fast lists:
from collections import deque

# Plotting:
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
 

class AnalogPlot:
  """This class handles adding new points to the plot window."""
  def __init__(self, strPort, baud, maxLen, indeces):
      # open serial port
      self.ser = serial.Serial(strPort, baud)
      self.indeces = indeces
      self.numSignals = len(indeces)
      # signals
      self.a = [deque([0.0]*maxLen) for i in range(self.numSignals)]
      self.maxLen = maxLen
      
  # add to buffer
  def addToBuf(self, buf, val):
      if len(buf) < self.maxLen:
          buf.append(val)
      else:
          buf.pop()
          buf.appendleft(val)
 
  # adds a single data point
  def add(self, data):
      assert(len(data) == self.numSignals)
      for i in range(self.numSignals):
        self.addToBuf(self.a[i], data[i])

  # update plot
  def update(self, frameNum, *larg):
      try:
          line = self.ser.readline()
          data = [float(val) for val in line.split()]
          # print data
          selected_sigs = [data[index] for index in self.indeces]
          self.add(selected_sigs)
          for i in range(self.numSignals):
            larg[i].set_data(range(self.maxLen), self.a[i])

      except KeyboardInterrupt:
          print('exiting')
      
      return larg[0], 
 
  # clean up
  def close(self):
      # close serial
      self.ser.close()    
      self.ser.flush()
 


def list_serial_ports():
    """Lists serial ports
    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of available serial ports
    """
    if sys.platform.startswith('win'):
        ports = ['COM' + str(i + 1) for i in range(256)]

    elif sys.platform.startswith('linux'):
        # this is to exclude your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')

    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')

    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except serial.SerialException:
            pass
    return result


def log_serial(strPort, baud, n):
  ser = serial.Serial(strPort, baud, timeout=5.0)
  for i in range(n):
    print(ser.readline().strip().decode("utf-8"))
  ser.flush()
  ser.close()  




def main():
  parser = argparse.ArgumentParser(description="Live Serial Plotter. Plots data coming in on the serial port. \
                                                Variables should be floats or integers seperated by spaces    \
                                                and terminated by a newline \\n, eg. 1023.6 28 126")
  
  # add arguments
  parser.add_argument('-p', '--port',
                      help="COM port to use. Defaults to 'COM1' eg. --port 'COM1'.",
                      required=True)
  
  parser.add_argument('-b', '--baud',
                      help="Baudrate in bits per second. Default is 115200.",
                      required=False, 
                      type=int, 
                      default=115200)
  
  parser.add_argument('-s', '--signals', 
                      help="Indeces of signals to plot seperated by spaces. \
                            Zero indexed. eg. To plot the 1st and 3rd variables: --signals 0 2",
                      required=False, 
                      type=int, 
                      nargs='+')
  
  parser.add_argument('--xmax',  
                      help="Specifies the time window to use for the plot in seconds.",
                      required=False, 
                      type=int, 
                      default=500)

  parser.add_argument('--ymax',  
                      help="Specifies the range of the window to use for the plot.",
                      required=False, 
                      type=int, 
                      default=5000)

  parser.add_argument('-l', '--list', 
                      help='Lists available ports',
                      required=False,
                      action='store_true')

  parser.add_argument('--log', 
                      help='Log the serial port to stdout',
                      required=False,
                      type=int)

  # parse args
  args = parser.parse_args()
  # required args
  strPort = args.port
  # optional args
  baud = args.baud
  xmax = args.xmax
  ymax = args.ymax

  if (args.list):
    print(list_serial_ports())
    return
  elif (args.log):
    log_serial(strPort, baud, args.log) 
    return

  # Configure number of signals.
  if (args.signals):
    indeces = args.signals
    numSignals = len(indeces)
  else:
    # Detect the number of signals based
    # on the data.
    numSignals = len(serial.Serial(strPort, baud).readline().split())
    indeces = list(range(numSignals))
 
  print('reading from serial port %s...' % strPort)
 
  # plot parameters
  analogPlot = AnalogPlot(strPort, baud, xmax, indeces)
 
  print('plotting signals %s...' % indeces)
  print('Ctrl+c to exit')
  
  # set up animation
  fig = plt.figure()
  ax = plt.axes(xlim=(0, xmax), ylim=(0, ymax))
  a = [ax.plot([],[])[0] for i in range(numSignals)]
  anim = animation.FuncAnimation(fig, analogPlot.update, 
                                 fargs=tuple(a), 
                                 interval=50)
 
  # axis labels
  plt.ylabel('Signals')
  plt.xlabel('# samples from now')
  plt.title('Live Plot')
  plt.grid()
  # show plot
  plt.show()
  
  # clean up
  analogPlot.close()
 
  print('exiting.')
  
 
# call main
if __name__ == '__main__':
  main()
  