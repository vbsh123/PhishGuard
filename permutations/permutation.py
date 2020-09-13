from permutations.permutation_level_1 import permutation_1
from permutations.permutation_level_2 import permutation_2
from permutations.permutation_level_3 import permutation_3


def permutation_go(level, domain_name, suffix):
    if level == 1:
        return permutation_1(domain_name)
    if level == 2:
        return permutation_2(domain_name)
    if level == 3:
        return permutation_3(domain_name,suffix)
