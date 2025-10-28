# Module argparse to parse the command line arguments
import argparse

import sys

import logging

from helpers import get_current_time, log_error
from qna_handler import load_dictionary_from_file, load_qna_from_csv, save_dictionary_to_file, add_question, remove_question, remove_answer
from user_interaction import print_help, handle_user_input, list_all_questions
from logging_config import setup_logging
from trivia_game import trivia_game
from data import question_and_answers
from scraping import fetch_web_data

import compare_temperatures

# Main function for chatbot app
def chat_app():
    
    # calling the trivia_game()
    #trivia_game()
        
    # using the class ArguemntParser from the Module argparse to create an object
    # t handle CLI arguments passed by the user
    parser = argparse.ArgumentParser(description="Chatbot Application")
    
    # using the method .add_argument
    # --question to allows the user to provide a question directly via the command line
    parser.add_argument("--question", type=str, help="Provide a question directly")
    
    # --import1 ==> it rturns true if the user want to import Q&A from a file
    # EX- python script.py --import1 --filetype CSV --filepath "/path/to/file.csv"
    parser.add_argument("--import1", action="store_true", help="Import Q&A from a file")
    
    # --filetype is a string CSV
    # EX- python main.py --add --q "What is AI?" --answer "Artificial Intelligence."
    parser.add_argument("--filetype", type=str, help="Specify the file type (e.g., CSV)")
    
    # CSV filepath & it works with the --import1 option
    parser.add_argument("--filepath", type=str, help="Path to the file", default=r"C:\Users\Student\Desktop\Projekt\questions_and_answers.txt")
    
    # --add to enable the user to add a new question and answer
    parser.add_argument("--add", action="store_true", help="Fügt eine Frage und/oder eine Antwort hinzu.")
    # EX- python script.py --remove --q "What is Python?"
    parser.add_argument("--remove", action="store_true", help="Entfernt eine Frage oder eine Antwort.")
    parser.add_argument("--answer", type=str, help="Die Antwort, die hinzugefügt oder entfernt werden soll.")
    parser.add_argument("--q", type=str, help="Die Frage, die hinzugefügt oder entfernt werden soll.")
    
    # --show ==> to enable the user via the command line to display all the questions in the dictionary
    # This way ==> python main.py --show "show all questions"
    parser.add_argument("--show", type=str, help="Show all questions")
    
    parser.add_argument("--debug", action="store_true", help="Enable debugging mode.")
    
    
    parser.add_argument("--log", action="store_true", help="Enable logging mode.")
    parser.add_argument("--log-level", type=str, choices=["INFO", "WARNING"], default="WARNING", help="Set the logging level (default: WARNING).")
    
    # New argument for comparing temperatures
    parser.add_argument("--compare-temperatures", action='store_true', help="Compare temperatures using default data")
    
    parser.add_argument("--scrape", type=str, help="Scrape data from the specified URL")

    
    
    
    args = parser.parse_args()    
            
    # Handle invalid arguments (if there are any unrecognized arguments)
    if len(sys.argv) > 1 and not any(arg in sys.argv[1:] for arg in ["--log", "--log-level", "--show", "--import1", "--add", "--remove", "--question", "--help", "--compare-temperatures", "--scrape"]):
        print(f"Error: Unrecognized argument(s): {', '.join(sys.argv[1:])}")
        print_help()
        sys.exit()
        
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        print(f"{get_current_time()} Debugging mode enabled.")
    else:
        logging.basicConfig(level=logging.INFO)
    
    
    setup_logging(args.log, args.log_level)
    
    if args.scrape:
        url = args.scrape.strip()
        print(f"{get_current_time()} ChatBot: Fetching data from {url}")
        result = fetch_web_data(url)
        print(result)

    
    
    # Handle compare-temperatures argument
    if args.compare_temperatures:
        print("Comparing temperatures using default data.")
        try:
            # Call compare_temperatures without location for default behavior
            temperature_differences = compare_temperatures()
            if isinstance(temperature_differences, list):
                for timestamp, temp_diff in temperature_differences:
                    print(f"At {timestamp}, local temp is {temp_diff:.2f}°C different from forecast.")
            else:
                print(temperature_differences)
        except Exception as e:
            logging.error(f"Failed to compare temperatures: {e}")

    

    # Handling the function "Show all questions()" via the command line
    '''   python main.py --show "show all questions"  '''
    if args.show == "show all questions":
        list_all_questions(question_and_answers)
    
    
    
    if args.log:
        logging.info("Application started in logging mode.")
    #log_feature_example()

    #print("Application executed. Check app.log if logging is enabled.")
    
        
    # Handle CSV import if specified
    # Here, check if the file exists
    if args.import1 and args.filetype and args.filepath:
        
        # Check if the file imported is a CSV file
        if args.filetype.lower() == "csv":
            print(f"{get_current_time()} ChatBot: Importieren von Daten aus {args.filepath}")
            
            # Read the CSV file using the function load_qna_from_csv & store it in the object "imported_data"
            imported_data = load_qna_from_csv(args.filepath)
            if imported_data:
                question_and_answers.update(imported_data) # Update the dictionary with the imported data
                print(f"{get_current_time()} ChatBot: Import abgeschlossen. Wissensbasis aktualisiert.")

    try:
        #load a saved dictionary (the Q&A database) from a file and update the question_and_answers dictionary
        question_and_answers.update(load_dictionary_from_file())
         # if the file exists, print a message to the user
    except Exception as e:
        log_error(e)

    # Command-Line Arguments for Adding, Removing, or retrieval Q&A
    if args.add: # Check if the --add argument is provided
        if args.q and args.answer: # Check if both question and answer are provided
            add_question(question_and_answers, args.q, args.answer) # Add the new question and answer to the dictionary
        elif args.q: # in case of ONLY the question is provided
            print("Bitte geben Sie '--answer' an, um eine neue Antwort hinzuzufügen.") # it prompts the user to also provide an answer (--answer).
    elif args.remove:
        if args.q and args.answer:
            remove_answer(question_and_answers, args.q, args.answer)
        elif args.q:
            remove_question(question_and_answers, args.q)
    elif args.question: # Check if the --question argument is provided, the function : handel_user_input() will be called
        handle_user_input(args.question.lower().strip(), question_and_answers)
    else:
        # In case of not providing add, remove or question the chatbot will interactive normally with the user
        # the conversation will be saved in log_file
        try:
            log_filename = f"chat_log_{get_current_time()}.txt"
            with open(log_filename, "w") as log_file:
                print(f"{get_current_time()} Hallo! Wie kann ich Ihnen helfen?")
                while True:
                    user_input = input(f"{get_current_time()} You: ").strip().lower()
                    if user_input == "trivia":
                        print(f"{get_current_time()} Lancement du jeu Trivia...")
                        trivia_game()  # Lancer la fonction trivia_game
                        continue 
                    log_file.write(f"{get_current_time()} You: {user_input}\n")
                    if user_input == "bye":
                        print(f"{get_current_time()} Auf Wiedersehen!")
                        break
                    #elif user_input == "show all questions":
                        #list_all_questions(question_and_answers)
                    else:
                        response = handle_user_input(user_input, question_and_answers)
                        log_file.write(f"{get_current_time()} ChatBot: {response}\n")
            print(f"{get_current_time()} ChatBot: Gesprächsprotokoll gespeichert in {log_filename}.")
        except Exception as e:
            log_error(e)

    save_dictionary_to_file(question_and_answers)

## Run the chatbot
if __name__ == "__main__":
    chat_app()