
SAMPLE_RATE=0.3
INPUT_FILE="/workspace/datasets/fasttext/titles.txt"
OUTPUT="/workspace/datasets/fasttext/title_model"

echo "Extracting titles"
python week3/extractTitles.py --sample_rate $SAMPLE_RATE
if [ $? -ne 0 ] ; then
  exit 2
fi
echo "Training the model"
~/fastText-0.9.2/fasttext skipgram -input $INPUT_FILE -output $OUTPUT -minCount 50
if [ $? -ne 0 ] ; then
  exit 2
fi
echo "Running Test nn queries on model"
python week3/test_syn.py --model $OUTPUT.bin