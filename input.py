#!/usr/bin/env python
# -- coding: utf-8 --
from serial.tools import list_ports
import serial


def read_serial(port):
    line = port.read(1000)
    return line.decode()


serial_ports = list_ports.comports()

pico_port = serial_ports[3].device

# Open a connection to the Pico
with serial.Serial(port=pico_port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1) as serial_port:
    time_in_seconds = input("How long do you want the timer to be in seconds?:")

    time_in_seconds_pico_acceptable = time_in_seconds + "\r"
    serial_port.write(time_in_seconds_pico_acceptable.encode())
    pico_output = read_serial(serial_port)
serial_port.close()
