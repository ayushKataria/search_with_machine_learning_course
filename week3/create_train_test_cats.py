import pandas as pd

print("Reading label product data")
data = pd.read_csv("/workspace/datasets/fasttext/output.fasttext", delimiter="\t", names=["categories", "products"])

#Shuffling
print("Shuffling label product data")
data = data.sample(frac=1).reset_index(drop=True)

#Writing train data
print("Getting training data for category")
data.head(10000).to_csv("/workspace/datasets/categories/train.csv", sep="\t",header=False, index=False)
#Writing test data
print("Getting testing data for category")
data.tail(10000).to_csv("/workspace/datasets/categories/test.csv", sep="\t",header=False, index=False)
