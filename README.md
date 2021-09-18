# Conference emailer utilities

This serves as an alternative to things like mail monkey and other letter chimps. It allows you to send bulk emails in a controlled and simple-for-coders way.

## Email lists

Lists of folks to email can come from:
- Google sheets
- [Wafer](https://github.com/CTPUG/wafer)
- Quicket

## Managing unsubscribes

On emails sent out, include a link to a Google form. Allow the user to fill in their email address. This will populate a Google sheet. When emails get sent out then this list of email addresses will get referenced and unsubscribed folks will be removed.

## The actual email

These are rendered using Mako templates. The current templates are all PyconZA2021 related.

## How to use

- Use `pipenv install` to install
- Look at settings.py to see available environmental variables
- The entry point of this is `send_emails.py`. Take a look.





## Example workflow: creating testing an sending a bulk email

### Step 1: Email content and layout:

Make a file that specifies the html of the email. Eg: templates/news/17_september_2021.html

We use Mako.

You can see what it will look like by running a command like this:
```
python send_emails.py --template_name "news/17_september_2021.html" --list_name="Community and event news" --subject="News" --dry_run_render_to_file_path="gitignore/now.html"  --from_email="form@org.whatevs" --dry_run_fetch_recipients=False
```

Note: The logo wont look good in the file. Don't panic. Email images are just a little weird. You'll see it in the next step.

### Step 2: Just send the email to yourself

Next up you'll want to make sure that it looks good as an actual email.  You can do it using a command like this:

```
python send_emails.py --dry_run_send_to_email_address="my@email.com"  --template_name "news/17_september_2021.html" --list_name="Community and event news" --subject="News" --from_email="form@org.whatevs" --dry_run_fetch_recipients=False
```

Go take a look at your inbox. Happy with what you see?

### Step 3: Optional. Check that you are happy with the recipient list

This does everything except send the actual emails. So you can see what is going to happen, who will get emailed etc.

```
python send_emails.py --template_name "news/17_september_2021.html" --list_name="Community and event news" --subject="News" --from_email="form@org.whatevs" --dry_run_dont_send=True --include_wafer_users=True
```

### Step 4: Send the emails

```
python send_emails.py --template_name "news/17_september_2021.html" --list_name="Community and event news" --subject="News" --from_email="form@org.whatevs" --include_wafer_users=True
```
