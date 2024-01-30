from flask import Flask, jsonify, request

app = Flask(__name__)

accounts = [{'account_id': 12345, 'balance': 1200}, {'account_id': 23456, 'balance': 1700}, {'account_id': 45678, 'balance': 2400}, {'account_id': 100, 'balance': 20}]

# Reset API
@app.route('/reset', methods=['POST'])
def reset():
    return "OK", 200

# Find Account by ID
def get_account(id):
    return next((a for a in accounts if a['account_id'] == id), None)

# Return Account
@app.route('/accounts', methods=['GET'])
def get_accounts():
    return jsonify(accounts), 200

# Get Account balance
@app.route('/balance/<int:id>', methods=['GET'])
def get_balance(id):
    account = get_account(id)
    if account is None:
        return "0", 404
    return str(account["balance"]), 200

# Create or deposit
@app.route('/deposit/<int:id>/<int:balance>', methods=['POST'])
def deposit(id, balance):
    account = get_account(id)
    if account is None:
        accounts.append({id:balance})
        return jsonify({"destination": {"id": id, "balance": balance}}), 201

    newBalance = (balance+account["balance"])
    account.update({"balance": newBalance})
    return jsonify({"destination": {"id": id, "balance": newBalance}}), 201


# Withdraw from existing and non-existing account
@app.route('/withdraw/<int:id>/<int:amount>', methods=['POST'])
def withdraw(id, amount):
    account = get_account(id)
    if account is None:
        return "0", 404

    newBalance = (account["balance"] - amount)
    account.update({"balance": newBalance})
    return jsonify({"destination": {"id": id, "balance": newBalance}}), 201


# Transfer from existing and non-existing account
@app.route('/transfer/<int:id>/<int:amount>/<int:destination>', methods=['POST'])
def transfer(id, amount, destination):
    account = get_account(id)
    if account is None:
        return "0", 404

    newBalance = (account["balance"] - amount)
    account.update({"balance": newBalance})

    destinAccount = get_account(destination)
    if destinAccount is None:
        accounts.append({id: amount})
        return jsonify({"destination": {"id": destination, "balance": amount}}), 201

    account.update({"balance": amount})
    return jsonify({"destination": {"id": destination, "balance": amount}}), 201


# Get Account ID
@app.route('/accounts/<int:id>', methods=['GET'])
def get_account_by_id(id: int):
    account = get_account(id)
    if account is None:
        return jsonify({ 'error': 'Account does not exist'}), 404
    return jsonify(account)


