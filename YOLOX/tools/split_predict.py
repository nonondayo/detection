import os


if __name__ == '__main__':
    countries = ["India", "Japan", "United_States"]
    all_predicts = os.path.join("RDD2022__China__Czech__India__Japan__United_States.csv")

    countries_results = {}
    for c in countries:
        countries_results[c] = []

    with open(all_predicts, "r") as file:
        results = file.readlines()
    results = [one.strip() for one in results]
    for oneline in results:
        imgname, res = oneline.split(",")
        country_may = imgname.split("_")
        if len(country_may) == 2:
            country = country_may[0]
        else:
            country = f"{country_may[0]}_{country_may[1]}"
        if country in countries:
            countries_results[country].append(oneline+"\n")

    for c in countries:
        with open(f"RDD2022_{c}.csv", "w") as f:
            for line in countries_results[c]:
                f.write(line)

