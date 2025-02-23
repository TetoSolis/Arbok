from Phidget22.Phidget import *
from Phidget22.Devices.DigitalOutput import *
import keyboard

# Initialisation des relais
relays = {}
serial_number = 369498  # Remplace par le numéro de série réel

for i in range(8):
    relay = DigitalOutput()
    relay.setDeviceSerialNumber(serial_number)
    relay.setChannel(i)
    relay.openWaitForAttachment(5000)
    relay.setState(False)  # Assure que tous les relais sont éteints au démarrage
    relays[i] = relay

# Stocker l'état des relais
relay_states = {i: False for i in range(8)}

def toggle_relay(num):
    if num in relays:
        relay_states[num] = not relay_states[num]
        relays[num].setState(relay_states[num])
        print(f"Relais {num} {'ON' if relay_states[num] else 'OFF'}")

def passOn(num):
    if num in relays:
        relays[num].setState(True)
        relay_states[num] = True
        print(f"Relais {num} ON")

def passOff(num):
    if num in relays:
        relays[num].setState(False)
        relay_states[num] = False
        print(f"Relais {num} OFF")

# Gestion des entrées clavier
def keyboard_listener():
    while True:
        for i in range(8):
            if keyboard.is_pressed(str(i)):
                toggle_relay(i)
                while keyboard.is_pressed(str(i)):  # Attendre le relâchement de la touche
                    pass

try:
    keyboard_listener()
except KeyboardInterrupt:
    print("Fermeture du programme...")
finally:
    for relay in relays.values():
        relay.setState(False)  # Éteindre tous les relais avant de fermer
        relay.close()
