import streamlit as st
import hashlib
import json
import time

# Define the Block class
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(
            str(self.index).encode('utf-8') +
            str(self.timestamp).encode('utf-8') +
            json.dumps(self.data).encode('utf-8') +
            str(self.previous_hash).encode('utf-8')
        )
        return sha.hexdigest()

# Define the Blockchain class
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), time.time(), data, previous_block.hash)
        self.chain.append(new_block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

# Initialize or load the blockchain in Streamlit
if 'ledger' not in st.session_state:
    st.session_state.ledger = Blockchain()

st.title("🧱 Simple Blockchain Explorer")

# Form to add a new block
with st.form("add_block_form"):
    transaction = st.text_input("Enter Transaction Detail", "Alice to Bob")
    amount = st.number_input("Enter Amount", min_value=0.0, value=10.0)
    submitted = st.form_submit_button("Add Block")
    if submitted:
        st.session_state.ledger.add_block({"transaction": transaction, "amount": amount})
        st.success("✅ Block added successfully!")

# Show the entire blockchain
st.subheader("📜 Blockchain Ledger")
for block in st.session_state.ledger.chain:
    st.json({
        "Index": block.index,
        "Timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block.timestamp)),
        "Data": block.data,
        "Previous Hash": block.previous_hash,
        "Hash": block.hash
    })

# Validate the blockchain
st.subheader("✅ Blockchain Validity Check")
if st.session_state.ledger.is_valid():
    st.success("Blockchain is valid! 🎉")
else:
    st.error("Blockchain is INVALID! ❌")
