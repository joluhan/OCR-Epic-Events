from django.core.management.base import CommandError
from django.core.management import call_command


def contract_update_input():
    total_amount = input(f'Enter new total amount or leave blank to maintain current value(int or decimal): ')
    if total_amount != '':
        total_amount = float(total_amount)
    
    amount_remaining = input(f'Enter new amount remaining or leave blank to maintain current value(int or decimal): ')
    if amount_remaining != '':
        amount_remaining = float(amount_remaining)

    status = input(f'Enter new status (waiting for signature, signed, in progress, finished, terminated, cancelled) or leave blank to maintain current value: ')
    
    sales_rep_id = input(f'Enter new sales rep ID or leave blank to maintain current value(int): ')
    if sales_rep_id != '':
        sales_rep_id = int(sales_rep_id)

    return (total_amount, amount_remaining, status, sales_rep_id)

def client_update_input():
    fullname = input("Enter new fullname or leave blank to maintain current value: ")
    phone = input("Enter new phone or leave blank to maintain current value: ")
    email = input("Enter new email or leave blank to maintain current value: ")
    company_name = input("Enter new company name or leave blank to maintain current value: ")
    return (fullname, phone, email, company_name)

def event_update_input():
    name = input("Enter new event name or leave blank to maintain current value: ")
    start_date = input("Enter new start date(YYYMMDD) or leave blank to maintain current value: ")
    end_date = input("Enter new end date(YYYMMDD) or leave blank to maintain current value: ")
    location = input("Enter new location or leave blank to maintain current value: ")
    num_of_participants = input("Enter new num of participants(int) or leave blank to maintain current value: ")
    notes = input("Enter new notes or leave blank to maintain current value: ")
    support_staff_id = input("Enter new support_staff_id or leave blank to maintain current value: ")
    if support_staff_id != '':
        support_staff_id = int(support_staff_id)
    return (name, start_date, end_date, location, num_of_participants, notes, support_staff_id)

def user_update_input():
    fullname = input("Enter new fullname or leave blank to maintain current value: ")
    new_username = input("Enter new username or leave blank to maintain current value: ")
    role = input("Enter new role or leave blank to maintain current value: ")
    return (fullname, new_username, role)


def create_user(self):
    try:
        call_command('create_new_user')
    except CommandError as e:
        self.stdout.write(self.style.ERROR(e))
    except ValueError as e:
        self.stdout.write(self.style.ERROR(e))


def view_users(self):
    # enter user id
    user_id = input('Enter ID to view a single user or leave blank to view all users: ')
    if user_id:
        try:
            call_command('read_users', int(user_id))
        except CommandError as e:
            self.stdout.write(self.style.ERROR(e))
    else:
        call_command('read_users')

def update_user(self):
    try:
        user_id = input("Enter user id to be updated(int): ")
        fullname, new_username, role = user_update_input()
        call_command('update_user', int(user_id), fullname=fullname, username=new_username, role=role)
    except CommandError as e:
        self.stdout.write(self.style.ERROR(e))
    except ValueError as e:
        self.stdout.write(self.style.ERROR(e))

def delete_user(self):
    # enter client id
    user_id = input('Enter ID  of user to be deleted: ')
    try:
        call_command('delete_user', int(user_id))
    except CommandError as e:
        self.stdout.write(self.style.ERROR(e))
    except ValueError as e:
        self.stdout.write(self.style.ERROR(e))


def create_client(self):
    try:
        call_command('create_client')
    except CommandError as e:
        self.stdout.write(self.style.ERROR(e))
    except ValueError as e:
        self.stdout.write(self.style.ERROR(e))

def view_client(self):
    # enter client id
    client_id = input('Enter ID to view a single client or leave blank to view all clients: ')
    if client_id:
        try:
            call_command('read_clients', int(client_id))
        except CommandError as e:
            self.stdout.write(self.style.ERROR(e))
    else:
        call_command('read_clients')

def update_client(self):
    # enter client id
    client_id = input('Enter client id: ')
    fullname, phone, email, company_name = client_update_input()
    try:
        call_command('update_client', int(client_id), fullname=fullname, phone=phone, email=email, company_name=company_name)
    except CommandError as e:
        self.stdout.write(self.style.ERROR(e))
    except ValueError as e:
        self.stdout.write(self.style.ERROR(e))

def delete_client(self):
    # enter client id
    client_id = input('Enter client id: ')
    try:
        call_command('delete_client', int(client_id))
    except CommandError as e:
        self.stdout.write(self.style.ERROR(e))
    except ValueError as e:
        self.stdout.write(self.style.ERROR(e))


def create_contract(self):
    try:
        call_command('create_contract')
    except CommandError as e:
        self.stdout.write(self.style.ERROR(e))
    except ValueError as e:
        self.stdout.write(self.style.ERROR(e))

def view_contract(self):
    # enter event id
    contract_id = input('Enter ID to view a single contract or leave blank to view all contracts: ')
    if contract_id:
        try:
            call_command('read_contracts', int(contract_id))
        except CommandError as e:
            self.stdout.write(self.style.ERROR(e))
    else:
        call_command('read_contracts')

def update_contract(self):
    # enter event id
    contract_id = input('Enter ID of contract: ')
    total_amount, amount_remaining, status, sales_rep_id = contract_update_input()
    try:
        call_command('update_contract', int(contract_id), total_amount=total_amount, amount_remaining=amount_remaining, status=status, sales_rep_id=sales_rep_id)
    except CommandError as e:
        self.stdout.write(self.style.ERROR(e))
    except ValueError as e:
        self.stdout.write(self.style.ERROR(e))

def delete_contract(self):
    # enter contract id
    contract_id = input('Enter id of contract to be deleted: ')
    try:
        call_command('delete_contract', int(contract_id))
    except CommandError as e:
        self.stdout.write(self.style.ERROR(e))
    except ValueError as e:
        self.stdout.write(self.style.ERROR(e))


def new_event(self):
    try:
        call_command('create_event')
    except CommandError as e:
        self.stdout.write(self.style.ERROR(e))
    except ValueError as e:
        self.stdout.write(self.style.ERROR(e))

def view_event(self):
    # enter event id
    event_id = input('Enter ID to view a single event or leave blank to view all events: ')
    if event_id:
        try:
            call_command('read_events', int(event_id))
        except CommandError as e:
            self.stdout.write(self.style.ERROR(e))
    else:
        call_command('read_events')

def update_evenvt(self):
    # enter event id
    event_id = input('Enter ID of event to be updated: ')
    name, start_date, end_date, location, num_of_participants, notes, support_staff_id = event_update_input()
    try:
        call_command('update_event', int(event_id), name=name, start_date=start_date, end_date=end_date, location=location, num_of_participants=num_of_participants, notes=notes, support_staff_id=support_staff_id)
    except CommandError as e:
        self.stdout.write(self.style.ERROR(e))
    except ValueError as e:
        self.stdout.write(self.style.ERROR(e))

def delete_event(self):
    # enter event id
    event_id = input('Enter ID of event to be deleted: ')
    try:
        call_command('delete_event', int(event_id))
    except CommandError as e:
        self.stdout.write(self.style.ERROR(e))
    except ValueError as e:
        self.stdout.write(self.style.ERROR(e))