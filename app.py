import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt

st.sidebar.title("WhatsApp Chat Analyser")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.dataframe(df)
    
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


        if selected_user == "Overall":
            st.title("Most Busy Users: ")
            x,new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()
            
            col1, col2 = st.columns(2)      
            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation="vertical")
                st.pyplot(fig)   
            with col2:
                st.dataframe(new_df)         