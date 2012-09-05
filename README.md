# Bank API

A python lib meant to define a simple API for communicating with a financial institution, and implementations for various banks.

The API is focused on basics: List accounts, get transactions. This could possibly be expanded in the future, but in the spirit of KISS,
the initial API design focuses on solving those two tasks as intuitively as possible.

There is currently only one institution implemented, Swedish Länsförsäkringar, because that is the bank I use, and as such it is the one I 
am interested in scripting against.

## Are these official APIs?

Absolutely not. The implementations provided here are based on talking to publicly available services, but they are not 
condoned by the institutions they talk to. 

These APIs may break at any time, without notice and might remain permanently unusable. Please use the libraries accordingly. 

## Installation

   python setup.py install

## Usage

For detailed usage, please just read the source, it's python for christ sake.

    from bank.impl.lfab import LFABSession
    
    session = LFABSession(u'8312120000', u'0000') # SSN and PIN
    
    # Begin session
    session.begin()
    
    for account in session.get_accounts():
        # Each account is a subclass of bank.domain.Account
        for transaction in session.get_transactions(account):
            # Each transaction is a subclass of bank.domain.Transaction
            print transaction
    
    # Disconnect
    session.end()

## RAWR! I'm a bank, and I'm really upset about this!

Well, you should be, there is a real danger in this. It isn't what you think though, it's not making it possible for bad people to access your services that is dangerous. 
That is not dangerous, because you can never stop people from writing code that accesses your services. 
If it can be accessed by a human through a browser, it can be accessed by a program through a browser.

The danger is good people, writing good services, and *you* forcing them to use these APIs.  
*That* is bad, because that means your customers learn to hand out their login credentials to third party services. 

*Then* bad people will be dangerous, because now your users have been trained to think handing out credentials to third parties is fine. 
That makes phishing a much more significant threat, not to mention security holes in third party services that end up storing these credentials.

We can avoid this. 

Please, design a publicly documented API that uses *your* service to provide authentication, use something like OAuth, it's built for that.
Third parties can build services that enrich your customer experience, and your customers learn to never give out credentials to anyone but you. 

Third party solutions are happening, whether you want to or not. You can choose to fight it, or you can choose to embrace it.
For the sake of your customers, embrace it. 
Be the bank that people switch to because third party services tell them "this feature is only available if you are a customer at bank X, because their incredible API is the only one that enables this feature".

## Backwards compatibility

I just built this, so the design might be way off. Therefore, expect APIs to break entirely in the future until we feel we've stabilized
on something good.
    
## License

Everything in here is MIT licensed, unless otherwise stated 
http://opensource.org/licenses/mit-license.html