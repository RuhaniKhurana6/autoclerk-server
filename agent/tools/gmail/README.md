# Gmail Automation Tool

This tool provides functionality to automate Gmail operations using the Gmail API. It allows you to send emails, manage drafts, list messages, and perform other email-related tasks programmatically.

## Features

- Send emails with attachments
- Create and manage draft emails
- List and search emails
- Delete messages
- Modify message labels
- OAuth 2.0 authentication

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up Google Cloud Project and Enable Gmail API:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Gmail API for your project
   - Create OAuth 2.0 credentials (Desktop application)
   - Download the credentials and save as `credentials.json` in the same directory as the script

## Usage Example

```python
from gmailauto import GmailAutomation

# Initialize the Gmail automation tool
gmail = GmailAutomation()

# Authenticate (this will open a browser window for OAuth)
gmail.authenticate()

# Create and send an email
message = gmail.create_message(
    sender='your.email@gmail.com',
    to='recipient@example.com',
    subject='Test Email',
    message_text='This is a test email.',
    attachments=['path/to/attachment.pdf']  # Optional
)

# Send the email
gmail.send_message(message)

# List recent messages
messages = gmail.list_messages(max_results=5)
for msg in messages:
    print(gmail.get_message(msg['id']))
```

## Security Notes

- The `credentials.json` file contains your OAuth 2.0 client credentials
- The `token.json` file will be created after authentication and contains your access tokens
- Keep both files secure and never commit them to version control
- Add both files to your `.gitignore`

## Error Handling

All methods include error handling and will return:
- `None` or `False` on failure
- Appropriate data structure or `True` on success
- Error messages are printed to console

## Contributing

Feel free to submit issues and enhancement requests!