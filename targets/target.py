from monero.wallet import Wallet
from targets.fields import Fields
from targets.lineitem import LineItem
import csv
import time

# print(jsonRPC.raw_request('get_attribute', 'wallet2.description')) #What's the key??? ATTRIBUTE_DESCRIPTION????
class target(object):
    min_height = 0
    mywallet = None
    currency = None

    def __init__(self, mywallet, min_height=0, currency='XMR'):
        self.mywallet = mywallet
        self.min_height = min_height
        self.currency = currency
        self.etl()

    def extract(self):
        return "extract functionality unavailable at this time"

    def load(self, stagedData):
        return "load functionality unavailable at this time"

    def transform(self, stagedData):
        return "transform functionality unavailable at this time"

    def etl(self):
        stagedData = self.extract()
        stagedData = self.transform(stagedData)
        self.load(stagedData)

class csvfile(target):
    def extract(self):
        lineitems = []
        incoming = self.mywallet.incoming(min_height=self.min_height)
        outgoing = self.mywallet.outgoing(min_height=self.min_height)
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

    def transform(self, lineitems):
        # sort list of incoming and outgoing payments(lineitem objects) by timestamp
        lineitems = sorted(lineitems, key=lambda lineitem: lineitem.timestamp)

        # set initial balance value
        balance = 0

        # calculate balance for each line item after debit or credit
        i = 0
        lines = len(lineitems)
        for lineitem in lineitems:
            i += 1
            finalBalance = True if lines == i else False
            balance = lineitem.calcBalance(balance, self.currency, finalBalance)

        # most recent tx should be on top with most recent balance
        lineitems = sorted(lineitems, key=lambda lineitem: lineitem.timestamp, reverse=True)

        return lineitems

    def load(self, lineitems):
        with open(time.strftime("%d-%m-%Y") + '_xmr.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)

            fieldnames = []
            for field in Fields.values:
                fieldnames.append(field)

            # write the field headers first
            writer.writerow(fieldnames)

            # load line item variables into row
            for lineitem in lineitems:
                row = []
                # using if statements to allow for fields to be rearranged
                # adding fields requires an additional if statement
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
                        row.append(str(lineitem.balance) + ' ' + self.currency)

                # write the line item into csv
                writer.writerow(row)

class SQL(target):
    def __init__(self, mywallet, min_height=0):
        target.__init__(self, mywallet, min_height=0)

class beanCounter(target):
    def __init__(self, mywallet, min_height=0):
        target.__init__(self, mywallet, min_height=0)




