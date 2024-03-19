from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime
from tkinter import ttk
import os.path
import sys
import tkinter as tk


class ClientSearchApp:
    def __init__(self, master):
        self.master = master
        self.master.title("NEDIS Client Search")

        # Set the initial size of the window (width x height)
        self.master.geometry("1050x600")

        # create the clients dictionary

        self.clients = get_results(all_values)

        #create collaborator dictionary

        self.collaborators = get_collaborator_info(all_values)

        # Create GUI components
        self.label = tk.Label(master, text="Search Clients:")
        self.label.grid(row=0, column=0, pady=10)

        self.entry = tk.Entry(master)
        self.entry.grid(row=0, column=1, pady=10)

        self.search_button = tk.Button(
        master, text="Search", command=self.search_client)
        self.search_button.grid(row=0, column=2, pady=10)

        self.result_label = tk.Label(master, text="")
        self.result_label.grid(row=1, column=0, columnspan=3, pady=10)

        self.result_frame = tk.Frame(master)
        self.result_frame.grid(row=1, column=1, columnspan=2, pady=10)

        # Bind the Enter key to the search function
        self.entry.bind("<Return>", self.search_client)

        # Create a dropdown menu for services
        self.service_var = tk.StringVar()
        self.service_dropdown = ttk.Combobox(master, textvariable=self.service_var, values=["Outreach (Casework)", "Outreach (Immigration)", "AMP (Tutoring)", "AMP (Advocacy)"])
        self.service_dropdown.grid(row=0, column=3, pady=10)

        # Create a button to trigger the search for clients based on the selected service
        self.service_search_button = tk.Button(master, text="Select Service", command=self.search_by_service)
        self.service_search_button.grid(row=0, column=4, pady=10)

        #Create GUI components to add collaborator search function
        self.label_collaborator = tk.Label(master, text="Search Collaborators:")
        self.label_collaborator.grid(row=2, column=0, pady=10)

        self.entry_collaborator = tk.Entry(master)
        self.entry_collaborator.grid(row=2, column=1, pady=10)


        self.search_button_collaborator = tk.Button(
        master, text="Search", command=self.search_collaborators)
        self.search_button_collaborator.grid(row=2, column=2, pady=10)

        #Bind the Enter key to the collab search function
        self.entry_collaborator.bind("<Return>", self.search_collaborators)

        self.entry.focus_set()

        #Create Demographic Info Display GUI Components

      

        #Create a seperate frame for displaying the counts
        # Create a separate frame for displaying counts
        self.counts_frame = tk.Frame(master)
        self.counts_frame.grid(row=7, column=0, columnspan=3)

        # Call a function to update these labels with counts
        self.update_concise_info_labels()



    def search_client(self, event=None):
        # Get the client name entered by the user
        client_name = self.entry.get()

        #remove the previous results from display
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        # Create a new frame to hold the results
        self.result_label = tk.Frame(self.result_frame)
        self.result_label.grid(row=0, column=0, pady=10)
        
        #Create array to store the entries of every client with that name
        matching_clients = []

        #fill out the array with the matching clients (NEW)
        for client_id, clientinfo in self.clients.items():
            if 'Name' in clientinfo and clientinfo['Name'] == client_name:
                matching_clients.append(client_id)

        if matching_clients:
        # Display information for each matching client using a grid
            row_num = 0
            if len(matching_clients)==1:
                client_id = matching_clients[0]
                client_info=self.clients[client_id]
                labels = [
                ('', client_info.get('Name', '')),
                ('DOB', client_info.get('DOB', '')),
                ('Town', client_info.get('Town', ''))
                # Add other client information as needed
                ]   
                self.display_info_in_grid(client_info, labels, row_num=1)
            else:
                for client_id in matching_clients:
             # Create labels for each piece of information and place them in a grid
                    client_info=self.clients[client_id]
                    self.result_label.grid(column=0, row=row_num)
                    labels = [
                    ('', client_info.get('Name', '')),
                    ('DOB', client_info.get('DOB', '')),
                    ('Town', client_info.get('Town', ''))
                    # Add other client information as needed
                    ]   
                    self.display_info_in_grid(client_info, labels, row_num)
                    row_num += 1
            
        else:
            not_found_label = tk.Label(self.result_frame, text="Client not found.")
            not_found_label.grid(row=0, column=0)


    def display_info_in_grid(self, client_info, labels, row_num=None):
    # Function to display client information in a grid
        if row_num is None:
         row_num = self.result_frame.grid_size()[1]

         #Create a new frame for each client's information
        client_frame = tk.Frame(self.result_frame)
        client_frame.grid(column=0, row=row_num, pady=10)


    # Display a "See More" button for each client
        if client_info not in self.collaborators.values():
            see_more_button = tk.Button(
            client_frame, text="Expand", command=lambda c=client_info: self.show_more_info(c, row_num))
            see_more_button.grid(column=len(labels)+1, row=0)
        # Display other information for each client
        for col_num, (label_text, value) in enumerate(labels, start=1):
            label = tk.Label(self.result_frame, text=f"{label_text}: {value}")
            label.grid(column=col_num, row=row_num)

    def show_more_info(self, client_info, row_num):
    # Function to show more information when "See More" button is clicked

    # You can customize this to show additional details
        additional_info = f"DOB: {client_info.get('DOB', '')}\nPhone: {client_info.get('Phone', '')}\nAddress: {client_info.get('Address', '')}\nMailable Address: {client_info['Mailable Address']}\nEmail: {client_info['Email']}\nPreference: {client_info['Preference']}\nCountry of Origin: {client_info['Country of Origin']}\nLanguage: {client_info['Language']}"
        additional_info += "\nAdvocates:"
        for key, value in client_info.get('Advocates', {}).items():
            additional_info += f"{key} ({value}), "
        if additional_info:
            additional_info = additional_info.rstrip(', ')
        additional_info += "\nServices: "
        for key, value in client_info.get('Services', {}).items():
            additional_info += f"{key} ({value}), "
        if additional_info:
            additional_info = additional_info.rstrip(', ')

    # Calculate the position for the additional information frame
        x_position = self.result_frame.winfo_rootx() + self.result_frame.winfo_width()
        y_position = self.result_frame.winfo_rooty() + row_num * 25  # Adjust the multiplier based on your layout

    # Create a new top-level window for each client's additional information
        additional_info_window = tk.Toplevel(self.master)
        additional_info_window.geometry(f"+{x_position}+{y_position}")

        additional_info_label = tk.Label(additional_info_window, text=additional_info)
        additional_info_label.pack()
    def search_by_service(self):
        # Get the selected service from the dropdown menu
        selected_service = self.service_var.get()
        service_label = selected_service
        if selected_service == "AMP (Tutoring)":
            service_label = selected_service
            selected_service = "Academic Mentoring Program (Tutoring)"
        if selected_service == "AMP (Advocacy)":
            service_label = selected_service
            selected_service = "Academic Mentoring Program (Advocacy)"

        # Remove all widgets from the result frame
        for widget in self.result_frame.winfo_children():
            widget.grid_forget()


        # Create a list of clients who have received the selected service
        matching_clients = [client_id for client_id, client_info in self.clients.items() if selected_service in client_info['Services']]


        # Sort clients based on the number of times the service has been received (descending order)
        matching_clients.sort(key=lambda client_id: self.clients[client_id]['Services'].get(selected_service, 0), reverse=True)

        row_num = 0
        for client_id in matching_clients:
            client_info = self.clients[client_id]
            # Display other information for each client
            labels = [
            ('', client_info.get('Name', '')),
            ('DOB', client_info.get('DOB', '')),
            ('Town', client_info.get('Town', '')),
            (f'{service_label} Count', client_info['Services'][selected_service])
            # Add other client information as needed
            ]
            self.display_info_in_grid(client_info, labels, row_num)
            row_num += 1

    def search_collaborators(self, event=None):
        #get the collaborator name entered by the user
        collaborator = self.entry_collaborator.get()

        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        #create a new frame to hold the results
        self.result_label = tk.Frame(self.result_frame)
        self.result_label.grid(row=0, column=0, pady= 10)

        #create array to store the entries of every collaboration with that collaborator
        matching_collaborators = []


        #fill out the array with the matching collaborators
        for collab_id, collabinfo in self.collaborators.items():
            if 'Collaborator' in collabinfo and collabinfo['Collaborator']==collaborator:
                matching_collaborators.append(collab_id)
        if matching_collaborators:
            #Display information for each matching collaboration using a grid
            row_num = 0
            if len(matching_collaborators)==1:
                collab_id = matching_collaborators[0]
                collab_info = self.collaborators[collab_id]
                labels = [
                    ('Collaborator', collab_info.get('Collaborator', "")),
                    ('Date', collab_info.get('Date', "")),
                    ('Location', collab_info.get('Location', "")),
                    ('Hours', collab_info.get('Hours', ""))
                ]
                self.display_info_in_grid(collab_info, labels, row_num=1)
            else:
                for collab_id in matching_collaborators:
                    collab_info=self.collaborators[collab_id]
                    self.result_label.grid(column=0, row=row_num)
                    labels = [
                    ('Collaborator', collab_info.get('Collaborator', '')),
                    ('Date', collab_info.get('Date', '')),
                    ('Location', collab_info.get('Location', '')),
                    ('Hours', collab_info.get('Hours', ''))
                    # Add other client information as needed
                    ]   
                    self.display_info_in_grid(collab_info, labels, row_num)
                    row_num += 1

        else:
            not_found_label = tk.Label(self.result_frame, text="Collaborator not found.")
            not_found_label.grid(row=0, column=0)
    
    def count_clients_by_category(self, category_key):
        distinct_values = set(client_info.get(category_key, '') for client_info in self.clients.values())
        return {value:sum(1 for client_info in self.clients.values() if client_info.get(category_key)==value) for value in distinct_values}
    
    def update_concise_info_labels(self):
        town_counts = self.count_clients_by_category('Town')
        language_counts = self.count_clients_by_category('Language')
        country_counts = self.count_clients_by_category('Country of Origin')

    # Display counts in columns
        self.display_counts_in_column(town_counts, column=0)
        self.display_counts_in_column(language_counts, column=1)
        self.display_counts_in_column(country_counts, column=2)

    def display_counts_in_column(self, counts, column):

    # Add new content
        # Add new content to the counts frame
        row_num = 0
        for value, count in counts.items():
            tk.Label(self.counts_frame, text=f"{value}: {count}").grid(row=row_num, column=column, sticky='w', padx=5)
            row_num += 1

def main():
    root = tk.Tk()
    app = ClientSearchApp(root)
    root.mainloop()


SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


def get_executable_directory():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))


""" def authenticate(credentials_file='credentials.json', token_file='token.json'):
    # The file token.json stores the user's access and refresh tokens, and is created automatically when the
    # authorization flow completes for the first time.
    credentials_path = os.path.join(get_executable_directory(), credentials_file)

    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(os.path.join(get_executable_directory(), 'credentials.json'), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(os.path.join(get_executable_directory(), 'token.json'), 'w') as token:
            token.write(creds.to_json())

    return creds """

def authenticate():
    # Define the path to the credentials.json file on the desktop
    desktop_path = os.path.expanduser("~/Desktop")
    credentials_path = os.path.join(desktop_path, "credentials.json")

    # The file token.json stores the user's access and refresh tokens and is created automatically when the
    # authorization flow completes for the first time.
    creds = None
    token_path = os.path.join(desktop_path, 'token.json')

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Adjust the path to the credentials.json file
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return creds



# Call this function to obtain credentials
credentials = authenticate()


# Create a Google Sheets API service
service = build('sheets', 'v4', credentials=credentials)


# Specify the spreadsheet ID and range
spreadsheet_id = "1SA1UuObM1NoD5REy1R4ngnIofMz7JoQjD-CHNBN6osY"

# Get spreadsheet information
spreadsheet_info = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()

# Extract sheet names from the spreadsheet information
sheet_names = [sheet['properties']['title'] for sheet in spreadsheet_info['sheets']]

all_values = []

for sheet_name in sheet_names:
    range_name = f"{sheet_name}!A1:ZZ100"
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    sheet_values = result.get('values', [])
    
    # Append the values from the current sheet to the overall list
    all_values.extend(sheet_values)

range_name = 'Responses1!A1:ZZ100'  # Update with the actual sheet name or range

""" # Retrieve values from the spreadsheet
result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
values = result.get('values', []) """

def get_results(values):
#Builds the client search dictionary from the google sheets responses

    # Assuming the first row contains headers
    headers = values[0]
    data = values[1:]



    # Create a dictionary to store the results
    result_dict = {}

    # Iterate through the rows
    for row in data:
     if len(row) < headers.index("Choose form type:"):
         continue
     if row[headers.index("Choose form type:")] == "New Client Intake":
        # Assuming the name is in the first column
        name = row[headers.index("Client's name")]
        DOB = row[headers.index("Client's Date of Birth:")]
        dob_date = datetime.strptime(DOB, "%m/%d/%Y")
        client_id = f"{name}_{dob_date.strftime('%m%d%Y')}"

        # Create a dictionary for the current response
        response_dict = {
        'Name': row[headers.index("Client's name")],
        'DOB': row[headers.index("Client's Date of Birth:")],
        'Age': row[headers.index("Client's Age:")],
        'Address': row[headers.index("Client's Address:")],
        'Mailable Address': row[headers.index("Can the Client receive mail at this address? (If not, please specify mailing address)")],
        'Town': row[headers.index("Town/Village")],
        'Phone': row[headers.index("Client's Phone Number:")],
        'Preference': row[headers.index("What is the Client's preferred mode of communication? (If other, please specify contact information)")],
        'Email': row[headers.index("Client's Email")],
        'Country of Origin': row[headers.index("Client's Country of Origin")],
        'Language': row[headers.index("Client's Preferred Language ")],
        'Advocates': {row[headers.index("Advocate's Name")]: 0},
        'Services': {}}
        # Add more fields as needed
        # Add the response dictionary to the main result dictionary
        result_dict[client_id] = response_dict
    
    
     if row[headers.index("Choose form type:")] == "New AMP/Outreach Entry":
        #Add to the client's existing entry to update the advocate count and service count
        name = row[headers.index("Client's Name:")]
        DOB = row[headers.index("Client's Date of Birth")]
        dob_date = datetime.strptime(DOB, "%m/%d/%Y")
        client_id = f"{name}_{dob_date.strftime('%m%d%Y')}"
        if client_id not in result_dict.keys():
            continue
        client_dict = result_dict[client_id]
        advocate = row[headers.index("Advocate's Name:")]
        service = row[headers.index("Service Type:")]
        if advocate in client_dict['Advocates'].keys():
            client_dict['Advocates'][advocate] += 1
        else:
            client_dict["Advocates"][advocate] = 1

        if service in client_dict['Services'].keys():
            client_dict['Services'][service] += 1
        else:
            client_dict['Services'][service] = 1

     if row[headers.index("Choose form type:")] == "New Food Distribution Entry":
         continue
         

    return result_dict

def get_collaborator_info(values):
    #Builds the client search dictionary from the google sheets responses

    # Assuming the first row contains headers
    headers = values[0]
    data = values[1:]

    # Create a dictionary to store the results
    result_dict = {}

    for row in data:
        if len(row) < headers.index("Choose form type:"):
         continue
        if row[headers.index("Choose form type:")] == "New Collaboration Entry":
            collaborator = row[headers.index('Collaborator')]
            collab_date = row[headers.index('Date of Collaboration')]
            collabdate = datetime.strptime(collab_date, "%m/%d/%Y")
            collab_id = f"{collaborator}_{collabdate.strftime('%m%d%Y')}"
            response_dict = {
                'Collaborator': collaborator,
                'Location': row[headers.index('Location of Collaboration')],
                'Date': collab_date,
                'Hours': row[headers.index('Hours of Collaboration')]
            }
            result_dict[collab_id] = response_dict
    return result_dict

        


    


if __name__ == "__main__":
    main()
