from get_calendar import NotionApi
from slack_notice import SlackApi
from datetime import datetime
from datetime import timedelta


notion = NotionApi()
slack = SlackApi()

notion.get_notion_token()
notion.notion_instance()
notion.get_one_day_schedule()
notion.get_week_schedules()
notion.preprocessing_one_day_schedules()
notion.preprocessing_week_schedules()

slack.get_bot_token()
slack.create_instance()

# git action은 UTC+0이라 보정
now = datetime.now()+timedelta(hours=9)

messages = list()
messages.append(f':one: 내일 할 일 ( {(now+timedelta(days=2)).strftime("%Y/%m/%d")} ) :one:')
for schedule in notion.one_day_schedules:
    date = str(schedule[1]).split('.000+')[0]
    messages.append(schedule[0] + ' ( ' + date + ' 까지 )')

messages.append(f':seven: 일주일 할 일 ( {(now+timedelta(days=3)).strftime("%Y/%m/%d")} ~ {(now+timedelta(days=9)).strftime("%Y/%m/%d")} ) :seven:')
for schedule in notion.week_schedules:
    date = str(schedule[1]).split('.000+')[0]
    messages.append(schedule[0] + ' ( ' + date + ' 까지 )')

slack.post_messages(messages)
