import struct


format = '?d20s'

class structManager:
    def __init__(self):
        self.format = '?d20s'
        self.struct_size = struct.calcsize(self.format)
        print(f'struct size: {self.struct_size}')

    def read(self,data):
        structure_data = struct.unpack(self.format, data[0:self.struct_size])
        data = data[self.struct_size:]
        return structure_data,data

    def read_and_print_data(self, data):
        structure_data, message = self.read(data)
        print(f'structure data: {structure_data}')
        print(f'message: {message}')
        return structure_data, message

    def write(self, structure_data, message):
        data = struct.pack(self.format, *structure_data)
        data = data + message.encode()
        return data

