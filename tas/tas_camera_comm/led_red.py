from gpiozero import RGBLED
from time import sleep
led = RGBLED(red=16, green=20, blue=21)

# LED Color table
led.color = (1,0,0) #red
sleep(0.1)