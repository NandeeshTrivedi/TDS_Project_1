import os
import requests

os.environ['AIPROXY_TOKEN'] = 'eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjMwMDIzMTZAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.DvLFDgvuV6vp37Tp89HhU-8vYu2FZCTXovK7U6oyjT8'

def extract_sender_email(input_file, output_file):
    # Read the email content
    with open(input_file, 'r') as f:
        email_content = f.read()

    # Set up the API request
    api_url = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.environ['AIPROXY_TOKEN']}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Extract the sender's email address from the given email content. Respond with only the email address."},
            {"role": "user", "content": email_content}
        ]
    }

    # Make the API request
    response = requests.post(api_url, headers=headers, json=data)
    
    # Extract the email address from the response
    try:
        sender_email = response.json()['choices'][0]['message']['content'].strip()
    except (KeyError, IndexError):
        print("Error: Unable to extract email address from API response")
        return

    # Write the extracted email address to the output file
    with open(output_file, 'w') as f:
        f.write(sender_email)

    print(f"Sender's email address extracted and written to {output_file}")