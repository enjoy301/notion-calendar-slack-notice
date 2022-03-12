from notion_client import Client
import yaml
import os


with open('secrets.yml') as f:
    config = yaml.load(f, Loader=yaml.BaseLoader)
    token = config['token']

notion = Client(auth=token)

calendar = notion.databases.query(
    **{
        "database_id": "6282847877b54bbfa3c9254df95e6bd4",
        "filter": {
            "property": "이름",
            "rich_text": {
                "is_not_empty": True
            }
        }
    }
)

results = calendar['results']
for result in results:
    print(result['properties']['이름']['title'][0]['plain_text'])
