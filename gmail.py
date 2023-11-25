from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.text import MIMEText
import json
import time

# Gmail credentials
gmail_username = 'jethwaninikhil1@gmail.com'
gmail_password = 'hhfg ydto tsut qptk'

# Recipient's email address (replace with the actual recipient's email)
recipient_email = 'keshavbrambhatt@gmail.com'  # Replace with the recipient's actual email address

# Initialize variables for previous notification
previous_notification = ""

while True:
    try:
        # Send an HTTP GET request to the URL and retrieve the page content
        html_text = requests.get('https://www.subodhpgcollege.com/notice_board').text

        # Create a BeautifulSoup object
        soup = BeautifulSoup(html_text, 'lxml')

        # Find all <ul> elements with class "list_none comment_list"
        news = soup.find(class_='tab-pane fade show active')
        lists = news.find('li', 'comment_info')
        content_element = lists.find(class_='comment_content')
        link_element = lists.find(class_='d-sm-flex align-items-center')

        # Check if the content element exists and extract the content
        content = content_element.text if content_element else "No content available"

        # Try to extract the link, if available
        linktopdf = link_element.h6.a['href'] if link_element and link_element.h6.a else ""

        # Construct the message
        if linktopdf:
            message = f"{content}\nwww.subodhpgcollege.com/{linktopdf}"
        else:
            message = content

        # Check if the current notification is different from the previous one
        if content != previous_notification:
            # Update the previous notification
            previous_notification = content

            # Send the email using Gmail
            subject = 'Notification from Your College'

            # Use Unicode encoding for the body
            body = MIMEText(f"To: {recipient_email}\nSubject: {subject}\n\n{message}", _charset="utf-8")

            # Connect to Gmail's SMTP server
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(gmail_username, gmail_password)

                # Send the email
                server.sendmail(gmail_username, recipient_email, body.as_string())

            # Update the previous notification in the JSON file
            file_path = 'previous_notification.json'
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(previous_notification, file, ensure_ascii=False)

            # Print the notification
            print(f"Notification sent:\n{message}")

        else:
            # If there is no new notification, send a message indicating that
            print("No new news received. Sending a notification.")

            # Send the email using Gmail for the "no new news" case
            no_news_message = "No new news available."
            no_news_subject = 'No New Notification from Your College'
            no_news_body = MIMEText(f"To: {recipient_email}\nSubject: {no_news_subject}\n\n{no_news_message}", _charset="utf-8")

            # Connect to Gmail's SMTP server for the "no new news" case
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(gmail_username, gmail_password)

                # Send the email for the "no new news" case
                server.sendmail(gmail_username, recipient_email, no_news_body.as_string())

        # Sleep for 10 minutes before checking again
        time.sleep(300)

    except Exception as e:
        # Handle exceptions, e.g., network errors or issues with the website
        print(f"An error occurred: {str(e)}")
        # Sleep for 10 minutes before retrying
        time.sleep(300)
