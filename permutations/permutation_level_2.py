from permutations.string_convertor import convert_to_string
from permutations.permutation_level_1 import permutation_1

def permutation_2(word):
    res=permutation_1(word)

    chars=["/","-","'",".","1",
            "2","3","4","5","6","7","8","9"]
            
    for LETTER in range(65,91):
        chars.append(chr(LETTER))

    for letter_1 in range(0, len(word)):
        for char in range(0, len(chars)):
            obj=[ word[letter_1]+chars[char] if letter_1==letter_2  else word[letter_2]  for letter_2 in range(0, len(word)) ]
            res.append(obj)
            obj=[ chars[char]+word[letter_1] if letter_1==letter_2  else word[letter_2]  for letter_2 in range(0, len(word)) ]
            res.append(obj)
    return convert_to_string(res)

