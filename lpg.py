print('''
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                          SHREE JEE LPG AGENCY
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
''')

import mysql.connector
con=mysql.connector.connect(user='root',host='localhost',password='Admin@1234')
cur=con.cursor()
cur.execute("create database if not exists lpg")
cur.execute("use lpg")
cur.execute("create table if not exists complain_department(user_id int not null primary key, complain varchar(200))")
cur.execute("create table if not exists customer_data(user_id int not null, name varchar(20) not null, mobile_number varchar(10) primary key, date date not null, address varchar(50))")
cur.execute("create table if not exists cylinder(order_id int not null, user_id int not null primary key, name varchar(20) not null, order_date date not null, address varchar(50))")
cur.execute("create table if not exists sno(order_id int not null, user_id int not null)")
cur.execute("create table if not exists faculty(username varchar(25) not null, pwd varchar(25) not null)")
con.commit()

                                             #order id=1000
                                             #user_id=100

x=0
cur.execute("select * from sno")
for i in cur:
    x=1                                      #updated value of variable confirms the existence of data
if x==0:
    cur.execute("insert into sno values(1000,100)")
    con.commit()
    
x=0
                                             #username (by faculty of agency)=Admin
                                             #pwd=agency1234
cur.execute("select * from faculty")
for i in cur:
    x=1                                      #updated value confirms the existence of data
if x==0:
    cur.execute("insert into faculty values('Admin','agency1234')")
    con.commit()
while True:
    print('''
1. Customer Login
2. Faculty Login
3. Exit
''')
    ch=int(input("Enter your choice: "))
    if ch==1:                                #customer login
        loop1="n"
        while loop1 in ("n","N"):
            print('''
1. User Login
2. New user
3. Back to mains
''')
            ch=int(input("Enter your choice: "))
            if ch==1:
                user=input("Enter your User ID: ")
                cur.execute("select * from customer_data where user_id='"+user+"'")
                x=0
                for i in cur:                                    #row of user_id
                    c_user,c_name,c_num,c_date,c_adrs=i
                    x=1
                if x==0:
                    print("No user is found with such User Id! Either recheck your id or register yourself first.")
                else:
                    print(f"{c_name} logged in successfully!")
                    print('''
1. Cylinder Booking
2. My Order
3. Billing Details
4. Complaint
5. Order Cancellation
6. Surrender your connection
7. Logout
''')
                    ch=int(input("Enter your choice: "))
                    if ch==1:
                        check=input("Are you confirm for booking the cylinder?(y/n) ").lower()
                        if check=="y":
                            cur.execute("select * from sno")
                            for i in cur:
                                c_user,c_order=i
                            c_order+=1
                            cur.execute("insert into cylinder values('"+str(c_order)+"','"+str(user)+"','"+c_name+"',curdate(),'"+c_adrs+"')")
                            cur.execute("update sno set order_id='"+str(c_order)+"'")
                            con.commit()
                            print("Your order has been placed successfully and you can either pay through online transactions or through cash.")
                    elif ch==2:
                        cur.execute("select * from cylinder where user_id='"+str(user)+"'")
                        for i in cur:
                            c_order,c_user,c_name,c_odate,c_adrs=i                    #this will generate an output for the user of his/her own info after booking.
                        print(f"ORDER ID => {c_order}")
                        print(f"USER ID => {c_user}")
                        print(f"USER NAME => {c_name}")
                        print(f"ORDER DATE => {c_odate}")
                        print(f"ADDRESS => {c_adrs}")
                        print(f"Your order is placed and will be delivered within 15 days from {c_odate}")
                    elif ch==3:
                        print("Total amount to be paid= Rs.950")
                    elif ch==4:
                        print("Please tell us the inconveniency you have gone through(keep it short and concise). ")
                        cur.execute("select * from complain_department where user_id='"+str(user)+"'")
                        x=0
                        for i in cur:
                            c_user,c_complain=i
                            x=1
                        if x==0:
                            complain=input("Enter your complaint: ")
                            cur.execute("insert into complain_department values('"+str(user)+"','"+complain+"')")
                            con.commit()
                        else:
                            print(f'{complain}')
                    elif ch==5:
                        check=input("Are you confirm with your order cancellation?(y/n)").lower()
                        if check=="y":
                            cur.execute("delete from cylinder where user_id='"+str(user)+"'")
                            con.commit()
                        elif check=="n":
                            print("Your order hasn't cancelled yet.")
                    elif ch==6:                           #it means to delete/remove the existing user from the customer_data.
                        check=input("Are you confirm with breaking your connection?(y/n)").lower()
                        if check=="y":
                            cur.execute("delete from customer_data where user_id='"+str(user)+"'")
                            con.commit()
                            print("Your connection has been removed now!!")
                        elif check=="n":
                            print("Your connection is still on going.")
                    elif ch==7:                           #get exit from the user login
                        break
            elif ch==2 or ch=="New user".lower():         #new user registration giving a unique id
                name=input("Enter your name: ")
                number=input("Enter your mobile no.: ")
                adrs=input("Enter your address: ")
                cur.execute("select * from sno")
                for i in cur:
                    c_user,c_order=i
                c_user+=1
                cur.execute("insert into customer_data values('"+str(c_user)+"','"+name+"','"+number+"',curdate(),'"+adrs+"')")
                cur.execute("update sno set user_id='"+str(c_user)+"'")
                con.commit()
                print(f"Now, you are registered successfully, with User Id: {c_user}")
            elif ch==3:
                break
    elif ch==2:                                           #faculty login
        pswd=input("Enter your password=")
        cur.execute("select * from faculty")
        for i in cur:
            f_username,f_pswd=i
        if pswd==f_pswd:
            print("Logged in successfully!")
            loop2='n'
            while loop2 in ('n','N'):
                print('''
        1. View Orders
        2. Delete Orders
        3. Delete Connection
        4. Logout
        ''')
                ch=int(input("Enter your choice: "))
                if ch==1:
                    cur.execute("select * from cylinder")
                    for i in cur:
                        c_order,c_user,c_name,c_odate,c_adrs=i
                        print("ORDER ID | USER ID | NAME | ORDER DATE | ADDRESS")
                        print(f"{c_order} | {c_user} | {c_name} | {c_odate} | {c_adrs}")
                elif ch==2:
                    user_id=int(input("Enter the user id: "))
                    cur.execute("delete from cylinder where user_id='"+str(user_id)+"'")
                    con.commit()
                    print("The order is deleted successfully. ")
                elif ch==3:
                    user_id=int(input("Enter the user id: "))
                    cur.execute("delete from customer where user_id='"+str(user_id)+"'")
                    cur.execute("delete from cylinder where user_id='"+str(user_id)+"'")
                    con.commit()
                    print("Connection is deleted now.")
                elif ch==4:
                    break
        else:
                print("Wrong Password. Try Again.")


    elif ch==3:                                          #exit the program
        break















                        
                        
                        
                        
                        






















                        

                     
        
        
