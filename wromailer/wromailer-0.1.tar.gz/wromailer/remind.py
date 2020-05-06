# -*- coding: utf-8 -*-
"""
Created on Sat Dec 15 08:27:19 2018

@author: lukasz
"""

from wromailer.icalendar_creator import create_ics
from wromailer.mailer import Mailer
from wromailer.task_reader import main_assignment_from_csv, assistant_from_csv, check_quality
import os
from argparse import ArgumentParser


def main(args):
    login = args.organizer
    filename = args.filename
    subject = args.subject
    check_quality(filename)
    mailer = Mailer(login, subject, args.template, args.assistant_template)
    for item in main_assignment_from_csv(filename):
        ical = create_ics(item['name'], item['email_task'], item['dt_assignment'], item['task_name'], login, offset_days=4)
        # print(item)
        mailer.send_email(ical, item['email_task'], item['name'], item['assistant'], item['dt_assignment'], item['task_name'], item['lesson'])    
    for item in assistant_from_csv(filename):
        # print(item)
        ical = create_ics(item['name'], None, item['dt_assignment'], item['task_name']+' [Assistant]', login, offset_days=4)
        mailer.send_email_assistant(ical, item['email_assistant'], item['name'], item['assistant'], item['dt_assignment'], item['task_name'])
    
    mailer.close_mailer()


def main_console():
    parser = ArgumentParser()
    parser.add_argument('-f', dest='filename', required=True)
    parser.add_argument('-o', dest='organizer', required=True)
    parser.add_argument('-t', '--template', required=True)
    parser.add_argument('-a', '--assistant_template', required=True)
    parser.add_argument('-s', '--subject', default='Assignment Reminder')
    args = parser.parse_args()
    main(args)


if __name__ == "__main__":
    main_console()