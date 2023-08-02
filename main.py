import pandas as pd
import streamlit as st
from datetime import date
from pandasql import sqldf
from datetime import timedelta
# A quick lambda function, so that you don’t have to pass in global variables every time an object is used
pysqldf = lambda q: sqldf(q, globals())
df = pd.read_excel('trz_timing.xlsx')
q = """
        SELECT
            date
            , vakth
            , start
            , end
            , DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME') now
            --, (JULIANDAY(start) - JULIANDAY(DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME'))) * 1440  mins_since_start
            --, ((JULIANDAY(end) - JULIANDAY(DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME'))) * 1440) mins_to_end
            , time(((JULIANDAY(end) - JULIANDAY(DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME'))) * 1440) , 'unixepoch') ends_in
            , (JULIANDAY(end) - JULIANDAY(start)) * 1440 dur
            , ((JULIANDAY(end) - JULIANDAY(DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME'))) * 1440) mins_to_end
            , round(1-(((JULIANDAY(end) - JULIANDAY(DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME'))) * 1440) / ((JULIANDAY(end) - JULIANDAY(start)) * 1440)),2)*100 completed_percent
        FROM 
            df  
        WHERE
            date=date()
            and ((JULIANDAY(start) - JULIANDAY(DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME'))) * 1440) < 0
            and ((JULIANDAY(end) - JULIANDAY(DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME'))) * 1440) > 0
    """
names = pysqldf(q)
#names

#Converting Start and End columns in the data frame from Text to Datetime type
df['start'] = pd.to_datetime(df['start'], errors='coerce')
df['end'] = pd.to_datetime(df['end'], errors='coerce')

dataFrameSerialization = "legacy"

d = date.today().strftime("%B %d, %Y")
vakth = names.vakth.to_string(index=False, header=False)
start = names.start.to_string(index=False, header=False)[-5:]
end = names.end.to_string(index=False, header=False)[-5:]
#ends_in = (pd.to_datetime(names.end) - pd.Timestamp.now()).to_string()[11:16]
ends_in = names.ends_in.to_string(index=False, header=False)[3:]
#vakth_dur = pd.to_datetime(names.end) - pd.to_datetime(names.start)
comp = names.completed_percent.to_string(index=False, header=False)[:]

#df.info()

st.divider()
st.write(d, "  |  Tiruchirapalli, India")
# Place holder for <Hijri Date>
st.divider()
st.header(vakth)
st.write(start," - ", end)
st.divider()
st.write("Ends in")
st.subheader(ends_in)
st.write("[hh : mm]")
st.write(comp.strip(),"% ")
st.write("Completed")
st.divider()
