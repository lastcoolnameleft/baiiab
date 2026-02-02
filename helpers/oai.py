# python3 

from tenacity import retry, stop_after_attempt, wait_random
import os, sys, argparse
from dotenv import load_dotenv
from openai import AzureOpenAI

parser = argparse.ArgumentParser(
    prog='oai',
    description='Show top lines from each file')
parser.add_argument('system', type=str, help='System message')
parser.add_argument('prompt', type=str, help='Prompt message')
parser.add_argument('-d', '--deployment', type=str, default='gpt-4', help='Deployment name')
args = parser.parse_args()
print(args)

load_dotenv()

client = AzureOpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
    api_version="2024-02-01",
    timeout=3.0,
)

#@retry(stop=stop_after_attempt(5), wait=wait_random(min=1, max=2))
def create_oai_completion(client, prompt, deployment):
    print(prompt)
    response = client.completions.create(
        model=deployment,
        prompt=prompt,
        temperature=1.3,
        max_tokens=100
    )

    print(response, flush=True)
    #result = self.cleanse_advice(response.choices[0].text) 
    result = response.choices[0].text
    if not result:
        raise Exception
    return result

def generate_and_print_bad_advice(client, system, prompt, deployment):
    messages= [
        { "role": "system", "content": system },
        { "role": "user", "content": prompt }
    ]
    print(messages)
    advice = create_oai_chat_completion(client, messages, deployment)
    print()
    print(advice)

#@retry(stop=stop_after_attempt(5), wait=wait_random(min=1, max=2))
def create_oai_chat_completion(client, messages, deployment):
    response = client.chat.completions.create(
        model=deployment,
        messages=messages,
        max_tokens=100,
        temperature=1.2,
        top_p=0.95,
        frequency_penalty=0.37,
        presence_penalty=0.63,
        stop=None,
        stream=False
    )
    print(response, flush=True)
    result = response.choices[0].message.content.strip()
    if not result:
        raise Exception
    return result

generate_and_print_bad_advice(client, args.system, args.prompt, args.deployment)
