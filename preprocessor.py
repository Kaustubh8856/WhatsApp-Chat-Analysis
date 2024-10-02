import pandas as pd
import re

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:AM|PM)\s-\s'
    data = data.replace('\u202f', ' ')

    messages = re.split(pattern, data)
    messages = [msg.strip() for msg in messages if msg.strip()]

    dates = re.findall(pattern,data)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    date_format = '%m/%d/%y, %I:%M %p'
    df['message_date'] = df['message_date'].str.extract(r'(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2} [APM]{2})')[0]
    df['message_date'] = pd.to_datetime(df['message_date'], format=date_format)
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s',message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Group notification')
            messages.append(entry[0])
    df['users'] = users
    df['messages'] = messages
    df.drop(columns=['user_message'],inplace=True)   

    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df 