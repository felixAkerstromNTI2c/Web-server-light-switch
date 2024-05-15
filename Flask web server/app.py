
from flask import Flask, render_template
import time
import RPi.GPIO as GPIO
import Adafruit_DHT


DHT_SENSOR = Adafruit_DHT.DHT11 # Initialisera sensor

# Tilldelar konstanterna GPIO pins
ledStripPin = 18
whiteLedPin = 15
heatingPin = 14
DHT_PIN = 4

# Skapa en flask server
app = Flask(__name__)

# Initialisera GPIO pins som output
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledStripPin, GPIO.OUT)
GPIO.setup(whiteLedPin, GPIO.OUT)
GPIO.setup(heatingPin, GPIO.OUT)

# Beskrivning: Funktionen tilldelar outvoltage strip HIGH eller LOW beroende på vad klockan är.
# Argument: Funktionen tar inte in några argument
# Return: Funktionen returnerar antingen GPIO.LOW eller GPIO.HIGH
def autoLedStrip():
    if (time.localtime()[3] <= 17):
        outVoltage = GPIO.HIGH
    else:
        outVoltage = GPIO.LOW
    return outVoltage

# Beskrivning: Funktionen tilldelar outvoltage strip HIGH eller LOW beroende på vad klockan är.
# Argument: Funktionen tar inte in några argument
# Return: Funktionen returnerar antingen GPIO.LOW eller GPIO.HIGH
def autoWhiteLed():
    if (time.localtime()[3] <= 16):
        outVoltage = GPIO.HIGH
    else:
        outVoltage = GPIO.LOW
    return outVoltage

# Beskrivning: Funktionen tilldelar outvoltage strip HIGH eller LOW beroende på om temperaturen eller fuktigheten är över/under eller under threshold värdena.
# Argument: Funktionen tar inte in några argument
# Return: Funktionen returnerar outViltage som antingen har värdet GPIO.LOW eller GPIO.HIGH
def autoHeating():
    thresholdTemperature = 18 # Värmning sätts igång om temperaturen är under detta värde
    thresholdHumidity = 70 # Värmning sätts igång när luftfuktigheten är för hög(varm luft håller mer vatten)
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN) # Avläs sensordata
    if  (temperature < thresholdTemperature) or (humidity > thresholdHumidity):
        outVoltage = GPIO.LOW
    else:
        outVoltage = GPIO.HIGH
    return outVoltage

# Beskrivning: Funktionen tar emot ett state från javascipten och gör olika saker beroende på vad state har för värde
# Argument:  class- integer
# Return: Funktionen returnerar en string och en integer. Om stringen är 204 betyder det att funktionen genomförts lyckat. 400 returnerar ett felmeddelande. 
@app.route("/ledStrip/<int:state>", methods=['POST'])
def setLedStrip(state):
    # route for led control
    print(f"Led strip state: {state}") # printa state i terminalen
    if state == 0:
        outVoltage = GPIO.LOW
        GPIO.output(ledStripPin, outVoltage)
    elif state == 1:
        outVoltage = GPIO.HIGH
        GPIO.output(ledStripPin, outVoltage)
    elif state == 2:
        outVoltage = autoLedStrip() # Kör funktionen och bestämmer om LED strip ska vara på eller av beroende på klockan
        GPIO.output(ledStripPin, outVoltage) # GPIO får värdet HIGH eller LOW beroende på var outVoltage strip tilldelas
    elif state == 3:
        outVoltage = GPIO.LOW
        GPIO.output(whiteLedPin, outVoltage)
    elif state == 4:
        outVoltage = GPIO.HIGH
        GPIO.output(whiteLedPin, outVoltage)
    elif state == 5:
        outVoltage = autoWhiteLed() # Kör funktionen och bestämmer om det vita ljuset ska vara på eller av beroende på klockan
        GPIO.output(whiteLedPin, outVoltage) # GPIO får vädet HIGH eller LOW beroende på var outVoltage strip tilldelas
    elif state == 6:
        outVoltage = GPIO.LOW
        GPIO.output(heatingPin, outVoltage)
    elif state == 7:
        outVoltage = GPIO.HIGH
        GPIO.output(heatingPin, outVoltage)
    elif state == 8:
        outVoltage = autoHeating() # Kör funktionen och bestämmer om det vita ljuset ska vara på eller av beroende på klockan 
        GPIO.output(heatingPin, outVoltage) # GPIO får vädet HIGH eller LOW beroende på var outVoltage strip tilldelas 
    else:
        return ('Unknown LED state', 400) # returnera felmeddelande
    return ('',204) # returnera lyckat genomförande av funktion



# Beskrivning: Funktionen avläser temperatur och fuktighetsvärden och uppdaterar dessa till startsidan när sidan laddas om  
# Argument: Funktionen tar inte in några argument
# Return: Funktionen returnerar temperatur och fuktighetsvärden till HTML sidan med hjälp av Jinja när sidan laddas om
@app.route("/")
def index():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    return render_template('home.html',temperature=temperature, humidity=humidity) # Returnerar temperatur och fuktighetsvärden till html-koden där de skrivs ut på skärmen


# __name__ är __main__ om detta är startfilen(den filen man kör först)
if __name__ == '__main__': # if satsen startar servern om man kör denna filen
    # Kör flask servern på denna ip address och port 5500
    app.run(host='0.0.0.0', port=5500, debug=True)


