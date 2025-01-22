import tkinter as tk
from tkinter import scrolledtext
import sqlite3
import openai
from datetime import datetime
import logging

# Setup logging
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('conversation_log.log'),
            logging.StreamHandler()
        ])
    logger = logging.getLogger(__name__)
    return logger

logger = setup_logging()

# Customizable text templates for GPT-3 prompts
prompt_templates = {
    "initial": "Provide as much information as possible about {}, and STOP and print 'Stopped, Ran out of unique Information' once you run out of unique information to provide. Use dashes for bullet points:",
    "follow_up": "Elaborate on this specific point, including the initial prompt for context:\nInitial Prompt: {}\nSpecific Point: {}\n\nProvide as much information as possible, and STOP and print 'Stopped, Ran out of unique Information' once you run out of unique information to provide. Details:"
}

# Function for querying GPT-3
def query_gpt(prompt, specific_point=None, prompt_type="initial"):
    openai.api_key = ""  # Replace with your OpenAI API key
    formatted_prompt = prompt_templates[prompt_type].format(prompt, specific_point) if specific_point else prompt_templates[prompt_type].format(prompt)
    try:
        response = openai.Completion.create(
    model="gpt-4",
    prompt=formatted_prompt,
    max_tokens=500
)

        return response.choices[0].text.strip()
    except Exception as e:
        logger.error(f"Error querying GPT: {e}")
        return None

# Function to extract bullet points
def extract_bullet_points(text):
    return [line.strip('- ').strip() for line in text.split('\n') if line.startswith('-')]

def handle_gpt_interaction(user_prompt):
    responses = {}

    # Level 1 Interaction
    update_progress_label("Querying GPT-3 for Level 1 response...")
    level_1_response = query_gpt(user_prompt, prompt_type="initial")
    responses["Level 1"] = level_1_response

    # Extract bullet points from Level 1 response
    bullet_points_level_1 = extract_bullet_points(level_1_response)

    # Level 2 Interaction
    level_2_responses = {}
    for point in bullet_points_level_1[:3]:  # Process only the first three bullet points
        update_progress_label(f"Querying GPT-3 for details on: {point}...")
        detail = query_gpt(user_prompt + ". " + point, None, "initial")  # Use entire Level 1 response for context
        level_2_responses[point] = detail
    responses["Level 2"] = level_2_responses

    # Level 3 Interaction
    level_3_responses = {}
    for key, level_2_response in level_2_responses.items():
        level_3_details = {}
        bullet_points_level_2 = extract_bullet_points(level_2_response)
        for point in bullet_points_level_2[:3]:  # Process only the first three bullet points of Level 2 response
            update_progress_label(f"Querying GPT-3 for further elaboration on: {point}...")
            detail_query = "Elaborate on the point: '{}' from the context of: '{}'".format(point, key)
            detail = query_gpt(detail_query, None, "initial")
            level_3_details[point] = detail
        level_3_responses[key] = level_3_details
    responses["Level 3"] = level_3_responses

    update_progress_label("Processing complete.")
    return responses

# Database setup and management functions
def create_database():
    conn = sqlite3.connect('conversation.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY,
        timestamp DATETIME,
        prompt TEXT,
        response TEXT,
        level INTEGER
    )
    ''')
    conn.commit()
    conn.close()

def store_conversation(prompt, response, level):
    conn = sqlite3.connect('conversation.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO conversations (timestamp, prompt, response, level)
    VALUES (?, ?, ?, ?)
    ''', (datetime.now(), prompt, response, level))
    conn.commit()
    conn.close()

# GUI Functions
def submit_topic():
    topic = entry_field.get()
    entry_field.config(state='disabled')
    submit_button.config(state='disabled')
    handle_interaction_and_display(topic)

def handle_interaction_and_display(topic):
    multi_level_responses = handle_gpt_interaction(topic)
    output_display.delete(1.0, tk.END)  # Clear existing text
    for level, response in multi_level_responses.items():
        output_display.insert(tk.END, f"\n{level} Responses:\n")
        if isinstance(response, dict):
            for key, value in response.items():
                if isinstance(value, dict):
                    output_display.insert(tk.END, f"\n- {key}:\n")
                    for sub_key, sub_value in value.items():
                        formatted_response = f"  - {sub_key}: {sub_value}\n"
                        output_display.insert(tk.END, formatted_response)
                else:
                    formatted_response = f"- {key}: {value}\n"
                    output_display.insert(tk.END, formatted_response)
        else:
            output_display.insert(tk.END, f"{response}\n")
        store_conversation(topic, str(response), 1)  # Storing all levels under level 1
    entry_field.config(state='normal')
    submit_button.config(state='normal')

def update_progress_label(text):
    progress_label.config(text=text)
    root.update_idletasks()

# GUI Setup
root = tk.Tk()
root.title("GPT Interaction")

# Make the window resizable
root.resizable(True, True)

# Progress Label
progress_label = tk.Label(root, text="Ready", wraplength=300)  # Adjust the wraplength as needed
progress_label.pack()

entry_field = tk.Entry(root, width=50)
entry_field.pack()

submit_button = tk.Button(root, text="Submit", command=submit_topic)
submit_button.pack()

output_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
output_display.pack(fill=tk.BOTH, expand=True)

# Initialize database and logger
create_database()
logger.info("Database initialized.")

root.mainloop()
