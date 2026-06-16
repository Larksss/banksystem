import random
import string
from datetime import datetime


#FUNCTIONS FOR VERIFICATION TO WORK WITH MENU

# Validates common American names, allowing up to four name parts,
# a maximum of 60 characters, and at most 2 apostrophe and 1 hyphen.

punctuations = list(string.punctuation.translate(str.maketrans("","",",-")))

def validate_name(prompt):
   while True:
    print(f"THIS CHARACTERES ARE NOT ALLOWED:\n\n {punctuations}\n")


    name = " ".join(input(prompt).lower().split()) #this way we avoid unnecesary spaces
    if any(char in punctuations for char in name):
       print("\nInvalid character entered, please use allowed characters only\n")
       continue
    
    #To avoid numeric format in the name
    invalid = False
    for part in name.replace("-", " ").replace("'", " ").split(): 
       if not part.isalpha():
          print("\nName contains invalid characters\n")
          invalid = True
          break  
    if invalid:
       continue

       
     #no more than one apostrophe allowed
    apostrophes = name.count("'")
    if apostrophes > 1:
       print("\nInvalid amount of apostrophes (')\n")
       continue  

     #no more than two hyphen allowed
    hyphens = name.count("-")
    if hyphens > 2:
       print("\nInvalid amount of hyphens (-)\n")
       continue
    
    #no more than four names
    number_of_names = len(name.split())
    if number_of_names > 4:
       print("\nInvalid amount of names\n")
       continue
    
    #one single name not allowed
    if number_of_names < 2:
       print("\nInvalid, full name required\n")
       continue
    
    # Taking into consideration that some people have very long names,
    # I set a 60-character limit, including spaces.
    if len(name) > 60:
       print("\nAccount name exceeds the allowed number of characters. Please ensure you enter your name exactly as it appears on your ID\n")
       continue
    
    return name
    

def validate_amount(prompt):
   while True:
      try:
       amount = float(input(prompt))
      except ValueError:
         print("\nIncorrect format try again\n")
         continue
      if amount < 1:
         print("\nInvalid amount, Try again\n")
         continue
      return amount
                 
           
def find_account(prompt):
    while True:
     account_number = input(prompt)
     if account_number.isdigit():
         account_number = int(account_number)
     else:
         print("\nIncorrect format, please enter valid digits\n")
         continue

     for account in bank.accounts:
      if account.account_number == account_number:
          return account
     print("\nWe could not find an account with that number, please try again\n")


def authenticate_pin(account): #This function requires account object to compare PIN entered with account's pin
    for _ in range(3):
     try:
        pin = int(input("Insert your pin: "))
     except ValueError:
        print("\nInvalid format\n")
        continue
     
     if pin == account.pin: 
         return True
     print("\nIncorrect PIN\n")
    print("\nMaximum PIN attempts exceeded. Please try again tomorrow")
    return False

#BANK SYSTEM

class BankAccount:
    ACTIVE = "active"
    UNACTIVE = 'inactive'
    USED_ACCOUNT_ID = set()         #Data base to avoid use the same account ID
    USED_TRAN_ID = set()         # or transaction ID
    
    
    def __init__(self, owner_name, balance):
         
         self.account_number = random.randint(100000,999999)
         while self.account_number in self.USED_ACCOUNT_ID:
            self.account_number = random.randint(100000,999999)
         BankAccount.USED_ACCOUNT_ID.add(self.account_number)
    
         self.pin = random.randint(1000,9999)

         self.owner_name = owner_name

         self.balance = balance

         self.transaction_history = list()

         self.account_status = BankAccount.ACTIVE

    @classmethod
    def _transaction_generator_info(cls, description, amount):
         
        transaction_id = random.randint(0,9999)
        while transaction_id in cls.USED_TRAN_ID:
           transaction_id = random.randint(0,9999)
        cls.USED_TRAN_ID.add(transaction_id)
        transaction_id = str(transaction_id)
        transaction_id = 'TXN-' + transaction_id

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #We pass this library as one item in the transaction list, this way is easier to organize it' 
        return {'TRANSACTION ID:' : transaction_id, 'DESCRIPTION:' : description, 'AMOUNT:': amount, 'DATE:': date}
    

    def deposit(self, amount):
        if self.account_status == BankAccount.UNACTIVE:
            return False, 'This account is currently inactive'
          
        self.balance += amount
        self.transaction_history.append(BankAccount._transaction_generator_info('Deposit', amount))
        return True, 'Deposit successful'
    
    def transfer(self, receiver, amount):
        if self.account_number == receiver.account_number:
            return False, "You cannot transfer money to your own account"

        #CONTINUE WORKING WITH CHATGPT 
        fee = amount * 0.02
        total = amount + fee

        success, message = self.withdraw(total)
        if not success:
            return success, message
        
        success, message = receiver.deposit(amount)
        if not success:
            return success, message

        return True, "Transferred successfully"
    
    def show_balance(self):
        print(f'BALANCE {self.balance}')

    def show_transactions(self):
        if self.transaction_history:
         print('\nTRANSACTION HISTORY\n\n')
         for transaction in self.transaction_history:
             for x,y in transaction.items():
                print(x,y,'\n')

        else:
           print("\nNo transactions has been made yet")
                
    def freeze_account(self):
        self.account_status = BankAccount.UNACTIVE
        return "Account has been frozen "
    
    def unfreeze_account(self):
        self.account_status = BankAccount.ACTIVE

class SavingsAccount(BankAccount):
    def __init__(self, owner_name, balance):
        super().__init__(owner_name, balance)
        self.minimum_balance = 100

    def withdraw(self, amount):
        if self.account_status == BankAccount.UNACTIVE:
            return False, 'This account is currently inactive'
        
        if self.balance - amount < self.minimum_balance:
            return False, 'Insufficient funds'
        
        self.balance -= amount
        self.transaction_history.append(BankAccount._transaction_generator_info('Withdrawal', amount))
        return True, "Withdrawal successful"
        

class CheckingAccount(BankAccount):
    def __init__(self, owner_name, balance):
        super().__init__(owner_name, balance)
        self.overdraft_limit = -200

    def withdraw(self, amount):
        if self.account_status == BankAccount.UNACTIVE:
            return False, 'This account is currently inactive'

        if amount <= 0:
            return False, 'Amount must be greater than 0'

        if self.balance - amount < self.overdraft_limit:
            return False, 'Insufficient funds'
        
        self.balance -= amount
        self.transaction_history.append(BankAccount._transaction_generator_info('Withdrawal', amount))
        return True, "Withdrawal successful"
    
    
class Bank:
    def __init__(self):
        self.accounts = list()

    def create_account_saving(self, owner, initial_balance):
        account = SavingsAccount(owner, initial_balance)
        self.accounts.append(account)
        return True, account
    
    def create_checking_account(self, owner, initial_balance):
        account = CheckingAccount(owner, initial_balance)
        self.accounts.append(account)
        return True, account
        
    def lookup_account(self, number):
        for account in self.accounts:
            if account.account_number == number:
                return True, account, "We have found your account"
        return False, None, "We couldn't find an account with that number"
    
    def delete_account(self, account):
        if account not in self.accounts:
            return False, "This account does not belong to our Bank system"
        
        if account.balance != 0:
            return False, "It's not possible to remove this account because of its remaining balance"
        
        self.accounts.remove(account)
        return True, f'Account under the name of {account.owner_name} has been deleted'

     
    def transfer_between_accounts(self):
        sender_account = find_account("Please enter sender account: ")
        receiver_account = find_account("Please enter receiver account")
        amount = validate_amount("Enter amount to be transfered")

        success, message = sender_account.transfer(receiver_account, amount)
        if success:
           print(message)
        else:
           print(message)


    def show_all_accounts(self):
        for line in self.accounts:
            print(f"Account: {line.account_number} | Owner: {line.owner_name} | Balance: ${line.balance}")
        

bank = Bank()


while True:
 try:
     menu = input("\nWELCOME TO BAC CREDOMATIC\n\n"
              "Please select one of the options below\n"
              "1. Create account\n"
              "2. Deposit\n"
              "3. Withdraw\n"
              "4. Transfer\n"
              "5. Show accounts\n"
              "6. Show transactions\n"
              "7. Freeze account\n"
              "8. Exit\n\n"
              )

     if not menu.isdigit():
         print("Incorrect format, try again")
         continue
     menu = int(menu)

     if menu not in range(1,9):
        print("Invalid number, Please try again") 
        continue
    
    
     if menu == 1:
          while True:
           try:
            account_type = int(input("Please enter (1) for Saving Account and (2) for Checking Account:\n"))
           except ValueError:
               print('Invalid input, please enter a number')
               continue
           
           if account_type not in (1,2):
              print("Invalid option, choose 1 or 2 \n")
              continue
           break
          

          owner_name = validate_name("Please enter your full name: ")
          
          initial_balance = validate_amount("Enter amount you would like to deposit for your initial Balance: ")
            

          if account_type == 1:
            success, account  = bank.create_account_saving(owner_name, initial_balance)

          else:
            success, account = bank.create_checking_account(owner_name, initial_balance)

          if success:
           print("\nAccount created successfully\n")
           print(f"OWNER NAME: {account.owner_name} ACCOUNT NUMBER: {account.account_number}\nPIN: {account.pin}")
          else:
            print("\nAccount creation failed\n")


     elif menu == 2:
        account = find_account("Please enter account number: ")
        amount = validate_amount("Enter the amount you would like to deposit: ")
        success, message = account.deposit(amount)
        if not success:
           print(message)
        else:
           print(message)

    
     elif menu == 3:
        account = find_account("Please enter account number: ")
        success = authenticate_pin(account)
        if not success:
                     continue
        
        amount = validate_amount("Enter the amount you would like to withdraw: ")

        success, message = account.withdraw(amount)
        if success:
            print(message)
        else:
            print(message)

     
     elif menu == 4:
            sender_account = find_account("Please enter your account: ")

            success = authenticate_pin(sender_account)
            if not success:
             continue


            receiver_account = find_account("Please enter account receiver number: ")

            #NO PIN REQUIRED FOR RECEIVER


            while True:
             amount_to_send = validate_amount("How much would you like to transfer: ")
             print(sender_account.transfer(receiver_account, amount_to_send))
             break

     
     elif menu == 5:
         bank.show_all_accounts()
    
     
     elif menu == 6:
        account = find_account("Please, enter the account number for the account you would like to see transaction histroy for: ")
        success = authenticate_pin(account)
        if not success:
           continue
        account.show_transactions()  
         

     elif menu == 7:
           account = find_account("Enter the account number you would like to freeze: ")
           success = authenticate_pin(account)
           if not success:
            continue
           print(account.freeze_account())


     elif menu == 8:
         print("GoodBye")
         exit()
 except ValueError:
    print("Invalid option entered")

