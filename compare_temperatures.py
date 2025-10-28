import csv
import logging
from datetime import datetime
from weather import get_weather  

def extract_temp_from_weather_string(weather_string):
    try:
        lines = weather_string.split("\n")
        for line in lines:
            if "Temperature:" in line:
                temp_part = line.split(":")[1].split("Celsius")[0].strip()
                return float(temp_part)
    except Exception as e:
        logging.error(f"Failed to extract temperature from weather string: {e}")
    return None

def compare_temperatures():
    
    weather_string, location = get_weather("Wolfenbüttel")  
    weather_temp = extract_temp_from_weather_string(weather_string)

    if weather_temp is None:
        return "Could not retrieve or parse weather temperature."

    
    local_temps = []
    try:
        with open("sense_hat_temperature_data.csv", mode="r") as file:
            reader = csv.reader(file)
            next(reader)  

            for row in reader:
                timestamp = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                temp = float(row[1])
                local_temps.append((timestamp, temp))

        
        if len(local_temps) >= 3:
            
            temperature_differences = []
            for timestamp, local_temp in local_temps[-3:]:
                temp_diff = local_temp - weather_temp  
                temperature_differences.append((timestamp, temp_diff))
            return temperature_differences, location
        else:
            return "Not enough local temperature data available.", location
    except FileNotFoundError:
        return "Local temperature data file not found.", location


if __name__ == "__main__":
    results, location = compare_temperatures()
    if isinstance(results, list):
        print(f"Temperature comparison results for {location}:")
        for timestamp, temp_diff in results:
            print(f"At {timestamp}, the temperature was {temp_diff:.2f}°C different from the forecast.")
    else:
        print(f"Error for {location}: {results}")