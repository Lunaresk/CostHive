from datetime import datetime

def getDictFromWords(words: list[tuple]):
    results = {"items": []}
    results['date'] = datetime.strptime(words[-6][4], "%d.%m.%y").date()
    results['bonid'] = words[-1][4]
    currentline = 0
    skipwords = 14
    for i, word in enumerate(words[skipwords:]):
        if currentline != word[5]:
            results['items'].append({"itemname": word[4]})
            currentline = word[5]
        elif word[6] == 0:
            results['items'][-1]["itemname"] += " " + word[4]
        if word[6] == 1 and word[7] == 1:
            results['items'][-1]["price"] = word[4].split("*")[0]
        if "----" in word[4]:
            del(results['items'][-1])
            break
    return results