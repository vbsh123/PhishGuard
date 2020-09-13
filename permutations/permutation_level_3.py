from permutations.dnstwist import main
import sys
import json


def permutation_3(domain_name, suffix):
    word = domain_name + "." + suffix
    sys.argv.append(word)
    out = main()
    
    domains = []

    for domain in out:
        print(domain)
        domains.append(str(domain)[31:-2])

    return domains
   



