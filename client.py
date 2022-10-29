import requests
import random
import sys
login = False
sess = requests.Session()
'''This is client python file'''
while(True):
    if(login != True):
        print("1. Signup\n2. Signin\n3.Exit")
        n = int(input("Enter choice:  "))
        if n == 3:
            sys.exit()
        elif n == 1:
            id = int(input("Enter id: "))
            name = input("Enter name: ")
            pas = input("Enter Password: ")
            str1 = ""
            chef = int(input("Are you a chef: "))
            data = {
                "id": id,
                "name": name,
                "pwd": pas,
                "is_chef": chef
            }
            response = sess.post('http://localhost:8000/signup', json=data)
            str1 = response.text
            print(str1)

        elif n == 2:
            id = input("Enter id:")
            id = int(id)
            pas = input("Enter password:")
            data = {
                "id": id,
                "password": pas,
            }
            l = []
            response = sess.post('http://localhost:8000/signin', json=data)
            if(response.text == "LoggedIn"):
                login = True
            print(response.text)
    else:
        print("1.Log Out\n2.Add Menu\n3. Read Menu")
        print("4.Order food items\n5.Generate Bill\n6. Exit")
        n = int(input("Enter choice:  "))
        if n == 1:
            response = requests.put('http://localhost:8000/logout', json=data)
            if(response.text == "logged out"):
                login = False
            print(response.text)

        elif n == 2:
            data = {
                'id': id
            }
            response = requests.post(
                'http://localhost:8000/checkchef', json=data)
            if(response.text == "0"):
                print("You are not chef")
                continue
            item_id = int(input("Enter item id:"))
            half_plate_price = int(input("Enter half plate price:"))
            full_plate_price = int(input("Enter full plate price:"))
            data = {
                "item_id": item_id,
                "half_plate_price": half_plate_price,
                "full_plate_price": full_plate_price
            }
            response = requests.post(
                'http://localhost:8000/addmenu', json=data)
            print(response.text)

        elif n == 3:

            response = requests.get('http://localhost:8000/readmenu').json()
            for i in response:
                h = response[i]
                if h["half_plate"] is not None:
                    print("Item", i, "[half]:", h["half_plate"])
                if h["full_plate"] is not None:
                    print("Item", i, "[full]:", h["full_plate"])

        elif n == 4:
            response = requests.get('http://localhost:8000/readmenu')
            full_plates = {}
            half_plates = {}
            print("Menu card:")
            print(response.text)
            items = []
            print(len(eval(response.text)))
            menu = eval(response.text)
            while(True):
                print("What item would you want to order")
                list1 = []
                item_num = (input())
                item_no = item_num
                items.append(item_no)
                print("what is the plate type: 0 for half and 1 for full")
                typep = int(input())
                list2 = []
                print("How many plates do you want")
                quantity = int(input())
                if(typep == 1):
                    if item_no in full_plates:
                        full_plates[item_no] += quantity

                    else:
                        full_plates[item_no] = quantity
                else:
                    if item_no in half_plates:
                        half_plates[item_no] += quantity

                    else:
                        half_plates[item_no] = quantity

                print("Do You want any other items 1 for YES 0 for NO")
                if(int(input()) == 0):
                    break
            prices = {}
            luckyamount = 0
            total = 0
            for i in half_plates:
                total += menu[i]["half_plate"] * half_plates.get(i)

            for i in full_plates:
                total += menu[i]["full_plate"] * full_plates.get(i)

            print("total price:  ", total)
            print("Tip percentage you want to give")
            print("0 for 0% 1 for 10% 2 for 20%")

            tip = input()
            tip = int(tip)
            tp = ""
            if tip == 2:
                tp += "20%"
                tipcost = total * 0.2
            elif tip == 1:
                tp += "10%"
                tipcost = total * 0.1
            else:
                tp += "0%"
                tipcost = 0
            total = total + tipcost
            print("total price after tip: ", total)
            share_bill = int(input("Enter how many people to share the bill"))
            print("Each person share: ", (total) / share_bill)
            play_game = int(input("Do you want to play game: 1:Yes 0:NO"))
            finalbill=total
            if play_game == 1:
                print("The Lucky draw has started. Let's see how much you win...")
                discount = 0
                luck = random.randint(1, 100)
                if luck > 0 and luck < 51:
                    discount = 20
                elif luck > 70 and luck < 86:
                    discount = -10
                elif luck > 50 and luck < 71:
                    discount = 0
                elif luck > 85 and luck < 96:
                    discount = -25
                else:
                    discount = -50
                if discount != 0:
                    luckyamount = (discount / 100) * total
                    finalbill = total + luckyamount
                else:
                    luckyamount = 0
                    finalbill = total
                if discount < 0:
                    print(" ****        ****", end="\n")
                    print("|    |      |    |", end="\n")
                    print("|    |      |    |", end="\n")
                    print("|    |      |    |", end="\n")
                    print(" ****        ****", end="\n")
                    print("\n", end="\n")
                    print("        {}", end="\n")
                    print("      ______")
                    print("Congrats! You have won", -discount, "% discount")
                    print("Discount amount: ", -luckyamount)
                else:
                    print(" ****")
                    print("*    *")
                    print("*    *")
                    print("*    *")
                    print("*    *")
                    print(" ****")
                    if(discount == 0):
                        print("Better luck next time! ")
                        print("Discount/Increase amount: ", discount)
                    else:
                        print(
                            "Hard Luck! I guess it's just not your day.You have got 20% increase on your bill.")
                        print("Increased amount:", +luckyamount)
            discount = luckyamount
            print("Final bill")
            for i in menu:
                if i in half_plates:
                    print("Item ", i, "[half]:", menu[i]["half_plate"])
                else:
                    print("Item ", i, "[full]:", menu[i]["full_plate"])

            print("Total:", total)
            print("Tip Percentage:", tp)
            print("Discount/Increase Value:", end="")
            if luckyamount >= 0:
                print("+", luckyamount)
            else:
                print("-", luckyamount)

            print("Final Total:", finalbill)
            print(
                "The updated Share price of per person is:",
                (finalbill / share_bill))

            
            data={
                "_id":id,
                "tip":tp,
                "discount":luckyamount,
                "share_bill":share_bill,
                "play_game":play_game,
                "total":finalbill,
                "half_plates":half_plates,
                "full_plates":full_plates
            }

            response =requests.post('http://localhost:8000/addtrans',json=data)
            print(response.text)
        elif n==5:
            data={
                "user_id":id
            }
            response=requests.post('http://localhost:8000/showtids',json=data).json()

            print(response)  

            tid=int(input("chose transaction id:"))
           
            data={
               
                "t_id":tid
            }
            response=requests.post('http://localhost:8000/getorder',json=data).json()

            print(response)
            response=requests.post('http://localhost:8000/gettransd',json=data).json()


        else:
            print("Incorrect Choice")
