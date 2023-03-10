import os, sys
import pdb
import hexdump

currentdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(currentdir)))
from LoRaRF import SX127x
import time


# Begin LoRa radio and set NSS, reset, busy, IRQ, txen, and rxen pin with connected Raspberry Pi gpio pins
# IRQ pin not used in this example (set to -1). Set txen and rxen pin to -1 if RF module doesn't have one
busId = 0; csId = 0
resetPin = 6; irqPin = -1; txenPin = -1; rxenPin = -1

LoRa = SX127x()

print("Begin LoRa radio")
if not LoRa.begin(busId, csId, resetPin, irqPin, txenPin, rxenPin) :
    raise Exception("Something wrong, can't begin LoRa radio")

i = 0
buffer = []

while  i <= 256 :
	val = LoRa.readRegister(i)
	i +=1
	buffer.append(val)

print("Readout Registe RfHope RFM96")
hexdump.hexdump(bytearray(buffer))

print("Read done")
exit(0)
pdb.set_trace()

# Set frequency to 433.775 Mhz
print("Set frequency to 433.775 Mhz")
LoRa.setFrequency(433775000)

# Set RX gain. RX gain option are power saving gain or boosted gain
print("Set RX gain to power saving gain")
LoRa.setRxGain(LoRa.RX_GAIN_POWER_SAVING, LoRa.RX_GAIN_AUTO)    # AGC on, Power saving gain

# Configure modulation parameter including spreading factor (SF), bandwidth (BW), and coding rate (CR)
# Receiver must have same SF and BW setting with transmitter to be able to receive LoRa packet
print("Set modulation parameters:\n\tSpreading factor = 7\n\tBandwidth = 125 kHz\n\tCoding rate = 4/5")
LoRa.setSpreadingFactor(12)                                      # LoRa spreading factor: 7
LoRa.setBandwidth(125000)                                       # Bandwidth: 125 kHz
LoRa.setCodeRate(1)                                             # Coding rate: 4/5

# Configure packet parameter including header type, preamble length, payload length, and CRC type
# The explicit packet includes header contain CR, number of byte, and CRC type
# Receiver can receive packet with different CR and packet parameters in explicit header mode
print("Set packet parameters:\n\tExplicit header type\n\tPreamble length = 12\n\tPayload Length = 0x80\n\tCRC ON")
LoRa.setHeaderType(LoRa.HEADER_EXPLICIT)                        # Explicit header mode
LoRa.setPreambleLength(12)                                      # Set preamble length to 12
LoRa.setPayloadLength(0x80)                                       # Initialize payloadLength to 15
LoRa.setCrcEnable(True)                                         # Set CRC enable

# Set syncronize word for public network (0x34)
#print("Set syncronize word to 0x34")
#LoRa.setSyncWord(0x34)

print("\n-- LoRa Receiver --\n")

# Receive message continuously
while True :

    # Request for receiving new LoRa packet
    LoRa.request()
    # Wait for incoming LoRa packet
    LoRa.wait()

    # Put received packet to message and counter variable
    # read() and available() method must be called after request() or listen() method
    message = ""
    # available() method return remaining received payload length and will decrement each read() or get() method called
    while LoRa.available() > 1 :
        message += chr(LoRa.read())
    counter = LoRa.read()

    #pdb.set_trace()
    # Print received message and counter in serial
    #print(f"{counter}")
    b_message = bytes(message,"utf-8")
    hexdump.hexdump(b_message)

    # Print packet/signal status including RSSI, SNR, and signalRSSI
    print("Packet status: RSSI = {0:0.2f} dBm | SNR = {1:0.2f} dB".format(LoRa.packetRssi(), LoRa.snr()))

    # Show received status in case CRC or header error occur
    status = LoRa.status()
    if status == LoRa.STATUS_CRC_ERR : print("CRC error")
    elif status == LoRa.STATUS_HEADER_ERR : print("Packet header error")
