from datetime import datetime

def getDictFromWords(words: list[tuple]):
    results = {"items": []}
    results['bonid'] = words[-1][4]
    currentline = 0
    skipwords = 9
    for i, word in enumerate(words[skipwords:]):
        if currentline != word[5]:
            results['items'].append({"itemname": word[4]})
            currentline = word[5]
        elif word[6] == 0:
            results['items'][-1]["itemname"] += " " + word[4]
        if word[6] == 1 and word[7] == 0:
            if word[4].lower() == "x":
                results['items'][-1]["amount"] = words[i+skipwords+1][4]
            else:
                results['items'][-1]["price"] = word[4]
        elif word[6] == 2:
                results['items'][-1]["price"] = word[4]
        if word[4].lower() == "gesamt":
             del(results['items'][-1])
             break
    for i, word in enumerate(words[::-1]):
         if word[4].lower() == "datum:":
            results['date'] = datetime.strptime(words[::-1][i-1][4], "%d.%m.%Y").date()
    return results