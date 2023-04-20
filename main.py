from heartrate_monitor import HeartRateMonitor
import time
import argparse
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="Read and print data from MAX30102")
parser.add_argument("-r", "--raw", action="store_true",
                    help="print raw data instead of calculation result")
parser.add_argument("-t", "--time", type=int, default=60,
                    help="duration in seconds to read from sensor, default 30")
args = parser.parse_args()

print('sensor starting...')
hrm = HeartRateMonitor(print_raw=args.raw, print_result=(not args.raw))
hrm.start_sensor()
try:
    time.sleep(args.time)
except KeyboardInterrupt:
    print('keyboard interrupt detected, exiting...')
    


hrm.stop_sensor()
print('sensor stopped!')

# ir=hrm.returnIrArray()
# red=hrm.returnRedArray()
# bpms=hrm.returnBPMArray()
# oxygen_data = hrm.returnOxygenArray()
#figure, axis = plt.subplots(1,2)
# plt.subplot(221)
# plt.plot(ir)
# plt.title("IR absorption (nm) vs poll number")
# plt.subplot(222)
# plt.plot(red)
# plt.title("Red absorption (nm) vs poll number")
# plt.subplot(223)
# plt.plot(bpms)
# plt.title("bpm")
# plt.subplot(224)
# plt.plot(oxygen_data)
# plt.title("Oxygen")
# plt.show()
# #axis = plt.subplots(1,2)
# #axis[0,1].plot(red)
# #plt.show()






