import time
import adafruit_dht
import board
import RPi.GPIO as GPIO 
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback

dht_device = adafruit_dht.DHT22(board.D18)
LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-bd17ee05-352b-4f4b-9a74-d3f91598f507"  
pnconfig.publish_key = "pub-c-a1bfc69b-5a49-4f45-9a35-d0177b206c7e"      
pnconfig.uuid = "raspberry_pi"
pubnub = PubNub(pnconfig)

class MySubscribeCallback(SubscribeCallback):
    def message(self, pubnub, message):
        try:
            publisher = getattr(message, "publisher", None)
            msg_content = getattr(message.message, "get", lambda x: x)("text", message.message)

            if publisher == "flask_app" and msg_content == "Food is Ready!":
                
                #  LED
                for _ in range(10):  # Blink 10 times
                    GPIO.output(LED_PIN, GPIO.HIGH)
                    time.sleep(0.5)
                    GPIO.output(LED_PIN, GPIO.LOW)
                    time.sleep(0.5)
            else:
               print(f"Message ignored. Publisher: {publisher}, Content: {msg_content}")
        except Exception as e:
            print(f"Error processing message: {e}")

pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels("sensor_data").execute()

def publish_callback(envelope, status):
    if not status.is_error():
        print("Message published successfully!")
    else:
        print("Message failed to publish:", status)


while True:
    try:
        temperature_c = dht_device.temperature
        temperature_f = temperature_c * (9 / 5) + 32

        humidity = dht_device.humidity

        print("Temp:{:.1f} C / {:.1f} F    Humidity: {}%".format(temperature_c, temperature_f, humidity))

      # Publish data to PubNub
        pubnub.publish().channel("sensor_data").message({
            "temperature_c": temperature_c,
            "temperature_f": temperature_f,
            "humidity": humidity
        }).sync()

    except RuntimeError as err:
        print(err.args[0])

    time.sleep(2.0)
