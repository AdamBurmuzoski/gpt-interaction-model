# GPT-4 Interaction Model

## Overview

The **GPT-4 Interaction Model** is a Python-based application that integrates multiple technologies to create an interactive interface for querying the GPT-4 API and handling conversational data. The application leverages a **Tkinter GUI**, an **SQLite database** for storing conversation history, **logging** for tracking application activity, and OpenAI's **GPT-4 API** for natural language processing. This tool is designed to provide users with a multi-level conversational experience, allowing for deeper insights and dynamic reporting.

---

## Key Features

- **Logging**  
  Track and log key application events and errors. Logs are written to both the console and a log file (`conversation_log.log`), capturing timestamps, log levels, and relevant messages.

- **GPT-4 Interaction**  
  Send user-defined prompts to the GPT-4 model and receive multi-level responses. The tool processes responses in three levels:
  - **Level 1**: General information about the topic.
  - **Level 2**: Elaboration on specific points.
  - **Level 3**: Further elaboration on detailed aspects.

- **Bullet Point Extraction**  
  Extract structured data from GPT-4’s responses, converting them into bullet points to facilitate deeper queries and analysis.

- **Database Management**  
  Use **SQLite** to store the conversation data (prompt, response, and interaction level) in a local database (`conversation.db`). This ensures that every query and response is stored for future reference.

- **GUI (Graphical User Interface)**  
  A **Tkinter**-based interface for user interaction:
  - **Entry Field**: Input area for entering prompts.
  - **Submit Button**: Initiates the GPT-4 interaction process.
  - **Progress Label**: Displays updates during the multi-step interaction.
  - **ScrolledText Output**: Shows the GPT-4 responses structured by interaction levels.

- **Data Flow & Interaction Workflow**  
  The application follows a multi-step workflow:
  - **Initial Query**: User inputs a prompt, and GPT-4 returns general information.
  - **Follow-Up Queries**: Bullet points are extracted from the initial response and elaborated upon in subsequent queries.
  - **Further Elaboration**: The process repeats for deeper insights, with each step displayed to the user.

---

## Technical Details

- **Language**: Python
- **GUI Framework**: Tkinter (for building the user interface)
- **Database**: SQLite (for storing conversation history)
- **API**: OpenAI GPT-4 (for generating conversational responses)
- **Logging**: Python logging module (for tracking application activity)
- **Error Handling**: Basic error handling for API requests and database operations

---

## Dependencies

- **Tkinter**: Built-in Python library for creating GUIs.
- **SQLite**: Lightweight relational database for managing conversation history.
- **OpenAI API**: To interact with the GPT-4 model.

---

## How to Run

1. Clone or download the repository.
2. Install the required dependencies:
   pip install openai sqlite3
3. Ensure that your OpenAI API key is configured in the script.
4. Run the script:
   pip install openai sqlite3
5. Use the Entry Field to enter a topic and click Submit to start querying GPT-4.
