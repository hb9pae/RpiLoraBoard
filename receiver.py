import os, sys
import pdb
import hexdump

currentdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(currentdir)))
from LoRaRF import SX127x
import time

# Begin LoRa radio and set NSS, reset, busy, IRQ, txen, and rxen pin with connected Raspberry Pi gpio pins
# IRQ pin not used in this example (set to -1). Set txen and rxen pin to -1 if RF module doesn't have one
#
busId = 0
csId = 0
spiSpeed = 100000

resetPin = 6; irqPin = -1; txenPin = -1; rxenPin = -1

# Header type
HEADER_EXPLICIT                        = 0x00        # explicit header mode
HEADER_IMPLICIT                        = 0x01        # implicit header mode

#LoRa Parameter
__bw = 125000		#Bandwith
__cr = 5  # 4/5		#Coding Rate
__sf = 12		#Spreading Factor
__hdtype = HEADER_EXPLICIT		#explicit Header
__rxfreq = 433775000	# RX Frequency
__prelng = 12		# Preamble lenght
__paylng = 0x80		# payload lenght
__crc = True		# CRC enable
__invertiq = False
__ldro = False

def readRegs() :
        buffer = [] 
        i = 0
        while  i <= 256 :
                val = LoRa.readRegister(i)
                i +=1
                buffer.append(val)
        hexdump.hexdump(bytes(buffer))

LoRa = SX127x()
print("Begin LoRa radio")
if not LoRa.begin(busId, csId, resetPin, irqPin, txenPin, rxenPin) :
    raise Exception("Something wrong, can't begin LoRa radio")

# Set Standby
print("Set Standby Mode ")
LoRa.standby()

# Set Modem 
print("Set Modem ", LoRa.LORA_MODEM)
LoRa.setModem(LoRa.LORA_MODEM)

# Set frequency 
print("Set frequency ", __rxfreq )
LoRa.setFrequency(__rxfreq)

# Set RX gain. RX gain option are power saving gain or boosted gain
print("Set RX gain to power saving gain")
LoRa.setRxGain(LoRa.RX_GAIN_POWER_SAVING, LoRa.RX_GAIN_AUTO)    # AGC on, Power saving gain

# Configure modulation parameter including spreading factor (SF), bandwidth (BW), and coding rate (CR)
# Receiver must have same SF and BW setting with transmitter to be able setLoRaModulation(self, sf: int, bw: int, cr: int, ldro: bool = False) :to receive LoRa packet

print("Set Modulation parameters")
print("... Set Spreading Factor ", __sf ) 
print("... Set Bandwithr ", __bw ) 
print("... Set Code Rate ", __cr )
print("... Set LDRO Enable ", __ldro ) 
LoRa.setLoRaModulation(__sf, __bw, __cr, __ldro) 

# Configure packet parameter including header type, preamble length, payload length, and CRC type
# The explicit packet includes header contain CR, number of byte, and CRC type
# Receiver can receive packet with different CR and packet parameters in explicit header mode

print("Set LoRaPacket")
LoRa.setLoRaPacket(__hdtype, __prelng, __paylng, __crc, __invertiq)
print("... Set HEADER_EXPLICIT", ) 
print("... Set Preamb. Length ", __prelng)
print("... Set Payload Lenght ", __paylng)                                      # Set preamble length to 12
print("... Set CRC enable ", __crc)
print("... Set Invert IRQ ", __invertiq)

# Set syncronize word for public network (0x34)
print("Set syncronize word to 0x34")
LoRa.setSyncWord(0x12)

#pdb.set_trace()

print("-- Read Registers --")
readRegs()

print("Reset RX-Buffer")
LoRa.beginPacket() 

print("-- LoRa Receiver ready--")
# Receive message continuously

while True :
	# Request for receiving new LoRa packet
	LoRa.request()
	# Wait for incoming LoRa packet
	LoRa.wait()

    	# Put received packet to message and counter variable
    	# read() and available() method must be called after request() or listen() method
	message = []

    	# available() method return remaining received payload length and will decrement each read() or get() method called
	while LoRa.available() > 1 :
			message += LoRa.get()
	counter = LoRa.read()
	hexdump.hexdump(bytes(message))

#	print("-- Read Registers --")
#	readRegs()
# 	print("--------------------")
#	pdb.set_trace()

	# Print received message and counter in serial
	#print(f"{counter}")
	print("Received Message (UTF-8)")
	print(f"Counter: {counter} Bytes")
	print(" Message: ", len(message))

# Print packet/signal status including RSSI, SNR, and signalRSSI
	print("Packet status: RSSI = {0:0.2f} dBm | SNR = {1:0.2f} dB".format(LoRa.packetRssi(), LoRa.snr()))

# Show received status in case CRC or header error occur
	status = LoRa.status()
	if status == LoRa.STATUS_CRC_ERR : print("CRC error")
	elif status == LoRa.STATUS_HEADER_ERR : print("Packet header error")
