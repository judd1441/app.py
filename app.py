import streamlit as st

# Configure the mobile page layout
st.set_page_config(page_title="Golf Skins", page_icon="⛳", layout="centered")

st.title("⛳ FCW Skins 🂡")
st.write("Determine who owes who money instantly on the 18th green.")

# 1. Inputs
skin_value = st.number_input("Skin Value (Paid Per Player): $", min_value=0.01, value=1.00, step=1.00)

st.subheader("Players & Skins Won")
st.write("Enter one player per line as `Name: Skins` (e.g., Alice: 3)")

# Default text for easy testing
default_text = "Will: 0\nSteve: 0\nChris: 0\nJudd: 0\nBryon: 0\nJohn: 0\nSean: 0\nKim: 0"
raw_text = st.text_area("Player List", value=default_text, height=180, label_visibility="collapsed")

if st.button("Calculate Payouts", type="primary"):
    # Parse input data
    players = {}
    valid = True
    
    for line in raw_text.strip().split("\n"):
        if not line.strip():
            continue
        if ":" not in line:
            st.error(f"⚠️ Invalid format on line: '{line}'. Use 'Name: Skins'")
            valid = False
            break
        
        name, skins = line.split(":")
        try:
            players[name.strip()] = int(skins.strip())
        except ValueError:
            st.error(f"⚠️ Entry for '{name.strip()}' must be a whole number.")
            valid = False
            break

    if valid and players:
        num_players = len(players)
        total_skins = sum(players.values())
        
        # Display Summaries
        st.markdown("---")
        st.subheader("📊 Round Summary")
        col1, col2 = st.columns(2)
        col1.metric("Total Players", num_players)
        col2.metric("Total Skins Won", total_skins)
        
        skin_payout_value = (num_players - 1) * skin_value
        st.info(f"Total value of **1 skin** to the winner: **${skin_payout_value:,.2f}**")

        # Calculate Balances
        balances = {}
        for player, skins in players.items():
            net_balance = (skins * num_players - total_skins) * skin_value
            balances[player] = round(net_balance, 2)

        # Optimize Payments
        st.subheader("💸 Who Pays Who")
        debtors = [[name, bal] for name, bal in balances.items() if bal < 0]
        creditors = [[name, bal] for name, bal in balances.items() if bal > 0]

        transactions = []
        while debtors and creditors:
            debtors.sort(key=lambda x: x[1])
            creditors.sort(key=lambda x: x[1], reverse=True)

            debtor_name, debtor_bal = debtors[0]
            creditor_name, creditor_bal = creditors[0]

            amount_to_pay = min(abs(debtor_bal), creditor_bal)
            amount_to_pay = round(amount_to_pay, 2)

            transactions.append(f"🟢 **{debtor_name}** pays **{creditor_name}**: `${amount_to_pay:,.2f}`")

            debtors[0][1] += amount_to_pay
            creditors[0][1] -= amount_to_pay

            if abs(debtors[0][1]) < 0.02:
                debtors.pop(0)
            if abs(creditors[0][1]) < 0.02:
                creditors.pop(0)

        if not transactions:
            st.write("Everyone broke even! No money changes hands.")
        else:
            for tx in transactions:
                st.markdown(tx)
