from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != "Overall":
        df = df[df['users']==selected_user]
        
    #number of messages: 
    num_messages = df.shape[0]
    #number of words:
    words=[]
    for message in df['messages']:
        words.extend(message.split())

    num_media = df[df['messages'] == "<Media omitted>"].shape[0]

    links = []
    for message in df['messages']:
        links.extend(extract.find_urls(message))


    return num_messages, len(words), num_media, len(links) 

def most_busy_user(df):
    x = df['users'].value_counts().head()   
    df = round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percentage'})
    return x,df

def create_wordCloud(selected_user,df):
    if selected_user != "Overall":
        df = df[df['users']==selected_user]
    temp = df[df['users'] != 'Group notification']
    temp = temp[temp['messages'] != '<Media omitted>']       

    wc = WordCloud(width=500,height=500,background_color='white',min_font_size=10)
    df_wc = wc.generate(temp['messages'].str.cat(sep=' '))
    return df_wc  

def most_commonWords(selected_user,df):
    if selected_user != "Overall":
        df = df[df['users']==selected_user]
    temp = df[df['users'] != 'Group notification']
    temp = temp[temp['messages'] != '<Media omitted>']    

    f = open("stop_hinglish.txt",'r')
    stop_words = f.read()

    words = []
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))            
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    
    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])  # Use is_emoji() to check each character
    
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns=['emoji', 'count'])
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    timeline = df.groupby(['year','month_num','month']).count()['messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + " - "+ str(timeline['year'][i]))
    timeline['time'] = time    
    return timeline 

def week_activity_map(selected_user,df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    return df['day_name'].value_counts()    
def month_activity_map(selected_user,df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    return df['month'].value_counts()
