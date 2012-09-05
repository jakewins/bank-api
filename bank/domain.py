
class FinancialSession(object):
    ''' The main entry point of the API.
    '''
    def begin(self):
        pass
        
    def list_accounts(self):
        pass
    
    def list_transactions(self, account):
        pass
        
    def end(self):
        pass
    
class Account(object):
    ''' An account object.
    '''
    def __init__(self, name, number, clearing_number):
        self.name = name
        self.number = number
        self.clearing_number = clearing_number
    
class Transaction(object):
    ''' A transaction
    '''
    
    def __init__(self, message, amount, timestamp):
        self.message = message
        self.amount = amount
        self.timestamp = timestamp