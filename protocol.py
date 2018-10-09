from enum import IntEnum
import struct

class MessageType(IntEnum):
    SET_PIN = 1
    RESPONSE = 2
    CHECK_PINS_STATUS = 3
    CHECK_PINS_RESPONSE = 4

class SetPin():
    def __init__(self, pin, state):
        self.pin = pin
        self.state = state

    def __str__(self):
        return "set pin {} to {}".format(self.pin, self.state)

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

    def __str__(self):
        return "Pin {} was set to {}".format(self.pin, self.state)

    def get_binary(self):
        return struct.pack('BBB?', MessageType.RESPONSE, self.pin, self.state, self.success)

    @classmethod
    def from_binary(cls, data):
        _, pin, state, success = struct.unpack('BBB?', data)
        return cls(pin, state, success)


class CheckPins():
    def get_binary(self):
        return struct.pack('B', MessageType.CHECK_PINS_STATUS)

    @classmethod
    def from_binary(cls, data):
        return cls()

class CheckPinsResponse():
    def __init__(self, statuses):
        self.statuses = statuses

    def get_binary(self):
        head = struct.pack('BB', MessageType.CHECK_PINS_RESPONSE, len(self.statuses))
        body = bytes(self.statuses)
        return head + body

    @classmethod
    def from_binary(cls, data):
        _, size = struct.unpack('BB', data[0:2])
        statuses = list(data[2:size+2])
        return cls(statuses)

command_dict = {
    MessageType.SET_PIN: SetPin,
    MessageType.RESPONSE: Response,
}

def from_binary(data):
    command = data[0]
    return command_dict[command].from_binary(data)