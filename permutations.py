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

def convert_to_string(res):
    last_res=[]
    chars=['[',']',' ',',',"'"]    
    for word in res:
        str_temp=""
        for letter in word:
            if chars.__contains__(letter) == False:
                str_temp=str_temp+letter 
        if last_res.__contains__(str_temp) == False:
            last_res.append(str_temp)        
    return last_res

def permutation_2(word):
    res=permutation_1(word)
    chars=["/","-","'",".","1"
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
    
