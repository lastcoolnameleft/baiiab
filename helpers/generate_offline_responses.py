#!/usr/local/opt/python/libexec/bin/python

from ast import literal_eval
import json, sys, os
from pathlib import Path
from dotenv import load_dotenv
from os.path import exists
from openai import AzureOpenAI

sys.path.append(str(Path(f"{__file__}").parent.parent))
from Baiiab import Baiiab
import argparse

load_dotenv()

menu_file = "conf/menu.json"
batch_count = 60
parser = argparse.ArgumentParser(description="Generate offline responses.")
parser.add_argument("match_topic", type=str, nargs="?", help="Specify the topic to match.")
parser.add_argument("match_subtopic", type=str, nargs="?", help="Specify the subtopic to match.")
parser.add_argument("batch_count", type=int, nargs="?", help="Specify the number of responses to generate.")
parser.add_argument("-s", "--save", help="Save the generated responses to a file.", action="store_true")
parser.add_argument("-m", "--menu", help="Show the menu", action="store_true")

args = parser.parse_args()

match_topic = args.match_topic
match_subtopic = args.match_subtopic
batch_count = args.batch_count if args.batch_count else batch_count
is_save = args.save
is_menu = args.menu

# Load menu data to validate the inputs
with open(menu_file, "r") as f:
    menu_data = literal_eval(f.read())

if is_menu:
    print("Menu:")
    for topic in menu_data:
        print("* " + topic)
        for subtopic in menu_data[topic]:
            print("    * " + subtopic)
    sys.exit(0)

if not match_topic and not match_subtopic:
    sys.exit("Error: Please provide at least a topic or subtopic to match.")

if not match_topic or match_topic not in menu_data:
    sys.exit(f"Error: The topic '{match_topic}' is not valid or not provided. Please provide a valid topic from the menu.json file.")

if not match_subtopic or match_subtopic not in menu_data.get(match_topic, {}):
    sys.exit(f"Error: The subtopic '{match_subtopic}' is not valid or not provided. Please provide a valid subtopic for the topic '{match_topic}' from the menu.json file.")

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
    if match_topic and topic != match_topic:
        continue
    for subtopic in menu_data[topic]:
        if match_subtopic and subtopic != match_subtopic:
            continue
        messages = menu_data[topic][subtopic]
        offline_file = baiiab.get_offline_location(topic, subtopic)
        print("processing " + offline_file)
        offline_responses = []
        
        if is_save:
            if (exists(offline_file)):
                with open(offline_file,"r") as f:
                    offline_responses = literal_eval(f.read())

        for i in range(batch_count):
            try:
                advice = baiiab.create_oai_chat_completion(messages, azure_openai_deployment)
                if not is_save:
                    print(advice)
                else:
                    offline_responses.append(advice)
            except Exception as e:
                print("GOT EXCEPTION")
                print(e)

        if is_save:
            with open(offline_file, "w") as outfile:
                # json_data refers to the above JSON
                json.dump(offline_responses, outfile, sort_keys=True, indent=4)
