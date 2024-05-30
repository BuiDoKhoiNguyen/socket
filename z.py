byte_string = b'Ud\xef\xff'
integer_value = int.from_bytes(byte_string, byteorder='little', signed=False)
print("Integer value:", integer_value)
number = -2**32 - 1
byte_string = number.to_bytes(4, byteorder='big', signed=True)
print(byte_string)