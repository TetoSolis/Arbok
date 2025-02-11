from Phidget22.Phidget import *
from Phidget22.Devices.DigitalOutput import *
import time

def main():
    serial_number = 369498  # Numro de srie du module Phidget
    num_outputs = 8  # Nombre total de sorties (modifier selon votre module)

    # Cration d'une liste pour stocker les objets DigitalOutput
    digitalOutputs = [DigitalOutput() for _ in range(num_outputs)]

    # Configuration des sorties
    for i, output in enumerate(digitalOutputs):
        output.setDeviceSerialNumber(serial_number)
        output.setChannel(i)  # Dfinit le numro de la sortie (0, 1, 2, 3...)
        output.openWaitForAttachment(5000)

    try:
        # Activation des sorties une par une
        for i, output in enumerate(digitalOutputs):
            print(f"Activation de la sortie {i}")
            output.setDutyCycle(1)  # Allume la sortie
            time.sleep(1)  # Attend 1 seconde
            output.setDutyCycle(0)  # teint la sortie

    except (Exception, KeyboardInterrupt):
        pass

    # Fermeture des connexions
    for output in digitalOutputs:
        output.close()

    print("Programme termin.")

# Excution du programme
main()

