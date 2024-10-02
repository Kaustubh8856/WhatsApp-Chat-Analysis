import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt

st.sidebar.title("WhatsApp Chat Analyser")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    # st.dataframe(df)
    
    user_list = df['users'].unique().tolist()
    user_list.remove('Group notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis w.r.t. ",user_list)

    if st.sidebar.button("Show Analysis: "):
        num_messages,words,num_media,num_links = helper.fetch_stats(selected_user,df)

        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header("Messages: ")
            st.title(num_messages)
        with col2:
            st.header("Words: ")
            st.title(words)
        with col3:
            st.header("Media: ")
            st.title(num_media)
        with col4:
            st.header("Links: ")
            st.title(num_links)     

        st.header("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['messages'],color='green' )
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        if selected_user == "Overall":
            st.header("Most Busy Users: ")
            x,new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()
            
            col1, col2 = st.columns(2)      
            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation="vertical")
                st.pyplot(fig)   
            with col2:
                st.dataframe(new_df)   


        st.header("WordCloud: ")
        df_wc = helper.create_wordCloud(selected_user,df) 
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)        

        st.header("20 Most Common Words: ")
        most_common_df = helper.most_commonWords(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        # st.dataframe(most_common_df)

        st.header("Emoji Analysis: ")
        emoji_df = helper.emoji_helper(selected_user, df)
        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df['count'].head(), labels=emoji_df['emoji'].head(), autopct='%0.2f')  # Access columns by their names
            st.pyplot(fig)