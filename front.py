import streamlit as st
import requests
 
BASE_URL = "https://bank-26.vercel.app/"
 
st.set_page_config(page_title="ATM System", layout="wide")
st.title(" ATM Transaction System")
 
tabs = st.tabs(["Accounts", "Transactions"])
 
 
#  Transfer dialog
@st.dialog("Transfer Amount")
def transfer_dialog():
    src = st.text_input("Source Account Number")
    dest = st.text_input("Destination Account Number")
    amount = st.number_input("Amount", min_value=1)
 
    if st.button("Transfer", type="primary", use_container_width=True):
        res = requests.post(
            BASE_URL + "/transaction",
            params={
                "source": src,
                "dest": dest,
                "amount": amount
            }
        )
 
        if res.status_code == 200:
            st.success("Transfer successful ")
            st.rerun()
        else:
            st.error(res.json()["detail"])
 
 
#  Transfer button
if st.button("Transfer Amount", type="primary"):
    transfer_dialog()
 
 
#  Accounts tab
with tabs[0]:
    res = requests.get(BASE_URL + "/accounts")
    st.subheader("All Accounts")
    st.dataframe(res.json(), use_container_width=True)
 
 
#  Transactions tab
with tabs[1]:
    res = requests.get(BASE_URL + "/transactions")
    st.subheader("Transaction History")
    st.dataframe(res.json(), use_container_width=True)
 