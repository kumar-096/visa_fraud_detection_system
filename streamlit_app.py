import streamlit as st
import pickle

st.title("Credit Card Fraud Detection Web App")

st.image("image.png")


# ---- Load the trained ML model once ----
@st.cache_resource
def load_model():
    with open("credit_fraud.pkl", "rb") as f:
        model = pickle.load(f)
    return model

model = load_model()


# ---- Sidebar inputs ----
st.sidebar.header("Input Features of The Transaction")

sender_name = st.sidebar.text_input("Input Sender ID")
receiver_name = st.sidebar.text_input("Input Receiver ID")

step = st.sidebar.slider("Number of Hours it took the Transaction to complete:", min_value=0, max_value=100, value=0)

st.sidebar.markdown(
    """
    **Enter Type of Transfer Made:**
    - 0 → Cash In  
    - 1 → Cash Out  
    - 2 → Debit  
    - 3 → Payment  
    - 4 → Transfer
    """
)

types = st.sidebar.selectbox("Transaction type (0–4)", (0, 1, 2, 3, 4))

x = ""
if types == 0:
    x = "Cash In"
elif types == 1:
    x = "Cash Out"
elif types == 2:
    x = "Debit"
elif types == 3:
    x = "Payment"
elif types == 4:
    x = "Transfer"

amount = st.sidebar.number_input("Amount in $", min_value=0, max_value=110000, value=0)
oldbalanceorg = st.sidebar.number_input("Sender Balance Before Transaction was made", min_value=0, max_value=110000, value=0)
newbalanceorg = st.sidebar.number_input("Sender Balance After Transaction was made", min_value=0, max_value=110000, value=0)
oldbalancedest = st.sidebar.number_input("Recipient Balance Before Transaction was made", min_value=0, max_value=110000, value=0)
newbalancedest = st.sidebar.number_input("Recipient Balance After Transaction was made", min_value=0, max_value=110000, value=0)

# Simple flag feature used in the original project
isflaggedfraud = 1 if amount >= 200000 else 0


if st.button("Detection Result"):
    # Show the transaction summary
    st.write(
        f"""### These are the transaction details:

- Sender ID: **{sender_name or "N/A"}**
- Receiver ID: **{receiver_name or "N/A"}**
- 1. Number of Hours it took to complete: **{step}**
- 2. Type of Transaction: **{x}**
- 3. Amount Sent: **{amount}$**
- 4. Sender Balance Before Transaction: **{oldbalanceorg}$**
- 5. Sender Balance After Transaction: **{newbalanceorg}$**
- 6. Recipient Balance Before Transaction: **{oldbalancedest}$**
- 7. Recipient Balance After Transaction: **{newbalancedest}$**
- 8. System Flag Fraud Status (amount ≥ $200000): **{isflaggedfraud}**
"""
    )

    if sender_name == "" or receiver_name == "":
        st.error("Please input Sender ID and Receiver ID!")
    else:
        # ---- Build feature vector for the model ----
        features = [[
            step,
            types,
            amount,
            oldbalanceorg,
            newbalanceorg,
            oldbalancedest,
            newbalancedest,
            isflaggedfraud
        ]]

        try:
            pred = model.predict(features)[0]  # 0 = not fraud, 1 = fraud (in original project)

            if pred == 1:
                result_text = "FRAUDULENT"
                st.error(
                    f"⚠️ The '{x}' transaction that took place between {sender_name} and {receiver_name} is **{result_text}**."
                )
            else:
                result_text = "LEGITIMATE"
                st.success(
                    f"✅ The '{x}' transaction that took place between {sender_name} and {receiver_name} is **{result_text}**."
                )

        except Exception as e:
            st.error("Something went wrong while running the prediction.")
            st.exception(e)
