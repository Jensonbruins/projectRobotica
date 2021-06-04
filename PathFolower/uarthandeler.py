from PathFolower import pad
import utilities
import serial, time
import RPi.GPIO as GPIO


class Uarthandeler:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.IN)
        self.draaicheck = 0
        self.ser = serial.Serial('/dev/serial0', baudrate=9600,
                                 parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE,
                                 bytesize=serial.EIGHTBITS
                                 )
        
    def extra_draai(self, startRichting, instructies, richting):
        # als er gedraaid moet zijn en de draai is niet volledig draai dan extra
        wielen = utilities.setup_wielen()
        extraDraai = pad.Pad()
        verwachteRichting = startRichting + self.draaicheck
        if verwachteRichting > 360:
            verwachteRichting -= 360
        while self.draaicheck != 0:
            huidigeRichting = richting.lees_richting()
            berekendeDraai = verwachteRichting - huidigeRichting
            if berekendeDraai < -5 or berekendeDraai > 5:
                extraDraai.set_vector(int(berekendeDraai), 0)
                instructies.rijinstructies.wielinstructies = []
                instructies.maak_instructie(wielen, extraDraai.get_vector())
                self.stuur_instructie(instructies)
            else:
                self.draaicheck = 0

    def stuur_instructie(self, instructie):
        for rijinstructie in instructie.rijinstructies.wielinstructies:
            # stuur de vier instructies naar de vier wielen en geef ze het start signaal
            for wielinstructie in rijinstructie:
                if wielinstructie.draai != 0:
                    # een variabele die gebruikt kan worden om te kijken of de juiste hoek gedraaid is
                    self.draaicheck = wielinstructie.draai
                self.ser.write(wielinstructie.instructie)

            self.ser.write(bytes("sssssss", 'utf-8'))

            time.sleep(0.1)
            # wacht tot de vorige actie klaar is
            while GPIO.input(17):
               niks = False
