from flask import Flask, request, jsonify
import os
import requests
import re
import hashlib
from pathlib import Path
from Wednesday import count_wednesdays
from Contacts import sort_contacts
from Markdown import create_markdown_index
from Sender_Email import extract_sender_email
from Credit_Card import extract_credit_card
from Similar_Comments import find_most_similar_comments
from Gold_Ticket import calculate_gold_ticket_sales
from API import fetch_and_save_api_data
from GIT_Repo import clone_and_commit_git_repo
from User_SQL import run_sql_query

os.environ['AIPROXY_TOKEN'] = 'eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjMwMDIzMTZAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.DvLFDgvuV6vp37Tp89HhU-8vYu2FZCTXovK7U6oyjT8'

DATA_DIR = Path('/data').resolve()  # Changed to '/data' for security

app = Flask(__name__)

class SecurityError(Exception):
    pass

class TaskAgent:
    def __init__(self):
        self.api_url = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {os.environ['AIPROXY_TOKEN']}",
            "Content-Type": "application/json"
        }

    def parse_task(self, task_description):
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a task parsing assistant. Identify the main steps required to complete the given task."},
                {"role": "user", "content": task_description}
            ]
        }
        response = requests.post(self.api_url, headers=self.headers, json=data)
        return response.json()['choices'][0]['message']['content']
    
    @staticmethod
    def validate_data_path(path: str) -> Path:
        try:
            full_path = (DATA_DIR / path).resolve()
            if DATA_DIR not in full_path.parents and full_path != DATA_DIR:
                raise SecurityError(f"Attempted access outside {DATA_DIR}")
            return full_path
        except (ValueError, FileNotFoundError):
            raise SecurityError("Invalid path")

    def check_for_delete_operations(self, task_description):
        delete_keywords = ['delete', 'remove', 'erase', 'clear']
        if any(keyword in task_description.lower() for keyword in delete_keywords):
            raise SecurityError("Delete operations are not permitted")

    def execute_task(self, task_description):
        self.check_for_delete_operations(task_description)
        steps = self.parse_task(task_description)
        results = []
        for step in steps.split('\n'):
            self.check_for_delete_operations(step)
            if "count wednesdays" in step.lower():
                count_wednesdays(str(self.validate_data_path('dates.txt')), str(self.validate_data_path('dates-wednesdays.txt')))
                results.append("Counted Wednesdays")
            elif "sort contacts" in step.lower():
                sort_contacts(str(self.validate_data_path('contacts.json')), str(self.validate_data_path('contacts-sorted.json')))
                results.append("Sorted contacts")
            elif "markdown" in step.lower():
                create_markdown_index(str(self.validate_data_path('docs')), str(self.validate_data_path('docs/index.json')))
                results.append("Created markdown index")
            elif "extract email" in step.lower():
                extract_sender_email(str(self.validate_data_path('email.txt')), str(self.validate_data_path('email-sender.txt')))
                results.append("Extracted sender email")
            elif "credit card" in step.lower():
                extract_credit_card(str(self.validate_data_path('credit-card.png')), str(self.validate_data_path('credit-card.txt')))
                results.append("Extracted credit card number")
            elif "similar comments" in step.lower():
                find_most_similar_comments(str(self.validate_data_path('comments.txt')), str(self.validate_data_path('comments-similar.txt')))
                results.append("Found similar comments")
            elif "ticket sales" in step.lower():
                calculate_gold_ticket_sales(str(self.validate_data_path('ticket-sales.db')), str(self.validate_data_path('ticket-sales-gold.txt')))
                results.append("Calculated gold ticket sales")

        return "; ".join(results)

agent = TaskAgent()

@app.route('/run', methods=['POST'])
def run_task():
    task = request.args.get('task')
    if not task:
        return jsonify({"error": "No task provided"}), 400
    try:
        result = agent.execute_task(task)
        return jsonify({"message": result}), 200
    except SecurityError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/read', methods=['GET'])
def read_file():
    path = request.args.get('path')
    if not path:
        return jsonify({"error": "No file path provided"}), 400
    try:
        full_path = agent.validate_data_path(path)
        with open(full_path, 'r') as file:
            content = file.read()
        return content, 200
    except SecurityError as e:
        return jsonify({"error": str(e)}), 403
    except FileNotFoundError:
        return "", 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
