import os
import requests
import base64

os.environ['AIPROXY_TOKEN'] = 'eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjMwMDIzMTZAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.DvLFDgvuV6vp37Tp89HhU-8vYu2FZCTXovK7U6oyjT8'

def extract_credit_card(image_path, output_file):
    # Read and encode the image
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    # Set up the API request
    api_url = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.environ['AIPROXY_TOKEN']}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Extract the credit card number from the given image. Respond with only the number, without spaces."},
            {"role": "user", "content": f"[IMAGE]{encoded_image}[/IMAGE]"}
        ]
    }

    # Make the API request
    response = requests.post(api_url, headers=headers, json=data)
    
    # Extract the credit card number from the response
    try:
        credit_card_number = response.json()['choices'][0]['message']['content'].strip()
        # Remove any spaces from the extracted number
        credit_card_number = credit_card_number.replace(" ", "")
    except (KeyError, IndexError):
        print("Error: Unable to extract credit card number from API response")
        return

    # Write the extracted credit card number to the output file
    with open(output_file, 'w') as f:
        f.write(credit_card_number)

    print(f"Credit card number extracted and written to {output_file}")
