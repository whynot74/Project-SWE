class user_details:
    def __init__(self, userid=None, name=None, email=None, password=None, preferences=None):
        self.userid = userid
        self.name = name
        self.email = email
        self.password = password
        self.preferences = preferences

    def register(self):
        self.name = input("Input Name: ")
        self.userid = input("Input user ID: ")
        self.email = input("Input email: ")
        self.password = input("Input password: ")
        self.preferences = input("Input preferences: ")
        print("Registration successful!")

    def login(self):
        if not self.email or not self.password:
            print("No user registered yet. Please register first.")
            return

        email = input("Input email: ")
        if email != self.email:
            print("Email not found or incorrect!")
            return

        password = input("Input password: ")
        if password != self.password:
            print("Incorrect password!")
            return

        print("Login successful!")

    def update_profile(self):
       
        self.login()

        
        print("What would you like to update?")
        editor = input("1 - Edit Name\n2 - Edit User ID\n3 - Edit Password\n")

        
        if editor == '1':
            self.name = input("Enter new name: ")
            print("Name updated successfully!")
        elif editor == '2':
            self.userid = input("Enter new user ID: ")
            print("User ID updated successfully!")
        elif editor == '3':
            self.password = input("Enter new password: ")
            print("Password updated successfully!")
        else:
            print("Invalid option. No changes were made.")




class event:

    def __init__(self, eventid=None, category=None, location=None, date=None, time=None, price=None):
        self.eventid = eventid
        self.category = category
        self.location= location
        self.date = date
        self.time = time
        self.price = price



    def add_event(self):
        self.eventid = input("input event id")
        self.category = input("input category")
        self.location = input("input location")
        self.date = input("input date")
        self.time = input("input time")
        self.price = input("input price")


    def update_event(self):
        eventid = input('please input event id')   
        if (eventid != self.eventid):
            print("invalid event id")
            return
        else:
            print("What would you like to update?")
            editor = input("1 - Edit Name\n2 - Edit category\n3 - Edit location\n4 - Edit date\n5 - edit time\n6 - edit price\n")

        
            if editor == '1':
                self.name = input("Enter new name: ")
                print("Name updated successfully!")
            elif editor == '2':
                self.category = input("Enter new category: ")
                print("category updated successfully!")
            elif editor == '3':
                self.location = input("Enter new location: ")
                print("location updated successfully!")
            elif editor == '4':
                self.date = input("Enter new date: ")
                print("date updated successfully!")
            elif editor == '5':
                self.time = input("Enter new time: ")
                print("time updated successfully!")
            elif editor == '6':
                self.price = input("Enter new price: ")
                print("price updated successfully!")            
            else:
                print("Invalid option. No changes were made.")


    def delete_event(self):
        eventid = input("Please input event ID to delete: ")
        if eventid != self.eventid:
            print("Invalid event ID! Event not found.")
            return
        else:
            
            self.eventid = None
            self.category = None
            self.location = None
            self.date = None
            self.time = None
            self.price = None
            print("Event deleted successfully!")


    def view_event(self):
         eventid = input("Please input event ID to view: ")
         if eventid != self.eventid:
            print("Invalid event ID! Event not found.")
            return
         else:
             print(self.eventid , self.category, self.location, self.date, self.time, self.price )



