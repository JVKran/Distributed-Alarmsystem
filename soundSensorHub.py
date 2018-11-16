import time
import paho.mqtt.client as mqttClient
import RPi.GPIO as GPIO
from gpiozero import Buzzer

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN)
buzzer = Buzzer(17)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

for x in range(3):
        GPIO.output(16, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(16, GPIO.LOW)
        time.sleep(1)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Verbonden met broker")
        global Connected
        Connected = True
        GPIO.output(16, GPIO.HIGH)
        client.publish('alarm/state', 'sound')
    else:
        print("Verbinding mislukt")
        GPIO.output(26, GPIO.HIGH)


def on_message(client, userdata, message):
        if message.payload.decode("utf-8") == 'alarm':
                for x in range(10):
                        buzzer.on()
                        GPIO.output(26, GPIO.HIGH)
                        time.sleep(1)
                        buzzer.off()
                        GPIO.output(26, GPIO.LOW)
                        time.sleep(1)

Connected = False

broker_address = "192.168.137.184"
port = 1883
user = ""
password = ""

client = mqttClient.Client("SENSOR")
client.username_pw_set(user, password=password)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port=port)
client.loop_start()
client.subscribe("python/alarm")


while True:
    client.publish('alarm/states', '{},{},{}'.format(GPIO.input(14), 0, 0))  ###Vervangen door GPIO readings ###
    time.sleep(0.1)


while Connected != True:
    time.sleep(0.1)

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Afsluiten")
    client.disconnect()
    client.loop_stop()

GPIO.output(16, LOW)
