cd ~/Documents/infrastructure/ab-reminder-bot
source .venv/bin/activate
next_date=`date -v+friday +'%Y-%m-%d'`
python run.py remind $next_date