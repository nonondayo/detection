import os


def readcsv(csvfile, countries):
    csv_res = {}
    for co in countries:
        csv_res[co] = []
    with open(csvfile, "r") as f:
        results = f.readlines()
    results = [one.strip() for one in results]
    for oneline in results:
        imgname, res = oneline.split(",")
        country_may = imgname.split("_")
        if len(country_may) == 2:
            country = country_may[0]
        else:
            country = f"{country_may[0]}_{country_may[1]}"
        csv_res[country].append(oneline)
    return csv_res


if __name__ == '__main__':
    all_res = ["China_MotorBike", "Czech", "India", "Japan", "Norway", "United_States"]

    Norway_predicts = os.path.join("RDD2022_Norway.csv")
    others_predicts = os.path.join("RDD2022__China__Czech__India__Japan__United_States.csv")
    merge_predicts = os.path.join("RDD2022_allcountries.csv")

    Norway_res = readcsv(Norway_predicts, ["Norway"])
    others_res = readcsv(others_predicts, ["China_MotorBike", "Czech", "India", "Japan", "United_States"])

    merge_res = []
    for c in all_res:
        if c != "Norway":
            merge_res.extend(others_res[c])
        if c == "Norway":
            merge_res.extend(Norway_res[c])

    with open(merge_predicts, "w") as file:
        for oneline in merge_res:
            file.write(oneline+"\n")
