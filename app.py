from postmark import Postmark
from scraper import Scrape, Clear
import config
import pandas as pd


def is_sending_email():
    sent_emails = 0
    data_frame = pd.read_csv('data_file.csv')
    public_email = data_frame['Public Email']
    public_email.fillna('MISSING', inplace=True)
    email_list = [email for email in public_email if email != 'MISSING']
    for recipient in email_list:
        post = Postmark(recipient)
        print(f"Postmark sending email to {recipient}")
        post.send_mail()
        sent_emails += 1

    print(f"{sent_emails} emails sent successful")


def is_scraping():
    target_profile = input(
        "[REQUIRED] - Whose profile will you like to scrape from? (INPUT IG USERNAME)\n").lower()
    scraper_option = input(
        "[REQUIRED] - What action do you want to perform? (OPTION ONE: INPUT '1' TO SCRAPE FOLLOWERS; "
        "OPTION TWO: INPUT '2' TO SCRAPE FOLLOWING;)\n")
    match scraper_option:
        case '1':
            num_to_scrape = int(input(
                "[REQUIRED] - How many followers data will you like to scrape?\n"))
            scrape = Scrape(target_profile, num_to_scrape)
            scrape.login()
            scrape.search()
            scrape.followers()
            scrape.scrape_data()
        case '2':
            num_to_scrape = int(input(
                "[REQUIRED] - How many following data will you like to scrape?\n"))
            scrape = Scrape(target_profile, num_to_scrape)
            scrape.login()
            scrape.search()
            scrape.following()
            scrape.scrape_data()
        case _:
            print("You entered a wrong option input. Choose from available OPTIONS")


is_running = True
while is_running:
    Clear()
    print(config.logo1)
    print("HELLO THERE... WELCOME! 🙂")
    user_input = input(
        "[REQUIRED] - CHOOSE AN OPTION TO PERFORM. (OPTION ONE: INPUT '1' TO SCRAPE; OPTION TWO: INPUT '2': TO SEND EMAILS;)\n")
    if __name__ == '__main__':
        match user_input:
            case '1':
                is_scraping()
            case '2':
                is_sending_email()
            case _:
                print("You entered a wrong option input. Choose from available OPTIONS")
        print(config.logo2)
        try_again = input(
            "Do you want to try again?... TYPE 'YES' to START program again; OR TYPE 'NO' to END program;\n").lower()
        if try_again == 'yes':
            is_running
        else:
            Clear()
            print("GOODBYE 😎")
            is_running = False
