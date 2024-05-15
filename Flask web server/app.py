
from flask import Flask, render_template
import time
import RPi.GPIO as GPIO
import Adafruit_DHT


DHT_SENSOR = Adafruit_DHT.DHT11 # Initialisera sensor

# Tilldelar olika GPIO pins
ledStripPin = 18
whiteLedPin = 15
heatingPin = 14
DHT_PIN = 4

# Skapa en flask server
app = Flask(__name__)

# Initialisera GPIO pin som output
GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
GPIO.setup(ledStripPin, GPIO.OUT)
GPIO.setup(whiteLedPin, GPIO.OUT)
GPIO.setup(heatingPin, GPIO.OUT)

# Beskrivning: Funktionen tilldelar outvoltage strip HIGH eller LOW beroende på vad klockan är.
# Argument: Funktionen tar inte in några argument
# Return: Funktionen returnerar antingen GPIO.LOW eller GPIO.HIGH
# Skriven av: Felix Åkerström
def autoLedStrip():
    if (time.localtime()[3] >= 20) or (time.localtime()[3] <= 16):
        outVoltageStrip = GPIO.HIGH
    else:
        outVoltageStrip = GPIO.LOW
    return outVoltageStrip

# Beskrivning: Funktionen tilldelar outvoltage strip HIGH eller LOW beroende på vad klockan är.
# Argument: Funktionen tar inte in några argument
# Return: Funktionen returnerar antingen GPIO.LOW eller GPIO.HIGH
# Skriven av: Felix Åkerström
def autoWhiteLed():
    if (time.localtime()[3] >= 21) or (time.localtime()[3] <= 15):
        outVoltage = GPIO.HIGH
    else:
        outVoltage = GPIO.LOW
    return outVoltage

# Beskrivning: Funktionen tilldelar outvoltage strip HIGH eller LOW beroende på om temperaturen är över eller under threshold.
# Argument: Funktionen tar inte in några argument
# Return: Funktionen returnerar antingen GPIO.LOW eller GPIO.HIGH
# Skriven av: Felix Åkerström
def autoHeating():
    threshold = 18 # Värmning sätts igång om temperaturen är under detta värde
    temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if  temperature < threshold:
        outVoltage = GPIO.HIGH
    else:
        outVoltage = GPIO.LOW
    return outVoltage

# Beskrivning: Funktionen tar emot ett state från javascipten och gör olika saker beroende på vad state har för värde
# Argument:  class- integer
# Return: Funktionen returnerar en string och en integer. Om stringen är 204 betyder det att funktionen genomförts lyckat. 400 returnerar ett felmeddelande 
# Skriven av: Felix Åkerström
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
        GPIO.output(ledStripPin, outVoltage) # GPIO får vädet HIGH eller LOW beroende på var outVoltage strip tilldelas
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




@app.route("/")
def index():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    return render_template('home.html',temperature=temperature, humidity=humidity) # Returnerar temperatur och fuktighetsvärden till html-koden där de skrivs ut på skärmen


# __name__ will be __main__ only if this file is the entry point
if __name__ == '__main__':
    # Kör flask servern på denna ip address och port 50100
    # run the server on this ip and port 50100
    app.run(host='0.0.0.0', port=50100, debug=True)



def temperature_sensor():
    while True:
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            print("Temp={0:0.1f}C  Humidity={1:0.1f}%".format(temperature, humidity))
            return render_template('home.html', temperature=temperature)
        else:
            print("Sensor failure. Check wiring.")
        time.sleep(3)
        print("-------------------------------------------------------------")

