import logging

from helpers import get_current_time

from weather import get_weather

# Module random to generate random operations
import random

# module re to split the user's input according to specific creiteria using REGEX
import re

# Add the function to print the help text
def print_help():
    help_text = """
    Usage:
    python main.py [OPTIONS]

    Options:
    --log           Enable logging mode.
    --log-level     Set the logging level (default: WARNING). Choose between INFO and WARNING.
    --show          Show all questions in the knowledge base.
    --import1       Import Q&A from a specified CSV file.
    --filetype      Specify the file type for import (currently supports 'csv').
    --filepath      Specify the path to the file to import.
    --add           Add a new question and answer to the knowledge base.
    --remove        Remove a question or an answer from the knowledge base.
    --question      Ask a question to the chatbot.
    --help          Show this help message and exit.
    
    Example:
    python main.py --help
    python main.py --log --log-level INFO
    python main.py --question "Wie geht es dir?"

    Notes:
    - If you mistype a command or use an unknown argument, an error message will be shown.
    """
    print(help_text)
    
# This function suggests questions based on a keyword entered by the user
def suggest_questions(user_input, question_and_answers):
    
    # List-comprehension containing the loop directly in the list for not using th method append()
    suggestions = [
        question
        
        # loop over all items of the dictionary regarding the Key & value of each item
        for question, data in question_and_answers.items()
        
        # if there is a match between the user's input and the predefined keywords
        if any(keyword in user_input for keyword in data["keywords"])
    ]
    return suggestions

# Function to handle the same user's input but in different form
def match_question(user_input, question_and_answers):
    user_input = user_input.strip().lower()
    for question, data in question_and_answers.items():
        if user_input in data["variants"]:
            return data
    return None

# This function handles the user's input in case of multiple questions connected by "and" | "or"
def handle_compound_questions(user_input, question_and_answers):
    '''
    Splits compound questions and handles each part individually using the module {re}
    '''
    
    # re.split ===> to Split the input into multiple questions using "\band\b" and "\bor\b"
    questions = re.split(r'\band\b|\bor\b', user_input)
    questions = [q.strip().lower() for q in questions if q.strip()]
    responses = [] # Collect responses for each question
    for question in questions:
        if question in question_and_answers:
            response = random.choice(question_and_answers[question]["answers"])
            responses.append(f"Q: {question.capitalize()} A: {response}")
        else:
            responses.append(f"Q: {question.capitalize()} A: Sorry, I don’t understand the question.")
            
    # return the list (Question : answer) then a line to print the rest of the list this way
    return "\n".join(responses)

# list all questions function will enable the users to see all questions when he types {"show all questions"}
def list_all_questions(question_and_answers):
    print(f"{get_current_time()} ChatBot: Hier sind alle Fragen:")
    
    # loop over the dictionary just to print all questions in ordered-list
    for i, question in enumerate(question_and_answers.keys(), 1):
        print(f"{i}. {question.capitalize()}")
        
def extract_location(user_input):
    known_locations = ["Wolfenbüttel", "Goslar", "Clausthal", "Braunschweig"]
    user_input_lower = user_input.lower()
    for location in known_locations:
        if location.lower() in user_input_lower:
            return location
        
    return None
        
        
# This function handles user input
def handle_user_input(user_input, question_and_answers):
    
    logging.info(f"User input received: {user_input}")
    
    
    # Check if the user is asking about weather or a location
    if "weather" in user_input or any(keyword in user_input.lower() for keyword in ["location", "where"]):
        location = extract_location(user_input)  # Extract the location from the user input
        if location:
            # Fetch and provide weather information
            weather_info = get_weather(location)
            print(f"{get_current_time()} ChatBot: {weather_info}")
            return weather_info
        else:
            print(f"{get_current_time()} ChatBot: I couldn't determine the location. Could you specify it?")
        return
    
    # handle_compound_questions functions will be called if the user ask two questions at the same time using and/or to connect between them
    if "and" in user_input or "or" in user_input:
        
        # Response is a {tuple} used to get ordered paired
        response = handle_compound_questions(user_input, question_and_answers)
        
        logging.info(f"Compound question response: {response}")
        
        print(f"{get_current_time()} ChatBot:\n{response}")
        return response
    else:
        
        # in case of not using {and/or} and the user types questions that are in the question_and_answers dictionary but in different form
        matched_question = match_question(user_input, question_and_answers)
        if matched_question:
            # random answer will be returned
            response = random.choice(matched_question["answers"])
            
            
            logging.info(f"Matched question: {matched_question}, Response: {response}")
            
            print(f"{get_current_time()} ChatBot: {response}")
            return response
        else:
            
            # in case the user just types a {keyword}, the chatbot will call the function: ==> suggest_questions()
            related_questions = suggest_questions(user_input, question_and_answers)
            if related_questions:
                print(f"{get_current_time()} ChatBot: Hier sind einige Vorschläge:")
                # this for-loop to return all related questions in a enumerated list on the screen
                for i, question in enumerate(related_questions, 1):
                    print(f"{i}. {question}")
                    
                    # this is infinite loop that will keep asking the user to type the number of the question he wants to ask
                while True:
                    # try except used to prevent the user from typing number out of the range
                    try: 
                        choice = int(input(f"{get_current_time()} Wählen Sie eine Nummer aus: ").strip())
                        if 1 <= choice <= len(related_questions):
                            selected_question = related_questions[choice - 1] #==>>> to convert the choice into 0-based according to the list
                            response = random.choice(question_and_answers[selected_question]["answers"])
                            print(f"{get_current_time()} ChatBot: {response}")
                            break # if the user type a matched number, it will return a random answer then break the loop
                        else:
                            print(f"{get_current_time()} ChatBot: Ungültige Auswahl!")
                    except ValueError:
                        print(f"{get_current_time()} ChatBot: Bitte geben Sie eine gültige Nummer ein.")
                return response
            else:
                
                logging.warning(f"Unrecognized input: {user_input}")
                
                print(f"{get_current_time()} Bot: Deine Eingabe '{user_input}' ist nicht bekannt.")
                print(f"{get_current_time()} Wie kann ich Ihnen helfen?")
                return "Ich kann nich verstanden, wie kann ich helfen?"