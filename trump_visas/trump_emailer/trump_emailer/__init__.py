import os
import boto.ses

# throw useful errors if environment vars are missing
try:
    user = os.environ['EMAIL_USER']
except KeyError:
    user = None
    print 'EMAIL_USER environment variable missing.'

try:
    password = os.environ['EMAIL_PASS']
except KeyError:
    password = None
    print 'EMAIL_PASS environment variable missing.'

# set defaults
default_from_addr = ''
default_aws_region = ''

class Email(object):
    def __init__(self, to, subject):
        self.to = to
        self.subject = subject
        self._html = None
        self._text = None
        self._format = 'html'

    def html(self, html):
        self._html = html

    def text(self, text):
        self._text = text

    def send(self, from_addr=None):
        body = self._html

        if isinstance(self.to, basestring):
            self.to = [self.to]
        if not from_addr:
            from_addr = default_from_addr
        if not self._html and not self._text:
            raise Exception('You must provide a text or html body.')
        if not self._html:
            self._format = 'text'
            body = self._text

        connection = boto.ses.connect_to_region(
            default_aws_region,
            aws_access_key_id=user,
            aws_secret_access_key=password
        )

        return connection.send_email(
            from_addr,
            self.subject,
            None,
            self.to,
            format=self._format,
            text_body=self._text,
            html_body=self._html
        )
