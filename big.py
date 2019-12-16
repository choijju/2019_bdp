#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import datetime
import requests

key = '1b8e339e4c9b02819762f38126e4003a'

def crawl_data(start_date, end_date, keys = key):
    
    final_list = []
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
    
    for single_date in pd.date_range(start_date, end_date):
        for multi, rep in zip(["N"], [""]):
            payload = {
                'key' : keys,
                'targetDt' : single_date.strftime('%Y%m%d'),
                'multiMovieYn' : 'N',
                'itemPerPage' : '10',
                'repNationCd' : rep
            }
            req = requests.get(url, params = payload)
            
            for item in req.json()['boxOfficeResult'] ['dailyBoxOfficeList'] :
                
                temp_list = []
                key_list = []
                
                for key, value in item.items():
                    key_list.append(key)
                    temp_list.append(value)
                    
                temp_list.append(single_date)
                key_list.append('CurrentDate')
                
                temp_list.append('N')
                key_list.append('multi')
                
                temp_list.append(rep)
                key_list.append('Nation')
                
                final_list.append(temp_list)
                
    return pd.DataFrame(final_list, columns=key_list)

movie = crawl_data("20190101", "20190131", keys = key)
movies = movie.filter(items=['rank', 'movieNm', 'movieCd', 'scrnCnt', 
                             'audiCnt', 'openDt', 'CurrentDate'])


# In[ ]:


movies


# In[78]:


movies.to_csv('movies_jan.csv', encoding = 'utf-8', index = False)


# In[ ]:




