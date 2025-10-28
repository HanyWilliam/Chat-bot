import logging

# This function create     
def setup_logging(log_mode, log_level):
    """
    Sets up logging based on mode and level.
    """
    if log_mode:
        # INFO ==> to recorde the normal events in the application in a form of informational messages to document all what happens daily
        # log_file object includes all message that generated according to ===>> logging.INGO
        log_level = logging.INFO if log_level.upper() == "INFO" else logging.WARNING
        logging.basicConfig(
            
            # create a log file called "app.log" to store messages
            filename="app.log",
            
            # Appends new messages to the file without overwriting existing ones
            filemode="a",
            format="%(asctime)s - %(levelname)s - %(message)s",
            
            #set the logging level (INFO - WARNING)
            level=log_level
        )
        # informational message indicating that logging has been enabled
        logging.info("Logging is enabled with level: %s", log_level)
    else:
        
        # if log_mode is False, disable logging and suppressing all log messages
        logging.disable(logging.CRITICAL)