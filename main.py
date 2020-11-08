import logging
import os
from tools import pdf_to_text, extractor_pg1, extractor_pg2, extractor_transactions

class Extractor():

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


if __name__ == '__main__':
    file = "DL template 02.pdf"
    My_Extractor = Extractor(file)
    My_Extractor.pdf_to_text()
    My_Extractor.extractor_pg1(print_yes=True)
    My_Extractor.extractor_pg2(print_yes=True)
    My_Extractor.extractor_transactions(print_yes=True)


