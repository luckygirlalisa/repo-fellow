import json
import time
import organization
import requests
from   requests_html import HTMLSession
import logging

class CrawlerClient:
    def __init__(self,site,token,data_path = "./data"):
        self.site = site
        self.token = token
        self.session = HTMLSession()
        self.data_path = data_path

    def getSingleResource(self,url,retry = True):
        query = self.site + url 
        logging.info(query)
        while True:
            try:
                response = self.session.get(url = query, timeout = 20)
                if response.status_code > 300:
                    print("Error {} to open {}".format(response.status_code,query))
                break
            except Exception as ex:
                print(ex)
                logging.info("retry {}".format(query))
                time.sleep(1)                
                continue
        return response.json()

    def check_last_value(self, data, last_field = None, last_value = None):
        if _last_field is None:
            return False
        values = []
        if len(_last_field) == 1:
            values = list(map(lambda x:x[_last_field[0]],data))
        if len(_last_field) == 3:
            values = list(map(lambda x:x[_last_field[0]][_last_field[1]][_last_field[2]],data))
        return last_value in values
        
    def getResource(self,url,limit = None, page = None, recordsPerPage = None, last = None, retry = True):
        _page,_recordsPerPage = 1, 100
        _last_field = None
        if page is not None:
            _page = page
        if recordsPerPage is not None:
            _recordsPerPage = recordsPerPage
        if last is not None:
            _last_field,_last_value = last
            _last_field = _last_field.split('/')
        data = []
        while True:
            query = self.site + url + "&page={}&per_page={}".format(_page,_recordsPerPage)
            print(query)
            try:
                response = self.session.get(url = query, timeout = 20)
                if response.status_code > 300:
                    print("Error {} to open {}".format(response.status_code,query))
                    break
                ret = response.json()
                data = data + ret
                _page = _page + 1
                if limit is not None and len(data) >= limit:
                    return data[:limit]
                if(len(ret) < _recordsPerPage):
                    break
            except(Exception):
                print("[ERROR] read failed {}".format(query))
                if retry:
                    break
                else:
                    continue
        return data