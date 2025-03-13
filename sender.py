import can
import time

bus = can.interface.Bus(interface='socketcand', host="172.16.4.106", port=29536, channel="can1")
 
message_id1=0x125 #Vehicle Speed
message_id2=0x128 #RPM
message_id3=0x131 #Speed Limit
message_id4=0x132 #ACC
message_id5=0x133 #weather Condition
message_id6=0x134 #LDW
message_id7=0x135 #PRND
message_id8=0x136 #TEMP
message_id9=0x138 #INC_TEMP
message_id10=0x139 #DEC_TEMP
message_id12=0x140 #AC_ON_OFF
message_id13=0x141 #Heater_ON_OFF





def pack_int_into_8B_array(data: int):
    data = data.to_bytes(1, byteorder="little")
    can_data = bytearray(1)
    can_data[:len(data)] = data
    return can_data
    
def position_and_temp(position: int, temp: int):
    can_data = bytearray(2)
    can_data[0] = position
    can_data[1] = temp #In faranheit upto 255
    return can_data

 
def send_can_message(message_id, data):
    msg = can.Message(arbitration_id=message_id, data=data, is_extended_id=False)
    bus.send(msg)
    print(msg)

"""
# loop until Ctrl-C
try:
  while True:
    #send_can_message(message_id1,pack_int_into_8B_array(100))#Vehicle Speed
    #time.sleep(1)
    #send_can_message(message_id2,pack_int_into_8B_array(8000)) #RPM
    #time.sleep(1)
    #send_can_message(message_id5,weather_and_temp(2,100)) #Weather and  Temperature
    #time.sleep(1)
    #send_can_message(message_id3,pack_int_into_8B_array(60)) #Speed Limit
    #time.sleep(1)
    #send_can_message(message_id4,pack_int_into_8B_array(1)) #ACC
    #time.sleep(1)
    #send_can_message(message_id6,pack_int_into_8B_array(1)) #LDW
    #time.sleep(1)
    #send_can_message(message_id7,pack_int_into_8B_array(1)) #PRND
    #time.sleep(1)
    send_can_message(message_id8,temp_and_degree(2,100)) #Weather and  Temperature
    time.sleep(1)
    send_can_message(message_id9,pack_int_into_8B_array(1)) #INC_TEMP
    time.sleep(1)
    send_can_message(message_id10,pack_int_into_8B_array(1)) #DEC_TEMP
    time.sleep(1)
    send_can_message(message_id11,pack_int_into_8B_array(1)) #AC_ON
    time.sleep(1)
    send_can_message(message_id12,pack_int_into_8B_array(0)) #AC_OFF
    time.sleep(1)
	send_can_message(message_id13,pack_int_into_8B_array(1)) #Heater_ON
    time.sleep(1)
    send_can_message(message_id14,pack_int_into_8B_array(0)) #Heater_OFF
    time.sleep(1)
	

  
except KeyboardInterrupt:
  pass
"""
