cd ~/Projects/ab-reminder-bot
source .venv/bin/activate
next_date=`date -v+friday +'%Y-%m-%d'`
python run.py page $next_date