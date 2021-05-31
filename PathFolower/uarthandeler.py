import serial, time
import RPi.GPIO as GPIO


class Uarthandeler:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.IN)
        self.draaicheck = 0
        self.ser = serial.Serial('/dev/ttyS0', baudrate=9600,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS
                            )

    def stuur_instructie(self, instructie):
        for rijinstructie in instructie.rijinstructies.wielinstructies:
            # wacht tot de vorige actie klaar is
            while GPIO.input(17):
                niks = False

            # stuur de vier instructies naar de vier wielen en geef ze het start signaal
            for wielinstructie in rijinstructie:
                if wielinstructie.draai != 0:
                    # een variabele die gebruikt kan worden om te kijken of de juiste hoek gedraaid is
                    self.draaicheck = wielinstructie.draai
                self.ser.write(wielinstructie.instructie)

            self.ser.write(bytes("sssssss", 'utf-8'))

            time.sleep(0.1)
