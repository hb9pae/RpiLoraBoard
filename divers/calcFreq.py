

'''
   // set frequency
    //@APA 434.400.000 = 0x6c 99 99  = 108, 153, 153
    //@APA 433.650.000 = 0x6c 69 99  = 108, 105, 153
    //    
    uint64_t frf = ((uint64_t)m_freq << 19) / 32000000;
    writeRegister(REG_FRF_MSB, (uint8_t)(frf>>16) );
    writeRegister(REG_FRF_MID, (uint8_t)(frf>> 8) );
    writeRegister(REG_FRF_LSB, (uint8_t)(frf>> 0) );
    //DebugPrint
    byte freq_MSB = readRegister(REG_FRF_MSB);
    byte freq_MID = readRegister(REG_FRF_MID);
    byte freq_LSB = readRegister(REG_FRF_LSB);
    printf("Freq is  %#04x  %#04x  %#04x \n", freq_MSB,freq_MID,freq_LSB);

'''
#RxFreq = 434400000



RX = 434400000
a = int (RX<<19)
b = int (a/32000000)

MSB = b>>16
MID = b>>8
LSB = b>>0


print(" MSB: %d, MID: %d, LSB: %d", MSB, MID, LSB)
print("RX Freq is  %#04x  %#04x  %#04x \n", hex(MSB), hex(MID), hex(LSB) )

