from Phidget22.Phidget import *
from Phidget22.Devices.DigitalOutput import *
import time

def main():
	digitalOutput0 = DigitalOutput()

	digitalOutput0.setDeviceSerialNumber(317286)

	digitalOutput0.openWaitForAttachment(5000)

	digitalOutput0.setDutyCycle(1)

	try:
		input("Press Enter to Stop\n")
	except (Exception, KeyboardInterrupt):
		pass

	digitalOutput0.close()

main()
