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





