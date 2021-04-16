
from nltk.corpus import wordnet as englishwordnet


def get_synsets(word, pos):
    synset_list = []
    for synset in englishwordnet.synsets(word):
        if synset.pos() == pos:
            synset_list.append(synset)
    return synset_list


def get_similarity(wd_dict, pos, f_name):

    synsets_word_1 = get_synsets(wd_dict["word_1"], pos)
    synsets_word_2 = get_synsets(wd_dict["word_2"], pos)

    n_computations = len(synsets_word_1) * len(synsets_word_2)

    f_call = getattr(englishwordnet, f_name)

    max_similarity = 0
    for synset_1 in synsets_word_1:
        for synset_2 in synsets_word_2:
            similarity = f_call(synset_1, synset_2)
            if similarity > max_similarity:
                max_similarity = similarity
                wd_dict[f_name] = round(max_similarity, 2)
                wd_dict[f_name + "_synset_1"] = ",".join(synset_1.lemma_names())
                wd_dict[f_name + "_synset_1_definition"] = synset_1.definition()
                wd_dict[f_name + "_synset_2"] = ",".join(synset_2.lemma_names())
                wd_dict[f_name + "_synset_2_definition"] = synset_2.definition()
    return n_computations
