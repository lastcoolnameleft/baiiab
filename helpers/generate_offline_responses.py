#!/usr/local/opt/python/libexec/bin/python

from ast import literal_eval
import json, sys, os
from pathlib import Path
from dotenv import load_dotenv
from os.path import exists
from openai import AzureOpenAI

sys.path.append(str(Path(f"{__file__}").parent.parent))
from Baiiab import Baiiab

load_dotenv()

menu_file = "conf/menu.json"
batch_count = 60
match_topic = 'Fake Facts'
match_subtopic = 'Darth Vader'

with open(menu_file,"r") as f:
    menu_data = literal_eval(f.read())
# Override if I just want to generate one


oai_client = AzureOpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
    api_version="2024-02-01",
    timeout=3.0,
)
azure_openai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

baiiab = Baiiab(None, oai_client)

for topic in menu_data:
    print(topic)
    if match_topic and topic != match_topic:
        continue
    for subtopic in menu_data[topic]:
        if match_subtopic and subtopic != match_subtopic:
            continue
        messages = menu_data[topic][subtopic]
        offline_file = baiiab.get_offline_location(topic, subtopic)
        print("processing " + offline_file)
        offline_responses = []
        
        if (exists(offline_file)):
            with open(offline_file,"r") as f:
                offline_responses = literal_eval(f.read())

        for i in range(batch_count):
            try:
                advice = baiiab.create_oai_chat_completion(messages, azure_openai_deployment)
                offline_responses.append(advice)
            except Exception as e:
                print("GOT EXCEPTION")
                print(e)

        with open(offline_file, "w") as outfile:
            # json_data refers to the above JSON
            json.dump(offline_responses, outfile, sort_keys=True, indent=4)
