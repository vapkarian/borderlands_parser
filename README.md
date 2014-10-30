[![Stories in Ready](https://badge.waffle.io/vapkarian/borderlands_parser.png?label=ready&title=Ready)](https://waffle.io/vapkarian/borderlands_parser)
Borderlands SHiFT codes parser
==================

Script for parsing Borderlands 2 and Borderlands Pre-Sequel SHiFT Codes from social networks and sending them by email.

**About SHiFT Codes**: http://borderlands.wikia.com/wiki/SHiFT

You can use script either by command-line or from another python script.
In first case you can call it like:<br>
`python borderlands_parser/main.py <user@example.com> <password> [option parameters]`<br>
You can also see help with:<br>
`python borderlands_parser/main.py -h`<br>
If you want use script from another python script, you should import it and calling function "main" with parameters.

In both case you can provide next parameters:
 - user (required): username to use for the SMTP server
 - password (required): password to use for the SMTP server
 - host (optional): the host to use for sending email (default: "smtp.gmail.com")
 - port (optional): port to use for the SMTP server (default: 587)
 - email_to (optional): list of email recipients separated by space (default: own user)
 - subject (optional): subject of the message (default: "SHiFT Codes")
 - ps (optional): find and parse Pre-Sequel codes instead of Borderland 2 (default: False)

If you import this module, you can override next parameters:
 - EMAIL_HOST: default of "host" parameter
 - EMAIL_PORT: default of "port" parameter
 - EMAIL_SUBJECT: default of "subject" parameter
 - BL2_SOURCES or BLPS_SOURCES: tuple of ("url", "prefix_re"), where "url" is url of page where SHiFT Codes are placed
    and "prefix_re" is pattern of special prefix of SHiFT codes for this page

Example of usage:<br>
`import borderlands_parser`<br>
`borderlands_parser.EMAIL_HOST = '127.0.0.1'`<br>
`borderlands_parser.SOURCES += (('<url>', '<prefix_re>'),)`<br>
`borderlands_parser.main('<user'>, '<password>', **kwargs)`<br>
