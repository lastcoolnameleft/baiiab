#!/usr/local/opt/python/libexec/bin/python

from tenacity import retry, stop_after_attempt, wait_random
import os, openai, sys
from dotenv import load_dotenv

load_dotenv()
DEPLOYMENT_NAME = 'text-davinci-003' #'text-davinci-003'
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_ENDPOINT") # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
openai.api_type = 'azure'
openai.api_version = '2023-05-15' # this may change in the future

def generate_prompt():
    return "You are an absurd robot.  Give me some silly advice"
    #return "You are a bad advice robot. Give me a single, short, absurd, bad advice.  For example: 'Swim in jelly!' or 'Eat a porcupine'"
    # pretty good + text-davinci-003: return "Give me a single, short, weird, bad advice" 

@retry(stop=stop_after_attempt(5), wait=wait_random(min=1, max=2))
def create_oai_completion(prompt):
    print(prompt)
    response = openai.Completion.create(
        engine=DEPLOYMENT_NAME,
        prompt=prompt,
        temperature=1.3,
        max_tokens=100
    )
    print(response, flush=True)
    result = self.cleanse_advice(response.choices[0].text) 
    if not result:
        raise Exception
    return result

def generate_and_print_bad_advice(prompt = None):
    if not prompt:
        prompt = generate_prompt()
    advice = create_oai_completion(prompt)
    print(advice)

@retry(stop=stop_after_attempt(5), wait=wait_random(min=1, max=2))
def create_oai_chat_completion():
    response = openai.ChatCompletion.create(
        engine="gpt-35-turbo", # engine = "deployment_name".
        messages=[
            {"role": "system", "content": "You are an unhelpful assistant that gives a single, short, absurd, bad advice."},
            {"role": "user", "content": "Give me some advice"},
            {"role": "assistant", "content": "Swim in jelly!"},
            {"role": "user", "content": "Give me some more advice"},
            {"role": "assistant", "content": "Eat a porcupine"},
            {"role": "user", "content": "Give me one piece of advice"}
        ],
        temperature=2
    )
    print(response, flush=True)
    result = response.choices[0].message.content.strip()
    if not result:
        raise Exception
    return result

prompt = sys.argv[1] if len(sys.argv) >= 2 else None
#print(create_oai_chat_completion())
generate_and_print_bad_advice(prompt)