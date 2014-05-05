borderlands_parser
==================

Script for parsing Borderlands 2 SHiFT Codes from social networks and sending them by email

About SHiFT Codes: http://borderlands.wikia.com/wiki/SHiFT

You can use script either by command-line or from another python script.
In first case you can call it like:
    python borderlands_parser/main.py <user@example.com> <password> [option parameters]
You can also see help with:
    python borderlands_parser/main.py -h
If you want use script from another python script, you should import it and calling function "main" with parameters.

In both case you can provide next parameters:
 - user: username to use for the SMTP server
 - password: password to use for the SMTP server
 - host (optional): the host to use for sending email (default: "smtp.gmail.com")
 - port (optional): port to use for the SMTP server (default: 587)
 - email_to (optional): list of email recipients separated by space (default: own user)
 - subject (optional): subject of the message (default: "SHiFT Codes")

If you import this module, you can override next parameters:
 - EMAIL_HOST: default of "host" parameter
 - EMAIL_PORT: default of "port" parameter
 - EMAIL_SUBJECT: default of "subject" parameter
 - SOURCES: tuple of ("url", "prefix_re"), where "url" is url of page where SHiFT Codes are placed and "prefix_re" is
    pattern of special prefix of SHiFT codes for this page
Example of usage:
    import borderlands_parser
    borderlands_parser.EMAIL_HOST = '127.0.0.1'
    borderlands_parser.SOURCES += (
        ('<url>', '<prefix_re>'),
    )
    borderlands_parser.main('<user'>, '<password>', **kwargs)
