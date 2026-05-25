import random
from datetime import datetime
class BankAccount:
    ACTIVE = "active"
    UNACTIVE = 'unactive'
    USED_NUMBERS = list()
    USED_TRAN_ID = list()
    
    
    def __init__(self, owner_name, balance):
        while True:
         self.account_number = random.randint(0000000,999999)
         if self.account_number in BankAccount.USED_NUMBERS:
             continue
         BankAccount.USED_NUMBERS.append(self.account_number)
         break
        self.pin = random.randint(0000,9999)
        self.owner_name = owner_name
        self.balance = balance
        self.transaction_history = list()
        self.account_status = BankAccount.ACTIVE

    @staticmethod
    def _transaction_generator_info(description, amount):
        generator = dict()
        dat = datetime.now()
        dat = dat.strftime("%Y-%m-%d %H:%M:%S")
        transaction_id = BankAccount._transaction_generator_id()
        #I place ID transaction as key just in case will be more than likely for customer service search data by transactions ID
        generator[('TRANSACTION ID:',transaction_id)] = [('DESCRIPTION' , description), ('AMOUNT:', amount),('DATE', dat )]
        return generator

    def _transaction_generator_id():
        while True:
          transaction_id = random.randint(0000,9999)
          if transaction_id in BankAccount.USED_TRAN_ID:
              continue
          break
        BankAccount.USED_TRAN_ID.append(transaction_id)
        transaction_id = str(transaction_id)
        transaction_id = 'TXN-' + transaction_id
        return transaction_id
        

    def deposit(self, amount):
        if self.account_status == BankAccount.UNACTIVE:
            return False, 'This account is currently unactive'
            
        if amount <= 0:
            print('Incorrect format, please try again')
            return False
          
        self.balance += amount
        self.transaction_history.append(BankAccount._transaction_generator_info('Deposit', amount))
        return True, 'Deposit successful'
    
    def transfer(self, receiver, amount):
        if self.account_number == receiver.account_number:
            self.transaction_history.append("Failed transfer: Invalid receiver")
            return False, "You can not transfer money to your own account"

        if amount <= 0:
            self.transaction_history.append("Failed transfer: Invalid amount")
            return False, "Incorrect format, Please try again'"
        
        if self.balance - amount < self.withdraw_limit:
            self.transaction_history.append("Failed transfer: insufficient funds")
            return False, "Amount exceeds account limit"
        fee = amount * 0.02
        total = amount + fee
        self.withdraw(total)
        receiver.deposit(amount)
        return True
    
    def show_balance(self):
        print(f'BALANCE {self.balance}')

    def show_transactions(self):
        print('\nTRANSACTION HISTORY\n')
        for transaction in self.transaction_history:
            if type(transaction) == dict:
             for id,info in transaction.items():
                 for line in info:
                     print(*line)
                 print(*id)
                 print('\n')
            else:
                print(transaction)
                
    def freeze_account(self):
        self.account_status = BankAccount.UNACTIVE
    
    def unfreeze_account(self):
        self.account_status = BankAccount.ACTIVE

class SavingsAccount(BankAccount):
    def __init__(self, owner_name, balance):
        super().__init__(owner_name, balance)
        self.withdraw_limit = 100

    def withdraw(self, amount):
        if self.account_status == BankAccount.UNACTIVE:
            return False, 'This account is currently unactive'

        if amount <= 0:
            return False, 'Incorrect format, please try again'
        
        if self.balance - amount < self.withdraw_limit:
            return False, 'Amount exceeds account limit'
        
        self.balance -= amount
        self.transaction_history.append(BankAccount._transaction_generator_info('Withdraw', amount))
        return True, "Withdrawal successful"
        
        
class CheckingAccount(BankAccount):
    def __init__(self, owner_name, balance):
        super().__init__(owner_name, balance)
        self.overdraft_limit = - 200

    def withdraw(self, amount):
        if self.account_status == BankAccount.UNACTIVE:
            return False, 'This account is currently unactive'

        if amount <= 0:
            return False, 'Incorrect format, Please try again'

        if self.balance - amount < self.overdraft_limit:
            return False, 'Amounts exceeds account limit'
        self.balance -= amount
        self.transaction_history.append(BankAccount._transaction_generator_info('Withdraw', amount))
        return True
    
class Bank:
    def __init__(self):
        self.accounts = list()

    def create_account_saving(self, owner, initial_balance):
        account = SavingsAccount(owner, initial_balance)
        self.accounts.append(account)
        return True, account, account.account_number, account.pin
    
    def create_checking_account(self, owner, initial_balance):
        account = CheckingAccount(owner, initial_balance)
        self.accounts.append(account)
        return True, account, account.account_number, account.pin
        
    def find_account(self, number):
        for obj in self.accounts:
            if obj.account_number is number:
                return True, obj, "We have found your account"
        return False, "We couldn't find an account with that number"
    
    def delete_account(self, account):
        if account not in self.accounts:
            return False, "This account does not belong to our Bank system"
        
        if account.balance != 0:
            return False, "It's not possible to remove this account because of its remaining balance"
        
        self.accounts.remove(account)
        return True, f'Account under de name of {account.owner_name} has been deleted'
        
    def transfer_between_accounts(self, sender_number, receiver_number, amount):
        result = 0
        for line in self.accounts:
            if line.account_number is sender_number:
                obj1 = line
                result = 1
                break
        if result == 0:
            return False, "We have not found sender account in the system"
        
        result = 0
        for line in self.accounts:
            if line.account_number is receiver_number:
                obj2 = line
                result = 1
                break
        if result == 0:
            return False, "We have not found that receiver account in the system"
        
        obj1.transfer(obj2, amount)
        return True, "Successful Transfer"
    
    def show_all_accounts(self):
        for line in self.accounts:
            print(f"Account: {line.account_number} | Owner: {line.owner_name} | Balance: ${line.balance}")
        

bank = Bank()

success, larks, account_number, pin  = bank.create_account_saving('larks', 1000)
success, warrent, account_number, pin = bank.create_account_saving('warrent', 2000)
success, fernando, account_number, pin = bank.create_checking_account('fernando', 1000)

print(larks.deposit(10000))
print(warrent.withdraw(100))

#MENU

while True:
 try:
     menu = int(input("\nWELCOME TO BAC CREDOMATIC\n\n"
              "Please select one of the options below\n"
              "1. Create account\n"
              "2. Deposit\n"
              "3. Withdraw\n"
              "4. Transfer\n"
              "5. Show accounts\n"
              "6. Show transactions\n"
              "7. Freeze account\n"
              "8. Exit\n\n"
              ))
    

     if menu not in range(1,9):
        print("Invalid number, Please try again") 
        continue
     break
 except ValueError:
    print('Invalid format\nPlease try again\n\n')
    continue

try:
     # OPTION 1
     if menu == 1:
          while True:
           account_type = int(input("Please enter (1) for Saving Account and (2) for Checking Account:\n"))
           if account_type not in range(1,3):
              print("Invalid option\n")
              continue
           break
            
          while True:
           owner_name = input("Please enter name: ").lower()
           if not owner_name.isalpha():
               print("Invalid name, only letters allowed")
               continue
           break
          
          while True:
           initial_balance = input("Please enter initial balance: ")
           if not initial_balance.isdigit():
               print('Invalid format, try againg')
               continue
           initial_balance = int(initial_balance)

           if account_type == 1:
              success, owner_name, account_number, pin  = bank.create_account_saving(owner_name, initial_balance)
              print("Saving Account created successfully\n")
              print(f"ACCOUNT NUMBER: {account_number}\nPIN: {pin}")
              break
           elif account_type == 2 :
              success, owner_name, account_number, pin  = bank.create_checking_account(owner_name, initial_balance)
              print("Saving Account created successfully\n")
              print(f"ACCOUNT NUMBER: {account_number}\nPIN: {pin}")
              break

     elif menu == 2:
        while True:
            num = input("Please enter account number:")
            if not num.isdigit():
                print("Please enter digits only")
                continue
            num = int(num)

            for account in bank.accounts:
                if num == account.account_number:
                    while True:
                     amount = input("How much you would like to deposit: ")
                     if not amount.isdigit():
                         print("Please enter digits only: ")
                         continue
                     break
                    amount = int(amount)
                    print(account.deposit(amount))
                else:
                    print("We haven't found accounts with that number")
                    break
            break
          
     elif menu == 3:
        while True:
            num = input("Please enter account number:")
            if not num.isdigit():
                print("Please enter digits only")
                continue
            num = int(num)
            num = larks.account_number

            for account in bank.accounts:
                check = 'false'
                if num == account.account_number:
                     for _ in range(3):
                         pin = input("Please enter your pin: ")
                         pin = larks.pin
                         if pin == account.pin:
                            check = 'true'
                            break
                         else:
                             print("Invalid PIN")
                     if check == 'true':
                      break
                     print('You have exceeded the number of attemps. Try tomorrow.')
                     exit()
            if check != 'true':
                print("We have not found account with that number")
                break
            break

        while True:                          
            amount = input("How much you would like to withdraw: ")
            if not amount.isdigit():
             print("Please enter digits only: ")
             continue
            break
    
        amount = int(amount)
        account.withdraw(amount)

     elif menu == 4:
           while True:
               acc = input("Please enter your account number:")
               if not acc.isdigit():
                print("Please enter digits only")
                continue
               acc = int(acc)
               break
           check = 'false'
           for account in bank.accounts:
               if acc == account.account_number:
                   for _ in range(3):
                         pin = input("Please enter your pin: ")
                         if pin == account.pin:
                            check = 'true'
                            sender = account
                            break
                         else:
                             print("Invalid PIN, try again tomorrow")
               elif check == "true":
                break         
           if check == 'false':
             print("We could not find your account")
             exit()


           while True:
               receiver = input("Plese enter account receiver number: ")
               if not receiver.isdigit():
                   print("Please enter digits only")
                   continue
               receiver = int(receiver)
               break
           check = "false"
           for account in bank.accounts:
               if receiver == account.account_number:
                   check = "true"
                   receiver = account
                   break
           if check == 'false':
               print('We have not found a receiver account with that number')
               exit()
           
           while True:
               amount = input("How much would you like to deposit: ")
               if not amount.isdigit():
                   print('Please enter digits only')
                   continue
               amount = int(amount)
               sender.transfer(receiver, amount)
               break            

     elif menu == 5:
         bank.show_all_accounts
    
     elif menu == 6:
         while True:
          acc = input("Please, enter the account number for the account you would like to see transaction histroy for: ")
          if not acc.isdigit():
              print("Please enter digits only")
              continue
          acc = int(acc)
          break
         
         check = 'false'
         for account in bank.accounts:
             if acc == account.account_number:
                 for _ in range(3):
                     pin = input("Insert your pin: ")
                     pin = int(pin)
                     if pin == account.pin:
                         account.show_transactions()
                     else:
                         print("Incorrect pin")
                 print('Invalid PIN, try again tomorrow')
                 exit()
         if check == 'false':
             print('We did not find an account with that number')
          
     elif menu == 7:
          while True:
           acc = input("Please, enter the account number for the account you would like to freeze: ")
           if not acc.isdigit():
               print("Please enter digits only")
               continue
           acc = int(acc)
           break
          
          check = 'false'
          for account in bank.accounts:
              if acc == account.account_number:
                  for _ in range(3):
                      print(account.pin)
                      pin = input("Insert your pin: ")
                      pin = int(pin)
                      if pin == account.pin:
                          account.freeze_account()
                          print(larks.account_status)
                      else:
                          print("Incorrect pin")
                  print('Invalid PIN, try again tomorrow')
                  exit()
          if check == 'false':
              print('We did not find an account with that number')
         
     elif menu == 8:
         print("GoodBye")
         exit()
except ValueError:
    print("Invalid digit entered")





