from postmarker.core import PostmarkClient


class Postmark:
    """Takes an input of the recipient email address"""

    def __init__(self, recipient):
        self.recipient = recipient

    def send_mail(self):
        postmarker = PostmarkClient(
            server_token='server_token')
        postmarker.emails.send(
            From='sample@email.com',
            To=self.recipient,
            Subject='Postmark test',
            HtmlBody='HTML body goes here'
        )
