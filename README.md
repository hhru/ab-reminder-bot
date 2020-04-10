# AB Reminder bot

AB fulfillment service. Creates wiki page, and reminds about it in specific Slack channel


### Requirements
 * Python 3
### How to use

Copy `bot_settings.py.ex` to `bot_settings.py` and fill empty values, update templates if needed

Install requirements with `pip install -r requirements.txt`

Commands:
* `python run.py users` to generate userlist, this must be done only if something changed since last run
* `python run.py page [<DATE>]` to create wiki page and send first reminder to Slack. `<DATE>` will be used in page title and must be unique. If date is not provided, bot will try to use `bot_settings.defaults['date']`
* `python run.py remind [<DATE>]` to send second Slack notification with non-filled cells mention
