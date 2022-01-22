#!/usr/bin/python3

# Run this script to check the status of the shows in shows.txt.
# It will send an email to the address specified in config.py
# if a show has received a dub and remove the show
# from the list. Check the README for instructions on
# setting this up in Windows Task Scheduler.
import os
import sys

import requests
from bs4 import BeautifulSoup  # for parsing HTML
from redmail import gmail

import config
from DubAlert import checkemail


def autodubcheck():
    with open(os.path.join(sys.path[0], "shows.txt"), "r") as shows:      # open for reading/writing
        shows_content = shows.read()
        shows_list = shows_content.split("\n")      # split into list
        shows_list_new = []                         # to be new shows.txt list
        email_list = []                             # list of shows to be included in email notification
        for i in shows_list:
            if i == "":             # check if empty line
                continue
            showurl = "https://isthisdubbed.com/media/" + i
            html_text = requests.get(showurl)
            soup = BeautifulSoup(html_text.content, 'html.parser')      # get HTML text
            try:
                hasdub = soup.find(class_="text-uppercase text-center").get_text()
            except:
                print("Invalid show ID.")
                continue
            if "Sorry" in hasdub:
                print(i + " is not dubbed.")
                shows_list_new.append(i)
                continue
            elif "It's dubbed" in hasdub:
                print(i + " is dubbed.", end = " ")
                email_list.append('<a href="' + showurl + '">' + i + '</a>')                    # add show to email list formatted with link
                print("An email will be sent to " + config.user_email + " and " + i + " will be removed from the list.")          # do not add show to new shows.txt
                continue
            else:
                print("Invalid show ID.")
                continue
    with open(os.path.join(sys.path[0], "shows.txt"), "w") as shows:
            shows.write("\n".join(shows_list_new) + "\n")
    if email_list:              # only send email if the list isn't empty
        global email_list_formatted
        email_list_formatted = "<br>".join(email_list)        # convert into newline-separated string
        sendemail()


def sendemail():
    gmail.user_name = config.user_email
    gmail.password = config.user_password
    gmail.send(
        subject="DubAlert: shows have received a dub",
        receivers=[config.user_email],
        html=email_list_formatted
    )

def main():
    checkemail()
    autodubcheck()
    print("Finished.")
    sys.exit()


if __name__ == '__main__':
    main()