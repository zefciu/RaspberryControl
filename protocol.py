from enum import IntEnum
import struct

class MessageType(IntEnum):
    SET_PIN = 1
    RESPONSE = 2

class SetPin():
    def __init__(self, pin, state):
        self.pin = pin
        self.state = state

    def get_binary(self):
        return struct.pack('BBB', MessageType.SET_PIN, self.pin, self.state)

    @classmethod
    def from_binary(cls, data):
        '''
        Function which will return class object
        '''
        _, pin, state = struct.unpack('BBB', data)
        return cls(pin, state)

class Response():
    def __init__(self, pin, state, success):
        self.pin = pin
        self.state = state
        self.success = success

    def get_binary(self):
        return struct.pack('BBB?', MessageType.RESPONSE, self.pin, self.state, self.success)

    @classmethod
    def from_binary(cls, data):
        _, pin, state, success = struct.unpack('BBB?', data)
        return cls(pin, state, success)


command_dict = {
    MessageType.SET_PIN: SetPin,
    MessageType.RESPONSE: Response,
}

def from_binary(data):
    command = data[0]
    return command_dict[command].from_binary(data)