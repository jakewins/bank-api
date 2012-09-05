''' FinancialSession implementation for Swedish Länsförsäkringar Bank.

Uses LFABs REST API, based on Björn Sållarps work, with updated client key. 

Copyleft 2012 Jacob Hansson <jakewins@gmail.com>

Released under the MIT license:

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of 
the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO 
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import hashlib
from datetime import datetime

from bank.domain import FinancialSession, Account, Transaction
from bank.io.http import HttpJsonClient

class LFABAccount(Account):
    
    @classmethod
    def from_map(cls, data):
        return cls(data['accountName'], data['accountNumber'], data['clearingNumber'], data['dispoibleAmount'], data['ledger'])
    
    def __init__(self, name, number, clearing_number, balance, ledger):
        super(LFABAccount, self).__init__(name, number, clearing_number)
        self.balance = balance
        self._ledger = ledger
        
        
class LFABTransaction(Transaction):

    @classmethod
    def from_map(cls, data):
        # Note timestamp is in milliseconds, and yes, their serialization actually contains spelling errors
        return cls(data['text'], data['ammount'], datetime.fromtimestamp(data['transactiondate'] / 1000)) 
        

class LFABSession(FinancialSession):
    
    def __init__(self, ssn, pin):
        self._ssn = str(ssn)
        self._pin = str(pin)
        self._client = HttpJsonClient("https://mobil.lansforsakringar.se/appoutlet")
        
        self._client.add_persistent_header("Accept", "application/json,text/plain")
        self._client.add_persistent_header("Accept-Charset", "utf-8")
        self._client.add_persistent_header("Accept-Encoding", "gzip,deflate")
        self._client.add_persistent_header('User-Agent', "lf-android-app")
    
    
    def begin(self):
        challenge = self._client.get('/security/client')
        session_token = self._client.post('/security/client', self._create_challenge_reply(challenge))
        
        # Set up session token header
        self._client.add_persistent_header('Ctoken', session_token['token'])
        self._client.add_persistent_header('DeviceId', '1a1805054248c4529340f4ee20bb1d1ec200a0b9') # TODO: Use a randomized ID instead? 
        
        # Log in
        login_response = self._client.post('/security/user', {"ssn":self._ssn,"pin":self._pin})
        
        # Utoken
        self._client.add_persistent_header('Utoken', login_response['ticket'])
    
        
    def get_accounts(self):
        for response in [self._client.post('/account/bytype', {"accountType":"CHECKING"}),
                         self._client.post('/account/bytype', {"accountType":"SAVING"})]:
            
            for account in response['accounts']:
                yield LFABAccount.from_map(account)
    
    
    def get_transactions(self, account):
        if not isinstance(account, LFABAccount):
            raise Exception("LFAB account required to list LFAB transactions")
            
        payload = {"requestedPage":0,"ledger":account._ledger,"accountNumber":account.number}
        current_response = None
        
        while current_response is None or current_response['hasMore'] is True:
            
            # Get a fresh page of transactions
            current_response = self._client.post("/account/transaction", payload)
            
            # Yield transactions
            for tx_json in current_response['transactions']:
                # Each tx looks like:
                #{ "ammount" : -248.0, "text" : "Transaction message", "transactiondate" : 1319580000000 }
                yield LFABTransaction.from_map(tx_json)
            
            # Next page
            payload['requestedPage'] += 1
    
        
    def end(self):
        self._client = None
    
    
    # Internals
        
    def _create_challenge_reply(self, challenge):
        # Add magic number
        number = challenge['number'] + 5616
        
        # Convert to lower-case hex, stripping off the first two chars that hex() adds ('0x')
        number = hex(number).lower()[2:]
        
        # Sha-hash
        number_hash = hashlib.sha1(number).hexdigest()
        
        # Return response in appropriate format
        return {
		  "originalChallenge" : challenge['number'],
		  "hash"              : number_hash,
		  "challengePair"     : challenge['numberPair']
		}

    