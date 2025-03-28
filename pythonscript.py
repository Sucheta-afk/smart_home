import serial
import pymongo
from datetime import datetime

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["sensor_database"]
collection = db["temperature_humidity"]

# Connect to Arduino
arduino = serial.Serial('COM8', 9600, timeout=1)  # Change 'COM3' if needed

print("Receiving data...")

while True:
    try:
        line = arduino.readline().decode().strip()
        if line:
            print(f"Raw data received: {line}")  # Debug print
            data = line.split(",")

            if len(data) == 3:
                temp = float(data[0])
                humidity = float(data[1])
                motion = int(data[2])

                sensor_data = {
                    "timestamp": datetime.now(),
                    "temperature": temp,
                    "humidity": humidity,
                    "motion": motion
                }

                collection.insert_one(sensor_data)
                print(f"Inserted into MongoDB: {sensor_data}")

    except Exception as e:
        print(f"Error: {e}")