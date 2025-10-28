# Module csv to read and write CSV files
import csv

# Module json used as a database to add/remove questions and answers
import json

from helpers import get_current_time

import logging

from helpers import log_error

'''This function takes file-path as a parameter to return questions and answers stored in a CSV file and:
   retrieve that data in an organized format of a dictionary '''
def load_qna_from_csv(file_path):
    
    logging.info(f"Attempting to load Q&A from file: {file_path}")
    
    # dictionary
    qna_data = {}
    try:
        # open the csv file and read ==> (mode ='r') it
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            
            # the class DictReader ==> is used to read the csv file and return a dictionary in form or {key: value}
            reader = csv.DictReader(csvfile)
            
            # loop through each row in the csv file to get each part and store in the dictionary
            for row in reader:
                question = row["question"].strip().lower()
                answers = [row[f"answer{i+1}"].strip() for i in range(4) if row.get(f"answer{i+1}")]
                variants = [v.strip().lower() for v in row["variants"].split(";")]
                keywords = [k.strip().lower() for k in row["keywords"].split(";")]
                qna_data[question] = {
                    "answers": answers,
                    "variants": variants,
                    "keywords": keywords
                }
            
            logging.info(f"Successfully loaded Q&A from {file_path}")
            
    except FileNotFoundError as e:
        
        logging.warning(f"File not found: {file_path}")
        
        print(f"{get_current_time()} ChatBot: Fehler - Datei nicht gefunden.")
        log_error(e)
    except PermissionError:
        
        logging.warning(f"Permission denied for file: {file_path}")
        
        print(f"{get_current_time()} ChatBot: Fehler - Keine Berechtigung zum Zugriff auf die Datei.")
    except (KeyError, csv.Error):
        
        logging.warning(f"Invalid file format: {file_path}")
        
        print(f"{get_current_time()} ChatBot: Fehler - Ungültiges Dateiformat.")
    except Exception as e:
        
        logging.error(f"Unexpected error: {str(e)}")
        
        print(f"{get_current_time()} ChatBot: Unerwarteter Fehler: {str(e)}")
        log_error(e)
    return qna_data

# Function takes 2 parameter Dictioary &  json file ==> to convert a dictionary into a json
def save_dictionary_to_file(dictionary, filename="questions_and_answers.json"):
    # open the json file in 'write' mode 
    with open(filename, "w", encoding="utf-8") as file:
        # json.dump() method is used to convert a dictionary into a json
        # {ensure_ascii=False} to allow special characters like arabic letters to be stored as it is.
        json.dump(dictionary, file, ensure_ascii=False, indent=4)
        
# Loading the dictionary of from a JSON file & read it then return it.
def load_dictionary_from_file(filename="questions_and_answers.json"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError: # If the file contains invalid JSON. Gives an error message and returns an empty dictionary
        print(f"{get_current_time()} ChatBot: Fehler - Ungültiges JSON-Dateiformat.")
        return {}
    
# To enable the user to add question and answer pairs storing it in the json file not just in the memory
'''when you  the code, it must be in the terminal with the following format:
python main.py --add --q "Wie alt bist du?" --answer "ich bin 17
'''
def add_question(question_and_answers, question, answer):
    if question in question_and_answers:
        print(f"Frage '{question}' existiert bereits. Nur die Antwort wird hinzugefügt.")
        # ONLY adding the answer by callig the function ---- add_answer()
        add_answer(question_and_answers, question, answer)
    else:
        
        # adding the question will be in th form of a dictionary {key:value}
        question_and_answers[question] = {
            "answers": [answer],
            "variants": [question], # another form if the same question
            "keywords": question.lower().split() # keywords are the words in the question
        }
        print(f"Frage '{question}' mit der Antwort '{answer}' wurde hinzugefügt.")
        
# remove the question from the dictionary
'''
when you  the code, it must be in the terminal with the following format:
--remove  --question="wie alt bist du?"
'''
def remove_question(question_and_answers, question):
    if question in question_and_answers:
        del question_and_answers[question]
        print(f"Frage '{question}' wurde entfernt.")
    else:
        print(f"Frage '{question}' wurde nicht im Wörterbuch gefunden.")
        
def add_answer(question_and_answers, question, answer):
    if question in question_and_answers:
        if answer not in question_and_answers[question]["answers"]:
            question_and_answers[question]["answers"].append(answer)
            print(f"Antwort '{answer}' wurde zur Frage '{question}' hinzugefügt.")
        else:
            print(f"Antwort '{answer}' existiert bereits für die Frage '{question}'.")       
    else: # if the question is not in the dictionary
        print(f"Frage '{question}' wurde nicht gefunden. Bitte verwenden Sie '--add' für eine neue Frage.")


def remove_answer(question_and_answers, question, answer):
    if question in question_and_answers:
        if answer in question_and_answers[question]["answers"]:
            question_and_answers[question]["answers"].remove(answer)
            print(f"Antwort '{answer}' wurde von der Frage '{question}' entfernt.")
        else: # if the answer is not in the list of answers
            print(f"Antwort '{answer}' wurde nicht für die Frage '{question}' gefunden.")
    else: # if the question is not in the dictionary
        print(f"Frage '{question}' wurde nicht gefunden.")