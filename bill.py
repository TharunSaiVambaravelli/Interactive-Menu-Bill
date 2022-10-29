import csv
import random
import sys
'''csv module is imported for opening the csv file using open function '''
with open('Menu.csv', newline='') as csvfile:
    def bill():
        '''
        bill() function is used for providing the
        command line interface for ordering the items 
        and display the final bill.
        '''
        list = []
        spam_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spam_reader:
            k = 0
            list.append(row)

        print(list[0][0] + " " + list[0][1] + " " + list[0][2])
        for i in range(1, len(list)):
            print(list[i][0] + "\t" + list[i][1] + "\t   " + list[i][2])
        itemsc = len(list) - 1
        cost = 0
        order = input("Do you want to order (yes/no):")
        #items = []
        count = 0
        half_items_list = {}
        full_items_list = {}
        half_items_quantity = {}
        full_items_quantity = {}
        while order.lower() != "no":
            if order.lower() != "yes":
                print("Invalid selection!!")

            else:
                #item = []
                itemid = input("Enter item id:")
                flag = False
                while flag == False:
                    try:
                        int(itemid)
                        flag = True
                    except ValueError:
                        flag = False
                    if flag:
                        itemid = int(itemid)
                        if itemid > itemsc or itemid <= 0:
                            print("Invalid item id!!")
                            flag = False
                            itemid = input("Enter item id:")
                    else:
                        print("Invalid item id!!")
                        itemid = input("Enter item id:")

                # item.append(itemid)
                plate = input("Enter plate type (half/full):")
                while (plate.lower() == "half" or plate.lower()
                       == "full") == False:
                    print("Choose valid plate!!")
                    plate = input("Enter plate type (half/full):")

                quantity = input("Enter quantity:")
                flag = False
                while flag == False:
                    try:
                        int(quantity)
                        flag = True
                    except ValueError:
                        flag = False
                    if flag:
                        quantity = int(quantity)
                        if quantity <= 0:
                            print("Invalid quantity!")
                            flag = False
                            quantity = input("Enter quantity:")

                    else:
                        print("Invalid quantity!")
                        quantity = input("Enter quantity:")
                # item.append(quantity)
                if plate.lower() == "half":
                    index = 1
                    if half_items_list.get(itemid) is None:
                        half_items_list[itemid] = 0
                        half_items_quantity[itemid] = 0
                else:
                    index = 2
                    if full_items_list.get(itemid) is None:
                        full_items_list[itemid] = 0
                        full_items_quantity[itemid] = 0

                curitemcost = int(list[itemid][index]) * quantity

                if index == 1:
                    half_items_list[itemid] += curitemcost
                    half_items_quantity[itemid] += quantity

                else:
                    full_items_list[itemid] += curitemcost
                    full_items_quantity[itemid] += quantity
               # item.append(curitemcost)
                cost = cost + curitemcost
               # print(itemid,quantity,list[itemid][index],cost)
               # items.append(item)
                count = count + 1
            order = input("Do you want to order (yes/no):")
        if count == 0:
            print("Thankyou for visiting!!!")
            sys.exit()

        print()
        print()
        print(
            "Choose the percentage of tip you wish to give\n1. 0%\n2. 10%\n3. 20%  \nEnter your choice:",
            end="")
        tip = input()
        flag = False
        while flag == False:
            try:
                int(tip)
                flag = True
            except ValueError:
                flag = False
            if flag:
                tip = int(tip)
                if tip < 1 or tip > 3:
                    print("Invalid choice!!")
                    flag = False
                    print(
                        "Choose the percentage of tip you wish to give\n1. 0%\n2. 10%\n3. 20%  \nEnter your choice:",
                        end="")
                    tip = input()
            else:
                print("Invalid choice!!")
                print(
                    "Choose the percentage of tip you wish to give\n1. 0%\n2. 10%\n3. 20%  \nEnter your choice:",
                    end="")
                tip = input()
        if tip == 2:
            tp = "20%"
            tipcost = cost * 0.1
        elif tip == 3:
            tp = "10%"
            tipcost = cost * 0.2
        else:
            tp = "0%"
            tipcost = 0
        totalbill = cost + tipcost
        print()
        print()

        print("The total bill of your order is :%.2f" % totalbill)
        # print("The cost of your bill :",cost)
        # print("The tip of your bill :",tipcost)
        print()
        print()

        quantity = input(
            "How many people are going to split the Bill? Enter the count:")
        flag = False
        while flag == False:
            try:
                int(quantity)
                flag = True
            except ValueError:
                flag = False
            if flag:
                quantity = int(quantity)
                if quantity <= 0:
                    print("Invalid count!")
                    flag = False
                    quantity = input(
                        "How many people are going to split the Bill? Enter the count:")

            else:
                print("Invalid count!")
                quantity = input(
                    "How many people are going to split the Bill? Enter the count:")

        print("The share of per person is :%.2f" %
              round((totalbill / quantity), 2))
        print()
        print()

        print("A limited time event is going on called 'TEST YOUR LUCK'.\nIt's a lucky draw where you can win upto 50% discount on your food.\nYou can also get an increase on your total bill.")
        tryluck = input("Do you like to participate ? (yes/no) :")
        while (tryluck.lower() == "yes" or tryluck.lower() == "no") == False:
            print("Invalid selection!!")
            tryluck = input("Do you like to participate ? (yes/no) :")
        discount = 0
        if tryluck.lower() == "yes":
            print("The Lucky draw has started. Let's see how much you win...")
            luck = random.randint(1, 100)
            if luck > 0 and luck <= 50:
                discount = 20
            elif luck > 50 and luck <= 70:
                discount = 0
            elif luck > 70 and luck <= 85:
                discount = -10

            elif luck > 85 and luck <= 95:
                discount = -25

            else:
                discount = -50
            if discount != 0:
                luckyamount = (discount / 100) * totalbill
                finalbill = totalbill + luckyamount
            else:
                luckyamount = 0
                finalbill = totalbill
            if discount < 0:
                print(" ****        ****", end="\n")
                print("|    |      |    |", end="\n")
                print("|    |      |    |", end="\n")
                print("|    |      |    |", end="\n")
                print(" ****        ****", end="\n")
                print("\n", end="\n")
                print("        {}", end="\n")
                print("     ________")
                discount = -discount
                print("Congrats! You have won ", discount, "% discount")
                print("Discount amount: %.2f" % (-luckyamount))
            else:
                print(" ****")
                print("*    *")
                print("*    *")
                print("*    *")
                print("*    *")
                print(" ****")
                if(discount == 0):
                    print("Better luck next time! ")
                    print("Discount/Increase amount:+%.2f" % discount)
                else:
                    print(
                        "Hard Luck! I guess it's just not your day.You have got 20% increase on your bill.")
                    print("Increased amount:%.2f" % luckyamount)
        else:
            luckyamount = 0
            finalbill = totalbill
        print()
        print()
        print("Final bill")
        '''for j in items:
            print("Item ",j[0],"[",j[1],"]:",j[2])
        '''
        for i in range(1, itemsc + 1):
            if half_items_list.get(i) is not None:
                print(
                    "Item ",
                    i,
                    " [Half] [",
                    half_items_quantity[i],
                    "] : %.2f" %
                    (half_items_list[i]))
            if full_items_list.get(i) is not None:
                print(
                    "Item ",
                    i,
                    " [Full] [",
                    full_items_quantity[i],
                    "] : %.2f" %
                    (full_items_list[i]))
        print("Total:%.2f" % cost)
        print("Tip Percentage:", tp)
        print("Discount/Increase Value:", end="")
        if luckyamount >= 0:
            print("+%.2f" % round(luckyamount, 2))
        else:
            print("%.2f" % round(luckyamount, 2))

        print("Final Total:%.2f" % round(finalbill, 2))
        print()
        print()
        print("The updated Share price of per person is:%.2f" %
              round((finalbill / quantity), 2))
        print("Thankyou for visiting!!!")
    bill()
    print(bill.__doc__)
