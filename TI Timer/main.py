import time
from machine import I2C, Pin
from pico_i2c_lcd import I2cLcd
import neopixel
from random import randint


# initialisatie neopixel
np = neopixel.NeoPixel(Pin(13), 8)

# declaratie patroon voor neopixel
patroon = int()

current_time = time.time()
wait_time = 0.5

# pin designation
buzzer_pin = Pin(20, Pin.OUT)
i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=400000)

# switch designation
switch_pin = Pin(19, Pin.IN, pull=Pin.PULL_DOWN)


def timer_ophalen():
    timerLengte = int(input())
    return timerLengte


def timer():
    global current_time
    if time.time() - current_time > wait_time:
        current_time = time.time()
        return True


def neopixel_patroon(iter_num):
    kleuren = [
        [255, 0, 0],
        [255, 255, 0],
        [0, 255, 0],
        [0, 255, 255],
        [0, 0, 255],
        [255, 0, 255]
    ]

    if patroon == 1:
        np[iter_num % 8] = kleuren[neopixel_kleuren_bepalen(iter_num)]
        np.write()

    elif patroon == 2:
        led_nmr = iter_num % 8
        led_nmr_neg = -led_nmr - 1
        np[led_nmr] = kleuren[neopixel_kleuren_bepalen(iter_num)]
        np[led_nmr_neg] = kleuren[neopixel_kleuren_bepalen((iter_num + 24))]
        np.write()

    elif patroon == 3:
        led_nmr = iter_num % 4
        led_nmr_neg = -led_nmr - 1
        np[led_nmr] = kleuren[neopixel_kleuren_bepalen(iter_num)]
        np[led_nmr_neg] = kleuren[neopixel_kleuren_bepalen((iter_num + 12))]
        np.write()

    elif patroon == 4:
        led_nmr = iter_num % 8
        led_nmr_2 = led_nmr + 1
        np[led_nmr] = kleuren[neopixel_kleuren_bepalen(iter_num)]
        np[led_nmr_2] = kleuren[neopixel_kleuren_bepalen(iter_num)]
        np.write()


def neopixel_kleuren_bepalen(iter_num):
    if patroon == 1:
        kleur_num = iter_num // 8
        kleur_num -= 3 * (kleur_num // 3)
        return kleur_num

    elif patroon == 2:
        kleur_num = iter_num // 8
        kleur_num -= 6 * (kleur_num // 6)
        return kleur_num

    elif patroon == 3:
        kleur_num = iter_num // 4
        kleur_num -= 6 * (kleur_num // 6)
        return kleur_num

    elif patroon == 4:
        kleur_num = iter_num // 2
        kleur_num -= 6 * (kleur_num // 6)
        return kleur_num


# formatteert de countdown timer
def timer_format(timerLengte):
    data_int_hour = int(timerLengte / 3600)
    data_int_min = int(int(timerLengte / 60) % 60)
    data_int_sec = timerLengte % 60
    timerFormat = f"{data_int_hour:02}:{data_int_min:02}:{data_int_sec:02}"
    return timerFormat


def countdown_lcd(timerLengte):

    while timerLengte > 0:
        I2C_ADDR = i2c.scan()[0]
        lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
        lcd.move_to(4, 0)
        lcd.putstr(timer_format(timerLengte))
        lcd.move_to(0, 1)
        lcd.putstr("HBLPHBL 2.0 INC.")
        timerLengte -= 1
        time.sleep(1)

    if timerLengte == 0:
        global patroon
        patroon = randint(0, 4)

        iter_num = 0
        I2C_ADDR = i2c.scan()[0]
        lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
        lcd.move_to(4, 0)
        lcd.putstr("Beep Beep")
        lcd.move_to(0, 1)
        lcd.putstr("HBLPHBL 2.0 INC.")

        while True:
            if switch_pin.value():
                # buzzer_pin.value(0)
                for num in range(8):
                    np[num] = [0, 0, 0]
                np.write()
                break
            elif timer():
                neopixel_patroon(iter_num)
                iter_num += 1
                if patroon == 4:
                    iter_num += 1


while True:
    countdown_lcd(timer_ophalen())
