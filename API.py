from flask import Flask, jsonify, request
import json

app = Flask(__name__)
accounts = []

# Reset API
@app.route('/reset', methods=['POST'])
def reset():
    accounts = []
    return "OK", 200

# Find Account by ID
def get_account(id):
    return next((a for a in accounts if a['account_id'] == id), None)

# Return Account
@app.route('/accounts', methods=['GET'])
def get_accounts():
    return jsonify(accounts), 200

# Get Account balance
@app.route('/balance', methods=['GET'])
def get_balance():
    if request.method == 'GET':
        id = int(request.args.get("account_id"))
        account = get_account(id)
        if account is None:
            return "0", 404
        return str(account["balance"]), 200

@app.route('/event', methods=['POST'])
def get_event():
    reset()
    requestData = json.loads(request.data)
    eventType = requestData["type"]

    # Deposit existing and non-existing account
    if eventType.lower() == 'deposit':
        id = int(requestData["destination"])
        amount = int(requestData["amount"])
        account = get_account(id)
        if account is None:
            accounts.append({'account_id': id, 'balance': amount})
            return '{"destination": {"id":"'+str(id)+'", "balance":'+str(amount)+'}}', 201


        newBalance = (amount + account["balance"])
        account.update({"balance": newBalance})
        return '{"destination": {"id":"'+str(id)+'", "balance":'+str(newBalance)+'}}', 201

    # Withdraw from existing and non-existing account
    elif eventType.lower() == 'withdraw':
        id = int(requestData["origin"])
        account = get_account(id)
        if account is None:
            return "0", 404

        amount = int(requestData["amount"])
        newBalance = (account["balance"] - amount)
        account.update({"balance": newBalance})
        return '{"origin": {"id":"'+str(id)+'", "balance":'+str(newBalance)+'}}', 201


    # Transfer from existing and non-existing account
    elif eventType.lower() == 'transfer':
        origin = int(requestData["origin"])
        originAccount = get_account(origin)
        if originAccount is None:
            return "0", 404

        amount = int(requestData["amount"])
        newBalance = (originAccount["balance"] - amount)
        originAccount.update({"balance": newBalance})

        destination = int(requestData["destination"])
        destinAccount = get_account(destination)

        if destinAccount is None:
            accounts.append({'account_id': destinAccount, 'balance': amount})
            return '{"origin": {"id":"'+str(origin)+'", "balance":'+str(newBalance)+'}, "destination": {"id":"'+str(destination)+'", "balance":'+str(amount)+'}}', 201

        originAccount.update({"balance": amount})
        return '{"origin": {"id":"'+str(origin)+'", "balance":'+str(amount)+'}, "destination": {"id":"'+str(destinAccount)+'", "balance":'+str(newBalance)+'}}', 201
    return "0"



# Get Account ID
@app.route('/accounts/<int:id>', methods=['GET'])
def get_account_by_id(id: int):
    account = get_account(id)
    if account is None:
        return jsonify({ 'error': 'Account does not exist'}), 404
    return jsonify(account)


