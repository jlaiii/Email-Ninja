import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

# Function to load email accounts from a config file
def load_email_accounts():
    try:
        with open('email_accounts.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to save email accounts to a config file
def save_email_accounts(accounts):
    with open('email_accounts.json', 'w') as file:
        json.dump(accounts, file, indent=4)

# Function to load recipient emails from a config file
def load_recipient_emails():
    try:
        with open('recipient_emails.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to save recipient emails to a config file
def save_recipient_emails(recipient_emails):
    with open('recipient_emails.json', 'w') as file:
        json.dump(recipient_emails, file, indent=4)

# Function to prompt the user to choose an email account
def choose_email_account(accounts):
    print("Choose an email account to use:")
    for i, account in enumerate(accounts, 1):
        print(f"{i}: {account}")
    print(f"{len(accounts) + 1}: New Account")

    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(accounts) + 1:
                return choice
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Function to prompt the user to choose a recipient email
def choose_recipient_email(recipient_emails):
    print("Choose a recipient email or enter a new one:")
    for i, email in enumerate(recipient_emails, 1):
        print(f"{i}: {email}")
    print(f"{len(recipient_emails) + 1}: New Email")
    print(f"{len(recipient_emails) + 2}: Send to ALL Recipients")

    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(recipient_emails) + 2:
                if choice == len(recipient_emails) + 1:
                    new_email = input("Enter a new recipient email address: ")
                    recipient_emails.append(new_email)
                    save_recipient_emails(recipient_emails)
                    return new_email
                elif choice == len(recipient_emails) + 2:
                    return recipient_emails  # Return all recipient emails
                else:
                    return recipient_emails[choice - 1]
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Main menu function
def main_menu():
    while True:
        email_accounts = load_email_accounts()
        recipient_emails = load_recipient_emails()

        choice = choose_email_account(email_accounts)

        if choice == len(email_accounts) + 1:
            sender_email = input("Enter your email address: ")
            sender_password = input("Enter your email password: ")
            email_accounts[sender_email] = sender_password
            save_email_accounts(email_accounts)
        else:
            sender_email = list(email_accounts.keys())[choice - 1]
            sender_password = email_accounts[sender_email]

        recipients = choose_recipient_email(recipient_emails)
        if isinstance(recipients, list):  # Send to all recipients
            subject = input("Enter the subject of your email: ")
            message = input("Enter your email message: ")

            # Create a MIMEText object for the email content
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = ", ".join(recipients)  # Join recipient emails with a comma
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            # Set up the SMTP server
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587

            # Establish a secure connection with the SMTP server
            try:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(sender_email, sender_password)
                
                # Send the email
                server.sendmail(sender_email, recipients, msg.as_string())
                print(f"Email sent successfully to ALL recipients!")
                
            except Exception as e:
                print(f"Error sending email to ALL recipients: {str(e)}")

            # Close the SMTP server
            server.quit()
        else:  # Send to a single recipient
            subject = input("Enter the subject of your email: ")
            message = input("Enter your email message: ")

            # Create a MIMEText object for the email content
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipients
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            # Set up the SMTP server
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587

            # Establish a secure connection with the SMTP server
            try:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(sender_email, sender_password)
                
                # Send the email
                server.sendmail(sender_email, recipients, msg.as_string())
                print(f"Email sent successfully to {recipients}!")
                
            except Exception as e:
                print(f"Error sending email to {recipients}: {str(e)}")

            # Close the SMTP server
            server.quit()

if __name__ == "__main__":
    main_menu()
