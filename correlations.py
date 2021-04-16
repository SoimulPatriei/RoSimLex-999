
"""The script computes the correlations reported in the paper"""

"""Run the script:
python correlations.py --scores Data/RoSimLex-Final.txt --results results_corr.txt
"""

__author__ = "Eduard Barbu"
__license__ = "LGPL"
__version__ = "1.0.0"
__maintainer__ = "Eduard Barbu"


from scipy.stats import spearmanr
import logging
import argparse
import sys


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


def compute_p_correlation(f_input, index_1, index_2, my_pos=""):

    x_human = []
    x_pred = []
    n_correlated = 0

    fi = open(f_input, mode='r', encoding='utf-8')
    fi.readline()
    for line in fi:
        line = line[:-1]
        components = line.split("\t")
        if my_pos:
            if components[0] != my_pos:
                continue
        if components[5] == "1" and components[index_1] and components[index_2]:
            x_human.append(float(components[index_1]))
            x_pred.append(float(components[index_2]))
            n_correlated += 1
    corr_coef, p = spearmanr(x_human, x_pred)
    fi.close()
    return n_correlated, round(corr_coef, 2)


def get_correlations(f_input, index_1, index_2, logger):

    n_correlated, corr_coef = compute_p_correlation(f_input, index_1,  index_2)
    logger.info("Total:" + str(n_correlated))
    logger.info("Spearman:" + str(corr_coef))
    logger.info("-----------------------------")

    # adjective
    n_correlated, corr_coef = compute_p_correlation(f_input, index_1,  index_2, "A")
    logger.info("Adjectives:" + str(n_correlated))
    logger.info("Spearman:" + str(corr_coef))
    logger.info("-----------------------------")

    # nouns
    n_correlated, corr_coef = compute_p_correlation(f_input, index_1, index_2, "N")
    logger.info("Nouns:" + str(n_correlated))
    logger.info("Spearman:" + str(corr_coef))
    logger.info("------------------------------")

    # verbs
    n_correlated, corr_coef = compute_p_correlation(f_input, index_1, index_2, "V")
    logger.info("Verbs:" + str(n_correlated))
    logger.info("Spearman:" + str(corr_coef))


def get_corola_correlations(f_input,logger,dict_index_scores):

    logger.info("ro_human_scores=> corola_400_5")
    get_correlations(f_input, dict_index_scores["ro_human_scores"], dict_index_scores["corola_400_5"], logger)
    logger.info("**************************************")
    logger.info("en_human_scores=> corola_400_5")
    get_correlations(f_input, dict_index_scores["en_human_scores"], dict_index_scores["corola_400_5"], logger)
    logger.info("**************************************")

    logger.info("ro_human_scores=> corola_300_20")
    get_correlations(f_input, dict_index_scores["ro_human_scores"], dict_index_scores["corola_300_20"], logger)
    logger.info("**************************************")
    logger.info("en_human_scores=> corola_300_20")
    get_correlations(f_input, dict_index_scores["en_human_scores"], dict_index_scores["corola_300_20"], logger)
    logger.info("**************************************")


def get_facebook_correlations(f_input, logger, dict_index_scores):

    logger.info("ro_human_scores=> facebook")
    get_correlations(f_input, dict_index_scores["ro_human_scores"], dict_index_scores["facebook"], logger)
    logger.info("**************************************")
    logger.info("en_human_scores=> facebook")
    get_correlations(f_input, dict_index_scores["en_human_scores"], dict_index_scores["facebook"], logger)
    logger.info("**************************************")


def get_conll_correlations(f_input, logger, dict_index_scores):
    logger.info("ro_human_scores=> conll_2017")
    get_correlations(f_input, dict_index_scores["ro_human_scores"], dict_index_scores["conll_2017"], logger)
    logger.info("**************************************")
    logger.info("en_human_scores=> conll_2017")
    get_correlations(f_input, dict_index_scores["en_human_scores"], dict_index_scores["conll_2017"], logger)
    logger.info("**************************************")


def get_wordnet_ro_correlations (f_input, logger, dict_index_scores):
    logger.info("ro_human_scores=> wordnet[path][ro]")
    get_correlations(f_input, dict_index_scores["ro_human_scores"], dict_index_scores["path_ro"], logger)
    logger.info("**************************************")
    logger.info("en_human_scores=> wordnet[path][ro]")
    get_correlations(f_input, dict_index_scores["en_human_scores"], dict_index_scores["path_ro"], logger)
    logger.info("**************************************")

    logger.info("ro_human_scores=> wordnet[lch][ro]")
    get_correlations(f_input, dict_index_scores["ro_human_scores"], dict_index_scores["lch_ro"], logger)
    logger.info("**************************************")
    logger.info("en_human_scores=> wordnet[lch][ro]")
    get_correlations(f_input, dict_index_scores["en_human_scores"], dict_index_scores["lch_ro"], logger)
    logger.info("**************************************")

    logger.info("ro_human_scores=> wordnet[wup][ro]")
    get_correlations(f_input, dict_index_scores["ro_human_scores"], dict_index_scores["wup_ro"], logger)
    logger.info("**************************************")
    logger.info("en_human_scores=> wordnet[wup][ro]")
    get_correlations(f_input, dict_index_scores["en_human_scores"], dict_index_scores["wup_ro"], logger)
    logger.info("**************************************")


def get_wordnet_en_correlations(f_input, logger, dict_index_scores):
    logger.info("ro_human_scores=> wordnet[path][en]")
    get_correlations(f_input, dict_index_scores["ro_human_scores"], dict_index_scores["path_en"], logger)
    logger.info("**************************************")
    logger.info("en_human_scores=> wordnet[path][en]")
    get_correlations(f_input, dict_index_scores["en_human_scores"], dict_index_scores["path_en"], logger)
    logger.info("**************************************")

    logger.info("ro_human_scores=> wordnet[lch][en]")
    get_correlations(f_input, dict_index_scores["ro_human_scores"], dict_index_scores["lch_en"], logger)
    logger.info("**************************************")
    logger.info("en_human_scores=> wordnet[lch][en]")
    get_correlations(f_input, dict_index_scores["en_human_scores"], dict_index_scores["lch_en"], logger)
    logger.info("**************************************")

    logger.info("ro_human_scores=> wordnet[wup][en]")
    get_correlations(f_input, dict_index_scores["ro_human_scores"], dict_index_scores["wup_en"], logger)
    logger.info("**************************************")
    logger.info("en_human_scores=> wordnet[wup][en]")
    get_correlations(f_input, dict_index_scores["en_human_scores"], dict_index_scores["wup_en"], logger)
    logger.info("**************************************")


def get_human_correlations (f_input, logger, dict_index_scores) :
    logger.info("en_human_scores=> ro_human_scores")
    get_correlations(f_input, dict_index_scores["en_human_scores"], dict_index_scores["ro_human_scores"], logger)
    logger.info("**************************************")


def compute_correlations(f_input):
    """Compute all correlations we need for the paper"""

    dict_index_scores = {"en_human_scores": 8, "ro_human_scores": 9,
                        "ro_specialists": 10, "corola_400_5": 11,
                        "corola_300_20": 12, "facebook": 13,
                         "conll_2017": 14, "path_ro": 15,
                         "lch_ro": 16, "wup_ro": 17,
                         "path_en": 18, "lch_en": 19, "wup_en": 20}

    logger = logging.getLogger("correlations")

    get_human_correlations(f_input, logger, dict_index_scores)
    get_corola_correlations(f_input, logger, dict_index_scores)
    get_facebook_correlations(f_input, logger, dict_index_scores)
    get_conll_correlations(f_input, logger, dict_index_scores)
    get_wordnet_ro_correlations(f_input, logger, dict_index_scores)
    get_wordnet_en_correlations(f_input, logger, dict_index_scores)


def main():

    parser = argparse.ArgumentParser(
        description='Compute the correlations between human similarity scores and machine similarity')
    parser.add_argument("--scores", type=str, help="The file containing the similarity scores")
    parser.add_argument("--results", type=str, help="The file the results are written")

    args = parser.parse_args()
    if not (args.scores and args.results):
        print("Wrong arguments!")
        sys.exit()

    init_logger(args.results)
    compute_correlations(args.scores)


if __name__ == '__main__':
    main()
