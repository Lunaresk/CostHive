from datetime import datetime
import fitz
from re import search

class PDFReceipt:
    """Class to use a PDF-Receipt as an object.

    Arguments:
    strPDFFile -- The path to the PDF-File as a string.
    parser -- A keyword in lowercase to tell how the receipt is formated.
        Currently supported: 'edeka'
    """
    def __init__(self, bPDFFile, parser: str = "edeka") -> None:
        self.text = PDFReceipt._getTextFromPDF(bPDFFile)
        self.id, self.date, self.items = PDFReceipt._getInfosFromText(self.text, parser)

    def _getTextFromPDF(file):
        with fitz.open("pdf", file) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
        return text.strip()

    def _getItemsTextFromText(text, start="", end=""):
        return text[text.index(start)+len(start):text.index(end)].strip()

    def _convertItemsTextToDict(text):
        temp = text.split("\n")
        resultsArr = []
        i = 0
        while i < len(temp):
            if search("(\d+) x", temp[i]):
                resultsArr.append({"itemname": temp[i+2], "price": temp[i+1], "amount": temp[i][:-2]})
                i += 4
            else:
                resultsArr.append({"itemname": temp[i], "price": temp[i+1][:-2]})
                i += 2
        return resultsArr

    def _getInfosFromText(text: str, parser: str = "edeka"):
        if parser.lower() == "edeka":
            items = PDFReceipt._convertItemsTextToDict(PDFReceipt._getItemsTextFromText(text, "EUR", "----------"))
            strDate = text.split("\n")[-1].split(" ")[0]
            date = datetime.strptime(strDate, "%d.%m.%y").date()
            strReceiptNumber = text.split("\n")[-1].split(" ")[-1]
            try:
                intReceiptNumber = int(strReceiptNumber)
            except:
                raise ValueError("Receipt Number not an integer.")
        return (intReceiptNumber, date, items)

    def getPDFReceiptFromFile(strPDFFile: str, parser: str = "edeka"):
        with open(strPDFFile) as doc:
            return PDFReceipt(doc, parser)