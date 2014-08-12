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
 
numXPoints = 500
numYPoints = 5000 

# plot class
class AnalogPlot:
  # constr
  def __init__(self, strPort, baud, maxLen, numSignals):
      # open serial port
      self.ser = serial.Serial(strPort, baud)
      self.numSignals = numSignals
      # signals
      self.a = [deque([0.0]*maxLen) for i in range(self.numSignals)]
      self.maxLen = maxLen
      self.indeces = []
 
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
 
# main() function
def main():
  # create parser
  parser = argparse.ArgumentParser(description="LDR serial")
  # add expected arguments
  parser.add_argument('--port', dest='port', required=True)
  parser.add_argument('--baud', dest='baud', required=False)
  parser.add_argument('--signals', dest='signals', required=False)
  # parse args
  args = parser.parse_args()
  
  # required args
  strPort = args.port

  # optional args
  if args.signals:
    strSignals = args.signals
  if args.baud:
    baud = int(args.baud)
  else:
    baud = 115200

  # Configure number of signals.
  if (args.signals):
    indeces = strSignals.split(',')
    indeces = [int(x) for x in indeces]
    numSignals = len(indeces)
  else:
    numSignals = len(serial.Serial(strPort, baud).readline().split())
    indeces = list(range(numSignals))
 
  print('reading from serial port %s...' % strPort)
 
  # plot parameters
  analogPlot = AnalogPlot(strPort, baud, numXPoints, numSignals)
  analogPlot.numSignals = numSignals
  analogPlot.indeces = indeces
 
  print('plotting data...')
  # set up animation
  fig = plt.figure()
  ax = plt.axes(xlim=(0, numXPoints), ylim=(0, numYPoints))
  a = [ax.plot([],[])[0] for i in range(numSignals)]

  anim = animation.FuncAnimation(fig, analogPlot.update, 
                                 fargs=tuple(a), 
                                 interval=50)
 
  # axis labels
  plt.ylabel('Signals')
  plt.xlabel('# samples from now')
  
  # show plot
  plt.show()
  
  # clean up
  analogPlot.close()
 
  print('exiting.')
  
 
# call main
if __name__ == '__main__':
  main()