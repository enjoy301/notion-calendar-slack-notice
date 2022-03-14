from notion_client import Client
import yaml
from datetime import datetime
from datetime import timedelta


class NotionApi:
    def __init__(self):
        self.week_schedules = None
        self.one_day_schedules = None
        self.token = None
        self.notion = None

    def get_notion_token(self):
        with open('secrets.yml') as f:
            config = yaml.load(f, Loader=yaml.BaseLoader)
            self.token = config['notion-token']

    def notion_instance(self):
        self.notion = Client(auth=self.token)

    def get_one_day_schedule(self):
        # query 칠 때 datetime.now()하면 자동으로 9시간을 더해줌 -> git action 적용할 때 개꿀
        # git action 할 때 13일 23시에 cron 적용 -> 13 23:00 ~ 15 23:59까지 결과 16
        one_day_schedules = self.notion.databases.query(
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
        self.one_day_schedules = one_day_schedules['results']

    def get_week_schedules(self):
        # 13일 23시에 cron 적용 -> 00:00 ~ 22 23:59까지 중 일주일알림 true
        week_schedules = self.notion.databases.query(
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
        self.week_schedules = week_schedules['results']

    def preprocessing_one_day_schedules(self):
        temp_list = list()
        for one_day_schedule in self.one_day_schedules:
            temp_list.append((one_day_schedule['properties']['이름']['title'][0]['text']['content'], one_day_schedule['properties']['날짜']['date']['start']))
        self.one_day_schedules = temp_list

    def preprocessing_week_schedules(self):
        temp_list = list()
        for week_schedule in self.week_schedules:
            temp_list.append((week_schedule['properties']['이름']['title'][0]['text']['content'], week_schedule['properties']['날짜']['date']['start']))
        self.week_schedules = temp_list
