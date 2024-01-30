import json

accounts = [{ 'account_id': 12345, 'balance':1200 }, { 'account_id': 23456, 'balance':1700 }, {'account_id': 45678, 'balance':2400 }]

def get_account(id):
    return next((a for a in accounts if a['account_id'] == id), None)

account = get_account(12345)
account.update({"balance":(1700+account["balance"])})
print(account)