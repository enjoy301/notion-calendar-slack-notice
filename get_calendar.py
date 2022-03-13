from notion_client import Client
import yaml
from datetime import datetime
from datetime import timedelta


with open('secrets.yml') as f:
    config = yaml.load(f, Loader=yaml.BaseLoader)
    token = config['token']

notion = Client(auth=token)

# query 칠 때 datetime.now()하면 자동으로 9시간을 더해줌 -> git action 적용할 때 개꿀
# git action 할 때 13일 23시에 cron 적용 -> 13 23:00 ~ 15 23:59까지 결과 or 16 00:00 ~ 22 23:59까지 중 일주일알림 true
one_day_schedules = notion.databases.query(
    **{
        "database_id": "6282847877b54bbfa3c9254df95e6bd4",
        "filter": {
            "and": [
                {
                    "property": "날짜",
                    "date": {
                        "on_or_after": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                    },
                },
                {
                    "property": "날짜",
                    "date": {
                        "on_or_before": (datetime.now()+timedelta(days=2)).strftime('%Y-%m-%dT23:59:59'),
                    },
                },
                {
                    "property": "title",
                    "rich_text": {
                        "is_not_empty": True,
                    },
                }
            ]
        }
    }
)

week_schedules = notion.databases.query(
    **{
        "database_id": "6282847877b54bbfa3c9254df95e6bd4",
        "filter": {
            "and": [
                {
                    "property": "날짜",
                    "date": {
                        "on_or_after": (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
                    },
                },
                {
                    "property": "날짜",
                    "date": {
                        "on_or_before": (datetime.now() + timedelta(days=9)).strftime('%Y-%m-%dT23:59:59'),
                    },
                },
                {
                    "property": "일주일알림",
                    "checkbox": {
                        "equals": True
                    }
                },
                {
                    "property": "title",
                    "rich_text": {
                        "is_not_empty": True,
                    },
                }
            ]
        }
    }
)

one_day_schedules = one_day_schedules['results']
for one_day_schedule in one_day_schedules:
    print(str(one_day_schedule['properties']['날짜']['date']['start'])+'까지', one_day_schedule['properties']['이름']['title'][0]['text']['content'])
print()

week_schedules = week_schedules['results']
for week_schedule in week_schedules:
    print(str(week_schedule['properties']['날짜']['date']['start'])+'까지', week_schedule['properties']['이름']['title'][0]['text']['content'])
