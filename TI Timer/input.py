#!/usr/bin/env python
# -- coding: utf-8 --
from serial.tools import list_ports
import serial
import time


def read_serial(port):
    line = port.read(1000)
    return line.decode()


serial_ports = list_ports.comports()

# als het niet bekend is op welke poort de pico is aangesloten
# print("[INFO] Serial ports found:")
# for i, port in enumerate(serial_ports):
#     print(str(i) + ". " + str(port.device))
#
# pico_port_index = int(input("Which port is the Raspberry Pi Pico connected to? "))
# pico_port = serial_ports[pico_port_index].device

# als het wel bekend is welke poort het is kan je dat hardcoden
pico_port = serial_ports[0].device

# Open a connection to the Pico
with serial.Serial(port=pico_port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1) as serial_port:
    timer_time = input("How long do you want the timer to be in seconds?: ")
    buzzer = input("Do you want the buzzer to be on, type 'on' or 'off': ")

    if buzzer == "on":
        buzzer = 1
    else:
        buzzer = 0

    serial_input = str(buzzer) + "," + str(timer_time) + "\r"
    serial_port.write(serial_input.encode())

    # pico_output = read_serial(serial_port)
    # pico_output = pico_output.replace('\r\n', ' ')
    # print(pico_output)
    serial_port.close()
