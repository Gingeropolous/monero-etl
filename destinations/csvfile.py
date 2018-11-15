from monero.wallet import Wallet
from destinations.fields import Fields
from destinations.lineitem import LineItem
import csv
import time

def extract(mywallet):
    lineitems = []
    incoming = mywallet.incoming()
    outgoing = mywallet.outgoing()
    for payment in incoming:
        lineitem = LineItem(payment)
        lineitems.append(lineitem)
    multiDestPayment = None
    for payment in outgoing:
        while True:
            lineitem = LineItem(payment)
            lineitems.append(lineitem)
            if not payment.destinations:  # don't add any more line items if there are no more destinations
                break
    return lineitems

def transform(lineitems):
    #sort list of incoming and outgoing payments(lineitem objects) by timestamp
    lineitems = sorted(lineitems, key=lambda lineitem:lineitem.timestamp)

    #set initial balance value
    balance = 0

    # calculate balance for each line item after debit or credit
    for lineitem in lineitems:
        balance = lineitem.calcBalance(balance)

    #most recent tx should be on top with most recent balance
    lineitems = sorted(lineitems, key=lambda lineitem: lineitem.timestamp, reverse=True)

    return lineitems

def load(lineitems):
    with open(time.strftime("%d-%m-%Y")+'_xmr.csv','w') as csvfile:
        writer = csv.writer(csvfile)

        fieldnames = []
        for field in Fields.values:
            fieldnames.append(field)

        # write the field headers first
        writer.writerow(fieldnames)

        #load line item variables into row
        for lineitem in lineitems:
            row = []
            #using if statements to allow for fields to be rearranged
            #adding fields requires an additional if statement
            for field in fieldnames:
                if field == "Timestamp":
                    row.append(lineitem.timestamp)
                if field == "Transaction Id":
                    row.append(lineitem.transaction_id)
                if field == "Payment ID":
                    row.append(lineitem.payment_id)
                if field == "Note":
                    row.append(lineitem.note)
                if field == "Receive/Send Address":
                    row.append(lineitem.address)
                if field == "Debit":
                    row.append(lineitem.debit)
                if field == "Credit":
                    row.append(lineitem.credit)
                if field == "Network Fee":
                    row.append(lineitem.transaction_fee)
                if field == "Balance":
                    row.append(lineitem.balance)

            #write the line item into csv
            writer.writerow(row)

def etl(mywallet):
    lineitems = extract(mywallet)
    lineitems = transform(lineitems)
    load(lineitems)
    #print(jsonRPC.raw_request('get_attribute', 'wallet2.description')) #What's the key??? ATTRIBUTE_DESCRIPTION????

