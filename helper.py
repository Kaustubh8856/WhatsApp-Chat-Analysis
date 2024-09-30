from urlextract import URLExtract
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