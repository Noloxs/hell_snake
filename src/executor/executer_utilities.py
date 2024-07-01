import serial.tools.list_ports

class ExecuterUtilities:

    @staticmethod
    def get_physical_addresses():
        ports = []
        for port in serial.tools.list_ports.comports():
            if port.vid is not None and port.pid is not None:
                ports.append(port)
        return ports
