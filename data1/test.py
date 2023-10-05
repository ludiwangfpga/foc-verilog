from pynq import Overlay
import numpy as np
import time

# Assuming that the bit file and the convert_to_signed function are correctly loaded
overlay = Overlay('foc249.bit')

def convert_to_signed(unsigned_value, bit_width):
    # Assuming this function is correctly defined
    pass

# Defining bit width, replace with the correct bit width value
bit_width = 32

def compute():
    add_ip.write(0x00, 0x01)  # 0 uq
    add_ip.write(0x04, 0x00)  # 1 uq
    add_ip.write(0x08, 0x01)  # 2 angle
    data_unsigned0 = add_ip.read(0x10)
    data_unsigned1 = add_ip.read(0x14)
    data_unsigned2 = add_ip.read(0x18)
    data_unsigned3 = add_ip.read(0x1c)
    data_unsigned4 = add_ip.read(0x20)
    data_unsigned5 = add_ip.read(0x24)
    data_unsigned6 = add_ip.read(0x28)
    data_unsigned7 = add_ip.read(0x2c)
    data_unsigned8 = add_ip.read(0x30)
    data_unsigned9 = add_ip.read(0x34)
    data_unsigned10 = add_ip.read(0x38)
    data_unsigned11 = add_ip.read(0x3c)

    data_signed0 = convert_to_signed(data_unsigned0, bit_width)
    data_signed1 = convert_to_signed(data_unsigned1, bit_width)
    data_signed2 = convert_to_signed(data_unsigned2, bit_width)
    data_signed3 = convert_to_signed(data_unsigned3, bit_width)
    data_signed4 = convert_to_signed(data_unsigned4, bit_width)
    data_signed5 = convert_to_signed(data_unsigned5, bit_width)
    data_signed6 = convert_to_signed(data_unsigned6, bit_width)
    data_signed7 = convert_to_signed(data_unsigned7, bit_width)
    data_signed8 = convert_to_signed(data_unsigned8, bit_width)
    data_signed9 = convert_to_signed(data_unsigned9, bit_width)
    data_signed10 = convert_to_signed(data_unsigned10, bit_width)
    data_signed11 = convert_to_signed(data_unsigned11, bit_width)
    # print(f" cs2: {data_signed10} degrees")
    # print(f" cs3: {data_signed11} degrees")

start_time = time.time()
end_time = start_time + 1  # 1 second later
iterations = 0

while time.time() < end_time:
    compute()
    iterations += 1

print(f"Number of computations in 1 second: {iterations}")
