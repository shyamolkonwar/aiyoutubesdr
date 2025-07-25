import os
import json
from openai import OpenAI

class LLM:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
        self.model_name = "deepseek-chat"

    def plan_next_action(self, observation, goal, collected_data):
        prompt = f"""You are a web scraping assistant.
Goal: {goal}

Required Data Points for Goal: channel name, description, latest video title, latest video description.

Collected Data So Far: {json.dumps(collected_data, indent=2)}

Analyze the following observation from the current webpage and decide the next action. Your goal is to collect all the necessary information efficiently.

If all Required Data Points are present in 'Collected Data So Far', your next action MUST be 'STOP'.
Otherwise, decide the next action to collect the missing information.

Observation:
```html
{observation}
```

What is the next single action to take? Your response must be a single line with one of the following commands:

- `CLICK [selector]` - to click on an element. Use simple CSS selectors like 'div.some-class', 'a#some-id', or 'button[name="some-name"]'. Avoid complex or nested selectors.
- `SCROLL` - to scroll down the page.
- `EXTRACT [data_to_extract]` - to extract specific information from the observation. (e.g., EXTRACT channel name, EXTRACT latest video title and description)
- `STOP` - if you have collected all the required information.

Your Answer:"""

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            stream=False
        )
        return response.choices[0].message.content

    def extract_data(self, html_chunk, data_to_extract):
        prompt = f"""From the following HTML snippet, extract the {data_to_extract}. Return the data in JSON format. Ensure the output is ONLY the JSON object, with no additional text or formatting.

HTML:
```html
{html_chunk}
```

JSON Output:"""
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            stream=False
        )
        raw_content = response.choices[0].message.content.strip()
        # Remove markdown code block if present
        if raw_content.startswith('```json') and raw_content.endswith('```'):
            raw_content = raw_content[len('```json'):-len('```')].strip()
        
        try:
            return json.loads(raw_content)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            print(f"Raw LLM response: {raw_content}")
            return {} # Return empty dict if JSON extraction fails

    def generate_email(self, context, service_to_sell=None, template_content=None):
        if template_content:
            from utils.template_engine import fill_template
            return fill_template(template_content, context, service_to_sell)
        
        prompt = f"""Based on the following information, write a personalized sales email:

Channel Name: {context.get('channel_name')}
About: {context.get('about')}
Latest Video Title: {context.get('latest_video_title')}
Latest Video Description: {context.get('video_description')}

Use the provided email template.
"""

        with open("templates/email_template.txt", "r") as f:
            template = f.read()

        prompt += f"\nEmail Template:\n{template}"

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            stream=False
        )
        return response.choices[0].message.content
