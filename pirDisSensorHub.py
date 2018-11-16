import time
import paho.mqtt.client as mqttClient
import RPi.GPIO as GPIO
time.sleep(10)
GPIO.setmode(GPIO.BCM)
TRIG = 24
ECHO = 25
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(23, GPIO.IN)
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
        client.publish('alarm/state', "sound")
    else:
        print("Verbinding mislukt")
        GPIO.output(26, GPIO.HIGH)


def on_message(client, userdata, message):
        if message.payload.decode("utf-8") =="alarm":
                for x in range(10):
                        GPIO.output(26, GPIO.HIGH)
                        time.sleep(1)
                        GPIO.output(26, GPIO.LOW)
                        time.sleep(1)


Connected = False

broker_address = "192.168.137.184"
port = 1883
user = ""
password = ""

client = mqttClient.Client("SENSOR_movement")
client.username_pw_set(user, password=password)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port=port)
client.loop_start()
client.subscribe("python/alarm")


while True:
    GPIO.output(TRIG, False)
    time.sleep(2)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()
    while GPIO.input(ECHO)==1:
        pulse_end=time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    print(distance)
    if distance > 200:
        client.publish('alarm/states', '{},1,{}'.format(GPIO.input(23), 0, 0)) ###$
    elif distance < 200:
        client.publish('alarm/states', '{},{},{}'.format(GPIO.input(23), 0, 0)) ###$
    time.sleep(1)


while Connected != True:
    time.sleep(0.1)
