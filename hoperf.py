#!/usr/bin/python3


import wiringpi
import spidev
import time
import pdb

#pdb.set_trace()

# http://wiringpi.com/reference/core-functions/
# https://github.com/WiringPi/WiringPi-Python


# SX127X LoRa Mode Register Map
REG_FIFO                               = 0x00
REG_OP_MODE                            = 0x01
REG_FRF_MSB                            = 0x06
REG_FRF_MID                            = 0x07
REG_FRF_LSB                            = 0x08
REG_PA_CONFIG                          = 0x09
REG_PA_RAMP                            = 0x0A
REG_OCP                                = 0x0B
REG_LNA                                = 0x0C
REG_FIFO_ADDR_PTR                      = 0x0D
REG_FIFO_TX_BASE_ADDR                  = 0x0E
REG_FIFO_RX_BASE_ADDR                  = 0x0F
REG_FIFO_RX_CURRENT_ADDR               = 0x10
REG_IRQ_FLAGS_MASK                     = 0x11
REG_IRQ_FLAGS                          = 0x12
REG_RX_NB_BYTES                        = 0x13
REG_RX_HEADR_CNT_VALUE_MSB             = 0x14
REG_RX_HEADR_CNT_VALUE_LSB             = 0x15
REG_RX_PKT_CNT_VALUE_MSB               = 0x16
REG_RX_PKT_CNT_VALUE_LSB               = 0x17
REG_MODEB_STAT                         = 0x18
REG_PKT_SNR_VALUE                      = 0x19
REG_PKT_RSSI_VALUE                     = 0x1A
REG_RSSI_VALUE                         = 0x1B
REG_HOP_CHANNEL                        = 0x1C
REG_MODEM_CONFIG_1                     = 0x1D
REG_MODEM_CONFIG_2                     = 0x1E
REG_SYMB_TIMEOUT_LSB                   = 0x1F
REG_PREAMBLE_MSB                       = 0x20
REG_PREAMBLE_LSB                       = 0x21
REG_PAYLOAD_LENGTH                     = 0x22
REG_MAX_PAYLOAD_LENGTH                 = 0x23
REG_HOP_PERIOD                         = 0x24
REG_FIFO_RX_BYTE_ADDR                  = 0x25
REG_MODEM_CONFIG_3                     = 0x26
REG_FREQ_ERROR_MSB                     = 0x28
REG_FREQ_ERROR_MID                     = 0x29
REG_FREQ_ERROR_LSB                     = 0x2A
REG_RSSI_WIDEBAND                      = 0x2C
REG_FREQ1                              = 0x2F
REG_FREQ2                              = 0x30
REG_DETECTION_OPTIMIZE                 = 0x31
REG_INVERTIQ                           = 0x33
REG_HIGH_BW_OPTIMIZE_1                 = 0x36
REG_DETECTION_THRESHOLD                = 0x37
REG_SYNC_WORD                          = 0x39
REG_HIGH_BW_OPTIMIZE_2                 = 0x3A
REG_INVERTIQ2                          = 0x3B
REG_DIO_MAPPING_1                      = 0x40
REG_DIO_MAPPING_2                      = 0x41
REG_VERSION                            = 0x42
REG_TCXO                               = 0x4B
REG_PA_DAC                             = 0x4D
REG_FORMER_TEMP                        = 0x5B
REG_AGC_REF                            = 0x61
REG_AGC_THRESH_1                       = 0x62
REG_AGC_THRESH_2                       = 0x63
REG_AGC_THRESH_3                       = 0x64
REG_PLL                                = 0x70

REG_FRF_MSB
REG_FRF_MID
REG_FRF_LSB

    # SPI and GPIO pin setting
_bus = 0
_channel = 0
_cs = 8
_reset = 6
_irq = -1
_txen = -1
_rxen = -1
_spiSpeed = 500000
_txState = 0
_rxState = 0
_did = 5

# Modem options
FSK_MODEM                              = 0x00 # GFSK packet type
LORA_MODEM                             = 0x01 # LoRa packet type
OOK_MODEM                              = 0x02 # OOK packet type

# Header type
HEADER_EXPLICIT                        = 0x00        # explicit header mode
HEADER_IMPLICIT                        = 0x01        # implicit header mode

# LoRa setting
_dio = 1
_modem = LORA_MODEM
_frequency = 434400000
_sf = 7
_bw = 125000
_cr = 5
_ldro = False
_headerType = HEADER_EXPLICIT
_preambleLength = 12
_payloadLength = 32
_crcType = False
_invertIq = False

# Globale Variablen
spi=""


def initGpio() :
	wiringpi.wiringPiSetupGpio()    # GPIO (BCM) numbering
	wiringpi.pinMode(_cs, 1)         # CS as OUTPUT
	wiringpi.pinMode(_did, 0)        # DID as INPUT
	wiringpi.pinMode(_reset, 1)        # RST as OUTPUT

def initSpi():
	global spi
	spi = spidev.SpiDev()
	spi.open(_bus, _channel)
	spi.max_speed_hz = _spiSpeed
	

def resetRFM95() :
	wiringpi.digitalWrite(_reset, 0)
	time.sleep(0.01)
	wiringpi.digitalWrite(_reset, 1)
	time.sleep(0.005)

def setFrequency() :
	# calculate frequency
	frf = int((_frequency << 19) / 32000000)
	#print(hex( (frf >> 16) & 0xFF) )
	#print(hex( (frf >> 8) & 0xFF) )
	#print(hex( frf & 0xFF)  )
	writeRegister( REG_FRF_MSB, ((frf >> 16) & 0xFF))
	writeRegister( REG_FRF_MID, ((frf >> 8) & 0xFF))
	writeRegister( REG_FRF_LSB, (frf & 0xFF))

def writeRegister(address: int, data: int) :
	_transfer(address | 0x80, data)

def readRegister(address: int) ->int:
	return _transfer(address & 0x7F, 0x00)

def _transfer(address: int, data: int) ->int:
	buf = [address, data]
	feedback = spi.xfer2(buf)
	if ( len(feedback) == 2 ) :
		return int(feedback[1])
	return -1

#        self.writeRegister(self.REG_FRF_MSB, (frf >> 16) & 0xFF)
#        self.writeRegister(self.REG_FRF_MID, (frf >> 8) & 0xFF)
#        self.writeRegister(self.REG_FRF_LSB, frf & 0xFF)

def bitwiseAND(bit, mask):
	return( bytes([bit[0] & mask[0]]) )

def selectreceiver():
	wiringpi.digitalWrite(CS, 0)

def unselectreceiver():
	wiringpi.digitalWrite(CS, 1)


if __name__ == "__main__":


	initGpio()
	initSpi()
	resetRFM95()
	Version = readRegister(REG_VERSION)
	print("Version ", hex(Version))
	setFrequency()
	v = readRegister(REG_FRF_MSB)
	print("MSB ", hex(v))
	v = readRegister(REG_FRF_MID)
	print("MID ", hex(v))
	v = readRegister(REG_FRF_LSB)
	print("LSB ", hex(v))
	spi.close()
	print("Done")

