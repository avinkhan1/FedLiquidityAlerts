import time
import datetime
import schedule

from utilities.liquidity import run_liquidty_calculations


def run_net_liquidity_script():
    # Check if current day is a weekday
    if datetime.datetime.today().weekday() < 5:
        now = datetime.datetime.now()
        if now.hour == 13 and now.minute == 16:
            run_liquidty_calculations('RRP')
        else:
            run_liquidty_calculations('TGA')


def run_net_liquidity_script_thursday():
    # Check if current day is Thursday
    if datetime.datetime.today().weekday() == 3:
        run_liquidty_calculations('WALCL')


def run_net_liquidity_script_immediately():
    # Your script here
    print("Running script immediately...")
    run_liquidty_calculations('TGA')


# Schedule the script to run at 1:01 PM and 4:01 PM on weekdays
schedule.every().day.at("13:16").do(run_net_liquidity_script)
schedule.every().day.at("16:01").do(run_net_liquidity_script)

# Schedule the script to run at 4:31 PM on Thursdays
schedule.every().day.at("16:31").do(run_net_liquidity_script_thursday)

# Schedule the script to run immediately
# Uncomment the following line when testing
# schedule.every().minute.do(run_net_liquidity_script_immediately)

while True:
    schedule.run_pending()
    time.sleep(1)
