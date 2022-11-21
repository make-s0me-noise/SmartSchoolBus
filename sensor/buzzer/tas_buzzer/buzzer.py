import RPi.GPIO as GPIO
import time
import sys
 
print(sys.argv)
cin = sys.argv[1]
if int(cin) > 0:
    GPIO.setmode(GPIO.BCM)

    buzzer = 12
    button = 26
    scale = 523

    GPIO.setup(buzzer, GPIO.OUT)
    GPIO.setup(button, GPIO.IN)
    
    try:
        p = GPIO.PWM(buzzer, 100)
        p.start(100)
        p.ChangeDutyCycle(90)

        while True:
            p.ChangeFrequency(scale)
            if GPIO.input(button) == 0:
                break

    finally:
        GPIO.cleanup()
