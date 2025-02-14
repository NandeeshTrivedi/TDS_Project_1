from flask import Flask, request, jsonify
import os
import requests
from Wednesday import count_wednesdays
from Contacts import sort_contacts
from Markdown import create_markdown_index
from Sender_Email import extract_sender_email
from Credit_Card import extract_credit_card
from Similar_Comments import find_most_similar_comments
from Gold_Ticket import calculate_gold_ticket_sales

os.environ['AIPROXY_TOKEN'] = 'eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjMwMDIzMTZAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.DvLFDgvuV6vp37Tp89HhU-8vYu2FZCTXovK7U6oyjT8'

app = Flask(__name__)

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

    def execute_task(self, task_description):
        steps = self.parse_task(task_description)
        for step in steps.split('\n'):
            if "count wednesdays" in step.lower():
                count_wednesdays('/data/dates.txt', '/data/dates-wednesdays.txt')
            elif "sort contacts" in step.lower():
                sort_contacts('/data/contacts.json', '/data/contacts-sorted.json')
            elif "markdown" in step.lower():
                create_markdown_index('/data/docs', '/data/docs/index.json')
            elif "extract email" in step.lower():
                extract_sender_email('/data/email.txt', '/data/email-sender.txt')
            elif "credit card" in step.lower():
                extract_credit_card('/data/credit-card.png', '/data/credit-card.txt')
            elif "similar comments" in step.lower():
                find_most_similar_comments('/data/comments.txt', '/data/comments-similar.txt')
            elif "ticket sales" in step.lower():
                calculate_gold_ticket_sales('/data/ticket-sales.db', '/data/ticket-sales-gold.txt')
        return "Task executed successfully"

agent = TaskAgent()

@app.route('/run', methods=['POST'])
def run_task():
    task = request.args.get('task')
    if not task:
        return jsonify({"error": "No task provided"}), 400
    try:
        result = agent.execute_task(task)
        return jsonify({"message": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/read', methods=['GET'])
def read_file():
    path = request.args.get('path')
    if not path:
        return jsonify({"error": "No file path provided"}), 400
    try:
        with open(path, 'r') as file:
            content = file.read()
        return content, 200
    except FileNotFoundError:
        return "", 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
