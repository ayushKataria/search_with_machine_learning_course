import argparse
import re

import fasttext

parser = argparse.ArgumentParser()
general = parser.add_argument_group("general")
general.add_argument("--model", default="/workspace/datasets/fasttext/title_model.bin",  help="The binary file location of the pre trained model")

args = parser.parse_args()
model_bin = args.model

model = fasttext.load_model(model_bin)

def transform_training_data(name):
    name = re.sub("[^0-9a-zA-Z]+", " ", name).lower()
    return name

test_dict = {
    "products": ["headphones", "mobile", "laptop", "mouse", "tablet"],
    "brands": ["apple", "sony", "blackberry", "android", "lenovo"],
    "models": ["iphone", "thinkpad", "xbox", "walkman", "playstation"],
    "attribs": ["black", "large", "12GB", "cheap", "best"]
}

for key, value in test_dict.items():
    print(f"TESTING {key}")
    for test in value:
        print(f"{test}: ")
        res = model.get_nearest_neighbors(transform_training_data(test))
        for nn in res:
            print(f"\t{nn[1]} {nn[0]}")
    print("___________________________________")
