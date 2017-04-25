#!/usr/bin/env python

import argparse

import bs4
import pandas as pd


def class_to_number(cls):
    if "wom_approved" in cls:
        return +1
    elif "wom_neutral" in cls:
        return 0
    elif "wom_negative" in cls:
        return -1
    else:
        raise Exception("Vote HTML has none of the classes wom_approved, "
                        "wom_neutral, wom_negative")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("html_files", nargs="+", help="Scraped HTML files")
    parser.add_argument("csv_path", help="CSV to write results into")
    args = parser.parse_args()

    html_files = args.html_files
    csv_path = args.csv_path

    # Parse HTML files
    docs = []
    for path in html_files:
        with open(path, "rb") as f:
            docs.append(bs4.BeautifulSoup(f, "html5lib"))

    # Extract the vote elements
    votes = [v for d in docs for v in d.select(".wom_votum_list.wom_on")]

    # Transform HTML into pandas columns
    df = pd.DataFrame()
    for v in votes:
        party_name = v.select_one(".wom_partei_balken").text
        classes = [el.attrs["class"] for el in v.select(".wom_antworten_partei")]
        answers = [None] * len(classes)
        for i, cls in enumerate(classes):
            answers[i] = class_to_number(cls)
        df[party_name] = answers

    # Save results
    df.to_csv(csv_path, index=False)


if __name__ == "__main__":
    main()
