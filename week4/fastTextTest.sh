# Train model
~/fastText-0.9.2/fasttext supervised -input /workspace/datasets/labeled_train.txt -output model_label
~/fastText-0.9.2/fasttext test model_label.bin /workspace/datasets/labeled_test.txt
~/fastText-0.9.2/fasttext test model_label.bin /workspace/datasets/labeled_test.txt 3
~/fastText-0.9.2/fasttext test model_label.bin /workspace/datasets/labeled_test.txt 5

# Increase number of epochs to 25
echo "EPOCH 25"
~/fastText-0.9.2/fasttext supervised -input /workspace/datasets/labeled_train.txt -output model_label -epoch 25
~/fastText-0.9.2/fasttext test model_label.bin /workspace/datasets/labeled_test.txt
~/fastText-0.9.2/fasttext test model_label.bin /workspace/datasets/labeled_test.txt 3
~/fastText-0.9.2/fasttext test model_label.bin /workspace/datasets/labeled_test.txt 5

# Increase number of epochs to 25 and LR to 0.4
echo "EPOCH 25 LR 0.4"
~/fastText-0.9.2/fasttext supervised -input /workspace/datasets/labeled_train.txt -output model_label -lr 0.4 -epoch 25
~/fastText-0.9.2/fasttext test model_label.bin /workspace/datasets/labeled_test.txt
~/fastText-0.9.2/fasttext test model_label.bin /workspace/datasets/labeled_test.txt 3
~/fastText-0.9.2/fasttext test model_label.bin /workspace/datasets/labeled_test.txt 5

# Increase number of epochs to 25 and LR to 0.4
echo "EPOCH 25 LR 0.4 ngram 2"
~/fastText-0.9.2/fasttext supervised -input /workspace/datasets/labeled_train.txt -output model_label -epoch 25 -lr 0.4 -wordNgrams 2
~/fastText-0.9.2/fasttext test model_label.bin /workspace/datasets/labeled_test.txt
~/fastText-0.9.2/fasttext test model_label.bin /workspace/datasets/labeled_test.txt 3
~/fastText-0.9.2/fasttext test model_label.bin /workspace/datasets/labeled_test.txt 5