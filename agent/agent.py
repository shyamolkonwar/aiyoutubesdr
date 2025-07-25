from browser_tools.browser import Browser
from llm_core.llm import LLM
import json
from bs4 import BeautifulSoup
import tiktoken

def chunk_html_by_sections(html, max_chars=2000):
    soup = BeautifulSoup(html, "html.parser")
    sections = soup.find_all(['section', 'div', 'article'])

    chunks = []
    current_chunk = ""
    for section in sections:
        text = section.get_text(separator=" ", strip=True)
        if len(current_chunk) + len(text) <= max_chars:
            current_chunk += "\n" + text
        else:
            chunks.append(current_chunk.strip())
            current_chunk = text
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def count_tokens(text):
    enc = tiktoken.encoding_for_model("gpt-4") # Using gpt-4 as a general model for token counting
    return len(enc.encode(text))

class Agent:
    def __init__(self, goal, service_to_sell=None, template_content=None):
        self.goal = goal
        self.service_to_sell = service_to_sell
        self.template_content = template_content
        self.browser = Browser()
        self.llm = LLM()
        self.memory = []
        self.collected_data = {}

    def run(self, start_url):
        self.browser.navigate(start_url)
        done = False
        while not done:
            observation = self.browser.get_visible_texts()
            thought = self.llm.plan_next_action(observation, self.goal, self.collected_data)
            action, result = self.execute(thought)
            self.memory.append((observation, action, result))
            if action == "STOP":
                done = True
        
        email = self.llm.generate_email(self.collected_data, self.service_to_sell, self.template_content)
        self.browser.close()
        return email

    def execute(self, thought):
        action, _, argument = thought.partition(' ')
        action = action.strip().replace('`', '')
        argument = argument.strip()

        if action == "CLICK":
            result = self.browser.click(argument)
        elif action == "SCROLL":
            result = self.browser.scroll_down()
        elif action == "EXTRACT":
            html_content = self.browser.get_visible_texts()
            
            # Safety check before chunking
            if count_tokens(html_content) > 30000: # for safety, keep under 30k
                print("HTML content is too long, chunking...")
                chunks = chunk_html_by_sections(html_content)
            else:
                chunks = [html_content]

            extracted_results = {}
            for i, chunk in enumerate(chunks):
                print(f"Processing chunk {i+1} with {len(chunk)} characters and {count_tokens(chunk)} tokens.")
                try:
                    data = self.llm.extract_data(chunk, argument)
                    extracted_results.update(data)
                except Exception as e:
                    print(f"Error extracting data from chunk {i+1}: {e}")
                    continue
            self.collected_data.update(extracted_results)
            result = f"Extracted data: {json.dumps(extracted_results)}"
        elif action == "STOP":
            result = "Stopping the agent."
        else:
            result = f"Unknown action: {action}"
        
        print(f"Action: {action}, Argument: {argument}, Result: {result}")
        return action, result