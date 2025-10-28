from sense_hat import SenseHat
import csv
from datetime import datetime
import time

sense = SenseHat()
CSV_FILE = "sense_hat_temperature_data.csv"

def log_data(temp, pressure, humidity):
    with open(CSV_FILE, mode="a") as file:
        writer = csv.writer(file)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, temp, pressure, humidity])

with open(CSV_FILE, mode="a") as file:
    if file.tell() == 0:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Temperature (°C)", "Pressure (hPa)", "Humidity (%)"])

try:
    while True:
        temp = sense.get_temperature()
        pressure = sense.get_pressure()
        humidity = sense.get_humidity()
        print(f"Temp: {temp:.2f}Celsius, Pressure: {pressure:.2f} hPa, Humidity: {humidity:.2f}%")
        log_data(temp, pressure, humidity)
        time.sleep(1800)
except KeyboardInterrupt:
    print("Program Stopped.")
