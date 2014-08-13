import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def dump_to_csv(filename, lst):
    resultFile = open(filename,'w', newline='')
    wr = csv.writer(resultFile, dialect='excel')
    for x in lst:
        wr.writerow([x])


def hex_to_uint16(str):
    rev_string = swap_bytes_uint16(str)
    return int(rev_string, 16)


def swap_bytes_uint16(str):
    firstbyte, secondbyte = str[:2], str[2:]
    return secondbyte + firstbyte

# Parses out binary data based on custom delimiter
def parse_blob(str, **kwargs):
    delimiter = kwargs.get('delimiter')
    max_val = kwargs.get('max_val')
    if delimiter is None or max_val is None:
        raise ValueError('Need to specify delimiter and max_val')
    seperated_list = str.split(delimiter)
    clean_list = [x for x in seperated_list if x]
    data = [hex_to_uint16(x) for x in clean_list]
    cleaned_data = [x for x in data if x < max_val]
    return cleaned_data


def plot_data():
    colnames = ['time', 'tick', 'highline', 'lowline', 'diffline', 'rawadc']
    data = pd.read_csv('../../../Users/ddevaz/Desktop/8-12-2014-MotionSensorCapture.csv',
           names=colnames,
           sep=' ')


    # Create plot
    sample_time = 50.0/1000 # s
    motion_threshold_value = 621
    t1 = [i*sample_time/60 for i,x in enumerate(data.tick)]
    threshhold_line = [motion_threshold_value for i in t1]
    lines = plt.plot(t1, data.diffline,   'b.--', 
                     t1, threshhold_line, 'r--')

    # configure plot
    plt.ylabel('Highline - Lowline (ADC counts)')
    plt.xlabel('Minutes from ' + data.time[0])
    plt.text(50, motion_threshold_value+20, 'Threshold = 621 counts', color='r')
    plt.title('Motion Sensor Output')
    plt.axis([0,950,0,4096])
    # plt.setp(lines, ms=1)
    plt.show()


    # FFT
    # dat = data.diffline
    # ps = np.abs(np.fft.fft(dat))**2
    # time_step = 0.05
    # freqs = np.fft.fftfreq(dat.size, time_step)
    # idx = np.argsort(freqs)
    # plt.plot(freqs[idx], ps[idx])
    # plt.axis([-5,5, 0,1.5e11])
    # plt.show()

if __name__ == '__main__':
    print(plot_data())