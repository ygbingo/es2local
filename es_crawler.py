# -*- coding: utf-8 -*-
"""
Download data from es
"""
import time
import requests
import json
from save_file import save_local_csv
import os
import re

class ES_CRALWER():
    def __init__(self, host, port, auth, PATCH_SIZE=100000, FETCH_SIZE=10000, file_head="es_crawler_res", res_path="./crawler_results/") -> None:
        self.url = host + ":" + port + "/_sql"
        self.auth = auth
        self.PATCH_SIZE = PATCH_SIZE
        self.FETCH_SIZE = FETCH_SIZE
        self.file_head = file_head
        self.res_path = res_path
        self.titles = []
        pass

    def check_query(self, query):
        if '*' in query:
            raise RuntimeError("not support * in query, please query ensure features.")

        select_pat = r'select (.*) from .*'
        self.titles = re.match(select_pat, query).group(1).replace(' ', '').split(',')
        if len(self.titles) < 1:
            raise RuntimeError("invalid sql, please check if any string between select and from: " + str(query))

        

    def get_response(self, url, headers, body):
        status_code = None
        content = None
        cursor = None
        for i in range(0, 4):
            try:
                response = requests.request("POST", url, headers=headers, data=json.dumps(body))
                status_code = response.status_code
                if status_code == 200:
                    content = json.loads(response.content)
                    if "cursor" in content:
                        cursor = content["cursor"]
                    else:
                        pass
                    content = json.loads(response.content)

                else:
                    content = json.loads(response.content)
                break
            except Exception as e:
                print("Failed: " + str(e))
                if content:
                    print(content)
                time.sleep(2)
                print("Query Again.")
        return status_code, content, cursor

    def run_sql(self, query):
        self.check(query)

        headers = {
            'Authorization': self.auth,
            'Content-Type': 'application/json',
            'Keep-Alive': 'false'
        }

        body = {
            'query': query,
            'fetch_size': self.FETCH_SIZE
        }
        idx = len(os.listdir(self.res_path))
        status_code, content, cursor = self.get_response(self.url, headers, body)

        if status_code == 200:
            columns = content["columns"]
            keys = []
            for column in columns:
                keys.append(column["name"])

            rows = content["rows"]
            while cursor:
                body = {
                    "cursor": cursor
                }
                status_code, content, cursor = self.get_response(self.url, headers, body)
                if status_code == 200:
                    rows.extend(content["rows"])
                    if len(rows) > self.PATCH_SIZE:
                        file_name = self.res_path + self.file_head + "_" + idx + ".csv"
                        save_local_csv(rows.copy(), self.titles, file_name)
                        idx += 1
                        rows.clear()
                time.sleep(3)
            if len(rows) > 0:
                save_local_csv(rows.copy(), self.titles, file_name)
            return
        else:
            raise RuntimeError("Error from es sql: " + str(content))
