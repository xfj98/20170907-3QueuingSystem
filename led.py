#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import serial
import array



##before officially start writing the message, clear the memory first
def send_message(message):

    #print(message)

    ser = serial.Serial('com12',57600)

    temp = []
    mes = list(message)
    #print(len(mes))
    for i in range(0,len(mes)):
        mes[i] = mes[i].encode('gb2312')
        if len(mes[i]) > 1:
           temp.append(int(mes[i][0]))
           temp.append(int(mes[i][1]))
        else:
            temp.append(int(mes[i][0]))
        
    length1 = len(temp)
    #print(length1)
    
    length2 = length1 + 27
    length3 = length2 + 31
    length4 = length3
    length5 = length3 + 18
    length0 = length3
       
    
    
    ##开始写文件的指令，先清除历史记录

    
    first_part = ([0xA5,0xA5,0xA5,0xA5,0xA5,0xA5,0xA5,0xA5])
    first_part2 = ([0x01,0x00,0x00,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0xFE,0x02,0x0E,0x00,0xA1,0x05,0x01,
    0x00,0x00,0x01,0x50,0x30,0x30,0x30])


    #length0 = length + 58
    binary_len0 = array.array('i',[length0]).tostring()
    lenList0 = list(binary_len0)
    file_len = (lenList0)
    
   
    #file_len = ([0x4D,0x00,0x00,0x00])
    from test import crc16
    
    crc = crc16()

    cal_crc = (first_part2 + file_len)

    crc_code = crc.createarray(cal_crc)

    #crc_code = ([0xE3,0x26])

    the_end = ([0x5A])

    testAll = crc_code
   
   
    pre_send = first_part+ testAll +the_end
    
    send1 = ser.write(pre_send)
    
   
    time.sleep(1)
     
   
    ##帧头和包头数据

    
    head0_start = ([0xA5,0xA5,0xA5,0xA5,0xA5,0xA5,0xA5,0xA5]) 
    head1_start = ([0x01,0x00,0x00,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0xFE,0x02]) #（一定）

    #length2 = length3 + 18
    
    binary_len5 = array.array('H',[length5]).tostring()
    lenList5 = list(binary_len5)
    content_len = (lenList5)
    
   
    #content_len = ([0x5F,0x00])

   
    head2_start = ([0xA1,0x06,0x01,0x00,0x00,0x50,0x30,0x30,0x30,0x01,0x00,0x00]) #（一定）

    #length3 = length + 58
    binary_len4 = array.array('H',[length4]).tostring()
    lenList4 = list(binary_len4)
    file_len2 = (lenList4)
    #file_len2 = ([0x4D,0x00])
    
    after_len = ([0x00,0x00,0x00,0x00])



    ##区数据格式

    
    file1_start = ([0x00,0x50,0x30,0x30,0x30])
    
    binaryLen3 = array.array('i',[length3]).tostring()
    lenList3 = list(binaryLen3)
    
    file_len3 = (lenList3)
   
    #file_len3 = [0x4D,0x00,0x00,0x00]

    
    file1_middle = ([0xFF,0x00,0x00,0x01,0xFF,0xFF,0x01,0x24,0x14,0x20,0x01,0x24,0xFF,0x00,0x00,0x01]) 

    #length4 = length + 27
    binary_len2 = array.array('i',[length2]).tostring()
    lenList2 = list(binary_len2)
    
    areaDataLen = (lenList2)
    

    #areaDataLen = [0x2E,0x00,0x00,0x00]
    areaType = ([0x00])
    file2_start = ([0x00,0x00,0x00,0x00,0x08,0x00,0x20,0x00,0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                    0x02,0x02,0x01,0x00,0x00,0x0A])

    binary_len1 = array.array('i',[length1]).tostring()
    lenList1 = list(binary_len1)
    
    data_len = (lenList1)
    
    
    #data_len = [0x13,0x00,0x00,0x00]
    

    ##字符串信息

    messageInList = temp
    
    #messageInList = [0x5C,0x43,0x32,0xD6,0xD0,0xBA,0xBD,0xB9,0xA4,0xD2,0xB5,0xCF,0xE8,0xD1,0xB8,0xBF,0xC6,0xBC,0xBC]
    

    ##校验码

    
    comprehensive1 = (file1_start + file_len3 + file1_middle + areaDataLen + areaType
    + file2_start + data_len + messageInList)

    #for i in range(0,len(comprehensive1)):
        #print('%02x '%(comprehensive1[i]),end = '')
    
   
       
    new_comprehensive1 = crc.createarray(comprehensive1)
    
    #for i in range(0,len(new_comprehensive1)):
        #print('%02x '%(new_comprehensive1[i]),end = '')
    

    new_all = (head1_start + content_len + head2_start + file_len2 + after_len + new_comprehensive1)

    #print('\n')

    new_comprehensive2 = crc.createarray(new_all)

    #for i in range(0,len(new_comprehensive2)):
        #print('%02x '%(new_comprehensive2[i]),end = '')


    #chk = [0x95,0x7B]
    #crc = [0xF1,0xBD]
    end_file = ([0x5A])
    
    allContent= (head0_start + new_comprehensive2+ end_file)
    #for i in range(0,len(allContent)):
        #print('%02x '%(allContent[i]),end = '')
    send2 = ser.write(allContent)
    send3 = ser.write(allContent)
    

