import json
import time
import random

# Load transactions from JSON file
with open('../data/transactions.json', 'r') as f:
    transactions = json.load(f)

# Ensure we have at least 20 records for comparison
while len(transactions) < 20:
    new_transaction = {
        "transaction_id": str(random.randint(1000000000, 9999999999)),
        "type": random.choice(["transfer", "payment", "deposit"]),
        "amount": str(random.randint(100, 10000)),
        "sender": "User" + str(random.randint(1, 100)),
        "receiver": "User" + str(random.randint(1, 100)),
        "timestamp": "2024-05-13T10:00:00",
        "new_balance": str(random.randint(1000, 50000)),
        "message": None,
        "financial_transaction_id": str(random.randint(1000000000, 9999999999)),
        "service_center": "+250788110381",
        "fee": "0"
    }
    transactions.append(new_transaction)

# Save the updated transactions back to the JSON file
with open('../data/transactions.json', 'w') as f:
    json.dump(transactions, f, indent=4)

# Linear Search Function
def linear_search(transactions, transaction_id):
    for transaction in transactions:
        if transaction['transaction_id'] == transaction_id:
            return transaction
    return None

# Dictionary Lookup Function
def create_transaction_dict(transactions):
    transaction_dict = {}
    for transaction in transactions:
        transaction_dict[transaction['transaction_id']] = transaction
    return transaction_dict

transaction_dict = create_transaction_dict(transactions)

# Measure Efficiency
def measure_efficiency(search_func, *args):
    start_time = time.time()
    result = search_func(*args)
    end_time = time.time()
    elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds
    return result, elapsed_time

# Test with a random transaction ID
test_transaction_id = transactions[0]['transaction_id']

# Measure Linear Search Efficiency
linear_result, linear_time = measure_efficiency(linear_search, transactions, test_transaction_id)

# Measure Dictionary Lookup Efficiency
dict_result, dict_time = measure_efficiency(transaction_dict.get, test_transaction_id)

# Print Results
print(f"Linear Search Result: {linear_result}")
print(f"Linear Search Time: {linear_time:.6f} milliseconds")

print(f"Dictionary Lookup Result: {dict_result}")
print(f"Dictionary Lookup Time: {dict_time:.6f} milliseconds")

# Compare Efficiency
print(f"\nComparison:")
print(f"Dictionary Lookup is {linear_time / dict_time:.2f} times faster than Linear Search for this test.")
