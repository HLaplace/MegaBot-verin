# dataframe.py
from struct import calcsize, pack, unpack

class DataFrame:
    def __init__(self, format_str, s1, s2, P, PWM, crc):
        self.format_str = format_str
        self.s1 = s1
        self.s2 = s2
        self.P = P
        self.PWM = PWM
        self.crc = crc

    def key_size(self):
        return calcsize(self.format_str)

    def frame_data(self):
        packed_data = pack(self.format_str, self.s1, self.s2, self.P, self.PWM, self.crc)
        binary_representation = ''.join(format(byte, '08b') for byte in packed_data)
        print("Suite binaire encadrée : ", binary_representation)
        return packed_data

    def unframe_data(self, value):
        unpacked_data = unpack(self.format_str, value)
        return unpacked_data

