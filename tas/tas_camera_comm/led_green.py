from gpiozero import RGBLED
from time import sleep
led = RGBLED(red=16, green=20, blue=21)

# LED Color table
led.color = (0,1,0) #green
sleep(3)