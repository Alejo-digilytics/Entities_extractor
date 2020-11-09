## Extractor.
This repository contains an entities extractor for determined type of document. 
The class plays mainly the roll 
of a wrapper and the file tools.py contains

    1 extractor_pg1: function for extracting the entities from the first page 
        with an assistant matcher with the necessary regexes
    2 extractor_pg2: function for extracting the entities from the second page 
        with an assistant matcher with the necessary regexes
    3 extractor_transactions: function for extracting the transactions from the whole text 
        with an assistant matcher containing the necessary regexes

This repository extracts the following entities

    Customer Address
    Account Number
    Customer Name
    Customer Country
    Statement Date
    Credit Limit
    Current Statement Balance
    Available to spend
    Card Purchase Interest Rate Applicable
    Cash Purchase Interest Rate Applicable
    Individual Transaction and Dates
    Minimum Payment
    Arrears Immediately Due
    Total Payment Due
    Total Payment Due by

### Launch.
1. This repository was developed using python 3.8.
2. The repository provides a requirements.txt file with all the necessary dependencies. 
They can be installed with the command `pip3 install -r requirements.txt`.

To process one of the pdf with a fixed format it is necessary to introduce it in `data/pdf/` 
and write its name in the Extractor class. The class Extractor will take the pdf,
convert it into txt and extract all the entities. 

#### REMARKS
This repository only works for a concrete type of document
One of the regexes use that some of the amounts are preceded by "€".