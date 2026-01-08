import streamlit as st
import requests

# 🔗 Vercel Backend URL
BASE_URL = "https://bank-26.vercel.app/api"

st.set_page_config(page_title="ATM System", layout="wide")
st.title("🏦 ATM Transaction System")

# ---------------- Tabs ----------------
tabs = st.tabs(["💳 Accounts", "📜 Transactions", "💸 Transfer"])


# ---------------- Accounts Tab ----------------
with tabs[0]:
    st.subheader("All Accounts")

    try:
        res = requests.get(f"{BASE_URL}/accounts", timeout=10)

        if res.status_code == 200:
            data = res.json()
            if data:
                st.dataframe(data, use_container_width=True)
            else:
                st.info("No accounts found")
        else:
            st.error(f"Backend error: {res.status_code}")
            st.code(res.text)

    except Exception as e:
        st.error("Backend se connect nahi ho pa raha")
        st.code(str(e))


# ---------------- Transactions Tab ----------------
with tabs[1]:
    st.subheader("Transaction History")

    try:
        res = requests.get(f"{BASE_URL}/transactions", timeout=10)

        if res.status_code == 200:
            data = res.json()
            if data:
                st.dataframe(data, use_container_width=True)
            else:
                st.info("No transactions found")
        else:
            st.error(f"Backend error: {res.status_code}")
            st.code(res.text)

    except Exception as e:
        st.error("Backend se connect nahi ho pa raha")
        st.code(str(e))


# ---------------- Transfer Tab ----------------
with tabs[2]:
    st.subheader("Transfer Money")

    col1, col2 = st.columns(2)

    with col1:
        source = st.text_input("Source Account Number")

    with col2:
        dest = st.text_input("Destination Account Number")

    amount = st.number_input("Amount", min_value=1, step=1)

    if st.button("💸 Transfer", type="primary", use_container_width=True):

        if not source or not dest:
            st.warning("Account numbers fill karo")
        else:
            try:
                res = requests.post(
                    f"{BASE_URL}/transaction",
                    params={
                        "source": source,
                        "dest": dest,
                        "amount": amount
                    },
                    timeout=10
                )

                if res.status_code == 200:
                    st.success("✅ Transfer successful")
                else:
                    try:
                        st.error(res.json().get("detail", "Transfer failed"))
                    except:
                        st.error("Transfer failed")
                        st.code(res.text)

            except Exception as e:
                st.error("Server reachable nahi hai")
                st.code(str(e))
