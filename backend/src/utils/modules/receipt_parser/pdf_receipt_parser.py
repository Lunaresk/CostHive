import fitz
from datetime import datetime, date
from .edeka.edeka_parser import getDictFromWords as edekaparser
from .kaufland.kaufland_parser import getDictFromWords as kauflandparser
from re import search

class PDFReceipt:
    """Class to use a PDF-Receipt as an object.

    Arguments:
    strPDFFile -- The path to the PDF-File as a string.
    parser -- A keyword in lowercase to tell how the receipt is formated.
        Currently supported: 'edeka'
    """
    def __init__(self, strPDFFile) -> None:
        try:
            self.words = PDFReceipt._getWordsFromPDF(strPDFFile)
            storename = PDFReceipt._getStoreName(self.words)
            self.id, self.date, self.items = PDFReceipt._getInfosFromText(self.words, store = storename)
        except:
            self.words = "PDF konnte nicht geladen werden."
            self.date = date.today()
            self.id = None
            self.items = []

    def _getWordsFromPDF(file):
        with fitz.open(file, filetype="pdf") as doc:
            words = []
            for page in doc:
                words.extend(page.get_text("words", textpage=page.get_textpage_ocr(), sort=True))
        return words
    
    def _getStoreName(words: list[tuple]) -> str:
        for word in words:
            if word[4].lower() in ("edeka", "kaufland"):
                return word[4].lower()
        return "unknown"

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

    def _getInfosFromText(words: str, store: str = "edeka"):
        if store == "edeka":
            result = edekaparser(words)
        elif store == "kaufland":
            result = kauflandparser(words)
        items = result.get("items")
        date = result.get("date")
        strReceiptNumber = result.get("bonid")
        try:
            intReceiptNumber = int(strReceiptNumber)
        except:
            raise ValueError("Receipt Number not an integer.")
        return (intReceiptNumber, date, items)

    def getPDFReceiptFromFile(strPDFFile: str):
        try:
            with open(strPDFFile) as doc:
                return PDFReceipt(doc)
        except FileNotFoundError as e:
            return PDFReceipt(None)