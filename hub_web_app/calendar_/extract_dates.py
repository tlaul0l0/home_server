import PyPDF2
import re
from calendar import monthrange

def read_pdf(path):
    """
    @path: path to pdf file
    @returns: file object in read binary mode
    """
    pdf_file = open(path, 'rb')
    return pdf_file

def get_page_text_from_pdf(pdf_file, page_index):
    """
    @pdf_file: file object
    @page_index: page number
    @returns: text from given files page
    """
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    page = pdf_reader.pages[page_index]
    return page.extract_text()

def clean_up_text(page_text):
    """
    @page_text: text
    @returns: text with unnecessary information removed
    """
    left_border_text = "01"
    right_border_text = "Abfallberatung"
    left_index = page_text.find(left_border_text    )
    right_index = page_text.find(right_border_text)

    page_text = re.sub("!", "", page_text)
    page_text = page_text[left_index:right_index]
    page_text = page_text.replace(" ", "")
    page_text = page_text.replace("\n", "")
    page_text = page_text.replace("RM4", "")

    return page_text

def get_month_from_text(page_text):
    """
    @page_text: text to search in
    @returns: extracted text for month and remaining page_text without month_text
    """
    # find the second "01" in page_text, cut till found index to extract first month in text
    index = page_text.find("01", page_text.find("01")+1)

    month_text = page_text[:index]
    page_text = page_text[index:]
    return month_text, page_text

def find_key_occurences(month_text, key):
    """
    @month_text: text to search in
    @key: [RM; BIO, PPK, GS, GA] to find in month_text
    @returns: start indexes of keys
    """
    occurences = list()
    for match in re.finditer(key, month_text):
        occurences.append(match.start())
    return occurences

def extract_date_info(month_text, occurences):
    """
    @month_text: text to extract occurences from
    @occurences: start indexes of key
    @returns: date and weekday e.g.: 06Sa or 19Fr
    """
    date_info = list()
    for occurence in occurences:
        date_info.append(month_text[occurence-4:occurence])
    return date_info

def pypdf_extract():
    pdf_file = read_pdf(path="Abfuhrkalender_2024_SalemSalem_I.pdf")
    
    # extract text from both pages
    first_page_text = get_page_text_from_pdf(pdf_file=pdf_file, page_index=0)
    second_page_text = get_page_text_from_pdf(pdf_file=pdf_file, page_index=1)

    # remove unnecessary information
    first_page_text = clean_up_text(page_text=first_page_text) # 1 Jan to 30 Jun
    second_page_text = clean_up_text(page_text=second_page_text) # 1 Jul to 31 Dec
    
    # add both pages text together
    text = first_page_text + second_page_text


    keys = ["RM2", "BIO2", "PPK4", "GS", "GA"] # dont look for RM4 as it is always on RM2
    for index in range(1, 13):
        # extract month from text
        month_text, text = get_month_from_text(page_text=text)
        print(month_text)

        for key in keys:
            # find occurences of keys
            occurences_end_indexes = find_key_occurences(month_text=month_text, key=key)
            
            # extract date info
            date_info = extract_date_info(month_text=month_text, occurences=occurences_end_indexes)
            print(f"Key: {key}, Occurences: {occurences_end_indexes}, date_info:{date_info}")
        print("----------------------------------------------\n\n")
    # closing the pdf file object
    pdf_file.close()

if __name__ == "__main__":
    pypdf_extract()