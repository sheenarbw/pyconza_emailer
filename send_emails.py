from pathlib import Path
import fire
import logging  # TODO: log to a file and console
import time
import settings
import utils

EMAIL = "email"


def _fetch_email_preferences_sheet(list_name):
    settings.EMAIL_PREFERENCE_SHEET_URL
    COL_LISTS = "Please tick the lists that you would like to be a part of"
    COL_EMAIL = "Email address"
    COL_TIMESTAMP = "Timestamp"


def _fetch_recipients(list_name):
    _fetch_email_preferences_sheet(list_name)


def send_emails(
    template_name,
    list_name,
    subject,
    from_email="from@example.com",
    # preference_sheet_url=None,
    dry_run_render_to_file_path=None,
    dry_run_send_to_email_address=None,
    dry_run_fetch_recipients=True,
    start_at_recipient_number=1,
    **template_kwargs,
):
    """
    Example usage:
    python send_emails.py --template_name "base.html" --list_name="boo" --subject="yay" --message="this is a test" --dry_run_render_to_file_path="gitignore/rendered_base.html"
    python send_emails.py --template_name "base.html" --list_name="boo" --subject="yay" --message="this is a test" --dry_run_send_to_email_address="sheena.oconnell@gmail.com" from_email="sponsorship@za.pycon.org"

    RECIPIENTS
    - list_name: this allows us to let people be on multiple email lists. eg "Community and event news","Sponsorship packages". The name passed in here should match something in the preferences sheet
    - preference_sheet_url. This can be a parameter or environmental variable. see settings.py
    - start_at_recipient_number: this allows us to pick up where we left off. Eg let's say we are sending 5 emails and the first 3 work then the power dies. We want to start the process again from number 4

    DRY RUNS
    - dry_run_render_to_file_path: this doesn't send an email, it rather just renders the email and sticks it in a file. NOTE: The logo wont render properly except as an email
    - dry_run_send_to_email_address: if this is set then the whole script will run EXCEPT emails wont actually get sent to the recipients. A single email will get sent to the dry_run_email_address
    - dry_run_fetch_recipients: if we are doing a dry run then making this true will tell the script to fetch all the recipients
    """

    preference_sheet_url = preference_sheet_url or settings.EMAIL_PREFERENCE_SHEET_URL

    template_kwargs["title"] = template_kwargs.get("title", subject)

    if dry_run_fetch_recipients:
        recipients = _fetch_recipients(list_name=list_name)
    if dry_run_send_to_email_address:
        recipients = [{EMAIL: dry_run_send_to_email_address}]
    elif dry_run_render_to_file_path:
        recipients = [{EMAIL: "someone-nice@example.com"}]

    total = len(recipients)
    for n, recipient in enumerate(recipients):
        number = n + 1
        if number < start_at_recipient_number:  # skip if we need to
            continue

        logging.info(f"sending to recipient {number}/{total}: {recipient[EMAIL]}")

        html = utils.render_template(
            name=template_name, template_kwargs=template_kwargs
        )
        if dry_run_render_to_file_path:
            with open(Path(dry_run_render_to_file_path), "w") as f:
                f.write(html)
            return

        # actually send the email
        utils.send_html_email(
            to_email=recipient[EMAIL], from_email=from_email, html=html, subject=subject
        )
        time.sleep(
            10
        )  # TODO: I'm not sure if there is any rate limiting set up on the smtp server. So this might need to change


if __name__ == "__main__":
    fire.Fire(send_emails)
