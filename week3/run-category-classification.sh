
MIN_PRODUCTS=200
TRAIN_FILE="/workspace/datasets/categories/train.csv"
TEST_FILE="/workspace/datasets/categories/test.csv"
MODEL_OUTPUT="/workspace/datasets/categories/categories_model"
LEARNING_RATE=1.0
EPOCH=25
WORD_GRAMS=2

python week3/createContentTrainingData.py --min_products $MIN_PRODUCTS
if [ $? -ne 0 ] ; then
  exit 2
fi
python week3/create_train_test_cats.py
if [ $? -ne 0 ] ; then
  exit 2
fi
~/fastText-0.9.2/fasttext supervised -input $TRAIN_FILE -output $MODEL_OUTPUT -lr $LEARNING_RATE -epoch $EPOCH -wordNgrams $WORD_GRAMS
if [ $? -ne 0 ] ; then
  exit 2
fi
~/fastText-0.9.2/fasttext test $MODEL_OUTPUT.bin $TEST_FILE