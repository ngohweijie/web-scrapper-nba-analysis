
# coding: utf-8

# In[2]:


import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
from time import sleep
from random import randint


# In[79]:


def extract_content(all_div,team,output):

    for container in all_div:
        output['Team'].append(team.capitalize())
        
        name = container.a.find('p', class_='nba-player-index__name').text
        output['Name'].append(name)
        
        details = container.a.find('div', class_='nba-player-index__details').text
        position = re.match('[A-Za-z]+',details).group(0)
        output['Position'].append(position)
        
        numbers = re.findall('\d+', details)
        height_in_inches = (int(numbers[0]) * 12) + int(numbers[1])
        height = round(height_in_inches * 2.54)
        output['Height (cm)'].append(height)
        
        weight = round((int(numbers[2])/2.205),2)
        output['Weight (kg)'].append(weight)
        
        bmi = round((weight/(height/100)**2),2)
        output['BMI'].append(bmi)
        
        name_len = len(re.findall('[A-Za-z]',name))
        output['Length of Name'].append(name_len)
        
    return output


# In[80]:


teams = [['atl','hawks'],
         ['bos','celtics'],
         ['bkn','nets'],
         ['cha','hornets'],
         ['chi','bulls'], 
         ['cle','cavaliers'],
         ['dal','mavericks'],
         ['den','nuggets'],
         ['det','pistons'],
         ['gsw','warriors'],
         ['hou','rockets'],
         ['ind','pacers'],
         ['lac','clippers'],
         ['lal','lakers'],
         ['mem','grizzlies'],
         ['mia','heat'],
         ['mil','bucks'],
         ['min','timberwolves'],
         ['nop','pelicans'],
         ['nyk','knicks'],
         ['okc','thunder'],
         ['orl','magic'],
         ['phi','sixers'],
         ['phx','suns'],
         ['por','blazers'],
         ['sac','kings'],
         ['sas','spurs'],
         ['tor','raptors'],
         ['uta','jazz'],
         ['was','wizards']]

#final output
output = {'Team': [], 'Name': [], 'Position': [], 'Height (cm)': [], 'Weight (kg)': [], 'BMI': [], 'Length of Name': []}

#create request object
for team in teams:
    url = "https://www.nba.com/teams/" + team[1]
    r = requests.get(url)

    #create soup object 
    soup = BeautifulSoup(r.text,'html.parser')
    
    #finding the right div container
    all_div = soup.find_all('section', class_='nba-player-index__trending-item small-4 medium-3 large-2 team-'+team[0]+'-'+team[1])

    #control crawler
    sleep(randint(2,10))
    
    #extract content and store into output
    results = extract_content(all_div,team[1],output)
    
#convert output into dataframe
results_df = pd.DataFrame(results)


# In[5]:


#shows entire 'inspect' in a clean form
print(soup.prettify())


# In[90]:


results_df.head()


# In[59]:


url = 'https://www.basketball-reference.com/leagues/NBA_2020_standings.html'
r = requests.get(url)
soup = BeautifulSoup(r.text,'html.parser')

output = {'Team': [], 'Record': [], 'Height (cm)': [], 'Weight (kg)': [], 'BMI': [], 'Length of Name': []}

all_div = soup.find_all('tr', class_='full_table')
for container in all_div:
    if len(output['Team']) < 30:
        team = container.th.a.text
        output['Team'].append(team)
        record = container.find('td', attrs={'data-stat': 'win_loss_pct'}).get_text()
        record_formatted = float('0' + record)
        output['Record'].append(record_formatted)
        
for height in results_df.groupby('Team')['Height (cm)'].mean():
    output['Height (cm)'].append(height)
    
for weight in results_df.groupby('Team')['Weight (kg)'].mean():
    output['Weight (kg)'].append(weight)

for bmi in results_df.groupby('Team')['BMI'].mean():
    output['BMI'].append(bmi)
    
for name_len in results_df.groupby('Team')['Length of Name'].mean():
    output['Length of Name'].append(name_len)
    
#convert output into dataframe
summary_df = pd.DataFrame(output)


# In[60]:


summary_df.sort_values('Record', ascending=False)


# In[77]:


import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[83]:


summary_df.describe()


# In[73]:


summary_df.corr()


# In[89]:


sns.heatmap(summary_df.corr(),annot=True, cmap='Spectral')


# In[75]:


sns.jointplot(x = 'Record', y='Weight (kg)', data=summary_df)

