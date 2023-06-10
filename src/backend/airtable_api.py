import requests
from airtable import Airtable

def clean_table(api_key, base_id, table_name):
    door_database = Airtable(base_id, table_name, api_key)
    door_records = door_database.get_all()

    # print(door_records)

    for i in range(len(door_records)):
        # print(door_records[i]['id'])
        door_database.delete(door_records[i]['id'])