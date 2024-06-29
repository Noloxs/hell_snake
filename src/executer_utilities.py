import serial.tools.list_ports

def get_physical_addresses():
        ports = []
        for port in serial.tools.list_ports.comports():
            if port.vid != None and port.pid != None:
                ports.append(port)
        return ports