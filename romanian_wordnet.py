

import rowordnet
wn = rowordnet.RoWordNet()


def _get_synsets (word, pos):
    synset_list = []
    for synset_id in wn.synsets(word, strict=True):
        synset_pos = synset_id.split("-")[-1]
        if synset_pos == pos:
            synset_list.append(synset_id)
    return synset_list


def get_similarity(wd_dict, pos, f_name):
    synsets_ids_1 = _get_synsets(wd_dict["word_1"], pos)
    synsets_ids_2 = _get_synsets(wd_dict["word_2"], pos)
    max_similarity = 0

    n_computations = len(synsets_ids_1) * len(synsets_ids_2)

    f_call = getattr(wn, f_name)
    for synset_id_1 in synsets_ids_1:
        for synset_id_2 in synsets_ids_2:
            print(f"{synset_id_1} : {synset_id_2}")
            similarity = f_call(synset_id_1, synset_id_2)
            if similarity > max_similarity:
                max_similarity = similarity
                wd_dict[f_name] = round(max_similarity, 2)
                wd_dict[f_name + "_synset_1"] = ",".join(wn.synset(synset_id_1).literals)
                wd_dict[f_name + "_synset_1_definition"] = wn.synset(synset_id_1).definition
                wd_dict[f_name + "_synset_2"] = ",".join(wn.synset(synset_id_2).literals)
                wd_dict[f_name + "_synset_2_definition"] = wn.synset(synset_id_2).definition
    return n_computations
