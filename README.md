## Erste Semester Projekt - Gruppe 8
A chatbot application developed as part of the first-semester project In DigiTec programm. The chatbot can answer questions, provide weather information, compare temperatures, and even play a trivia game.

**Chatbot Application**  
This project is a chatbot application designed to:
- Answer a variety of questions, including banking-related queries and weather information.
- Fetch and display weather information for specific locations using the OpenWeatherMap API.
- Compare local temperature data logged using a Sense HAT with weather forecasts.
- Play a fun trivia game.
- Log errors and user interactions for debugging and monitoring purposes.


## Installation


### Prerequisites
- Python 3.12.2 or pythton 3.x
- Sense HAT 
- OpenWeatherMap API key
- Virtual environment venv

### Steps
Clone the repository:
   
- [ ] [Git Link](https://gitlab-fi.ostfalia.de/lv/dt-ep-ws24/group_8/erstsemester-projekt-g8.git)

   
## Usage

### Chatbot Interaction
- Run the Chatbot application using this line of command : "python main.py"
- Ask questions directly to the chatbot.
- Ask the chatbot coumpound questions. 
- Use the `--show` option to list all available questions.
- Add or remove questions using the `--add` and `--remove` options.
- Play the trivia game by typing "trivia".


### Weather Information
Ask the chatbot about the weather in a specific location while runing the application:

For example :"What is the weather in Wolfenbüttel"


### Add and remove Questions/Answers
Adding question with the answer:
  
- `python main.py --add --q "Question" --answer "Answer"`

Adding another answer to an existing question:

- `python main.py --add --q "Existing question" --answer "New answer"`

Remove a specified answer form a question:

- `python main.py --remove --q "Existing question" --answer "Specified answer"`

Remove an entire Question:

- `python main.py --remove --q "Existing question"`

### List all questions
To list all qustions:

- `python main.py --show "show all questions"`

### Web Scrapping
To scrape a specified web site you should run this line of command:

- `python main.py --scrape "url"`

### Graphical user interface
To run th application using the GUI:

- `python "graphical_user_interface.py"`

### Logging

Logs are stored in `app.log` for debugging and monitoring.


### Support

For help, please contact:

- **Mohammed**: [m.echtouki@ostfalia.de](mailto:m.echtouki@ostfalia.de)
- **Hany**: [s.william@ostflia.de](mailto:s.william@ostflia.de)
- **Haris**: [h.masood@ostfalia.de](mailto:h.masood@ostfalia.de)



### Roadmap

- Add more questions and answers to the chatbot's knowledge base.
- Improve the trivia game with more questions and features.
- Enhance temperature comparison functionality.
- Add support for more languages.

### Authors and acknowledgment

### Authors
- **Mohamed**
- **Hany**
- **Haris**


### Acknowledgments
We would like to thank our professors:
- **Lukas Bartenstein** (Product Owner)
- **Seba Motie** (Product Owner)
- **Tobias** (Product Owner)
and mentors at Ostfalia University for their guidance and support throughout this project.




### License

This project is not licensed but made for educational purpose as a project to prepare Chatbot with different features.



### Project status

The project is almost finished but we can continuously adding new features and improving existing ones.

