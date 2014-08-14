import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np



def plot_data():
    colnames = ['time','tick', 'highline', 'lowline', 'diffline', 'rawadc']
    # '../../../Users/ddevaz/Desktop/8-12-2014-MotionSensorCapture.csv'
    data = pd.read_csv('../../../Users/ddevaz/Desktop/8-12-2014-MotionSensorCapture.csv',
           names=colnames,
           sep=' ')

    # Create plot
    sample_time = 50.0/1000.0 # s
    motion_threshold_value = 621
    t1 = [i*sample_time/60 for i,x in enumerate(data.tick)]
    t = np.linspace(0,len(data.tick)*sample_time/60,len(data.tick))
    threshhold_line = [motion_threshold_value for i in t1]
    lines = plt.plot(t, data.rawadc,   'b.--')

    # configure plot
    plt.ylabel('(ADC counts)')
    plt.xlabel('Minutes from ' + data.time[0])
    plt.text(50, motion_threshold_value+20, 'Threshold = 621 counts', color='r')
    plt.title('Motion Sensor Output')
   # plt.axis([0,t1[-1],0,4096])
    # plt.setp(lines, ms=1)
    plt.show()


    #FFT
    # dat = data.rawadc
    # ps = np.abs(np.fft.fft(dat))**2
    # time_step = sample_time
    # freqs = np.fft.fftfreq(dat.size, time_step)
    # idx = np.argsort(freqs)
    # plt.plot(freqs[idx], ps[idx])
    # plt.axis([-5,5, 0,max(ps)])
    # plt.show()

if __name__ == '__main__':
    print(plot_data())