"""
Compute the cosine similarity between the word pairs in RoSimlex-999 in different corpora models
"""

"""Run the script:
python corpus-cosine_embeddings.py
"""


__author__ = "Eduard Barbu"
__license__ = "LGPL"
__version__ = "1.0.0"
__maintainer__ = "Eduard Barbu"



from gensim.models import KeyedVectors
from gensim.models.wrappers import FastText
import logging


def init_logger(logging_file):
    """Init the logger for the console and logging file"""

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename=logging_file,
                        filemode='w')

    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format

    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)


def _replace(wd, particule):

    components = wd.split()
    if components[0] == particule:
        return " ".join(components[1:])
    return " ".join(components)


def replace_particule (line, particule):
    """Replace the particle"""

    components = line.split("\t")

    if components[-1] == "???":
        components[-3] = _replace(components[-3], particule)
        components[-2] = _replace(components[-2], particule)
    else:
        components[-2] = _replace(components[-2], particule)
        components[-1] = _replace(components[-1], particule)

    return "\t".join(components)


def _check_word2vec(word):
    try:
        current_model.get_vector(word)
    except KeyError:
        return 0
    return 1


def _check_fastext(word):

    if word in current_model.wv.vocab:
        return 1
    return 0


def check_exists(word, my_corpus):
    """If the embedding vector exists in the model or not"""

    if my_corpus == "Corola.300.20" or my_corpus == "Corola.400.5" or my_corpus == "CONLL2017-Word2vec":
        return _check_word2vec(word)
    return _check_fastext(word)


def get_model(my_corpus, f_embeddings):
    """Get the appropriate model for the corpus"""

    global current_model

    f_output = ""
    if my_corpus == "Corola.300.20" :
        current_model = KeyedVectors.load_word2vec_format(f_embeddings, binary=False)
        f_output = "Corola.300.20-cosine_similarity.txt"

    elif my_corpus == "Corola.400.5":
        current_model = KeyedVectors.load_word2vec_format(f_embeddings, binary=False)
        f_output = "Corola.400.5-cosine_similarity.txt"

    elif my_corpus == "Facebook":
        current_model = FastText.load_fasttext_format(f_embeddings)
        f_output = "Facebook-cosine_similarity.txt"

    elif my_corpus == "CONLL2017-Word2vec":
        current_model = KeyedVectors.load_word2vec_format(f_embeddings, binary=True)
        f_output = "CONLL22017-Word2Vec-cosine_similarity.txt"
    return f_output


def compute_cosine_similarity(f_translations, f_embeddings, my_corpus):
    """Compute cosine similarity of the words in the set using my_corpus embeddings"""

    logger = logging.getLogger("compute_cosine_similarity")

    logger.info("Load Model => "+my_corpus)
    f_output = get_model(my_corpus, f_embeddings)
    logger.info("Model loaded")

    fo = open(f_output, mode='w', encoding='utf-8')

    fi = open(f_translations, mode='r', encoding='utf-8')
    fi.readline()

    for line in fi:

        line = line.rstrip()
        line = replace_particule(line, "se")
        components = line.split("\t")

        word1 = components[0]
        word2 = components[1]
        if components[5] != "1":
            exists1 = check_exists(word1, my_corpus)
            exists2 = check_exists(word2, my_corpus)
            similarity = "null"
            if exists1 and exists2:
                similarity = round(current_model.similarity(word1, word2),2)
            fo.write(str(exists1)+"\t"+str(exists2)+"\t"+str(similarity)+"\n")
        else:
            fo.write("0\t0\tnull\n")
    fi.close()
    fo.close()


def main():

    logging_file = "compute_cosine_similarity.log"
    init_logger(logging_file)
    logger = logging.getLogger("main")

    f_translations = "Data/RoSimLex-Final.txt"
    f_embeddings = "Embeddings/CONLL2017_Word2vec/model.bin"
    compute_cosine_similarity(f_translations, f_embeddings, "CONLL2017-Word2vec")
    logger.info("Cosine Similarity computed for CONLL 2017 Word2vec Training Embeddings\n")

    f_embeddings = "Embeddings/Facebook/cc.ro.300.bin"
    compute_cosine_similarity(f_translations, f_embeddings, "Facebook")
    logger.info("Cosine Similarity computed for Facebook Fastext Training Embeddings\n")

    f_embeddings = "Embeddings/Corola/corola.300.20.vec"
    compute_cosine_similarity(f_translations, f_embeddings, "Corola.300.20")
    logger.info("Cosine Similarity computed for Corola (300.20) Word2vec Training Embeddings\n")

    f_embeddings = "Embeddings/Corola/corola.400.5.vec"
    compute_cosine_similarity(f_translations, f_embeddings, "Corola.400.5")
    logger.info("Cosine Similarity computed for Corola (400.5) Word2vec Training Embeddings\n")

    logger.info("End")


if __name__ == '__main__':
    main()
