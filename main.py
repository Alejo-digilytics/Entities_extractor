import logging
import os
from tools import pdf_to_text, extractor_pg1, extractor_pg2, extractor_transactions
import json

class Extractor():
    """
    This class Extracts information from the pdfs credit card statements.
    Even if these functions extract the information from different pages we can input the document and not just the
    concrete page, i.e, they are flexible about the pages to introduce whenever those pages are in the fixed format
    and contain the entities.
    Methods:
            - pdf_to_text: converts the pdfs into txt
            - extractor_pg1: It extracts the entities which are not transactions and use to appear in the first page.
                It extracts the following entities:
                    1. Customer Address
                    2. Account Number
                    3. Customer Name
                    4. Customer Country
                    5. Statement Date
                    6. Credit Limit
                    7. Current statement Balance
                    8. Available to spend
                    9. Minimum Payment
                    10. Arrears Immediately Due
                    11. Total Payment Due
                    12. Total Payment Due by"
            - extractor_pg2:It extracts the entities which are not transactions and use to appear in the last page.
                It extracts the following entities:
                    1. Card Purchase Interest Rate Applicable
                    2. Cash Purchase Interest Rate Applicable
            - extractor_transactions: This function extracts the transactions from the whole document as a list
                containing:
                    - Transaction Date
                    - Posting Date
                    - Description of the transaction
                    - Amount
            - extract_entities: This function outputs a json with the entities and summarizing all the other methods.
    RMK: by the default the class introduces the whole text in the three methods for extraction.
    """

    def __init__(self,my_pdf):
        self.name = my_pdf.split(".")[0]
        self.text = ""
        self.path_pdf = os.path.join(os.getcwd(), "data", "pdf", self.name + ".pdf")
        self.path_txt = os.path.join(os.getcwd(), "data", "text", self.name + ".txt")

    def pdf_to_text(self):
        self.text = pdf_to_text(self.name + ".pdf",save=True, giveback=True)
        logging.info('The file has been converted')

    def extractor_pg1(self, print_yes=False, return_yes=False):
        with open(self.path_txt, "r") as pg1:
            my_dict1 = extractor_pg1(pg1)
            pg1.close()
        if print_yes:
            [print("{}: {}".format(x, y)) for x, y in my_dict1.items()]
        if return_yes:
            return my_dict1

    def extractor_pg2(self, print_yes=False, return_yes=False):
        with open(self.path_txt, "r") as pg2:
            my_dict2 = extractor_pg2(pg2)
            pg2.close()
        if print_yes:
            [print("{}: {}".format(x, y)) for x, y in my_dict2.items()]
        if return_yes:
            return my_dict2

    def extractor_transactions(self, print_yes=False, return_yes=False):
        with open(self.path_txt, "r") as whole_text:
            my_dict3 = extractor_transactions(whole_text)
            whole_text.close()
        if print_yes:
            [print(x) for x in my_dict3.items()]
        if return_yes:
            return my_dict3

    def extract_entities(self):
        self.pdf_to_text()
        dict1 = self.extractor_pg1(print_yes=False,return_yes=True)
        dict2 = self.extractor_pg2(print_yes=False,return_yes=True)
        dict3 = self.extractor_transactions(print_yes=False,return_yes=True)
        output_dict = {**dict1,**dict2,**dict3}
        return json.dumps(output_dict)


if __name__ == '__main__':
    file = "DL template 03.pdf"
    My_Extractor = Extractor(file)
    #My_Extractor.pdf_to_text()
    #My_Extractor.extractor_pg1(print_yes=True)
    #My_Extractor.extractor_pg2(print_yes=True)
    #My_Extractor.extractor_transactions(print_yes=True)

    My_json = My_Extractor.extract_entities()

    [print("{}: {}".format(x, y)) for x, y in My_dict.items()]