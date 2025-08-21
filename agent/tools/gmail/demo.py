from gmailauto import GmailAutomation

def main():
    # Initialize the Gmail automation tool
    gmail = GmailAutomation()

    # Authenticate with Gmail API
    print("Authenticating with Gmail...")
    gmail.authenticate()
    print("Authentication successful!")

    # Example: Send a test email
    print("\nCreating a test email...")
    message = gmail.create_message(
        sender='your.email@gmail.com',  # Replace with your email
        to='recipient@example.com',     # Replace with recipient's email
        subject='Test Email from Gmail Automation',
        message_text='This is a test email sent using the Gmail Automation tool.'
    )

    print("Sending the test email...")
    result = gmail.send_message(message)
    
    if result:
        print("Email sent successfully!")
    else:
        print("Failed to send email.")

    # Example: List recent messages
    print("\nFetching recent messages...")
    messages = gmail.list_messages(max_results=5)
    
    if messages:
        print(f"Found {len(messages)} recent messages:")
        for msg in messages:
            message_data = gmail.get_message(msg['id'])
            if message_data:
                headers = {header['name']: header['value'] 
                          for header in message_data['payload']['headers']}
                print(f"\nFrom: {headers.get('From', 'Unknown')}")
                print(f"Subject: {headers.get('Subject', 'No subject')}")
    else:
        print("No messages found.")

if __name__ == '__main__':
    main()