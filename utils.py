import smtplib, ssl
from email.message import EmailMessage
from email.utils import formatdate
from config import SMTP_HOST, SMTP_PASSWORD, SMTP_USERNAME

# import markdown


def send_email(to_email, from_email, text):
    context = ssl.create_default_context()

    PORT = 587
    server = smtplib.SMTP(SMTP_HOST, PORT)
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(SMTP_USERNAME, SMTP_PASSWORD)

    message = EmailMessage()
    message.set_content(text)
    message["Subject"] = f"test"
    message["From"] = from_email
    message["To"] = to_email
    message["Date"] = formatdate(localtime=True)
    server.send_message(message)
    server.quit()


# with open("templates/base_sponsorship_email.md") as f:
#     message = f.read()


# html = markdown.markdown(message)

# send_email(
#     to_email="sheena.oconnell@umuzi.org",
#     from_email="sponsorship@za.pycon.org",
#     text=message,
#     html=html,
# )


def render_template(name):
    from mako.template import Template
    from mako.lookup import TemplateLookup

    lookup = TemplateLookup(directories=["templates"])
    template = lookup.get_template(name)
    return template.render()


def render_to_file(name):
    """just for testing purposes"""
    from pathlib import Path

    result = render_template(name)
    with open(Path("gitignore") / name, "w") as f:
        f.write(result)


render_to_file("base.html")
render_to_file("first_time_sponsor_email.html")
