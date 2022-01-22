# About

DubAlert enables you to receive an email notification when a specified anime gets an English dub. It scrapes IsThisDubbed.com.


# Dependencies

* Python 3.x
* Beautiful Soup 4
* RedMail (Python library to simplify sending emails) 
* Gmail account (optional, can configure another SMTP service)


# How to use

1. Rename testconfig.py to config.py and assign values
2. Run DubAlert.py to input shows. Or manually enter the show IDs from IsThisDubbed.com in shows.txt, one ID per line.
3. Set up runDubEmailer.bat (with the correct directories) to run on a schedule, e.g. with Windows Task Scheduler.