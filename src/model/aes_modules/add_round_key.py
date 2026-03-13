import src.model.abstract_algebra as aa


def add_round_key(state, key):
    return aa.xor_matrix(state, key)