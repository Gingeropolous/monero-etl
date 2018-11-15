from monero.transaction import IncomingPayment, OutgoingPayment
from destinations.fields import Fields

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
                    #last destination contains the transaction fee
                    self.debit = self.debit - payment.transaction.fee
                else:
                    #not last destination, then no fees
                    self.transaction_fee = '0'
            else:
                self.address = 'No Destination Address in Wallet Cache'
            self.credit = None
            self.timestamp = payment.timestamp
            self.transaction_id = payment.transaction.hash
            self.note = payment.note
    def calcBalance(self, existingBalance):
        if self.debit:
            self.balance = existingBalance + self.debit
        else:
            if self.credit:
                self.balance = existingBalance + self.credit

        return self.balance


