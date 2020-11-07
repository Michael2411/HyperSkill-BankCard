import random
import sqlite3
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute("""CREATE TABLE if not exists card(
id INTEGER,
number TEXT,
pin TEXT,
balance INTEGER DEFAULT 0)""")
conn.commit()


class Card:

    def __init__(self):
        self.account = 0
        self.pin = 0
        self.balance = 0

    def start(self):
        print("""1. Create an account
2. Log into account
0. Exit""")
        x = int(input())
        if x == 1: self.create()
        elif x == 2: self.login()
        elif x == 0:
            print("Bye!")

    def create(self):
        self.balance = 0
        mid = str(random.randint(000000000, 999999999))
        while len(mid) < 9:
            mid = str(random.randint(000000000, 999999999))
        self.account = '400000' + str(mid)
        self.check()
        self.pin = str(random.randint(0000, 9999))
        while len(self.pin) < 4:
            self.pin = str(random.randint(0000, 9999))
        cur.execute(f'INSERT INTO card(number,pin) VALUES ({self.account},{self.pin}) ')
        conn.commit()
        print(f'''\nYour card has been created
Your card number:
{self.account}
Your card PIN:
{self.pin}''')
        self.start()

    def login(self):
        print("\nEnter your card number:")
        self.account = input()
        print("Enter you PIN:")
        self.pin = input()
        cur.execute(f'SELECT number, pin FROM card')
        accounts = cur.fetchall()
        user = (self.account, self.pin)
        conn.commit()
        if user in accounts:
            print("\nYou have successfully logged in!\n")
            print(accounts)
            self.acc()
        else:
            print("\nWrong card number or PIN!\n")
            self.start()

    def acc(self):
        print("""\n1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")
        x = int(input())
        if x == 1:
            print(f'Balance: {self.balance}')
            self.acc()
        elif x == 2:
            money = int(input())
            self.balance = self.balance + money
            print("Income was added!")
            cur.execute(f'UPDATE card SET balance = {self.balance} WHERE number = {self.account}')
            conn.commit()
            self.acc()
        elif x == 3:
            print("Enter card number:")
            num = str(input())
            odd = num[0:15:2]
            even = num[1:15:2]
            sum = 0
            for i in odd:
                i = int(i) * 2
                if i > 9:
                    i = i - 9
                    sum = sum + i
                else:
                    sum = sum + i
            for i in even:
                i = int(i)
                sum = sum + i
            cur.execute(f'SELECT number FROM card')
            numbers = cur.fetchall()
            num1 = (num,)
            if ((sum + int(num[15])) % 10) != 0:
                print("Probably you made a mistake in the card number. Please try again!")
                self.acc()
            elif num == self.account:
                print("You can't transfer money to the same account!")
                self.acc()
            elif num1 not in numbers:
                print("Such a card does not exist.")
                self.acc()
            else:
                print("Enter how much money you want to transfer:")
                trans = int(input())
                cur.execute(f'SELECT balance FROM card WHERE number ={self.account}')
                check = cur.fetchone()
                if trans > int(check[0]):
                    print("Not enough money!")
                    conn.commit()
                    self.acc()
                else:
                    cur.execute(f'UPDATE card SET balance = (balance + {trans}) WHERE number = {num};')
                    cur.execute(f'UPDATE card SET balance = (balance - {trans}) WHERE number = {self.account};')
                    print("Success!")
                    conn.commit()
                    self.acc()

        elif x == 4:
            cur.execute(f"DELETE FROM card WHERE number = {self.account}")
            print("The account has been closed!")
            conn.commit()
            self.start()
        elif x == 5:
            print("\nYou have successfully logged out!\n")
            self.start()
        elif x == 0:
            print("Bye!")

    def check(self):
        odd = self.account[0:15:2]
        even = self.account[1:15:2]
        sum = 0
        for i in odd:
            i = int(i) * 2
            if i > 9:
                i = i - 9
                sum = sum + i
            else:
                sum = sum + i
        final_digit = 0
        for i in even:
            i = int(i)
            sum = sum + i
        for i in range(0, 10):

            if (sum + int(i)) % 10 == 0:
                final_digit = int(i)
                break
        self.account = self.account + str(final_digit)


Card().start()
