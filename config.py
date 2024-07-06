MODEL_DIR = r'D:/Users/17614/PycharmProjects/BiLSTM_CRF_NER/output/'

ORIGIN_DIR = './input/origin/'
ANNOTATION_DIR = './output/annotation/'

TRAIN_SAMPLE_PATH = 'output/train_data.txt'
TEST_SAMPLE_PATH = 'output/test_data.txt'
# TRAIN_SAMPLE_PATH = r'D:\QA_train\QA\wordtag.txt'
# TEST_SAMPLE_PATH = r'D:\QA_train\QA\wordtag.txt'

VOCAB_PATH = MODEL_DIR+'vocab.txt'
LABEL_PATH = MODEL_DIR+'tags.txt'
# LABEL_PATH = './output/tag.txt'

WORD_PAD = '<PAD>'
WORD_UNK = '<UNK>'

WORD_PAD_ID = 0
WORD_UNK_ID = 1
LABEL_O_ID = 0

VOCAB_SIZE = 3000
# EMBEDDING_DIM = 1200
# EMBEDDING_DIM2 = 1000
# HIDDEN_SIZE = 600
# TARGET_SIZE = 6
# LR = 0.0001

EMBEDDING_DIM = 768
HIDDEN_SIZE = 328
EMBEDDING_DIM2 = 328
EMBEDDING_DIM3 = 128
TARGET_SIZE = 7
LR = 0.0001
EPOCH = 100


