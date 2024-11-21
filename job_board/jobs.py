import numpy as np
import requests
from collections import defaultdict
from bs4 import BeautifulSoup
import pandas as pd


def get_data_frame():

    def description(ref):

        url = "https://news.ycombinator.com/"+ref
        res = requests.get(url)

        soup=BeautifulSoup(res.text,'html.parser')
        title= str(soup.select('title')).replace('[','').replace(']','')[:-21]
        content = str(soup.select('div.toptext')).replace('[','').replace(']','').replace('\n','')


        soup1 = BeautifulSoup(content, 'html.parser')
        text_content = soup1.get_text()

        soup2 = BeautifulSoup(title, 'html.parser')
        text_title = soup2.get_text()

        return text_content



    def combine_links(url):
        i=1
        mega_link=[]
        while i<2 and url:
            #res=requests.get('https://news.ycombinator.com/jobs?p='+str(i))
            res = requests.get(url + str(i))
            soup=BeautifulSoup(res.text,'html.parser')
            links=soup.select('.titleline')
            mega_link=mega_link+links
            i=i+1
        return mega_link


    def combine_subtext(url):
        i=1
        mega_subtext=[]
        while i<2 and url:
            res=requests.get('https://news.ycombinator.com/jobs?p='+str(i))
            soup=BeautifulSoup(res.text,'html.parser')
            subtext=soup.select('.subtext')
            mega_subtext=mega_subtext+subtext
            i=i+1
        return mega_subtext

    def create_custom_hacker_jobs(links,subtext):
        hn=[]
        hn1=[]
        for idx,item in enumerate(links):

            title=item.getText()
            href=item.find('a').get('href',None)
            hn.append({'title': title, 'link': href})

        return hn


    list_jobs = create_custom_hacker_jobs(combine_links('https://news.ycombinator.com/jobs?p='),combine_subtext('https://news.ycombinator.com/jobs?p='))
    result = defaultdict(list)
    # Loop through the list of dictionaries
    for d in list_jobs:
        for key, value in d.items():
            result[key].append(value)
    # Print the result
    result=dict(result)
    df = pd.DataFrame(result)

    df['description'] = df.apply(lambda row: description(row['link']) if row['link'].startswith('item') else row['link'], axis=1)
    #df.to_csv("posting_jobs.csv",index=False)
    return df