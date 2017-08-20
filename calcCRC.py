import binascii

def calcCRC(cmnd):
    # cmnd is a byte array containing the command ASCII string; example: cmnd="Sinv2.000"
    # an unsigned 32 bit integer is returned to the calling program
    # only the lower 16 bits contain the crc

    crc = 0xffff # initialize crc to hex value 0xffff
    
    for character in cmnd: # this for loop starts with ASCCII 'S' and loops through to the last ASCII '0'
        hex_char = (int(ord(character)))
        #hex_char = character
        crc=crc^(hex_char*0x0100) # the ASCII value is times by 0x0100 first then XORED to the current crc value
        #for(j=0; j<8; j++) # the crc is hashed 8 times with this for loop
        j = 0
        for j in range(0,8):
            # if the 15th bit is set (tested by ANDING with hex 0x8000 and testing for 0x8000 result) 
            # then crc is shifted left one bit (same as times 2) XORED with hex 0x1021 and ANDED to 
            # hex 0xffff to limit the crc to lower 16 bits. If the 15th bit is not set then the crc 
            # is shifted left one bit and ANDED with hex 0xffff to limit the crc to lower 16 bits.
            if((crc&0x8000)==0x8000):
                crc=((crc<<1)^0x1021)&0xffff
            else:
                crc=(crc<<1)&0xffff
            # end of j loop
        # end of i loop
    # There are some crc values that are not allowed, 0x00 and 0x0d

    # These are byte values so the high byte and the low byte of the crc must be checked and incremented if 
        # the bytes are either 0x00 0r 0x0d
    if((crc&0xff00)==0x0d00):
        crc +=0x0100
    if((crc&0x00ff)==0x000d):
        crc +=0x0001
    if((crc&0xff00)==0x0000):
        crc +=0x0100
    if((crc&0x00ff)==0x0000):
        crc +=0x0001

    crc_hex_string = str(hex(crc))
    if len(crc_hex_string) < 6:
        crc_hex_string_final = crc_hex_string[:2] + '0' + crc_hex_string[2:]
    else:
        crc_hex_string_final = crc_hex_string
    first_byte = crc_hex_string_final[2:4]
    second_byte = crc_hex_string_final[4:6]
    final = binascii.unhexlify(first_byte + second_byte)

    #return(final)
    return(final)

    # If the string Sinv2.000 is sent through this routine the crc = 0x8f55
    # The complete command "Sinv2.000" will look like this in hex: 
        # 0x53 0x69 0x6E 0x76 0x32 0x2e 0x30 0x30 0x30 0x8f 0x55 0x0d