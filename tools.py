import os
import pdftotext
import logging
import re


def pdf_to_text(name, save=False, giveback=False):
    """
     This function onvert pdf to txt
    Input:
        - name: string with the name of the pdf, including .pdf
        - save (Boolean): conditional to save or not
        - giveback (Boolean): conditional to save or not
    Output:
        - It saves the txt into data/text/~
    """
    not_fail = True
    try:
        with open(os.path.join("data", "pdf", name), "rb") as f:
            salida = pdftotext.PDF(f)
            f.close()
    except:
        not_fail = False
        logging.info("There was a problem converting the pdf")
    if save or giveback:
        rename = name.split(".")[0]
        output_dir = os.getcwd()
        local_dir_txt = os.path.join(output_dir, "data", "text")
        try:
            os.mkdir(local_dir_txt)
        except FileExistsError:
            pass
        if rename + ".txt" in local_dir_txt:
            logging.info("The txt file already exists")
        elif not_fail:
            with open(os.path.join(local_dir_txt, rename + ".txt"), "w+") as file:
                for page in salida:
                    file.write(page)
            file.close()
        else:
            logging.info(rename + ".txt was not created")
        if giveback:
            text = ""
            with open(os.path.join(local_dir_txt, rename + ".txt"), "r") as file:
                for line in file:
                    text = text + line
                return text
    else:
        logging.info("The file was not saved")


def extractor_pg1(text):
    """
    Thus function extract the desired entities and give them back as dictionary
    Input:
        - text (.txt): text file containing the first page
    Output:
        - output (python dict): dictionary with the entities from the first page
    """
    limited = "NAC"
    name_string = account_string = statement_date = credit = CSB = ATS = TPD = \
        TPDB = MP = AID = ""
    for line in text:
        # Delimiters conditionals
        if ("account number" in line.lower()) and (limited == "NAC"):
            limited = "AN"
        elif ("statement date" in line.lower()) and (limited == "AN"):
            limited = "SD"
        elif ("date" in line.lower()) and (limited == "SD"):
            limited = "CL"
        elif ("current statement balance" in line.lower()) and (limited == "CL"):
            limited = "CSB"
        elif ("available to spend" in line.lower()) and (limited == "CSB"):
            limited = "ATS"
        elif ("minimum payment" in line.lower()) and (limited == "ATS"):
            limited = "MP"
        elif ("arrears immediately due" in line.lower()) and (limited == "MP"):
            limited = "AID"
        elif ("total payment due" in line.lower()) and (limited == "AID"):
            limited = "TPD"
        elif ("by" in line.lower()) and (limited == "TPD"):
            limited = "TPDB"
        # Texts extractions based on delimiters
        if limited == "NAC":
            name_string = name_string + line
        elif limited == "AN":
            account_string = account_string + line
        elif limited == "SD":
            statement_date = statement_date + line
        elif limited == "CL":
            credit = credit + line
        elif limited == "CSB":
            CSB = CSB + line
        elif limited == "MP":
            MP = MP + line
        elif limited == "AID":
            AID = AID + line
        elif limited == "ATS":
            ATS = ATS + line
        elif limited == "TPD":
            TPD = TPD + line
        elif limited == "TPDB":
            TPDB = TPDB + line
        else:
            pass
    # Extract banck account
    account = [int(s) for s in account_string.split() if s.isdigit()][:-1]

    # Extract name, address and country
    name_string = name_string.split("Your Avant")[0].strip()
    N_A_C = name_string.split("\n")
    name_string = N_A_C[0].strip()
    country_string = N_A_C[-1].strip()
    N_A_C = N_A_C[1:-1]
    address_string = ', '.join([x.strip() for x in N_A_C])

    # Extract statement date
    statement_list = matcher_pg1(statement_date, "date")[0]

    # Extract Credit limit
    credit = matcher_pg1(credit, "amount")[0]

    # Extract Current Statement Balance
    currentSB = matcher_pg1(CSB, "amount")[0]

    # Extract Available to spend
    available = matcher_pg1(ATS, "amount")[0]

    # Extract Total Payment Due
    total_Due = matcher_pg1(TPD, "total")[0]

    # Extract Total Payment Due
    min_Payment = matcher_pg1(MP, "total")[0]

    # Extract Total Payment Due
    arrears_immediately_due = matcher_pg1(AID, "total")[0]

    # Extract Total Payment Due By
    total_due_by = matcher_pg1(TPDB, "date")[0]

    # Prepare output
    my_keys = ["Customer Address", "Account Number", "Customer Name", "Customer Country",
               "Statement Date", "Credit Limit", "Current statement Balance", "Available to spend",
               "Minimum Payment", "Arrears Immediately Due", "Total Payment Due", "Total Payment Due by"]
    my_values = [address_string, account, name_string, country_string, statement_list, credit, currentSB, available,
                 min_Payment, arrears_immediately_due, total_Due, total_due_by]
    output = dict(zip(my_keys, my_values))
    return output


def matcher_pg1(text, search):
    if search == "total":
        return re.findall("\d+[,.]\d*[,.]*\d\d", text)
    if search == "amount":
        return re.findall("[€]\d+[,.]*\d+[,.]\d*", text)
    if search == "date":
        return re.findall("\d\d\s[a-zA-Z]+\s\d\d", text)


def extractor_pg2(text):
    """
    Thus function extract the desired entities and give them back as dictionary
    Input:
        - text (.txt): text file containing the second page
    Output:
        - output (python dict): dictionary with the entities from the second page
    """
    limited = "Dontcare"
    MR = ""
    for line in text:
        # Delimiters conditionals
        if "monthly rates" in line.lower():
            limited = "MR"
        else:
            pass
        # Texts extractions based on delimiters
        if limited == "MR":
            MR = MR + line
        else:
            pass

    # Extract Cash Purchase Interest Rate Applicable and Card Purchase Interest Rate Applicable
    MR = matcher_pg2(MR, "rate")

    # Prepare output
    my_keys = ["Card Purchase Interest Rate Applicable", "Cash Purchase Interest Rate Applicable"]
    output = dict(zip(my_keys, MR[:2]))
    return output


def matcher_pg2(text, search):
    if search == "rate":
        return re.findall("\d+[.]\d{1,2}\%", text)


def extractor_transactions(text):
    """
    Thus function extract the transactions and returns a dictionary containing them
    Input:
        - text (.txt): text file containing the first page
    Output:
        - output (python dictionary): dictionary containing the transactions
    """
    transactions_dict = {}
    transaction_num = 0
    old_match = None
    for line in text:
        if "current statement balance" in line.lower():
            transaction_num = 0
        if "continued on next page" in line.lower():
            transaction_num = 0
        if (matcher_transaction(line, "transactions_date") != None and transaction_num == 0) or transaction_num > 0:
            transaction_num += 1
            new_match = matcher_transaction(line, "transactions_date")
            if new_match == old_match or new_match == None:
                transactions_dict[old_match] = transactions_dict[old_match] + line
            elif new_match != None:
                transactions_dict[new_match] = line
                old_match = new_match

    # Extraction Transactions
    output = {}
    for k, v in transactions_dict.items():
        transaction_num += 1
        transaction_amount = matcher_transaction(v, "transaction_amount")[0].strip()
        v = v.replace(k[0], "").replace(transaction_amount, "").replace("Available to spend", "")
        v = v.replace("Contacting us Online", "").replace("§ check your balance", "").replace("You can", "")
        other_amounts = matcher_transaction(v, "euro_amount")
        if other_amounts != []:
            for amount in other_amounts:
                v = v.replace(amount, "")
        transaction = " ".join(v.split()).strip()
        dates = k[0].split()
        output[transaction_num] = [" ".join(dates[:3]), " ".join(dates[3:]), transaction_amount, transaction]

    return output


def matcher_transaction(text, search):
    # All transactions dates
    if search == "transactions_dates":
        return re.findall("\d\d\s[a-zA-Z]+\s\d\d\s+\d\d\s[a-zA-Z]+\s\d\d\s+", text)
    # The first transaction date
    if search == "transactions_date":
        return re.search("\d\d\s[a-zA-Z]+\s\d\d\s+\d\d\s[a-zA-Z]+\s\d\d\s+", text)
    if search == "transaction_amount":
        return re.search(" [^€]\d*[,]*\d{1,3}[.]\d\d\s{1}C*r*", text)
    if search == "euro_amount":
        return re.findall("[€]\d+[,.]*\d+[,.]\d*", text)
