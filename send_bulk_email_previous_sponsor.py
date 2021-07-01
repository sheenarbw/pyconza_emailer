from utils import send_email_from_template
import csv
import time


with open("gitignore/PyConZA Sponsor Contact List - Sponsors.csv") as f:
    reader = csv.reader(f)
    headers = next(reader)
    rows = [dict(zip(headers, line)) for line in reader]

rows = [row for row in rows if row["Previous Status"].strip() == "Sponsored"]
rows = [row for row in rows if row["Email"].strip() != ""]


for row in rows:
    print(f"processing {row['Organization']} {row['Email']}")

    send_email_from_template(
        template_name="email_previous_sponsor.html",
        template_kwargs={
            "title": "PyConZA 2021 is looking for sponsors",
            "company": row["Organization"],
        },
        # to_email="sheena.oconnell@umuzi.org",
        to_email=row["Email"],
        from_email="sponsorship@za.pycon.org",
        subject="PyConZA call for sponsors",
    )
    # break

    time.sleep(10)
