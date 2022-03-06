import argparse
import os
import random
import xml.etree.ElementTree as ET
from pathlib import Path
from nltk.stem.snowball import SnowballStemmer
import pandas as pd
import re

max_depth = 2
category_dict = {}

def transform_name(product_name):
    lower_product = re.sub("[^0-9a-zA-Z]+", " ", product_name).lower()
    stemmer = SnowballStemmer("english")
    stemmed_product = " ".join((stemmer.stem(w) for w in lower_product.split()))
    return stemmed_product

categories_file = "/workspace/datasets/product_data/categories/categories_0001_abcat0010000_to_pcmcat99300050000.xml"

tree = ET.parse(categories_file)
root = tree.getroot()

for child in root:
    cat_path = child.find("path")
    cat_id = child.find("id").text
    category_dict[cat_id] = []
    for cat in cat_path:
        category_dict[cat_id].append(cat.find("id").text)
# Directory for product data
directory = r'/workspace/search_with_machine_learning_course/data/pruned_products/'

parser = argparse.ArgumentParser(description='Process some integers.')
general = parser.add_argument_group("general")
general.add_argument("--input", default=directory,  help="The directory containing product data")
general.add_argument("--output", default="/workspace/datasets/fasttext/output.fasttext", help="the file to output to")

# Consuming all of the product data will take over an hour! But we still want to be able to obtain a representative sample.
general.add_argument("--sample_rate", default=1.0, type=float, help="The rate at which to sample input (default is 1.0)")

#Setting min_products removes infrequent categories and makes the classifier's task easier.
general.add_argument("--min_products", default=0, type=int, help="The minimum number of products per category (default is 0).")

args = parser.parse_args()
output_file = args.output
path = Path(output_file)
output_dir = path.parent
if os.path.isdir(output_dir) == False:
        os.mkdir(output_dir)

if args.input:
    directory = args.input
# IMPLEMENT:  Track the number of items in each category and only output if above the min
min_products = args.min_products
sample_rate = args.sample_rate

print("Writing results to %s" % output_file)
with open(output_file, 'w') as output:
    for filename in os.listdir(directory):
        if filename.endswith(".xml"):
            print("Processing %s" % filename)
            f = os.path.join(directory, filename)
            tree = ET.parse(f)
            root = tree.getroot()
            for child in root:
                if random.random() > sample_rate:
                    continue
                # Check to make sure category name is valid
                if (child.find('name') is not None and child.find('name').text is not None and
                    child.find('categoryPath') is not None and len(child.find('categoryPath')) > 0 and
                    child.find('categoryPath')[len(child.find('categoryPath')) - 1][0].text is not None):
                      # Choose last element in categoryPath as the leaf categoryId
                      cat = child.find('categoryPath')[len(child.find('categoryPath')) - 1][0].text
                      if cat in category_dict:
                          cat = category_dict[cat][max_depth] if len(category_dict[cat]) > max_depth else cat
                      # Replace newline chars with spaces so fastText doesn't complain
                      name = child.find('name').text.replace('\n', ' ')
                      output.write("__label__%s\t%s\n" % (cat, transform_name(name)))

#Updating min_products
data = pd.read_csv(output_file, delimiter="\t", names=["categories", "products"])
data = data.groupby(["categories"]).filter(lambda x: len(x) >= min_products)
data.to_csv(output_file, sep="\t",header=False, index=False)