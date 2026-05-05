from utilities import hexstr2int, int2hexstr, hexstr2ascii
from commands import table, handles
from parser import parse_header
import time

MAP = table['MAP']
FIXED = table['FIXED']
HWCHAN = table['HWCHAN']
CHAN = table['CHAN']
STATUS = table['STATUS']
TRIGGER = table['TRIGGER']
HDR = table["HDR"]

class KLC():
    
    def __init__ (self, devicename:str, serial_no=str, verbose=False):
        # set True for debugging class
        self.DEBUG = False

        if serial_no:
            if isinstance(serial_no, int):
                self.serial_no == str(serial_no)
            else:
                self.serial_no = serial_no
            if verbose:
                print(f"Device Serial Number : {self.serial_no}")

    def __str__(self):
        self.get_info()
        return "Is a serial instance of a KLC controller."
    
    def _connect(self):
        return 

    def _connected(self):
        return self.device is not None and self.device.is_open
       
    def identify(self):
        self._write(FIXED["identify"], "flash device display")    
        
    def get_info(self):
        self._write(FIXED["req_info"], "get device info")
        self._read()

    def get_serial(self):
        self._write(FIXED["req_serial"], "get device serial no.")

    def lock_wheel(self):
        self._write(FIXED["lock_wheel"], "lock wheel")
        self.wheel_status()

    def unlock_wheel(self):
        self._write(FIXED["unlock_wheel"], "unlock wheel")
        self.wheel_status()

    def wheel_status(self):
        self._write(FIXED["wheel_status"], "get wheel status")
        header, payload = self._read()
        return self._interpret(header, payload)

    def save_params(self):
        self._write(FIXED["save_params"], "save params to eeprom")

    def _write(self, command, name: str=None):
        '''
        Write commands to device
        '''
        if not self.connected():
            raise RuntimeError("No device connected")
        if not isinstance(command, (bytes, bytearray)):
            raise TypeError("Command must be type: bytes")
        if self.DEBUG:
            label = f"[{name}]" if name else ""
            print(f"TX {label}: {command.hex(' ')}")
        self.device.write(command)

    def _read(self):
        '''
        Read data from device and extract packet if exists
        '''
        if not self.connected():
            raise RuntimeError("No device connected")
        # extract the header information
        raw_header = self._read_exact()
        # create dictionary of header data
        header = parse_header(raw_header)
        # default to empty if no payload
        payload = b""   
        if header.has_payload:
            length = header.param2
            if length > 0:
                # extract the payload
                payload = self._read_exact(length)

        return header, payload

    def _read_exact(self, n=6):
        '''
        Read data from device
        '''
        # set default to empty
        data = b""
        start = time.time()
        # read each byte
        while len(data) < n:
            chunk = self.device.read(n-len(data))
            if chunk:
                data += chunk
                # error on timeout
            if time.time() - start > self.device.timeout:
                raise TimeoutError(f"Timeout reading {n} bytes")
            
        return data
    
    def _interpret(self, header, payload):
        msg = handles.get(header.msg_id)

        return msg, payload
        

