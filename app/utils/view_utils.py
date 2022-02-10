from app import LOGGER

def group_results(results: tuple) -> dict:
    result_dict = {}
    LOGGER.debug("Grouping...")
    for result in results:
        if result[0] not in result_dict:
            result_dict[result[0]] = {"sum": 0}
        if str(result[1]) not in result_dict[result[0]]:
            result_dict[result[0]][str(result[1])] = {}
        result_dict[result[0]][str(result[1])][result[2]] = (
            result[3], result[4])
        price = int(result[3]) * int(float(result[4].split(" ")[0].replace(",", "."))*100)
        result_dict[result[0]]["sum"] += price
    for key in result_dict.keys():
        result_dict[key]["sum"] /= 100
    LOGGER.debug("Grouped.")
    return result_dict