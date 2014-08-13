#!/usr/bin/env python
"""
serial_plotter.py
 
Display serial data as scrolling plot.

"""
 
import sys, serial, argparse
# import numpy as np
# from time import sleep
from collections import deque
 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
 

# plot class
class AnalogPlot:
  # constr
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
 
  # add data
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
      self.ser.flush()
      self.ser.close()    
 


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


# main() function
def main():
  # create parser
  parser = argparse.ArgumentParser(description="Live Serial Plotter. Plots data coming in on the serial port. Variables should be floats or integers seperated by spaces and terminated by a newline \\n, eg. 1023.6 28 126")
  # add expected arguments
  parser.add_argument('-p', '--port',  required=False, default='COM1', help="COM port to use. Defaults to 'COM1' eg. --port 'COM1'.")
  parser.add_argument('-b', '--baud',  type=int, required=False, help="Baudrate in bits per second. Default is 115200.")
  parser.add_argument('-s', '--signals', type=int, nargs='+', required=False, help="Indeces of signals to plot seperated by spaces. Zero indexed. eg. To plot the 1st and 3rd variables: --signals 0 2")
  parser.add_argument('--xmax',  type=int, required=False)
  parser.add_argument('--ymax',  type=int, required=False)
  parser.add_argument('-l', '--list', action='store_true', required=False, help='Lists available ports')
  # parse args
  args = parser.parse_args()

  if (args.list):
    print(list_serial_ports())
    return

  # required args
  strPort = args.port

  # optional args
  baud = args.baud if args.baud else 115200
  xmax = args.xmax if args.xmax else 500
  ymax = args.ymax if args.ymax else 5000

  # Configure number of signals.
  if (args.signals):
    indeces = args.signals
    numSignals = len(indeces)
  else:
    numSignals = len(serial.Serial(strPort, baud).readline().split())
    indeces = list(range(numSignals))
 
  print('reading from serial port %s...' % strPort)
 
  # plot parameters
  analogPlot = AnalogPlot(strPort, baud, xmax, indeces)
 
  print('plotting signals %s...' % indeces)
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
  # show plot
  plt.show()
  
  # clean up
  analogPlot.close()
 
  print('exiting.')
  
 
# call main
if __name__ == '__main__':
  main()