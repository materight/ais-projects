# Dialogue 1: enable user to apply for a new credit card
- Q: Hello, Bank of Trento, please state your request.
- A: I'd like to open a new credit card
- Q: Do you want to open a new credi card?
- A: Yes
- Q: Ok, please state your name
- A: Matteo Destro
- Q; Your name is Matteo Destro, correct?
- A: Yes
- Q: Ok, now please spell you codice fiscale letter by letter
- A: A B C D E F 1 2 3 4 5
- Q: Your CF is A B C D E F 1 2 3 4 5, correct?
- A: Yes
- Q: Ok thank you, I'll need some more information to determine your current credit score. This informations will be checked after this procedure has been completed. Do you have any debt history?
- A: No
- Q: Are you current employed?
- A: Yes
- Q: Please state your current employer and annual salary
- A: Amazon, 50k dollars
- Q: Thank you, you're currently employed by Amazon with a 50k salary, correct?
- A: Yes
- Q: Thank you for the information. You're eligible to open a new credit card at our bank. Please confirm that you want to open a new credit card by saying "I confirm I want to open a new credit card".
- A: I confirm I want to open a new credit card
- Q: Thank you, you're new account has been opened. Please spell you email address so that we can send you the final documentation
- A: matteo@email.com
- Q: Thank you, we have sent you the documentation with the details of your new account.


# Dialogue 2 [user initiative]: increase credit card limit
- Q: Hello Bank of Trento, how can I help you?
- A: Hello, I would like to change my credit card limit, my credit card number is 12345
- Q: Ok, what limit would you like to set?
- A: I'm not sure, what I even now is definitely not enough... What is the maximum limit I can have?
- Q: With your current plan, 1000 for month.
- A: And what is my current plan?
- Q: You currently have the standard plan.
- A: Ok, I think I might need to move to another plan, what are the available options?
- Q: We currently offer a standard plan, a advanced plan and a premium plan.
- A: And what are their limits?
- Q: the standard plan offers 1000 euros per month, the advanced plan 2000 euros per month... [interrupted]
- A: Perfect, the advanced plan would be enough for me. Can I enable it?
- Q: Yes, would you like to move to the advanced plan right now?
- A: Well wait, how much is going to cost me?
- Q: The advanced plan has a monthly cost of 20 euros per month
- A: Ok, enable it.
- Q: Done, you have been moved to the advanced plan.


# Informable/Requestable Slots
### Informable Slots:
- User:
    - first name
    - last name
    - address
    - phone number
    - email
    - codice fiscale
    - monthly salary
    - current employer
    - debt history
- Credit card:
    - number
    - limit extension
    - activated

### Requestable Slots:
- Credit card:
    - maximum credit limit
    - current credit limit
    - current plan
    - current balance
    - expiry date
- Bank:
    - available credit card plans
    - 


# Noisy channel
- Q: Hello, Bank of Trento, please state your request.
- A: I'd like to open a new credit card
- Q: Do you want to open a new credi card?
- A: I'm not sure
- Q: I'm sorry I couldn't understand, do you want to open a new credi card?
- A: Yes
- Q: Ok, please state your name
- A: Mattia Destro
- Q; Your name is Mattia Destro, correct?
- A: No, it's Matteo not Mattia
- Q: Sorry I couldn't understand, please state your name
- A: Matteo Destro
- Q; Your name is Matteo Destro, correct?
- A: Yes
- Q: Ok, now please spell you codice fiscale letter by letter
- A: A B C D E F 1 2 3 4 5
- Q: Your CF is A B C D E F 1 2 3 4 5, correct?
- A: Yes
- Q: Ok thank you, I'll need some more information to determine your current credit score. This informations will be checked after this procedure has been completed. Do you have any debt history?
- A: No
- Q: Are you current employed?
- A: Yes
- Q: Please state your current employer and annual salary
- A: Amazon, 50k dollars
- Q: Thank you, you're currently employed by Amazon with a 50k salary, correct?
- A: Yes
- Q: Thank you for the information. You're eligible to open a new credit card at our bank. Please confirm that you want to open a new credit card by saying "I confirm I want to open a new credit card".
- A: Yes, I confirm
- Q: Please confirm that you want to open a new credit card by saying "I confirm I want to open a new credit card".
- A: I confirm I want to open a new credit card
- Q: Thank you, you're new account has been opened. Please spell you email address so that we can send you the final documentation
- A: matteo@email.com
- Q: Thank you, we have sent you the documentation with the details of your new account.


# Under-informative user
- Q: Hello Bank of Trento, how can I help you?
- A: Hello, I would like to modify my card
- Q: Ok, what kind of operations do you want to perform? You can: change the credit limit, switch to another plan, cancel your credit card, see your current balance
- A: I want to change the credit limit
- Q: Ok, I need your name and credit card number
- A: It's 12345
- Q: I'm sorry, I need your name and credit card number
- A: Matteo Destro and 12345
- Q: Ok, what limit would you like to set?
- A: More than what I have now
- Q: I'm sorry I need a precise limit value
- A: 1000 euros per month
- Q: Ok, do you confirm you want to change your credit card limit to 1000 euros per month?


# Incoherent user
- Q: Hello Bank of Trento, how can I help you?
- A: Hello, I would like to modify my card
- Q: Ok, what kind of operations do you want to perform? You can: change the credit limit, switch to another plan, cancel your credit card, see your current balance
- A: I want to switch to another plan
- Q: Ok, I need your credit card number
- A: It's 12345
- Q: Thank you, to what plan would you like to switch?
- A: To a 1000 euros per month
- Q: I'm sorry, I couldn't understand the plan name, to what plan would you like to switch?
- A: I don't want to switch plan
- Q: Ok, what kind of operations do you want to perform?
- A: I want to increase my credit limit
- Q: Ok, what limit would you like to set?
- A: 1000 euros per month
- Q: Ok, do you confirm you want to change your credit card limit to 1000 euros per month?
- A: Mh no, maybe it's better to set it to 1100 euros per month
- Q: Ok, do you confirm you want to change your credit card limit to 1100 euros per month?
- A: Yes
- Q: Ok done, your new credit card limit is 1100 per month


# Flexible system
- Q: Hello Bank of Trento, how can I help you?
- A: Hello, I would like to change my credit card limit, my credit card number is 12345
- Q: Ok, what limit would you like to set?
- A: I'm not sure, what I even now is definitely not enough... What is the maximum limit I can have?
- Q: With your current plan, 1000 for month.
- A: And what is my current plan?
- Q: You currently have the standard plan.
- A: Ok, I think I might need to move to another plan, what are the available options?
- Q: We currently offer a standard plan, a advanced plan and a premium plan.
- A: And what are their limits?
- Q: The standard plan offers 1000 euros per month, the advanced plan 2000 euros per month... [interrupted]
- A: Perfect, the advanced plan would be enough for me. Can I enable it?
- Q: Yes, would you like to move to the advanced plan right now?
- A: Well wait, how much is going to cost me?
- Q: The advanced plan has a monthly cost of 20 euros per month
- A: Ok, enable it.
- Q: Done, you have been moved to the advanced plan.


# Explicit confirmation
- Q: Hello Bank of Trento, how can I help you?
- A: Hello, I would like to increase my credit limit
- Q: Ok, do you want to increase your credit limit?
- A: Yes
- Q: Ok, I need your credit card number
- A: It's 12345
- Q: Your credit card number is 12345, correct?
- A: Yes
- Q: Thank you, what credit limit would you like to set?
- A: 1000 euros per month
- Q: Ok, do you confirm you want to change your credit card limit to 1000 euros per month?
- A: Yes
- Q: Ok done, your new credit card limit is 1000 per month


# Implicit confirmation
- Q: Hello Bank of Trento, how can I help you?
- A: Hello, I would like to increase my credit limit
- A: Yes
- Q: Ok, to increase your credit card limit I need your credit card number
- A: It's 12345
- Q: Thank you, what credit limit would you like to set?
- A: 1000 euros per month
- Q: Ok, your credit card limit will be set to 1000 euros per month, do you want to confirm?
- A: Yes
- Q: Ok done, your new credit card limit is 1000 per month


# General implicit confirmation
- Q: Hello Bank of Trento, how can I help you?
- A: Hello, I would like to increase my credit limit
- A: Yes
- Q: Ok, I need your credit card number
- A: It's 12345
- Q: Thank you, what value would you like to set?
- A: 1000 euros per month
- Q: Ok done, your new credit card limit is 1000 per month