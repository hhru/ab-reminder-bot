# AB Reminder bot

AB fulfillment service

### How to use

Copy `bot_settings.py.ex` to `bot_settings.py` and fill empty values

Update `/lib/templates.py` according your needs

Commands:
* `python run.py users` to generate userlist
* `python run.py page <DATE>` to create wiki page and send first reminder to Slack. `<DATE>` will be used in page title and must be unique
* `python run.py remind <DATE>` to send second Slack notification with non-filled cells mention
