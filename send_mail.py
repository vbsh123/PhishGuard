import yagmail

def send_email(email_to_send, contents_to_send):
    yag = yagmail.SMTP('phishguard2020@gmail.com', 'zxbhfkcvmnd123')
    yag.send(email_to_send, 'Scan Results', contents=contents_to_send)
    
#send_email("yoelvb5801@gmail.com","hi")