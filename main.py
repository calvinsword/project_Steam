from machine import I2C, Pin
from pico_i2c_lcd import I2cLcd
import time
#input in seconds

data_int = -1

#pin designation
buzzer_pin = Pin(20, Pin.OUT)
i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=400000)

while True:
    buzzer_pin.value(0)
    data = input()
    data_int = int(data)
    data_error_check = data
    while data_int > 0:
        #here i make the time readable
        data_int_hour = data_int / 3600
        data_int_hour_int = int(data_int_hour)
        data_int_min = int(data_int / 60) % 60
        data_int_min_int = int(data_int_min)
        data_int_sec = data_int % 60
        time_display = f"{data_int_hour_int:02}:{data_int_min_int:02}:{data_int_sec:02}"
        #countdown for on de the display
        I2C_ADDR = i2c.scan()[0]
        lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
        lcd.move_to(4, 0)
        lcd.putstr(time_display)
        lcd.move_to(0, 1)
        lcd.putstr("HBLPHBL2.0 INC.")
        data_int -= 1
        time.sleep(1)
    #end of timer
    if data_int == 0:
        I2C_ADDR = i2c.scan()[0]
        lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
        lcd.move_to(2, 0)
        lcd.putstr("TIMER IS DONE")
        buzzer_pin.value(1)
        time.sleep(0.5)
        buzzer_pin.value(0)
        time.sleep(0.5)
        buzzer_pin.value(1)
        time.sleep(0.5)
        buzzer_pin.value(0)
        time.sleep(0.5)
        buzzer_pin.value(1)
        time.sleep(0.5)
        buzzer_pin.value(0)
        time.sleep(0.5)
        buzzer_pin.value(1)
        time.sleep(0.5)
        buzzer_pin.value(0)
        time.sleep(0.5)
        buzzer_pin.value(1)
        time.sleep(0.5)
        buzzer_pin.value(0)
        time.sleep(0.5)
        buzzer_pin.value(1)
        time.sleep(0.5)
        buzzer_pin.value(0)
        time.sleep(0.5)



