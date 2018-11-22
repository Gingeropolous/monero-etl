from monero.transaction import IncomingPayment, OutgoingPayment
from targets.currencyconversion import CurrencyHDP
import datetime

class LineItem(object):
    """
    A class used to store both In/Out monero payments. Also contains calculated summary fields for the user.
    """
    payment_id = None
    account = None
    address = None
    transaction_fee = None
    debit = None
    credit = None
    balance = None
    timestamp = None
    transaction_id = None
    note = ''
    converter = None

    def __init__(self, payment):
        if type(payment) is IncomingPayment:
            self.payment_id = payment.payment_id
            self.address = payment.local_address
            self.transaction_fee = None #payment.transaction.fee the sender pays the transaction fee so you don't care what it is
            self.debit = None
            self.credit = payment.amount
            self.timestamp = payment.timestamp
            self.transaction_id = payment.transaction.hash
            self.note = payment.note

        if type(payment) is OutgoingPayment:
            #process outgoing payment

            # transfers with multiple destinations will be tied by the payment id
            self.payment_id = payment.payment_id

            # assign the debit amount, but the amount will be reassigned if the transfer has destinations
            self.debit = (payment.amount * -1) - payment.transaction.fee

            # assign the transaction fee,
            # but for transfers with destinations the transaction fee will be set to 0 except for the last destination
            self.transaction_fee = payment.transaction.fee

            if payment.destinations:
                # grab and remove the last destination within from the destination list
                destination = payment.destinations.pop()

                # destination tuple contains [0] address and [1] amount
                self.address = destination[0]

                self.debit = (destination[1] * -1)

                if not payment.destinations:
                    # last destination will contain the transaction fee
                    xmrAmount = self.debit - payment.transaction.fee
                    self.debit = xmrAmount
                else:
                    # not last destination, then no fees
                    self.transaction_fee = 0
            else:
                self.address = 'No Destination Address in Wallet Cache'
            self.credit = None
            self.timestamp = payment.timestamp
            self.transaction_id = payment.transaction.hash
            self.note = payment.note

    def calcBalance(self, existingBalance, currency, finalBalance):
        if finalBalance == True and currency != 'XMR':
            #we want the final balance to be representative of the current market price
            self.converter = CurrencyHDP(time=datetime.datetime.now(), targetCurrency=currency)
        else:
            if self.converter is None and currency != 'XMR':
                self.converter = CurrencyHDP(time=self.timestamp, targetCurrency=currency)

        #calculate the balance
        if self.debit:
            #print('debug:debit:'+self.transaction_id+' value: '+str(self.debit))
            xmrAmount = existingBalance + self.debit
            if currency != 'XMR':
                self.debit = self.converter.convert(amount=self.debit)
        else:
            if self.credit:
                #print('debug:credit:' + self.transaction_id+' value: '+ str(self.credit))
                xmrAmount = existingBalance + self.credit
                if currency != 'XMR':
                    self.credit = self.converter.convert(amount=self.credit)

        if currency == 'XMR':
            self.balance = xmrAmount
        else:
            self.balance = self.converter.convert(xmrAmount)

        #convert transaction fees to the target currency if applicable
        if currency != 'XMR' and self.transaction_fee is not None and self.transaction_fee > 0:
            self.transaction_fee = self.converter.convert(self.transaction_fee)

        #always return the value in XMR, because for each line item we want the balance at that specific point in time
        return xmrAmount

