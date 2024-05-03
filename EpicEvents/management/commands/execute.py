from django.core.management.base import BaseCommand
from django.core.management import call_command
from . import utils

class Command(BaseCommand):
    help = 'Perform an action'

    def add_arguments(self, parser):
        parser.add_argument('user_role', type=str, help='Role of logged in user')

    def handle(self, *args, **kwargs):
        user_role = kwargs['user_role']
        user_input = 0

        if user_role == "management":
            while(user_input != 'x'):
                print("\n1 - Create a new user\n2 - View users\n3 - Update user\n4 - Delete user\n5 - View clients\n6 - Update client\n7 - Delete client\n8 - Create a new contract\n9 - View contracts\n10 - Update contract\n11 - Delete contract\n12 - View events\n13 - Update event\n14 - Delete event\nX - logout")
                user_input = input("Enter a number to execute the function: ").lower()

                if user_input == '1':  # add new user
                    utils.create_user(self)

                # View users
                elif user_input == '2':
                    utils.view_users(self)

                # update user
                elif user_input == '3':  
                    utils.update_user(self)

                # delete user
                elif user_input == '4':
                    utils.delete_user(self)
                        
                # View client
                elif user_input == '5':
                    utils.view_client(self)
                        
                # update client
                elif user_input == '6':
                    utils.update_client(self)
                        
                # delete client
                elif user_input == '7':
                    utils.delete_client(self)
                        
                # create contract
                elif user_input == '8':
                    utils.create_contract(self)
                
                # View contracts
                elif user_input == '9':
                    utils.view_contract(self)
                
                # update contract
                elif user_input == '10':
                    utils.update_contract(self)
                
                # delete contract
                elif user_input == '11':
                    utils.delete_contract(self)
                            
                # View events
                elif user_input == '12':
                    utils.view_event(self)
                
                # update events
                elif user_input == '13':
                    utils.update_evenvt(self)
                
                # delete events
                elif user_input == '14':
                    utils.delete_event(self)

                # Logout
                elif user_input == 'x':
                    call_command('logout')

                else:
                    self.stdout.write(self.style.ERROR('\nInvalid input! Enter a choice from the list'))
                    continue


        elif user_role == "sales":
            while(user_input != 'x'):
                print("\n1 - Add a new client\n2 - View clients\n3 - Update a client\n4 - View contracts\n5 - Update a contract\n6 - Create a new event\n7 - View events\nX - logout")
                user_input = input("Enter a number to execute the function: ").lower()

                if user_input == '1':  # add a new client
                    utils.create_client(self)

                # View clients
                elif user_input == '2':
                    utils.view_client(self)

                # update client
                elif user_input == '3':
                    utils.update_client(self)

                # View contracts
                elif user_input == '4':
                    utils.view_contract(self)
                
                # update contract
                elif user_input == '5':
                    utils.update_contract(self)

                # create new event
                elif user_input == '6':
                    utils.new_event(self)
                
                # View events
                elif user_input == '7':
                    utils.view_event(self)

                # Logout
                elif user_input == 'x':
                    call_command('logout')

                else:
                    self.stdout.write(self.style.ERROR('\nInvalid input! Enter a choice from the list'))
                    continue

        else:
            while(user_input != 'x'):
                print("\n1 - View events\n2 - Update event\nX - logout")
                user_input = input("Enter a number to execute the function: ").lower()
                                
                # View events
                if user_input == '1':
                    utils.view_event(self)

                # Update an event
                elif user_input == '2':
                    utils.update_evenvt(self)

                # Logout
                elif user_input == 'x':
                    call_command('logout')

                else:
                    self.stdout.write(self.style.ERROR('\nInvalid input! Enter a choice from the list'))
                    continue

