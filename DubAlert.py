#!/usr/bin/python3

# Run this script to check the dub status of shows and add new ones to the alert list.
import os
import re
import sys

import requests
from bs4 import BeautifulSoup  # for parsing HTML

import config  # contains user email variable


def checkemail():
    if not re.match(r"[^@]+@[^@]+\.[^@]+", config.user_email):
        print("Enter a valid email in config.py then rerun script.")
        input()
        sys.exit()


def idinput():  # define URL input function
    global showid
    showid = input("Enter the ID for the show in the format used on IsThisDubbed.com: ")
    dubcheck()


def invalid():  # Invalid show ID
    print("Invalid show ID.")
    idinput()


def dubcheck():
    showurl = "https://isthisdubbed.com/media/" + showid
    html_text = requests.get(showurl)
    soup = BeautifulSoup(html_text.content, 'html.parser')  # get HTML text
    try:
        # iserror = soup.find(class_="card-img-top")            # TODO: find way to timeout script, e.g. with the showid "e" which results in an extremely large page.
        hasdub = soup.find(class_="text-uppercase text-center").get_text()
    except:
        invalid()
    if "Sorry" in hasdub:
        print(showid + " is not dubbed.")
        confirm = input("Enter the letter 'y' if you would like to receive a one-time email notification when this show receives a dub.")
        if confirm.lower() == "y":
            with open(os.path.join(sys.path[0], "shows.txt"), "a") as shows:
                shows.write(showid + "\n")                          # add show to list
            print(showid + " added to notification list.")
            idinput()
        else:
            print(showid + " not added to notification list.")
            idinput()
    elif "It's dubbed" in hasdub:
        print(showid + " is dubbed.")
        idinput()
    else:
        invalid()


def main():
    checkemail()
    idinput()


if __name__ == '__main__':
    main()
