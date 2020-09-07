import html_similarity

def similiar(document_1,document_2,k):
    return k * html_similarity.structural_similarity(document_1, document_2) + (1 - k) * html_similarity.style_similarity(document_1, document_2)

    
