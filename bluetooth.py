import serial
import time
import paho.mqtt.client as mqttClient
time.sleep(15)
bluetoothSerial = serial.Serial( "/dev/rfcomm1", baudrate=9600 )


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Verbonden met broker")
        global Connected
        Connected = True
        bluetoothSerial.write(b'k')
        bluetoothSerial.write(b'k')
        client.publish('alarm/state', "sound")
    else:
        print("Verbinding mislukt")
        GPIO.output(26, GPIO.HIGH)


def on_message(client, userdata, message):
    if message.payload.decode("utf-8") == 'alarm':
        bluetoothSerial.write(b'a')
    elif message.payload.decode("utf-8") == 'Het alarm staat aan':
        bluetoothSerial.write(b'u')
    elif message.payload.decode("utf-8") == 'Het alarm staat uit':
        bluetoothSerial.write(b'o')
    elif message.payload.decode("utf-8") == 'sound':
        bluetoothSerial.write(b'c')

Connected = False

broker_address = "192.168.137.184"
port = 1883
user = ""
password = ""

client = mqttClient.Client("Python")
client.username_pw_set(user, password=password)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port=port)
client.loop_start()
client.subscribe("alarm/state")


while 1:
        if b'g' in bluetoothSerial.readline():
                client.publish('alarm/states', '5678')
                print('ok')


while Connected != True:
    time.sleep(0.1)

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Afsluiten")
    client.disconnect()
    client.loop_stop()
