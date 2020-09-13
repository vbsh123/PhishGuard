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