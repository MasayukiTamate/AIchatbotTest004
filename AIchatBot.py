'''
import openai


openai.api_key = 

def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user", "content":prompt}]
    )

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    while True:
        user_input = input("YOU: ")
        if user_input.lower() in ["quit","exit", "bye"]:
            break

        response = chat_with_gpt(user_input)
        print("Chatbot: ", response)'''

'''
import openai
import OpenAI


def main():
    client = OpenAI(
         api_key=
    )
    messages = []

    while True:
        user_input = input("\n[Input](or 'exit'): ")
        if user_input.lower() == "exit":
            break

        messages.append({"role": "user", "content": user_input})
        completion = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=messages,
        )
        bot_response = completion.choices[0].message.content
        messages.append({"role": "assistant", "content": bot_response})

        print(bot_response)

if __name__ == "__main__":
    main()
'''

import os
import openai



class AIchatBotTest001:
    def __init__(self):
        
# APIキーの設定
#        openai.api_key = "sk-proj-9"
        pass

    def response(self,seikaku,mondai):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system","content":seikaku},
            {"role": "user", "content": mondai},
            {"role": "system","content":"教えることが楽しい風で"},
        ],
        )

    

        return response.choices[0]["message"]["content"].strip()

'''

from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)'''
'''
import argparse
import json
import os
#import readline
import threading
import time
import openai

class ANSIColor:
    RED = "\033[31m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    RESET = "\033[0m"
    BOLD = '\033[1m'

class Color:
    USER = ANSIColor.RED
    SYSTEM = ANSIColor.BLUE
    BOT = ANSIColor.GREEN

class Role:
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class OpenAIChatBot:
    def __init__(self, model_name="gpt-4-1106-preview"):
        self.client = OpenAI()
        self.model_name = model_name
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def get_bot_response(self, user_input):
        try:
            self.add_message(Role.USER, user_input)
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=self.messages,
            )
            bot_response = completion.choices[0].message.content
            self.add_message(Role.ASSISTANT, bot_response)
            return bot_response
        except Exception as e:
            print(f"{ANSIColor.RED}[Error]: {e}{ANSIColor.RESET}")
            return ""

class PreLoader:
    def __init__(self, folder_path, extensions):
        self.folder_path = folder_path
        self.extensions = extensions

    def combine_files(self):
        combined_text = ""
        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                if any(file.endswith(ext) for ext in self.extensions):
                    with open(os.path.join(root, file), 'r') as infile:
                        combined_text += f"// Begin of {file}\n{infile.read()}\n// End of {file}\n\n"
        return combined_text

class ChatLogger:
    def __init__(self, history_file='chatbot_history.json'):
        self.history_file = history_file

    def save_history(self, messages):
        with open(self.history_file, 'w') as file:
            json.dump(messages, file, ensure_ascii=False, indent=4)

    def print(self, color, message):
        print(f"\n{ANSIColor.BOLD}{color}{message}{ANSIColor.RESET}")

class Indicator:
    def __init__(self, sleep_time=0.2):
        self.sleep_time = sleep_time
        self.indicator_thread = threading.Thread(target=self.show_indicator)
        self.indicator_active = False
        self.indicators = ["-", "\\", "|", "/"]

    def start(self):
        self.indicator_active = True
        if not self.indicator_thread.is_alive():
            self.indicator_thread = threading.Thread(target=self.show_indicator)
            self.indicator_thread.start()

    def stop(self):
        self.indicator_active = False
        if self.indicator_thread.is_alive():
            self.indicator_thread.join()

    def show_indicator(self):
        elapsed_time = 0.0
        indicator_msg = ""
        i = 0
        while self.indicator_active:
            indicator_msg = f"{self.indicators[i % len(self.indicators)]} [Waiting Time]: {elapsed_time:.1f} seconds"
            print(f"\r{ANSIColor.BOLD}{Color.SYSTEM}{indicator_msg}{ANSIColor.RESET}", end="")
            time.sleep(self.sleep_time)
            elapsed_time += self.sleep_time
            i += 1
        print("\r" + " " * len(indicator_msg) + "\r", end="") # Clear Indicator

class Configuration:
    def __init__(self):
        self.api_key = self.get_env_variable("sk-proj-9")
        self.args = self.parse_command_line_arguments()

    def get_env_variable(self, var_name):
        try:
            return os.environ[var_name]
        except KeyError:
            raise SystemExit(f"{ANSIColor.RED}[Error]: Environment variable '{var_name}' is not set.{ANSIColor.RESET}")

    def parse_command_line_arguments(self):
        parser = argparse.ArgumentParser(description='Terminal interface for OpenAI Chatbot')
        parser.add_argument('--use-preload', action='store_true',
                            help='Please specify if you want to preload a specific file.')
        parser.add_argument('--path', type=str, default=".",
                            help='Path to the folder for preloading. Default is the current directory.[Example]: --path /path/to/directory')
        parser.add_argument('--ext', nargs='*', default=[".py"],
                            help='Specify multiple file extensions for preloading, separated by spaces. Default is ".py". [Example]: --ext .py .md .txt')
        return parser.parse_args()

class Chatbot:
    def __init__(self):
        self.config = Configuration()
        self.chatbot = OpenAIChatBot()
        self.preloader = PreLoader(folder_path=self.config.args.path, extensions=self.config.args.ext)
        self.logger = ChatLogger()
        self.indicator = Indicator()

    def wake_up(self):
        self.preload_if_needed()
        while True:
            if self.start_chat() == "exit":
                break

    def preload_if_needed(self):
        if self.config.args.use_preload:
            preload_text = self.preloader.combine_files()
            if preload_text:
                self.chatbot.add_message(Role.SYSTEM, preload_text)
            self.logger.print(Color.SYSTEM, f"[Preloaded char count]: {len(preload_text):,}")

    def start_chat(self):
        # Waiting User Input
        self.logger.print(Color.USER, "[User Input](or 'exit'): ")
        user_input = input().strip()
        if user_input.lower() == "exit":
            return user_input
        elif user_input == "":
            return user_input

        # Start Log
        start_time = time.time()
        self.logger.print(Color.SYSTEM, "[Bot Output]: ")

        # Get Response
        self.indicator.start()
        bot_response = self.chatbot.get_bot_response(user_input)
        self.indicator.stop()
        self.logger.print(Color.BOT, bot_response)

        # End Log
        response_time = time.time() - start_time
        self.logger.print(Color.SYSTEM, f"[Response Time]: {response_time:.2f} seconds")

        # Save History
        self.logger.save_history(self.chatbot.messages)

def main():
    chatbot = Chatbot()
    chatbot.wake_up()

if __name__ == "__main__":
    main()
'''