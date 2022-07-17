# Rosie 

---Rosie is a robotic personal assistant built on top of Amazon Lex's platform which allows for easy bootstrapping of chatbots with conversational AI capabilities.  Using Amazon Lambda functions and their integration with Amazon Lex, we created a chatbot with several intents at its disposal. 

## Technologies

You must have access to AWS to use Amazon Lex for the chatbot.
Here is a link to the website where you can make a free account: https://aws.amazon.com/

Every dependency needed to run the bot is provided in each lambda function, but below are examples of required libraries that we included:

```from datetime import datetime```
```from dateutil.relativedelta import relativedelta```
```from botocore.vendored import requests```
```import json```

## Sample Utterances

### Crypto Utterance

* What is todays price

* What is the rate of return

* Where can I buy crypto

### Transaction Tracker Utterance

* What was the amount of my last purchase

* What were the top merchants where I spent money

### Expense Tracker Utterance

* What are my expenses balance

* What are my expenses

* When is my expenses bill due.

### Subscription Tracker Utterance

* When does my subscription end
 
* When does my subscription renew

* How much does my subscription cost


### Crypto Intent Example
![alt_text](https://github.com/Crena94/TeamRosie/blob/main/crypto_bot_test.png)

### Transcation Tracker Example
![alt text](https://github.com/Crena94/TeamRosie/blob/main/transaction_bot_test.png)

### Expense Tracker Example
![alt text](https://github.com/Crena94/TeamRosie/blob/63acc68cb2a55de5ad7c7e5d13b3798c7ad235a4/expense_tracker_bot_test.png)

### Subscription Intent Examples

![alt text](https://github.com/Crena94/TeamRosie/blob/main/Pic%20of%20subscription%20tracker%20.png)


## Contributors

--- David Ports - dave.ports.1@gmail.com

--- Darian Saunders - dariansaunders@ymail.com

--- Matt Crater - mathias1026@gmail.com

--- Ashleigh Davis - rashleighdavis@yahoo.com



## License

MIT
