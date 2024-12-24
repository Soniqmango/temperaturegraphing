import csv
from datetime import datetime, timedelta
import random
import math
from matplotlib import pyplot as plt
import pyinputplus as pyip

def generate_weather_data():
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2023, 12, 31)
    delta = timedelta(days=1)
    
    location = "New York"
    
    with open('new_york_weather_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        
        writer.writerow(['Name', 'Date', 'Max Temperature (F)', 'Min Temperature (F)', 'Precipitation (in)', 'Wind Speed (mph)'])
        
        current_date = start_date
        while current_date <= end_date:
            days_since_start = (current_date - start_date).days
            
            # Base seasonal temperature using a sinusoidal pattern
            base_temp = 50 + 10 * math.sin(2 * math.pi * (days_since_start % 365) / 365)
            
            # Add randomness to the base temperature
            max_temp = base_temp + random.uniform(-5, 5)
            min_temp = max_temp - random.randint(5, 15)
            
            # Simulate precipitation and wind speed
            precipitation = round(random.uniform(0, 0.3) if current_date.month in [3, 4, 5, 9, 10, 11] else random.uniform(0, 0.1), 2)
            wind_speed = random.randint(10, 20) if current_date.month in [12, 1, 2] else random.randint(5, 15)
            
            # Write the row to the CSV file
            writer.writerow([location, current_date.strftime('%Y-%m-%d'), round(max_temp, 1), round(min_temp, 1), precipitation, wind_speed])
            
            current_date += delta

def process_weather_file(filename):
    try:
        with open(f"/Users/riesjoos/Desktop/{filename}") as f:
            reader = csv.reader(f)
            header_row = next(reader)
            
            # Use a dictionary to store column indices based on flexible matching
            column_indices = {}
            for i, header in enumerate(header_row):
                header_lower = header.lower()
                if 'name' in header_lower:
                    column_indices['name'] = i
                elif 'date' in header_lower:
                    column_indices['date'] = i
                elif 'max' in header_lower:
                    column_indices['max_temp'] = i
                elif 'min' in header_lower:
                    column_indices['min_temp'] = i
            
            # Check if all required columns are found
            required_columns = ['name', 'date', 'max_temp', 'min_temp']
            missing_columns = [col for col in required_columns if col not in column_indices]
            if missing_columns:
                raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
            
            location = None
            dates, highs, lows = [], [], []
            for row in reader:
                try:
                    current_date = datetime.strptime(row[column_indices['date']], '%Y-%m-%d')
                    if not location:
                        location = row[column_indices['name']]
                    highs.append(float(row[column_indices['max_temp']]))
                    lows.append(float(row[column_indices['min_temp']]))
                    dates.append(current_date)
                except ValueError:
                    print(f"Skipping invalid row: {row}")
        
        if not dates:
            print("No valid data to plot.")
            return
        
        start_year = dates[0].year
        end_year = dates[-1].year

        fig, ax = plt.subplots(figsize=(15, 9))
        ax.plot(dates, highs, c='red', alpha=0.5, label='Highs')
        ax.plot(dates, lows, c='blue', alpha=0.5, label='Lows')
        plt.fill_between(dates, highs, lows, facecolor='gray', alpha=0.1)
        plt.legend()
        
        if start_year == end_year:
            plt.title(f"Daily High and Low Temperatures in {location} - {start_year}", fontsize=24)
        else:
            plt.title(f"Daily High and Low Temperatures in {location} - {start_year}-{end_year}", fontsize=24)
        
        plt.xlabel('', fontsize=16)
        fig.autofmt_xdate()
        plt.ylabel("Temperature (F)", fontsize=16)
        plt.tick_params(axis='both', which='major', labelsize=16)
        plt.show()

    except FileNotFoundError:
        raise FileNotFoundError(f"File '{filename}' not found.")
    except ValueError as e:
        raise ValueError(f"Error processing file: {e}")

def main():
    user_choice = pyip.inputYesNo("Do you have a weather data file? (yes/no): ")
    
    if user_choice.lower() == 'yes':
        while True:
            filename = pyip.inputStr("Enter the filename (e.g., new_york_weather_data.csv) or type 'exit' to quit: ")
            if filename.lower() == 'exit':
                print("Exiting the program.")
                return
            try:
                process_weather_file(filename)
                break  
            except FileNotFoundError as e:
                print(e)
                print("Please try again.")
            except ValueError as e:
                print(e)
                print("Please check the file and try again.")
    
    elif user_choice.lower() == 'no':
        print("Simulating weather data...")
        generate_weather_data() 
        print("Simulated weather data has been saved as 'new_york_weather_data.csv'.")
        try:
            process_weather_file('/Code/python/new_york_weather_data.csv')
        except ValueError as e:
            print(e)
            print("There was an issue processing the simulated data.")
    else:
        print("Invalid choice. Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    main()
