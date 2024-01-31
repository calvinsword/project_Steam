import time
from machine import I2C, Pin
from pico_i2c_lcd import I2cLcd
import neopixel
from random import randint

# different colors for the neopixel
np_colors = [
    [255, 0, 0],
    [255, 255, 0],
    [0, 255, 0],
    [0, 255, 255],
    [0, 0, 255],
    [255, 0, 255]
]

# declaration current time
current_time = time.time()

# pin designation
buzzer_pin = Pin(20, Pin.OUT)
i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=400000)
switch_pin = Pin(19, Pin.IN, pull=Pin.PULL_DOWN)
np = neopixel.NeoPixel(Pin(13), 8)

# declaration pattern for neopixel
pattern = int()
# declaration buzzer toggle
buzzer_toggle = int()


# waits till there is a serial input
def recieve_serial_input():
    global buzzer_toggle
    serial_input = input()
    serial_input = serial_input.split(',')
    buzzer_toggle = int(serial_input[0])
    timer_length = int(serial_input[1])
    return timer_length


# software timer used instead of importing time. Because the switch pin doesnt register when the program is sleeping
def timer(wait_time):
    global current_time
    if time.time() - current_time > wait_time:
        current_time = time.time()
        return True


# Enables/disables the buzzer
def buzzer():
    if buzzer_pin.value() == 0:
        buzzer_pin.value(1)
    else:
        buzzer_pin.value(0)


def neopixel_pattern(iter_num):
    if pattern == 1:
        np[iter_num % 8] = np_colors[neopixel_colors(iter_num)]
        np.write()

    elif pattern == 2:
        led_nmr = iter_num % 8
        led_nmr_neg = -led_nmr - 1
        np[led_nmr] = np_colors[neopixel_colors(iter_num)]
        np[led_nmr_neg] = np_colors[neopixel_colors((iter_num + 24))]
        np.write()

    elif pattern == 3:
        led_nmr = iter_num % 4
        led_nmr_neg = -led_nmr - 1
        np[led_nmr] = np_colors[neopixel_colors(iter_num)]
        np[led_nmr_neg] = np_colors[neopixel_colors((iter_num + 12))]
        np.write()

    elif pattern == 4:
        led_nmr = iter_num % 8
        led_nmr_2 = led_nmr + 1
        np[led_nmr] = np_colors[neopixel_colors(iter_num)]
        np[led_nmr_2] = np_colors[neopixel_colors(iter_num)]
        np.write()


# determines the color that will be displayed on the neopixel
def neopixel_colors(iter_num):
    if pattern == 1:
        color_num = iter_num // 8
        color_num -= 3 * (color_num // 3)
        return color_num

    elif pattern == 2:
        color_num = iter_num // 8
        color_num -= 6 * (color_num // 6)
        return color_num
    #
    elif pattern == 3:
        color_num = iter_num // 4
        color_num -= 6 * (color_num // 6)
        return color_num

    elif pattern == 4:
        color_num = iter_num // 2
        color_num -= 6 * (color_num // 6)
        return color_num


# format countdown timer
def timer_format(timerLengte):
    data_int_hour = int(timerLengte / 3600)
    data_int_min = int(int(timerLengte / 60) % 60)
    data_int_sec = timerLengte % 60
    timerFormat = f"{data_int_hour:02}:{data_int_min:02}:{data_int_sec:02}"
    return timerFormat


# displays the remaining time on the lcd screen
def countdown_lcd(timer_lengte):
    while timer_lengte > 0:
        if switch_pin.value():
            timer_lengte = -1
            break
        elif timer(0.5):
            I2C_ADDR = i2c.scan()[0]
            lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
            lcd.move_to(4, 0)
            lcd.putstr(timer_format(timer_lengte))
            lcd.move_to(0, 1)
            lcd.putstr("HBLPHBL 2.0 INC.")
            timer_lengte -= 1

    if timer_lengte == 0:
        # chooses a random number to select a pattern to be displayed on the neopixel
        global pattern
        pattern = randint(1, 4)

        iter_num = 0
        I2C_ADDR = i2c.scan()[0]
        lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
        lcd.move_to(1, 0)
        lcd.putstr("Timer is done")
        lcd.move_to(0, 1)
        lcd.putstr("HBLPHBL 2.0 INC.")

        while True:
            # if the switch is pressed down the lights and buzzer are disabled
            if switch_pin.value():
                buzzer_pin.value(0)
                for num in range(8):
                    np[num] = [0, 0, 0]
                np.write()
                break
            elif timer(0.25):
                if buzzer_toggle == 1:
                    buzzer()
                neopixel_pattern(iter_num)
                iter_num += 1
                # iter_num += 1 because there are 2 leds enabled at the same time
                if pattern == 4:
                    iter_num += 1

    I2C_ADDR = i2c.scan()[0]
    lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
    lcd.move_to(2, 0)
    lcd.putstr("Timer ended")
    lcd.move_to(0, 1)
    lcd.putstr("HBLPHBL 2.0 INC.")


while True:
    countdown_lcd(recieve_serial_input())
