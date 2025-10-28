# Module datetime to extract the actual date and time
from datetime import datetime

# Module traceback to determine the kinds of error, but not to correct them
import traceback

# This function returns the current time formatted as HH:MM:SS
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# This function logs errors to a file while the application is running
def log_error(exception):
    # Creating a filename with a precise timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"error_log_{timestamp}.txt"
    
    # Open the file in 'write' mode and store the error message
    with open(filename, "w") as error_file:
        # Log the full traceback of the exception
        error_file.write(traceback.format_exc())
        
    print(f"{timestamp} ChatBot: Error log saved to {filename}.")
    
