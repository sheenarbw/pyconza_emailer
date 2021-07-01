import smtplib, ssl
from email.message import EmailMessage
from email.utils import formatdate
from config import SMTP_HOST, SMTP_PASSWORD, SMTP_USERNAME


def send_email(message):
    context = ssl.create_default_context()
    PORT = 587
    server = smtplib.SMTP(SMTP_HOST, PORT)
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(SMTP_USERNAME, SMTP_PASSWORD)
    server.send_message(message)
    server.quit()


def send_text_email(to_email, from_email, subject, text):
    message = EmailMessage()
    message.set_content(text)
    message["Subject"] = subject
    message["From"] = from_email
    message["To"] = to_email
    message["Date"] = formatdate(localtime=True)
    send_email(message)


def send_html_email(to_email, from_email, subject, html):
    import html2text
    from email.utils import make_msgid
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = from_email
    message["To"] = to_email

    h = html2text.HTML2Text()
    h.ignore_emphasis = True
    h.ignore_images = True
    h.ignore_tables = True

    text = h.handle(html)

    logo_cid = make_msgid()

    html = html.replace("{logo_cid}", logo_cid[1:-1])

    message.set_content(text)
    message.add_alternative(html, subtype="html")

    with open("images/logo.png", "rb") as img:
        message.get_payload()[1].add_related(img.read(), "image", "png", cid=logo_cid)

    send_email(message)


def render_template(name, render_kwargs):
    from mako.lookup import TemplateLookup

    lookup = TemplateLookup(directories=["templates"])
    template = lookup.get_template(name)
    return template.render(**render_kwargs)


def render_to_file(name, render_kwargs):
    """just for testing purposes"""
    from pathlib import Path

    result = render_template(name, render_kwargs)
    with open(Path("gitignore") / name, "w") as f:
        f.write(result)


def send_email_from_template(
    template_name, template_kwargs, to_email, from_email, subject
):
    html = render_template(
        template_name,
        template_kwargs,
    )

    send_html_email(
        to_email=to_email,
        from_email=from_email,
        html=html,
        subject=subject,
    )
