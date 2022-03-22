#!/usr/bin/python3
from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import transaction
from algosdk import account

#Connect to Algorand node maintained by PureStake
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "B3SU4KcVKi94Jap2VXkK83xx38bsv95K5UZm2lab"
#algod_token = 'IwMysN3FSZ8zGVaQnoUIJ9RXolbQ5nRY62JRqF2H'
headers = {
   "X-API-Key": algod_token,
}

#generate account using terminal
#private_key, public_address = account.generate_account()
#print("private_key: ", private_key)
#print("public_address: ", public_address)

#private_key:  JnU3uxlyHBK5Dut5KSzkkYu+FauQeG0U/iGLMmn4bt04XRixztR3qSmFsGpJL4BUeggwv35632TAUBmfXlJzMQ==
#public_address:  HBORRMOO2R32SKMFWBVESL4AKR5AQMF7PZ5N6ZGAKAMZ6XSSOMY2IRKSHU

acl = algod.AlgodClient(algod_token, algod_address, headers)
min_balance = 100000 #https://developer.algorand.org/docs/features/accounts/#minimum-balance

def send_tokens( receiver_pk, tx_amount ):
    params = acl.suggested_params()
    gen_hash = params.gh
    first_valid_round = params.first
    tx_fee = params.min_fee
    last_valid_round = params.last

    #Your code here
    private_key = "JnU3uxlyHBK5Dut5KSzkkYu+FauQeG0U/iGLMmn4bt04XRixztR3qSmFsGpJL4BUeggwv35632TAUBmfXlJzMQ=="
    public_address = "HBORRMOO2R32SKMFWBVESL4AKR5AQMF7PZ5N6ZGAKAMZ6XSSOMY2IRKSHU"

    tx = transaction.PaymentTxn(public_address, tx_fee, first_valid_round, last_valid_round, gen_hash, receiver_pk,
                                tx_amount)
    signed_tx = tx.sign(private_key)
    txid = tx.get_txid()
    acl.send_transaction(signed_tx)

    return public_address, txid

# Function from Algorand Inc.
def wait_for_confirmation(client, txid):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return txinfo

