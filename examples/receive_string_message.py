# Author: Renzo Mischianti
# Website: www.mischianti.org
#
# Description:
# This script demonstrates how to use the E220 LoRa module with Orange Pi.
# It includes examples of sending and receiving string using both transparent and fixed transmission modes.
# The code also configures the module's address and channel for fixed transmission mode.
# Address and channel of this receiver:
# ADDH = 0x00
# ADDL = 0x01
# CHAN = 23
#
# Can be used with the send_fixed_string and send_transparent_string scripts
#
# Note: This code was written and tested using Orange Pi on an ESP32 board.
#       It works with other boards, but you may need to change the UART pins.

import serial
import time

from lora_e220 import LoRaE220, Configuration
from lora_e220_operation_constant import ResponseStatusCode

from lora_e220_constants import FixedTransmission, RssiEnableByte

# Initialize the LoRaE220 module
loraSerial = serial.Serial('/dev/ttyS3') #(, baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)

lora = LoRaE220('900T22D', loraSerial, aux_pin='PA7', m0_pin='PA8', m1_pin='PA9')
code = lora.begin()
print(f"Initialization: {ResponseStatusCode.get_description(code)}")

# Set the configuration to default values and print the updated configuration to the console
# Not needed if already configured
configuration_to_set = Configuration('900T22D')
configuration_to_set.ADDH = 0x00 # Address of this receive no sender
configuration_to_set.ADDL = 0x01 # Address of this receive no sender
configuration_to_set.CHAN = 23 # Address of this receive no sender
configuration_to_set.TRANSMISSION_MODE.fixedTransmission = FixedTransmission.FIXED_TRANSMISSION
# To enable RSSI, you must also enable RSSI on sender
configuration_to_set.TRANSMISSION_MODE.enableRSSI = RssiEnableByte.RSSI_ENABLED

code, confSetted = lora.set_configuration(configuration_to_set)
print(f"Set configuration: {ResponseStatusCode.get_description(code)}")

print("Waiting for messages...")
while True:
    if lora.available() > 0:
        # If the sender not set RSSI
        # code, value = lora.receive_message()
        # If the sender set RSSI
        code, value, rssi = lora.receive_message(rssi=True)
        print('RSSI: ', rssi)

        print(ResponseStatusCode.get_description(code))

        print(value)
        time.sleep(2)
