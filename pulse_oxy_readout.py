# Scott Norton and Daniel Hull
# Baebies NC May 20, 2016
# pulse_oxy_readout_v1

'''
    Function: This code will eventually take a continuous stream of data
    from the RS-232 microcontroller provided by ITEC Engineering LLC.
    This code will interpret the UNICODE data output from the microcontroller
    according to the Communication Protocol given by ITEC Engineering LLC
'''

'''
    The code provided follows a clear format
    1) Definition functions SPO2, Signal_strength, Flags, Pulse_Rate, Instantaneous_SPO2
    2) Pulse Oxy Readout function
        a) verifies data 
'''
# four_byte_data = [130, 50, 4, 127]

# If Address is Zero
def SPO2_invalid():
    print("SPO2 level is invalid")

# If Address is One
def Pulse_Rate (byte_two, byte_three):
    PR_mask = int('0b01000000',2)
    sig_bit = PR_mask&byte_two
    if sig_bit == 0:
        Pulse = byte_three
    else:
        Pulse = byte_three+128
    print "The Pulse Rate is %d" %byte_three
    return(Pulse)

# If Address is Two
def Signal_strength((byte_three)): 
    print "The Signal Strength is %d" %byte_three
    return byte_three
     
# If Address is Three 
def Flags(byte_three):
    print(FLAGS[byte_three])
   
# If Address is Four
def Instantaneous_SPO2(byte_three):
    print "Instantaneous_SPO2 is %d" %byte_three
    return byte_three

# If Address is Five
def Red_gain_index(byte_three):
    print "Red gain index is %d" %byte_three
    return byte_three

# If Address is Six  
def Infrared_gain_index(byte_three):
    print "The Infrared_gain_index is %d" %byte_three
    return byte_three

# Plesmythograph isolation
def plesmythograph_data(byte_one):
    print "The plesmythograph value is %d" %byte_one
    return byte_one

# Bar graph sifting
def bar_graph_sifting(byte_two):
    mask_b2 = int('0b00001111',2)
    bar_graph_bits = byte_two&mask_b2
    print "bar_graph_bit value is %d" %bar_graph_bits
    
def slow_data_address(byte_zero):
    mask = int("0b00001110",2)
    slow_data_address_out_of_place = byte_zero&mask
    slow_data_address_val = slow_data_address_out_of_place>>1 
    print "the slow data address is %d" % slow_data_address_val
    return slow_data_address_val
    
# Main Body function
def pulse_oxy_readout(four_byte_data): 

    if len(four_byte_data) == 4 and four_byte_data[0]>127:
        NO_ALERTS = 0 ; SENSOR_UNPLUGGED = 1 ; NO_FINGER_DETACHED = 2 ; SEARCHING = 3;
        SEARCHING_TOO_LONG = 4 ; LOST_PULSE = 5 ; ARTIFACT = 6;

        FLAGS = {NO_ALERTS: 'No alerts', SENSOR_UNPLUGGED: 'sensor Unplugged', 
        NO_FINGER_DETACHED: 'No finger in sensor', SEARCHING: 'Searching...', 
        SEARCHING_TOO_LONG: 'Searching too long...', LOST_PULSE: 'Lost pulse',
        ARTIFACT: 'Artifact'}
        
        binary_representation =[bin(b) for b in four_byte_data]
        
        # byte zero data
        address = slow_data_address(four_byte_data[0])
        
        # byte one data
        plesmythograph_data(four_byte_data[1])
        
        # byte two data
        bar_graph_sifting(four_byte_data[2])
        
        # byte_three data
        if address == 0:
            SPO2_invalid()
        elif address == 1:
            Pulse_Rate(four_byte_data[2], four_byte_data[3])
        elif address == 2:
            Signal_strength(four_byte_data[3])
        elif address == 3:
            FLAGS(four_byte_data[3])
        elif address == 4:
            Instantaneous_SPO2(four_byte_data[3])
        elif address == 5:
            Red_gain_index(four_byte_data[3])
        elif address == 6:
            Infrared_gain_index(four_byte_data[3])
    else:
        print("length is not four or byte zero isn't greater than 127")
        raise

    
