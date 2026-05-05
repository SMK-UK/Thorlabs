from dataclasses import dataclass

"""
Represents a 6-byte protocol header.

Fields:
- msg_id: command/message identifier (2 bytes)
- param1: first parameter byte (or control value)
- param2: second parameter byte (or payload length depending on mode)
- dest: destination byte (MSB indicates presence of payload)
- src: source byte

Provides helpers to interpret routing and payload flags.

"""
@dataclass
class Header:
    msg_id: bytes
    param1: int
    param2: int
    dest: int
    src: int

    @property
    # check if there is a payload
    def has_payload(self) -> bool:
        return (self.dest & 0x80) != 0

    @property
    # clean the destination if no payload
    def dest_clean(self) -> int:
        return self.dest & 0x7F
    
def parse_header(data: bytes) -> Header:
    if len(data) != 6:
        raise ValueError(
            f"Expected header to be 6 bytes, got {len(data)} bytes"
            )
    # extract the relevant byte information from header
    return Header(
        msg_id=data[0:2],
        param1=data[2],
        param2=data[3],
        dest=data[4],
        src=data[5]
    )