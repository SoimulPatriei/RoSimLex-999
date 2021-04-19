
"""The script computes the correlations between Semantic Networks (Princeton Wordnet and Romanian Wordnet)
and the human scores"""

"""Run the script:
python wordnet_correlations.py
"""

__author__ = "Eduard Barbu"
__license__ = "LGPL"
__version__ = "1.0.0"
__maintainer__ = "Eduard Barbu"



from scipy.stats import spearmanr
import logging
import os


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


def get_pos_list(f_translations, indexes_list,  pos):

    index_wd_1, index_wd_2, index_pos, index_score = indexes_list
    fi = open(f_translations, mode='r', encoding='utf-8')
    fi.readline()
    pair_list = []
    for line in fi:
        line = line.rstrip()
        components = line.split("\t")
        if components[index_pos] == pos:
            pair_list.append({"word_1": components[index_wd_1], "word_2": components[index_wd_2],
                              "pos": pos, "score": components[index_score]})
    return pair_list


def scores(wd_dict, label_list, fo):
    sir = ""
    for label in label_list:
        if label in wd_dict:
            sir += str(wd_dict[label])+"\t"
    fo.write(sir[:-1]+"\n")
    components = sir[:-1].split("\t")
    return [components[0], components[1], components[2], components[-2], components[-1]]


def get_corr_scores (my_list, pos="all"):
    x_human = []
    x_pred = []
    for one_list in my_list:
        if pos == "all":
            x_human.append(float(one_list[-1]))
            x_pred.append(float(one_list[-2]))
        elif one_list[2].lower() == pos:
            x_human.append(float(one_list[-1]))
            x_pred.append(float(one_list[-2]))

    return x_human, x_pred


def correlations(my_list, my_measure):
    logger = logging.getLogger("correlations")

    x_human, x_pred = get_corr_scores(my_list)
    coef, p = spearmanr(x_human, x_pred)
    logger.info(f"{len(x_human)} {my_measure}:{round(coef,2)}")

    x_human, x_pred = get_corr_scores(my_list, "n")
    coef, p = spearmanr(x_human, x_pred)
    logger.info(f"{len(x_human)} {my_measure} Noun:{round(coef,2)}")

    x_human, x_pred = get_corr_scores(my_list, "v")
    coef, p = spearmanr(x_human, x_pred)
    logger.info(f"{len(x_human)} {my_measure} Verb:{round(coef,2)}")


def get_list(measure):
    return ["word_1", "word_2", "pos", f"{measure}_synset_1", f"{measure}_synset_2",
            f"{measure}_synset_1_definition", f"{measure}_synset_2_definition", f"{measure}",
            "score"]


def get_handle(output_dir, measure, l_code):

    return open(os.path.join(output_dir, f"{measure}_{l_code}.txt"), mode='w', encoding='utf-8')


def wordnet_correlations(d_parameters):

    init_logger(d_parameters["logging_file"])
    logger = logging.getLogger("main")

    import english_wordnet as wn
    if d_parameters["l_code"] == "ro":
        import romanian_wordnet as wn

    noun_list = get_pos_list(d_parameters["rosimlex_file"], d_parameters["indexes"], "N")
    verb_list = get_pos_list(d_parameters["rosimlex_file"], d_parameters["indexes"], "V")

    path_labels = get_list("path_similarity")
    fo_path = get_handle(d_parameters["output_dir"], "path", d_parameters["l_code"])

    lch_labels = get_list("lch_similarity")
    fo_lch = get_handle(d_parameters["output_dir"], "lch", d_parameters["l_code"])

    wup_labels = get_list("wup_similarity")
    fo_wup = get_handle(d_parameters["output_dir"], "wup", d_parameters["l_code"])

    path_list = []
    lch_list = []
    wup_list = []

    for wd_dict in noun_list:
        logger.info(wd_dict)
        if wn.get_similarity(wd_dict, "n", "path_similarity"):
            path_list.append(scores(wd_dict, path_labels, fo_path))
        else:
           logger.info("Not in wordnet")

        if wn.get_similarity(wd_dict, "n", "lch_similarity") :
            lch_list.append(scores(wd_dict, lch_labels, fo_lch))
        else:
            logger.info("Not in wordnet")

        if wn.get_similarity(wd_dict, "n", "wup_similarity") :
            wup_list.append(scores(wd_dict, wup_labels, fo_wup))
        else:
            logger.info("Not in wordnet")
    logger.info("Finished computing noun similarity")

    for wd_dict in verb_list:
        print(wd_dict)
        if wn.get_similarity(wd_dict, "v", "path_similarity"):
            path_list.append(scores(wd_dict, path_labels, fo_path))
        else:
            logger.info("Not in wordnet")

        if wn.get_similarity(wd_dict, "v", "lch_similarity"):
            lch_list.append(scores(wd_dict, lch_labels, fo_lch))
        else:
            logger.info("Not in wordnet")

        if wn.get_similarity(wd_dict, "v", "wup_similarity"):
            wup_list.append(scores(wd_dict,wup_labels, fo_wup))
        else:
            logger.info("Not in wordnet")
    logger.info("Finished computing verb similarity")

    fo_path.close()
    fo_lch.close()
    fo_wup.close()

    logger.info("Get correlations")
    correlations(path_list, "path_similarity")
    logger.info("----------------------------------------------")
    correlations(lch_list, "lch_similarity")
    logger.info("----------------------------------------------")
    correlations(wup_list, "wup_similarity")


def main():

    print("Get English synsets similarities and compute correlations")
    d_parameters_english = {
         "rosimlex_file": "Data/RoSimLex-Maximal.txt",
         "output_dir": "Results/Wordnet_Similarities",
         "logging_file": "english_wordnet_correlations.log",
          "l_code": "en",
          "indexes": [1, 2, 0, 8]
     }
    wordnet_correlations(d_parameters_english)
    print("End English computation")
    print("-----------------------------------------------------------------")

    print("Get Romanian synsets similarities and compute correlations")
    d_parameters_romanian = {
         "rosimlex_file": "Data/RoSimLex-Maximal.txt",
         "output_dir": "Results/Wordnet_Similarities",
         "logging_file": "romanian_wordnet_correlations.log",
         "l_code": "ro",
          "indexes": [3, 4, 0, 9]
      }
    wordnet_correlations(d_parameters_romanian)
    print("End Romanian computation")


if __name__ == '__main__':
    main()

