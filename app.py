import streamlit as st
import pandas as pd
from datetime import datetime

st.title("AMS Lab Management App")

st.write("In this application, we would like to provide real time status of our labs.")

st.subheader("Status of our labs")
current_date = datetime.now()
st.write(f"Current date: {current_date.strftime('%d-%B-%Y')}")

# latest status
df = pd.read_excel('current_stat.xlsx', na_filter=False)

# Function to apply custom styling
def highlight_text(cell):
    return 'color: green' if 'Available' in cell else 'color: red'

# Apply custom styling to the 'Status' column
styled_df = df.style.applymap(lambda cell: highlight_text(cell), subset=['Status'])
styled_df = styled_df.hide_index()


# Display the table without the index column using HTML
st.markdown(styled_df.to_html(), unsafe_allow_html=True)
st.write('\n')
# Display a web link
st.markdown('[Click here](https://docs.google.com/spreadsheets/d/1_IVksfmKi8lxfHcUD-qgFm-vPgqTXohnld9FkTa-4HE/edit?usp=sharing) to see our lab schedule.')
st.markdown('[Click here](https://docs.google.com/spreadsheets/d/1YY7TXEHvCvMn-DkrQDjyUXLIO1fnPV7xlOb-NvwHtwo/edit?usp=sharing) to see detail information of each lab.')
st.write("If you have any questions, feel free to contact our secretary, Ms. Chheang Sreypich via 096 76 11 471 .")


# Convert dataframe to dictionnary
data = df.to_dict(orient='list')

st.sidebar.markdown("<h2 style='color: blue;'>To use lab, fill in the infomaton below:</h2>", unsafe_allow_html=True)
room = st.sidebar.selectbox("Select a room: ", df['Labs'][df['Status']=='Available'])
name = st.sidebar.text_input('Enter your name:')
s_id = st.sidebar.text_input('Enter your student id:')
p_no = st.sidebar.text_input("Enter your phone number:")
t_in = st.sidebar.text_input("Enter time in:")
t_out = st.sidebar.text_input("Enter time out:")

# Custom CSS to style the button area
button_area_css = """
    <style>
    div.stButton > button {
        background-color: blue;
        color: white;
    }
    </style>
    """

# Apply the custom CSS
st.markdown(button_area_css, unsafe_allow_html=True)

bu = st.sidebar.button("Enter")

if bu:
    r_index = data['Labs'].index(room)
    data['Status'][r_index] = "Unavailable"
    data['Key at/with'][r_index] = name
    data['Stduent ID'][r_index] = s_id
    data['Phone number'][r_index] = p_no
    data['Time In'][r_index] = t_in
    data['Time Out'][r_index] = t_out

    # Update DataFrame
    df_updated = pd.DataFrame(data)
    # Save DataFrame to Excel without index
    df_updated.to_excel('current_stat.xlsx', index=False)

    # this section is for creating log file
    log_dic = {'Date': [current_date], 'Lab':[room], 'Name': [name], 'Student ID': [s_id], 'Phone Number': [p_no], 'Time In': [t_in], 'Time Out': [t_out]}
    log_df = pd.DataFrame(log_dic) 
    existing_file_path = 'log.xlsx'
    # Check if the file already exists
    try:
         # Read the existing Excel file
        existing_df = pd.read_excel(existing_file_path)
        # Append new data to the existing DataFrame
        updated_df = existing_df.append(log_df, ignore_index=True)
        # Write the updated DataFrame back to the Excel file
        updated_df.to_excel(existing_file_path, index=False, engine='openpyxl')
    except FileNotFoundError:
        # If the file doesn't exist, simply write the DataFrame to a new Excel file
        log_df.to_excel(existing_file_path, index=False, engine='openpyxl')

    # Refresh page
    st.experimental_rerun()

        
st.sidebar.markdown("<h2 style='color: red;'>This section is for AMS admins only!</h2>", unsafe_allow_html=True)

st.sidebar.write("Select lab room that you want to reset")
lab = st.sidebar.selectbox("Select a lab: ", df['Labs'][df['Status']=='Unavailable'])

# User credentials
valid_users = {'Sreypich': 'Sreypich29', 'Sopheak': '@1234', 'AMS': '@AMS'}

username = st.sidebar.text_input("Username:")
password = st.sidebar.text_input("Password:", type="password")

r_bu = st.sidebar.button("Reset")

if ((username not in valid_users) or (password != valid_users[username])) and r_bu:
    st.sidebar.error("Login Failed!") 
elif (username in valid_users and password == valid_users[username]) and r_bu:
    r_index = data['Labs'].index(lab)
    data['Status'][r_index] = "Available"
    data['Key at/with'][r_index] = "AMS-103F"
    data['Stduent ID'][r_index] = ""
    data['Phone number'][r_index] = ""
    data['Time In'][r_index] = ""
    data['Time Out'][r_index] = ""

    # Update DataFrame
    df_updated = pd.DataFrame(data)
    # Save DataFrame to Excel without index
    df_updated.to_excel('current_stat.xlsx', index=False)
    # Refresh page
    st.experimental_rerun()


l_bu = st.sidebar.button("See logs")

if ((username not in valid_users) or (password != valid_users[username])) and l_bu:
    st.sidebar.error("Login Failed!") 
elif (username in valid_users and password == valid_users[username]) and l_bu:
    st.title("AMS Lab Logs")
    log_df = pd.read_excel('log.xlsx', na_filter=False)

    # Sort DataFrame by the 'date_column' in descending order (latest to oldest)
    df_sorted = log_df.sort_values(by='Date', ascending=False)

    st.markdown(df_sorted.to_html(index=False), unsafe_allow_html=True)

    




