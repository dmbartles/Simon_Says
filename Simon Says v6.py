# Simon Says by Matt Bartles
# Created for Andy Bartles

# Import packages
from machine import I2C, Pin, PWM
from pico_i2c_lcd import I2cLcd
from time import sleep
import random

# Define variables
buzzer_volume = 1000

# Define IC2 LED | GP0 + GP1 + VBUS + GND
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

# Define buzzer | GP15 + GND
buzzer = PWM(Pin(15))

# Define buttons 
red_button = Pin(16, Pin.IN, Pin.PULL_DOWN)
yellow_button = Pin(18, Pin.IN, Pin.PULL_DOWN)
white_button = Pin(20, Pin.IN, Pin.PULL_DOWN)
blue_button = Pin(22, Pin.IN, Pin.PULL_DOWN)
green_button = Pin(26, Pin.IN, Pin.PULL_DOWN)

# Define LEDs
onboard_led = Pin(25, Pin.OUT)
red_led = Pin(17, Pin.OUT)
yellow_led = Pin(19, Pin.OUT)
white_led = Pin(21, Pin.OUT)
blue_led = Pin(4, Pin.OUT)
green_led = Pin(2, Pin.OUT)

# Define colors
colors = ["RED","YELLOW","WHITE","BLUE","GREEN"]

# Define solfège tones
tones = {"DO": 262,"RE": 294,"MI": 330,"FA": 349,"SO": 392,"LA": 440,"TI": 494}

# Define songs
tone_song = ["DO","RE","MI","FA","SO","LA","TI"]
intro_song = ["DO","RE","MI","FA","SO","LA","TI"]
fail_song = ["MI","RE","DO"]
pass_song = ["SO","LA","TI"]

# Define functions
def play_tone(frequency):
    buzzer.duty_u16(buzzer_volume)
    buzzer.freq(frequency)
    sleep(tone_length)
    buzzer.duty_u16(0)
    sleep(quiet_length)

def play_song(mysong):
    for i in range(len(mysong)):
        play_tone(tones[mysong[i]])
    
def play_intro():
    lcd.clear()
    lcd.putstr("Hello Andy!"+"\n")
    red_led.value(1)
    yellow_led.value(1)
    white_led.value(1)
    blue_led.value(1)
    green_led.value(1)
    red_led.value(0)
    play_tone(tones["DO"])
    yellow_led.value(0)
    play_tone(tones["MI"])
    white_led.value(0)
    play_tone(tones["FA"])
    blue_led.value(0)
    play_tone(tones["SO"])
    green_led.value(0)
    play_tone(tones["TI"])
    lcd.putstr("Get  Ready!")
    red_led.value(1)
    sleep(pattern_quite_length)
    yellow_led.value(1)
    sleep(pattern_quite_length)
    white_led.value(1)
    sleep(pattern_quite_length)
    blue_led.value(1)
    sleep(pattern_quite_length)
    green_led.value(1)
    sleep(1.00)

# Clear board
def clear_board():
    red_led.value(1)
    yellow_led.value(1)
    white_led.value(1)
    blue_led.value(1)
    green_led.value(1)
    sleep(1.00)

# Reset board
def reset_board():
    global lives
    global retry
    global light_pattern
    global pattern_display_length
    global pattern_quite_length
    global tone_length
    global pause_length
    global quiet_length
    global level    
    global last_level   
    global boost_level  
    global boost_percent    
        
    lives = 1
    retry = 0
    light_pattern = []
    pattern_display_length = 0.80
    pattern_quite_length = 0.10
    tone_length = 0.35
    pause_length = 0.15
    quiet_length = 0.025

    level = 1
    last_level = 0
    boost_level = 3
    boost_percent = 0.30
      
# Clear board and play intro
reset_board()
clear_board()
play_intro()
    
while True:
    # Add color to light pattern
    if retry == 0:
        light_pattern.append(random.choice(colors))
        level = len(light_pattern)
        last_level = level - 1
    
    # Start game
    clear_board()
    lcd.clear()
    if level > 1:
        # If the level is a retry
        if retry == 1:
            lcd.putstr("Try Again!"+"\n")
        
        # If speed boost level
        elif last_level%boost_level == 0:
            lcd.putstr("Let's speed up!"+"\n")
            play_song(pass_song)
            
            # Reduce pauses and delays by the boost percent
            pattern_display_length = pattern_display_length * (1-boost_percent)
            pattern_quite_length = pattern_display_length * (1-boost_percent)
            tone_length = tone_length * (1-boost_percent)
            quiet_length = quiet_length * (1-boost_percent)
            
            # Add a life
            lives = lives + 1
        
        # If other level            
        else:
            lcd.putstr("Great work!"+"\n")
            play_song(pass_song)
            
    # If first level
    else:
        lcd.putstr("Go, Andy!"+"\n")

    lcd.putstr("Lvl:" + str(level) + " Try:" + str(lives))
    sleep(1.00)  
 
    # Display pattern for player
    for color in light_pattern:
        
        if color == 'RED':
            red_led.value(0)
            play_tone(tones["DO"])
            sleep(pattern_display_length)
            red_led.value(1)
            sleep(pattern_quite_length)

        if color == 'YELLOW':
            yellow_led.value(0)
            play_tone(tones["MI"])
            sleep(pattern_display_length)
            yellow_led.value(1)
            sleep(pattern_quite_length)
            
        if color == 'WHITE':
            white_led.value(0)
            play_tone(tones["FA"])
            sleep(pattern_display_length)
            white_led.value(1)
            sleep(pattern_quite_length)
                
        if color == 'BLUE':
            blue_led.value(0)
            play_tone(tones["SO"])
            sleep(pattern_display_length)
            blue_led.value(1)
            sleep(pattern_quite_length)
            
        if color == 'GREEN':
            green_led.value(0)
            play_tone(tones["TI"])
            sleep(pattern_display_length)
            green_led.value(1)
            sleep(pattern_quite_length)

    # Get input pattern from player
    lcd.clear()
    lcd.putstr("Your turn!"+"\n")
    lcd.putstr("Lvl:" + str(level) + " Try:" + str(lives))
  
    for color in light_pattern:

        while True:
        
            if red_button.value() == 1:
                red_led.value(0)
                user_pressed = "RED"
                play_tone(tones["DO"])
                red_led.value(1)
                break
                
            if yellow_button.value() == 1:
                yellow_led.value(0)
                user_pressed = "YELLOW"
                play_tone(tones["MI"])
                yellow_led.value(1)
                break
                
            if white_button.value() == 1:
                white_led.value(0)
                user_pressed = "WHITE"
                play_tone(tones["FA"])
                white_led.value(1)
                break
                
            if blue_button.value() == 1:
                blue_led.value(0)
                user_pressed = "BLUE"
                play_tone(tones["SO"])
                blue_led.value(1)
                break

            if green_button.value() == 1:
                green_led.value(0)
                user_pressed = "GREEN"
                play_tone(tones["TI"])
                green_led.value(1)
                break

        # Compare user input to light pattern
        sleep(pause_length)
        if user_pressed == color:
            retry = 0
            pass
        else:
            lcd.clear()
            lcd.putstr("Wrong button!"+"\n")
            play_song(fail_song)
            if lives == 1:
                # Reset game
                lcd.putstr("Game over!")
                reset_board()
                break
            else:
                # Reduce lives by one and
                lcd.putstr("Try Again!")
                lives = lives - 1
                retry = 1
                break
            sleep(2.00)
