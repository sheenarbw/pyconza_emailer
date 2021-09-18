from pathlib import Path
import fire
import logging
import time
import settings
import utils
from google_sheet_utls import fetch_sheet
import wafer_utils

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

EMAIL = "Email address"


def _fetch_email_preferences():
    COL_LISTS = "Please tick the lists that you would like to be a part of"
    sheet = fetch_sheet(url=settings.EMAIL_PREFERENCE_SHEET_URL)
    preferences = {}
    for line in sheet:
        # the later ones overwrite the earlier ones
        preferences[line[EMAIL]] = line[COL_LISTS]
    return preferences


def _fetch_recipients(list_name, include_wafer_users, include_google_sheet):
    """returns an array of email addresses"""
    users = []
    if include_google_sheet:
        logging.info("fetching sheet users")
        users.extend([d[EMAIL] for d in fetch_sheet(url=include_google_sheet)])
    if include_wafer_users:
        logging.info("fetching wafer users")
        users.extend(wafer_utils.fetch_all_users_and_ticket_emails())
    known_preferences = _fetch_email_preferences()

    final_users = []
    for user in users:
        if user in known_preferences:
            if list_name in known_preferences[user]:
                final_users.append(user)
            else:
                logging.info(f"removing user: {user}")
        else:
            final_users.append(user)
    return set(final_users)


def send_emails(
    template_name,
    list_name,
    subject,
    from_email="from@example.com",
    dry_run_render_to_file_path=None,
    dry_run_send_to_email_address=None,
    dry_run_fetch_recipients=True,
    dry_run_dont_send=False,
    start_at_recipient_number=1,
    include_wafer_users=False,
    include_google_sheet=None,
    **template_kwargs,
):
    """
    Example usage:
    python send_emails.py --template_name "base.html" --list_name="boo" --subject="yay" --message="this is a test" --dry_run_render_to_file_path="gitignore/rendered_base.html"

    python send_emails.py --template_name "base.html" --list_name="boo" --subject="yay" --message="this is a test" --dry_run_send_to_email_address="sheena.oconnell@gmail.com" --from_email="team@za.pycon.org"

    RECIPIENTS
    - list_name: this allows us to let people be on multiple email lists. eg "Community and event news","Sponsorship packages". The name passed in here should match something in the preferences sheet EXACTLY
    - preference_sheet_url. This can be a parameter or environmental variable. see settings.py
    - start_at_recipient_number: this allows us to pick up where we left off. Eg let's say we are sending 5 emails and the first 3 work then the power dies. We want to start the process again from number 4

    DRY RUNS
    - dry_run_render_to_file_path: this doesn't send an email, it rather just renders the email and sticks it in a file. NOTE: The logo wont render properly except as an email
    - dry_run_send_to_email_address: if this is set then the whole script will run EXCEPT emails wont actually get sent to the recipients. A single email will get sent to the dry_run_email_address
    - dry_run_fetch_recipients: if we are doing a dry run then making this true will tell the script to fetch all the recipients
    """

    template_kwargs["title"] = template_kwargs.get("title", subject)

    if dry_run_fetch_recipients:
        logging.info("FETCHING RECIPIENTS...")
        recipients = _fetch_recipients(
            list_name=list_name,
            include_wafer_users=include_wafer_users,
            include_google_sheet=include_google_sheet,
        )
    else:
        logging.info("FETCHING RECIPIENTS SKIPPED")
    if dry_run_send_to_email_address:
        logging.info("...dry run: Overriding recipient list")

        recipients = [dry_run_send_to_email_address]
    elif dry_run_render_to_file_path:
        recipients = ["someone-nice@example.com"]

    total = len(recipients)
    for n, recipient in enumerate(recipients):
        number = n + 1
        if number < start_at_recipient_number:  # skip if we need to
            continue

        logging.info(f"sending to recipient {number}/{total}: {recipient}")

        html = utils.render_template(
            name=template_name, template_kwargs=template_kwargs
        )
        if dry_run_render_to_file_path:
            logging.info("...dry run: rendering to file")

            with open(Path(dry_run_render_to_file_path), "w") as f:
                f.write(html)
            return

        if dry_run_dont_send:
            logging.info("...dry run: Not sent")

        else:
            # actually send the email
            utils.send_html_email(
                to_email=recipient,
                from_email=from_email,
                html=html,
                subject=subject,
            )
            logging.info("...sent")
            time.sleep(
                10
            )  # TODO: I'm not sure if there is any rate limiting set up on the smtp server. So this might need to change


if __name__ == "__main__":
    fire.Fire(send_emails)
