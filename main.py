import argparse
from email.mime.text import MIMEText
from itertools import repeat
import smtplib
import urllib2
import os
import re


BL2_SOURCES = (
    ('https://twitter.com/duvalmagic', 'WinPC/Mac: '),
    ('https://www.facebook.com/Borderlands2ShiftCodes', 'Borderlands 2.{10,200}PC: '),
)
BLPS_SOURCES = (
    ('https://twitter.com/duvalmagic', 'WinPC/Mac/Linux: '),
    ('https://www.facebook.com/Borderlands2ShiftCodes', 'The Pre-Sequel!.{10,200}PC: '),
)
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_SUBJECT = 'SHiFT Codes'


def parse_source(url, prefix_re):
    """
    Parse html page from url and find SHiFT codes with special prefix (i.e. for PC only).

    :param url: url of page with SHiFT codes
    :type url: str or unicode
    :param prefix_re: pattern of special prefix of SHiFT codes for this page
    :type prefix_re: str or unicode
    :return: keys from page
    :rtype: list
    """
    code_re = '-'.join(repeat('\w{5,5}', 5))
    compiled_code_re = re.compile(code_re)
    source_html = urllib2.urlopen(url).read()
    keys = []
    for line in re.compile(prefix_re + code_re).findall(source_html):
        code = compiled_code_re.findall(line)[0]
        keys.append(code)
    return keys


def main(user, password, host=None, port=None, email_to=None, subject=None, ps=False):
    """
    Parse pages from SOURCES, save new keys into file and send them to recipient from email_to.

    :param user: username to use for the SMTP server
    :type user: str or unicode
    :param password: password to use for the SMTP server
    :type password: str or unicode
    :param host: the host to use for sending email (default: EMAIL_HOST)
    :type host: str or unicode
    :param port: port to use for the SMTP server (default: EMAIL_PORT)
    :type port: str or unicode or int
    :param email_to: list of email recipients separated by space (default: own user)
    :type email_to: str or unicode
    :param subject: subject of the message (default: EMAIL_SUBJECT)
    :type subject: str or unicode
    """
    host = host or EMAIL_HOST
    port = port or 587
    email_to = email_to or [user]
    subject = '%s: %s' % (subject or EMAIL_SUBJECT, 'Borderlands 2' if not ps else 'Borderlands Pre-Sequel')

    filename = os.path.join(os.path.dirname(__file__), '.borderlands_codes')
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            existed_keys = f.read().splitlines()
    else:
        existed_keys = []

    sources = BL2_SOURCES if not ps else BLPS_SOURCES
    parsed_keys = []
    for url, prefix_re in sources:
        parsed_keys.extend(parse_source(url, prefix_re))

    new_keys = set(parsed_keys) - set(existed_keys)
    if new_keys:
        with open(filename, 'w') as f:
            f.write('\n'.join(set(parsed_keys + existed_keys)))
        msg = MIMEText('\n'.join(new_keys))
        msg['Subject'] = subject
        msg['From'] = user
        msg['To'] = ', '.join(email_to)
        server = smtplib.SMTP('{host}:{port}'.format(host=host, port=port))
        server.starttls()
        server.login(user, password)
        server.sendmail(user, email_to, msg.as_string())
        server.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Parse messages from official Borderlands social networks and find SHiFT codes, '
                    'if there are new keys - send them by email')
    parser.add_argument('user', help='Username to use for the SMTP server')
    parser.add_argument('password', help='Password to use for the SMTP server')
    parser.add_argument('--host', help='The host to use for sending email (default: "%s")' % EMAIL_HOST)
    parser.add_argument('--port', help='Port to use for the SMTP server (default: %s)' % EMAIL_PORT)
    parser.add_argument('--email_to', nargs='+', help='List of email recipients separated by space (default: own user)')
    parser.add_argument('--subject', help='Subject of the message (default: "%s")' % EMAIL_SUBJECT)
    parser.add_argument('-ps', action="store_true", help='Find and parse Pre-Sequel codes instead of Borderland 2')
    args = parser.parse_args()
    main(**args.__dict__)
