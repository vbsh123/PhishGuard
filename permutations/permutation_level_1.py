from permutations.string_convertor import convert_to_string

def permutation_1(word):
    res=[]    
    for letter_1 in range(0, len(word)):
        obj=[ word[letter_1]+word[letter_1] if letter_1==letter_2  else word[letter_2]  for letter_2 in range(0, len(word)) ]
        res.append(obj)

    for letter_1 in range(0, len(word)):
        for abc in range(97, 123):
            obj=[ word[letter_1]+chr(abc) if letter_1==letter_2  else word[letter_2] for letter_2 in range(0, len(word)) ]
            res.append(obj)
            obj=[ chr(abc)+word[letter_1] if letter_1==letter_2  else word[letter_2] for letter_2 in range(0, len(word)) ]
            res.append(obj)

    return convert_to_string(res)


