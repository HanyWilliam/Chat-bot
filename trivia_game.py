import random

# this function is just a funny trivia game that ask the user questions and evaluate the user's answers to be true or false gives the user a score
# if the user enter "trivia" ==> the function will be called and start the play
# if the user enter "trivia" one more time during the game, so it will calculate the user's score, diplay it and exit the game
# if the user enter "normal start" ==> the Chat_bot will be activited normally
def trivia_game():
    
    # Trivia List containing {questions, choice to allow the user to choose one of them, correct answers}
    # this list will be only used here in this function so that it is included inside the function
    TRIVIA_QUESTIONS = [
    {
        "question": "What is the capital of France?",
        "options": ["A. Paris", "B. Berlin", "C. Madrid", "D. Rome"],
        "answer": "A"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["A. Earth", "B. Venus", "C. Mars", "D. Jupiter"],
        "answer": "C"
    },
    {
        "question": "Who wrote 'To Kill a Mockingbird'?",
        "options": ["A. Harper Lee", "B. J.K. Rowling", "C. Ernest Hemingway", "D. Mark Twain"],
        "answer": "A"
    },
    
]

# processing the trivia_game() function
    print("If you would like to start a funny game, type 'trivia' or 'normal start'")
    user_input = input("Enter your choice: ").lower()
    if user_input == "trivia":
        print("Trivia game activated! Answer the questions or type 'trivia' to exit.")
    
        score = 0
        questions_asked = 0
        while questions_asked < 10:
            question = random.choice(TRIVIA_QUESTIONS)
            print(f"\nQuestion: {question['question']}")
            for option in question['options']:
                print(option)

            user_input = input("Your answer (A/B/C/D) or type 'trivia' to exit: ").strip().upper()

            # The user write "trivia" to exit the game anytime They would like
            if user_input == "TRIVIA":
                print('****************')
                print(f"Exiting trivia game. Your final score is {score}/10.")
                print('****************\n')
                return 

            if user_input == question['answer']:
                print("** Correct!")
                score += 1
            else:
                print(f"** Wrong! The correct answer was {question['answer']}.")

            questions_asked += 1
            
            ##### Task 24 #######
            # It will show the number of questions you have answered and you total Score to decide to continue or exit as you like
            print(f"** Question {questions_asked} of 10. Your current score is {score} /10.")
    
    elif user_input == "normal start".lower():{
            print("Chat_Bot activated..."),
            print("===================")
        }
