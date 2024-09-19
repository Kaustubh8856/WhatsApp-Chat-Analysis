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


    return num_messages, len(words), num_media 

   