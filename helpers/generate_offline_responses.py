#!/usr/local/opt/python/libexec/bin/python

from ast import literal_eval
import json, sys
from pathlib import Path
from dotenv import load_dotenv
from os.path import exists

sys.path.append(str(Path(f"{__file__}").parent.parent))
from Baiiab import Baiiab

load_dotenv()

menu_file = "conf/menu.json"
offline_file = "conf/offline_advice_2.json"
batch_count = 20

with open(menu_file,"r") as f:
    menu_data = literal_eval(f.read())
# Override if I just want to generate one
menu_data = { 'insult': { "Shakespeare": "Give me a Shakespeare style of insult." }}

offline_responses = {}
if (exists(offline_file)):
    with open(offline_file,"r") as f:
        offline_responses = literal_eval(f.read())

baiiab = Baiiab()

for topic in menu_data:
    for subtopic in menu_data[topic]:
        prompt = menu_data[topic][subtopic]

        offline_file = baiiab.get_offline_location(topic, subtopic)
        with open(offline_file,"r") as f:
            offline_responses = literal_eval(f.read())

        for i in range(batch_count):
            try:
                advice = baiiab.create_oai_completion(prompt)
                offline_responses.append(advice)
            except:
                print("GOT EXCEPTION")

        with open(offline_file, "w") as outfile:
            # json_data refers to the above JSON
            json.dump(offline_responses, outfile, sort_keys=True, indent=4)
