import pandas as pd
import streamlit as st
from datetime import date
from pandasql import sqldf

st.set_page_config(layout='wide')

# A quick lambda function, so that you don’t have to pass in global variables every time an object is used
pysqldf = lambda q: sqldf(q, globals())
df = pd.read_excel('trz_timing.xlsx')
q = """
        SELECT
            date
            , vakth
            , start
            , end
            , DATETIME(CURRENT_TIMESTAMP) now
            , DATETIME(CURRENT_TIMESTAMP, '+5.5 hours') offset
            --, (JULIANDAY(start) - JULIANDAY(DATETIME(CURRENT_TIMESTAMP, '+5.5 hours'))) * 1440  mins_since_start
            --, ((JULIANDAY(end) - JULIANDAY(DATETIME(CURRENT_TIMESTAMP, '+5.5 hours'))) * 1440) mins_to_end
            , time(((JULIANDAY(end) - JULIANDAY(DATETIME(CURRENT_TIMESTAMP, '+5.5 hours'))) * 1440) , 'unixepoch') ends_in
            , (JULIANDAY(end) - JULIANDAY(start)) * 1440 dur
            , ((JULIANDAY(end) - JULIANDAY(DATETIME(CURRENT_TIMESTAMP, '+5.5 hours'))) * 1440) mins_to_end
            , round(1-(((JULIANDAY(end) - JULIANDAY(DATETIME(CURRENT_TIMESTAMP, '+5.5 hours'))) * 1440) / ((JULIANDAY(end) - JULIANDAY(start)) * 1440)),2)*100 completed_percent      

        FROM 
            df  

        WHERE
            date=date()
            and ((JULIANDAY(start) - JULIANDAY(DATETIME(CURRENT_TIMESTAMP, '+5.5 hours'))) * 1440) < 0
            and ((JULIANDAY(end) - JULIANDAY(DATETIME(CURRENT_TIMESTAMP, '+5.5 hours'))) * 1440) > 0
    """
names = pysqldf(q)
# names

# Converting Start and End columns in the data frame from Text to Datetime type
df['start'] = pd.to_datetime(df['start'], errors='coerce')
df['end'] = pd.to_datetime(df['end'], errors='coerce')

dataFrameSerialization = "legacy"

d = date.today().strftime("%B %d, %Y")
vakth = names.vakth.to_string(index=False, header=False)
start = names.start.to_string(index=False, header=False)[-5:]
end = names.end.to_string(index=False, header=False)[-5:]
ends_in = names.ends_in.to_string(index=False, header=False)[3:]
comp = names.completed_percent.to_string(index=False, header=False)[:2]
curr_time = names.offset.to_string(index=False, header=False)[10:16]

# df.info()

st.markdown(
    """
    <style>
        div[data-testid="column"]:nth-of-type(1)
        {
            border: # 1px solid red;
            text-align: ;
        } 

        div[data-testid="column"]:nth-of-type(2)
        {
            border:;
            text-align: center;
            .bigfont1 {font-size:60px !important;};
            .bigfont2 {font-size:40px !important;};
            .bigfont3 {font-size:30px !important;};
            .smallfont1 {font-size:14px !important;};
            .smallfont2 {font-size:12px !important;};
            .smallfont3 {font-size:9px !important;};
            
        } 
        
                div[data-testid="column"]:nth-of-type(3)
        {
            border:;
            text-align: end;
        } 
    </style>
    """, unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    """
    
    """
    st.write("")

with col2:
    """
    """
    st.markdown('<p class="smallfont1">'+ d+' </p>', unsafe_allow_html=True)
    #st.write('<p style="font-size:9px; color:red;">Here is some red text'+'test'+'</p>', unsafe_allow_html=True)
    st.markdown('<p class="smallfont1">'+ curr_time+' </p>', unsafe_allow_html=True)
    # Place holder for <Hijri Date>
    st.divider()
    st.markdown('<p class="bigfont1">'+ vakth+' </p>', unsafe_allow_html=True)
    st.write(start, " - ", end)
    st.divider()
    st.markdown('<p class="smallfont1">'+ "Ends in: "+' </p>', unsafe_allow_html=True)
    st.markdown('<p class="bigfont2">'+ ends_in+' </p>', unsafe_allow_html=True)
    st.markdown('<p class="smallfont2">'+ "[hh:mm]"+' </p>', unsafe_allow_html=True)
    st.markdown('<p class="bigfont3">'+ comp + "%"+' </p>', unsafe_allow_html=True)
    st.markdown('<p class="smallfont2">'+ "Completed"+' </p>', unsafe_allow_html=True)
    st.divider()
    st.markdown('<p class="smallfont3">'+ "Trichy, India"+' </p>', unsafe_allow_html=True)

with col3:
    """

    """
    #st.write("")
    #st.write(curr_time)
    #st.button("🐈")
