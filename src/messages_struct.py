import struct

class structManager:
    MAX_STRING_LENGTH = 20

    def __init__(self):
        self.format = f'?d{self.MAX_STRING_LENGTH}s'
        self.struct_size = struct.calcsize(self.format)

    def get_max_string_length(self):
        return self.MAX_STRING_LENGTH

    def read(self,data):
        structure_data = struct.unpack(self.format, data[0:self.struct_size])
        data = data[self.struct_size:]
        return structure_data,data

    def read_and_print_data(self, data):
        structure_data, message = self.read(data)
        
        return structure_data, message

    def write(self, structure_data, message):
        data = struct.pack(self.format, *structure_data)
        data = data + message.encode()
        return data