import tkinter as tk
from tkinter import Toplevel, ttk, messagebox, font, Menu
import smartsheet
import codecs
from configparser import ConfigParser
import os
from symspellpy import SymSpell, Verbosity
import json
import time
import webbrowser
import re
import sys

#SE Geneator Test sheet ID = 2320617425921924
#Smartsheet token = V3fXgr7Mlyo1ORkTq1pkG2OHc5x0O6a1m5mS7

#Set our network folder for the dictionary that will be static
jcc_network_drive_folder = "S:/All Technical & Support Files/Dictionaries/SEGeneratorDictionary.json"
home_network_drive_folder = "/Volumes/home/Dictionaries/SEGeneratorDictionary.json"
corp_network_folder = "C:/Users/cbrichardson/Documents/SEGeneratorDictionary.json"

# Initialize SymSpell library for spellchecking and set dictionary path to use
sym_spell = SymSpell(max_dictionary_edit_distance=3, prefix_length=7)
frequency_count = 10000
correction_dictionary_path = "S:/All Technical & Support Files/Dictionaries/dictionaryupdates.json"

#test

#open dictionary file
with open(jcc_network_drive_folder, 'r') as dictionary_file:
    dictionary_data = json.load(dictionary_file)

for word, count in dictionary_data.items():
    sym_spell.create_dictionary_entry(word, count)

#Set the icon of our application window
def window_icon():
    global image
    if getattr(sys, 'frozen', False):
        image = tk.PhotoImage(file=os.path.join(sys._MEIPASS, "files/jh.png"))
        return image
    else:
        image = tk.PhotoImage(file="C:\\Users\\cbrichardson\\Documents\\GitHub\\Service-Event-Generator\\jh.png")
        return image


# - Function to translate an rgb tuple of int to a tkinter friendly color code - #
def _from_rgb(rgb):
    return '#%02x%02x%02x' % rgb  


#handle options within the Spell Check pop up window
def handle_options(word: str, suggestions):
    #lowercase the word and start a new spell check window with the word, wait for an option to be selected
    word = word.lower()
    dialog = SpellCheckDialog(root, word, suggestions)
    root.wait_window(dialog)

    if dialog.result[0] == "correct":
        apply_correction(word, dialog.result[1])
    elif dialog.result[0] == "add":

        # Step 2: Check if the word exists in the dictionary and update the value as needed
        if word in dictionary_data:
            dictionary_data[word] += frequency_count
        else:
            dictionary_data[word] = frequency_count

        # Step 3: Write the updated dictionary back to the JSON file
        with open(correction_dictionary_path, "w") as f:
            json.dump(dictionary_data, f, indent=4)

#Function to apply the corrected word to the text entry
def apply_correction(word, corrected_word):
    text = MainApplication.reason_entry.get("1.0", tk.END)
    MainApplication.reason_entry.delete("1.0", tk.END)

    # Check if the word is the first word in the text entry
    first_word = text.split()[0]
    if first_word.lower() == word.lower():
        corrected_word = corrected_word.capitalize()

    # Replace the word while preserving the capitalization of the original word
    words = text.split()
    for i, w in enumerate(words):
        if w.lower() == word.lower():
            words[i] = corrected_word

    #add the corrected words and insert in to the reason for calling box
    corrected_text = ' '.join(words)
    MainApplication.reason_entry.insert("1.0", corrected_text)
    MainApplication.combine_text(MainApplication)

#main spellcheck function, will add suggestions to a list
def spellcheck():
    text = MainApplication.reason_entry.get("1.0", tk.END).strip()
    misspelled_words = 0
    # Split the text into words while ignoring punctuation
    words = re.findall(r'\b\w+\b', text)

    misspelled = []
    for word in words:
        suggestions = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=3)
        first_three_suggestions = [suggestion.term for suggestion in suggestions[:3]]
        first_three_suggestions_capitalized = [suggestion.capitalize() for suggestion in first_three_suggestions]

        if word not in first_three_suggestions and word not in first_three_suggestions_capitalized:
            misspelled.append((word, first_three_suggestions))
            misspelled_words = 1

    for word, suggestions in misspelled:
        handle_options(word, suggestions)
    if misspelled_words == 1:
        return
    elif misspelled_words == 0:
        messagebox.showinfo("Attention", "No misspelled words were found")

#check if text has changed and if so call the update to find new misspelled words
def on_text_changed(event):
    if MainApplication.reason_entry.after_id is not None:
        MainApplication.reason_entry.after_cancel(MainApplication.reason_entry.after_id)
    MainApplication.reason_entry.after_id = MainApplication.reason_entry.after(1000, update_misspelled_tags)

#When text entry is updated this function will be called to re-evaluate misspellings
def update_misspelled_tags(corrected_word=None):
    if corrected_word:
        index = MainApplication.reason_entry.search(corrected_word, "1.0", stopindex=tk.END)
        if index:
            end_index = MainApplication.reason_entry.index(f"{index} + {len(corrected_word)}c")
            MainApplication.reason_entry.tag_remove("misspelled", index, end_index)

    text = MainApplication.reason_entry.get("1.0", tk.END).strip()
    words = re.findall(r'\b\w+\b', text)

    for i, word in enumerate(words):
        # If the word is the corrected word, skip checking it
        if word == corrected_word:
            continue

        suggestions = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)


        if suggestions:
            # Check if the word is equal to any of the first three suggestions
            first_three_suggestions = [suggestion.term for suggestion in suggestions[:3]]
            first_three_suggestions_capitalized = [suggestion.capitalize() for suggestion in first_three_suggestions]

            if word not in first_three_suggestions and word not in first_three_suggestions_capitalized:
                # Check if the first character of the original word is uppercase and if the suggested word is lowercase
                suggested_word = suggestions[0].term
                if word[0].isupper() and suggested_word[0].islower():
                    suggested_word = suggested_word.capitalize()

                if suggested_word != word:
                    index = MainApplication.reason_entry.search(word, "1.0", stopindex=tk.END)
                    if index:
                        end_index = MainApplication.reason_entry.index(f"{index} + {len(word)}c")
                        MainApplication.reason_entry.tag_add("misspelled", index, end_index)

#on a right click this function creates a context menu with the suggested spellings of the word
def on_right_click(event):
    MainApplication.reason_entry.focus()
    index = MainApplication.reason_entry.index(f"@{event.x},{event.y}")
    clicked_word_start = MainApplication.reason_entry.index(f"{index} wordstart")
    clicked_word_end = MainApplication.reason_entry.index(f"{index} wordend")
    clicked_word = MainApplication.reason_entry.get(clicked_word_start, clicked_word_end)
    suggestions = sym_spell.lookup(clicked_word, Verbosity.CLOSEST, max_edit_distance=2)

    if suggestions:
        context_menu = Menu(MainApplication.reason_entry, tearoff=0)
        context_menu.add_command(label="Suggested Spellings")   
        for suggestion in suggestions:
            context_menu.add_command(
            label=suggestion.term,
            command=lambda term=suggestion.term: replace_clicked_word(clicked_word, term))

        context_menu.post(event.x_root, event.y_root)

#will replace the right clicked word with the selected word from the context menu
def replace_clicked_word(original_word, replacement_word):
    text = MainApplication.reason_entry.get("1.0", tk.END)
    MainApplication.reason_entry.delete("1.0", tk.END)

    # Check if the word is the first word in the text entry
    first_word = text.split()[0]
    if first_word.lower() == original_word.lower():
        replacement_word = replacement_word.capitalize()

    # Replace the word while preserving the capitalization of the original word
    words = text.split()
    for i, w in enumerate(words):
        if w.lower() == original_word.lower():
            words[i] = replacement_word

    corrected_text = ' '.join(words)
    MainApplication.reason_entry.insert("1.0", corrected_text)

    # Update the misspelled tags after replacing the word
    update_misspelled_tags(replacement_word)
    MainApplication.combine_text(MainApplication)

#request settings from the agent if no settings file is found
def request_initial_settings(self):
    config=ConfigParser()
    
    # Define the main section name
    main_section = 'main'
    
    if os.path.exists('ServiceEventGeneratorSettings.ini'):
        ini_file_path = os.path.abspath("ServiceEventGeneratorSettings.ini")
        #config.read("config.ini")
        with codecs.open(ini_file_path, 'r', encoding='utf-8-sig') as f:
            config.read_file(f)
        if config.has_option(main_section, 'welcome_message'):
            pass
        # Check if the main section contains the 'agent type' key
        if config.has_option(main_section, 'agent_type'):
            agent_type = config.get(main_section, 'agent_type')
            AgentSettings.agentType.set(agent_type)
            if agent_type == 'Credit Union':
                MainApplication.customer_name_label.config(text='Member Name:*')
                MainApplication.accountnum_label.config(text="Member #")
            elif agent_type == 'Bank':
                MainApplication.customer_name_label.config(text='Customer Name:*')
                MainApplication.accountnum_label.config(text="Account #")
        if config.has_option(main_section, 'extension'):
            ext = config.get('main', 'extension')
            AgentSettings.extension.set(ext)
        
        else:
            settings_request_window = tk.Toplevel(root)
            settings_request_window.attributes('-topmost', True)
            settings_request_window.iconphoto(False, image)
            settings_request_window.winfo_toplevel().title("Agent Setting")
            settings_request_window.configure(bg=jhblue)
            settings_request_window.geometry('300x200')
            settings_request_window.protocol("WM_DELETE_WINDOW", lambda: AgentSettings.on_closing(AgentSettings))
            AgentSettings.extension = tk.StringVar()
            AgentSettings.agentType = tk.StringVar()
            info = tk.Label(settings_request_window, text= "Please enter your extension and set your agent type", font=('Poppins 12'), bg=jhblue, fg="white", wraplength=280)
            extensionEntry = tk.Entry(settings_request_window, textvariable=AgentSettings.extension, width=5, font=("Poppins 12"))
            extension_label = tk.Label(settings_request_window, text= "Extension:", font=('Poppins 12'), bg=jhblue, fg="white")
            bank_agentType = tk.Radiobutton(settings_request_window, variable=AgentSettings.agentType, value = "Bank", bg = jhblue, indicatoron=1)
            bank_agent_label = tk.Label(settings_request_window, text= "Bank Agent", font=('Poppins 12'), bg=jhblue, fg="white")
            cu_agentType = tk.Radiobutton(settings_request_window, variable=AgentSettings.agentType, value = "Credit Union", bg = jhblue, indicatoron=1)
            cu_agent_label = tk.Label(settings_request_window, text= "CU Agent", font=('Poppins 12'), bg=jhblue, fg="white")
            save = tk.Button(settings_request_window, text="Save", command = lambda: AgentSettings.save_settings(AgentSettings, settings_request_window))
            info.place(x=20,y=5)
            extensionEntry.place(x=115, y=68, height=25)
            extension_label.place(x=25, y=67)
            bank_agentType.place(x=30, y=110, width=20, height=20)
            cu_agentType.place(x=165, y=110, width=20, height=20)
            bank_agent_label.place(x=50, y=105)
            cu_agent_label.place(x=185, y=105)
            save.place(x=115,y=145)
            if AgentSettings.agentType.get() == 'Credit Union':
                MainApplication.customer_name_label.config(text='Member Name:*')
                MainApplication.accountnum_label.config(text="Member #")

            elif AgentSettings.agentType.get() == 'Bank':
                MainApplication.customer_name_label.config(text='Customer Name:*')
                MainApplication.accountnum_label.config(text="Account #")

#show a welcome message
def welcome_message(setting):
    config = ConfigParser()
    ini_file_path = os.path.abspath("ServiceEventGeneratorSettings.ini")
    welcome_message_status = tk.IntVar()

    if os.path.exists(ini_file_path):
        with open(ini_file_path, 'r', encoding='utf-8-sig') as f:
            config.read_file(f)
        if setting == 1:
            pass
        elif config.has_section('main'):
            if config.get('main', 'welcome message') == 'no':
                return
            
    def close_window():
        if setting == 1:
            if welcome_message_status.get() == 1:
                with open(ini_file_path, 'w') as f:
                    config.set('main', 'welcome message', 'yes')
                    config.write(f)
            welcome_message_window.destroy()
        else:
            if config.has_section('main'):
                pass
            else:
                config.add_section('main')
            if welcome_message_status.get() == 1:
                with open(ini_file_path, 'w') as f:
                    config.set('main', 'welcome message', 'yes')
                    config.write(f)
            elif welcome_message_status.get() == 0:
                with open(ini_file_path, 'w') as f:
                    config.set('main', 'welcome message', 'no')
                    config.write(f)
            welcome_message_window.destroy()
            request_initial_settings(AgentSettings)

    welcome_message_window = tk.Toplevel(root)
    welcome_message_window.attributes('-topmost', True)
    welcome_message_window.winfo_toplevel().title("Welcome")
    welcome_message_window.configure(bg=jhblue)
    welcome_message_window.geometry('600x785')
    welcome_message_window.iconphoto(False, image)

    welcome_message_label = tk.Label(welcome_message_window, text="Welcome to the Service Event Generator! The purpose of this program is to give you, the agent, an easy to use tool that can automatically format a Service Event with the information you provide in the input fields. All of the features found in the previous version have been implemented in this version, as well as a few new improvements: Spellcheck and Send Event. The Spellcheck feature will look at the Reason for Calling field (the second to last field) and alert you to any misspelled words for correction. It will also highlight any misspelled words in red that you can right click to quickly correct without launching the full dialog via the Spellcheck button. The Send Event button will be used when the Synapsys Plugin in Call Center does not load. It will automatically enter the event in to Smartsheet for a ResQ agent to submit for you. This feature does have safeguards in place to ensure you do not enter duplicate events and it will also refer you to enter a tech error form if you use it. Please enjoy using this program and if you have any issues report them to your supervisor who will direct them to the appropriate parties.", wraplength=575, bg=jhblue, fg='white', font="Poppins 14")
    welcome_message_label.place(x=10, y=5)
    
    welcome_checkbutton = tk.Checkbutton(welcome_message_window, font="Poppins 12", variable=welcome_message_status, bg=jhblue)
    welcome_checkbutton.place(x=145, y=685)
    welcome_checkbutton_label = tk.Label(welcome_message_window, font="Poppins 12", bg=jhblue, fg='white', text="Show welcome message on startup")
    welcome_checkbutton_label.place(x = 165, y = 688)
    welcome_button = tk.Button(welcome_message_window, font="Poppins 12", text="Let's go!", command=close_window)
    welcome_button.place(x=240, y=730)

#Configure name and reference number labels depending on what agent type is set to if there is a settings file already
def check_settings():
    config = ConfigParser()
    if os.path.exists('ServiceEventGeneratorSettings.ini'):
        ini_file_path = os.path.abspath("ServiceEventGeneratorSettings.ini")
        with codecs.open(ini_file_path, 'r', encoding='utf-8-sig') as f:
            config.read_file(f)
        
        agentType = config.get('main', 'agent_type')
        if agentType == 'Credit Union':
            MainApplication.customer_name_label.config(text='Member Name:*')
            MainApplication.accountnum_label.config(text="Member #")

        elif agentType == 'Bank':
            MainApplication.customer_name_label.config(text='Customer Name:*')
            MainApplication.accountnum_label.config(text="Account #")
        AgentSettings.agentType = agentType
        
# - Colors used for programs color scheme - #
jhblue = _from_rgb((26, 54, 104))
highlight = _from_rgb((104, 226, 255))

#Smartsheet API token
api_token = 'V3fXgr7Mlyo1ORkTq1pkG2OHc5x0O6a1m5mS7'


# - Main GUI class and functions - #
class MainApplication(tk.Frame):

    # - Initialize the GUI - #
    def __init__(self, master, SE_smartsheet, *args, **kwargs):
        self.master = master
        self.sheet_id = 2320617425921924
        tk.Frame.__init__(self, self.master, *args, **kwargs)
        SE_smartsheet = SE_smartsheet
        MainApplication._instance_counter = 0
        MainApplication._last_radio_value = str("Phone")
        self.check_debit_card_digits_cmd = (self.register(self.restrict_debit_card_field))
        self.configure_gui()
        self.create_strings()
        self.create_labels()
        self.create_field_entries()
        self.create_radiobuttons()
        self.create_scrollbars()
        self.create_text_entries()
        self.create_buttons()
        self.create_configs()
        self.configure_element_placement()
        self.create_bindings()
        self.combined_text = ''
        self.labelFont = font.nametofont('TkDefaultFont')
        self.labelFont.configure(family = 'Poppins', size = 12)
        MainApplication.reason_entry.after_id = None
        

    # - GUI Setup Functions - #
    def configure_gui(self):
        self.winfo_toplevel().title("Service Event Generator")
        self.master.configure(bg = jhblue)
        self.master.geometry('475x820')
        self.master.iconphoto(False, image)
        self.master.option_add('*tearOff', False)
    
    def create_strings(self):
        MainApplication.customer_name = tk.StringVar()
        MainApplication.reference_radio_value = tk.StringVar(value="Account #")
        MainApplication.reference_number = tk.StringVar()
        MainApplication.contact_radio_value = tk.StringVar(value="Phone #")
        MainApplication.contact_info = tk.StringVar()
        MainApplication.debit_card_number = tk.StringVar()
        MainApplication.transactions = tk.StringVar()
        MainApplication.clearundobtntxt = tk.StringVar()
        MainApplication.combined_text = tk.StringVar()
        MainApplication.phonecopy = str('')
        MainApplication.emailcopy = str('')
        MainApplication.bothcopy = str('')
        
    def create_labels(self):
        self.app_label = tk.Label(root, bg = jhblue, fg = 'white', text = "Service Event Generator", font = "Poppins 12")
        MainApplication.customer_name_label = tk.Label(root, bg = jhblue, fg = 'white', text = "Customer Name*:")
        self.customer_name_copy = tk.Label(root, bg = jhblue, fg = highlight, font = "Poppins 12 underline", text = "Copy", cursor = 'hand2')
        self.reference_number_label = tk.Label(root, bg = jhblue, fg = 'white', text = "Reference Number*:", font = ('Poppins', 30))
        MainApplication.accountnum_label = tk.Label(root, bg = jhblue, fg = 'white', text = "Account #")
        self.netteller_id_label = tk.Label(root, bg = jhblue, fg = 'white', text = "Netteller ID", font = ('Poppins', 12))
        self.reference_number_copy = tk.Label(root, bg = jhblue, fg = highlight,font = "Poppins 12 underline", text = "Copy", cursor = 'hand2')
        self.contact_info_label = tk.Label(root, bg = jhblue, fg = 'white', text = "Contact Info*:")
        self.phone_num_label = tk.Label(root, bg = jhblue, fg = 'white', text = "Phone #")
        self.email_address_label = tk.Label(root, bg = jhblue, fg = 'white', text = "Email Address")
        self.both_label = tk.Label(root, bg = jhblue, fg = 'white', text = "Both")
        self.contact_info_copy = tk.Label(root, bg = jhblue, fg = highlight, font = "Poppins 12 underline", text = "Copy", cursor = 'hand2')
        self.debit_card_number_label = tk.Label(root, bg = jhblue, fg = 'white', text = "Last 4 Digits of Debit Card:")
        self.transactions_label = tk.Label(root, bg = jhblue, fg = 'white', text = "Transactions (Date, Amount, and Merchant):")
        self.reason_label = tk.Label(root, bg = jhblue, fg = 'white', text = "Reason for Calling*:")
        self.reason_copy = tk.Label(root, bg = jhblue, fg = highlight, text = "Copy", font = "Poppins 12 underline", cursor = 'hand2')
        self.required_label = tk.Label(root, bg = jhblue, fg = 'white', font = ('Poppins.Italicized', 10), text = "* Required field for any Service Events going back to the Financial Institution")
        self.copypaste_label = tk.Label(root, bg = jhblue, fg = 'white', font = ('Poppins', 12), text = "Copy and paste to Synapsys")
        
    def create_field_entries(self):
        self.customer_name_entry = tk.Entry(root, textvariable = self.customer_name, width = 30, font = ('Poppins', 14))
        self.reference_number_entry = tk.Entry(root, width = 30, textvariable = self.reference_number, font = ('Poppins', 14))
        self.contact_info_entry = tk.Entry(root, textvariable = self.contact_info, validate = 'all', width = 30, font = ('Poppins', 14))
        self.debit_card_number_entry = tk.Entry(root, textvariable = self.debit_card_number, validate = 'all', validatecommand = (self.check_debit_card_digits_cmd, '%P'), width = 30, font = ('Poppins', 14))
        
    def create_radiobuttons(self):
        MainApplication.account_radio_button = tk.Radiobutton(root, variable = self.reference_radio_value, value = "Account #", bg = jhblue, indicatoron = 1)
        self.netteller_radio_button = tk.Radiobutton(root, variable = self.reference_radio_value, value = "Netteller ID", bg = jhblue, indicatoron = 1)
        self.phone_radio_button = tk.Radiobutton(root, variable = self.contact_radio_value, value = "Phone #", bg = jhblue, indicatoron = 1, command = self.radiobutton_wrapper)
        self.email_radio_button = tk.Radiobutton(root, variable = self.contact_radio_value, value = "Email Address", bg = jhblue, indicatoron = 1, command = self.radiobutton_wrapper)
        self.both_radio_button = tk.Radiobutton(root, variable = self.contact_radio_value, value = "Both", bg = jhblue, indicatoron = 1, command = self.radiobutton_wrapper)

    def create_scrollbars(self): 
        self.transaction_scrollbar = tk.Scrollbar(root, orient = 'vertical')
        self.reason_scrollbar = tk.Scrollbar(root, orient = 'vertical')
        self.event_scrollbar = tk.Scrollbar(root, orient = 'vertical')
       
    def create_text_entries(self):
        MainApplication.transactions_entry = tk.Text(root, width = 43, font = ('Poppins', 10), wrap = 'word', yscrollcommand = self.transaction_scrollbar.set)
        MainApplication.reason_entry = tk.Text(root, width = 43, font = ('Poppins', 10), wrap = 'word', yscrollcommand = self.reason_scrollbar.set)
        MainApplication.event_entry = tk.Text(root, width = 54, height = 5, font = ('Poppins', 10), wrap = 'word', yscrollcommand = self.event_scrollbar.set)
 
    def create_buttons(self):
        self.event_copy = tk.Button(root, text = "Copy text", font = ('Poppins', 12), fg = jhblue)
        self.event_clear_undo = tk.Button(root, textvariable = self.clearundobtntxt, font = ('Poppins', 12), fg = jhblue, command = ClearUndo)
        self.spellcheck_event = tk.Button(root, text = "Spellcheck", font = ('Poppins', 12), fg = jhblue, command=spellcheck)
        self.send_event = tk.Button(root, text = "Send Event", font = ('Poppins', 12), fg = jhblue, command= lambda: SE_smartsheet.smartsheet_event_options(SE_smartsheet, self.sheet_id))
        
    def create_configs(self):
        self.app_label.config(font = ('Poppins, 20'))
        self.customer_name_label.config(font = ('Poppins', 12))
        self.reference_number_label.config(font = ('Poppins', 12))
        self.contact_info_label.config(font = ('Poppins', 12))
        self.debit_card_number_label.config(font = ('Poppins', 12))
        self.transactions_label.config(font = ('Poppins', 12))
        self.transaction_scrollbar.config(command = self.transactions_entry.yview)
        self.reason_label.config(font = ('Poppins', 12))
        self.reason_scrollbar.config(command = self.reason_entry.yview)
        self.event_scrollbar.config(command = self.event_entry.yview)
        self.clearundobtntxt.set("Clear Text")
        
    def configure_element_placement(self):
        self.app_label.place(x = 50, y = 5)
        self.customer_name_label.place(x = 50, y = 50)
        self.customer_name_entry.place(x = 50, y = 75, height = 28)
        self.customer_name_copy.place(x = 365, y = 45)
        self.reference_number_label.place(x = 50, y = 110)
        self.account_radio_button.place(x = 50, y = 138, width = 20, height = 20) 
        self.accountnum_label.place(x = 62, y = 133)
        self.accountnum_label.lift()
        self.netteller_id_label.lift()
        self.phone_num_label.lift()
        self.email_address_label.lift()
        self.both_label.lift()
        self.contact_info_entry.lift()
        self.reference_number_entry.lift()
        self.netteller_id_label.place(x = 212, y = 132)
        self.netteller_radio_button.place(x = 200, y = 138, width = 20, height = 20)
        self.reference_number_copy.place(x = 365, y = 130)
        self.reference_number_entry.place(x = 50, y = 160, height = 28)
        self.contact_info_label.place(x = 50, y = 190)
        self.phone_num_label.place(x = 62, y = 212)
        self.phone_radio_button.place(x = 50, y = 218, width = 20, height = 20)
        self.email_address_label.place(x = 162, y = 212)
        self.email_radio_button.place(x = 150, y = 218, width = 20, height = 20)
        self.both_label.place(x = 307, y = 212)
        self.both_radio_button.place(x = 295, y = 218, width = 20, height = 20)
        self.contact_info_copy.place(x = 365, y = 210)
        self.contact_info_entry.place(x = 50, y = 240, height = 28)
        self.debit_card_number_label.place(x = 50, y = 273)
        self.debit_card_number_entry.place(x = 50, y = 300, height = 28)
        self.transactions_label.place(x = 50, y = 328)
        self.transactions_entry.place(x = 50, y = 355, height = 70)
        self.transaction_scrollbar.place(x = 399, y = 355, height = 70)
        self.reason_label.place(x = 50, y = 428)
        self.reason_entry.place(x = 50, y = 455, height = 100)
        self.reason_scrollbar.place(x = 399, y = 455, height = 100)
        self.reason_copy.place(x = 365, y = 425)
        self.required_label.place(x = 5, y = 565)
        self.copypaste_label.place(x = 5, y = 585)
        self.event_entry.place(x = 10, y = 610)
        self.event_scrollbar.place(x = 447, y = 610, height = 119)
        self.event_copy.place(x = 10, y = 735, height = 60, width = 105)
        self.event_clear_undo.place(x = 127, y = 735, height = 60, width = 105)
        self.spellcheck_event.place(x = 243, y = 735, height = 60, width = 105)
        self.send_event.place(x = 360, y = 735, height = 60, width = 105)
           
    def create_bindings(self):
        self.customer_name_copy.bind("<Button-1>", lambda event: self.copy_to_clipboard(None, self.customer_name.get(), "Customer Name"))
        self.reference_number_copy.bind("<Button-1>", lambda event: self.copy_to_clipboard(None, self.reference_number.get(), "Reference Number"))
        self.contact_info_copy.bind("<Button-1>", lambda event: self.copy_to_clipboard(None, self.contact_info.get(), "Contact Info"))
        self.debit_card_number_entry.bind("<FocusOut>", self.check_debit_card)
        self.reason_copy.bind("<Button-1>", lambda event: self.copy_to_clipboard(None, self.reason_entry.get("1.0", tk.END), "Reason for Calling"))
        self.event_copy.bind("<Button-1>", lambda event: self.copy_to_clipboard(None, self.event_entry.get("1.0", tk.END), "Synapsys Event"))
        self.contact_info_entry.bind("<KeyRelease>", lambda event: [self.format_phone_number(self.contact_info_entry.get()), self.combine_text(None)])
        self.customer_name_entry.bind("<KeyRelease>", lambda event: self.combine_text(None))
        self.reference_number_entry.bind("<KeyRelease>", lambda event: self.combine_text(None))
        self.debit_card_number_entry.bind("<KeyRelease>", lambda event: self.combine_text(None))
        self.transactions_entry.bind("<KeyRelease>", lambda event: self.combine_text(None))
        self.reason_entry.bind("<KeyRelease>", lambda event: self.entry_wrapper(None))
        self.reason_entry.bind("<ButtonRelease-3>", on_right_click)
        self.reason_entry.tag_configure("misspelled", foreground="red", underline=True)
        self.widgets = [self.customer_name_entry, self.reference_number_entry, self.contact_info_entry, self.debit_card_number_entry, MainApplication.transactions_entry, MainApplication.reason_entry, MainApplication.event_entry]
        for i, widget in enumerate(self.widgets):
            widget.bind('<Tab>', lambda e, i=i: self.focus_next(self.widgets, i, e))

            self.customer_name_entry.focus_set()  # Set initial focus to the first entry field
        for i, widget in enumerate(self.widgets):
            widget.bind('<Shift-Tab>', lambda e, i=i: self.focus_prev(self.widgets, i, e))

            self.customer_name_entry.focus_set()  # Set initial focus to the first entry field

# - Operation Functions - ##  

    def focus_next(self, widgets, current_index, event = None):
        next_index = (current_index + 1) % len(widgets)
        widgets[next_index].focus_set()
        return 'break'
    
    def focus_prev(self, widgets, current_index, event = None):
        next_index = (current_index - 1) % len(widgets)
        widgets[next_index].focus_set()
        return 'break'

    def entry_wrapper(self, event = None):
        self.combine_text(None)
        on_text_changed(None)

    def radiobutton_wrapper(self):
        #This is a wrapper function so that the combined text updates if one of the contact radio buttons is selected and no text updated
        self.contact_update()
        self.combine_text()

    #Check the debit card number to be 4 digits or allow if it there is nothing in the field, otherwise show a warning        
    def check_debit_card(self, event):
        #check if the debit card is valid
        card_number = self.debit_card_number_entry.get()
        if card_number != '' and (not card_number.isdigit() or len(card_number) not in (0, 4)):
            messagebox.showwarning("Data Input Error", "Please check last 4 of debit card number field for accuracy")

    #Copy field to clipboard according to which copy button is pressed                      
    def copy_to_clipboard(self, event, value, value_name):
        self.clipboard_clear()
        self.clipboard_append(value)
        messagebox.showinfo("Clipboard Updated", f"{value_name} copied to clipboard successfully!")
        return
     
# ---- CURRENTLY NOT ACCESSED ---- #
    #Update the Customer Name and Account Number labels depending on the agent type
    def update_name(self, agentType):
        
        if agentType == 'Credit Union':
            MainApplication.customer_name_label.config(text = 'Member Name:*')
            MainApplication.accountnum_label.config(text = "Member #")
        elif agentType == 'Bank':
            MainApplication.customer_name_label.config(text = 'Customer Name:*')
            MainApplication.accountnum_label.config(text = "Account #")
        else:
            messagebox.showerror('Settings File Error', 'A settings file error has occured, please delete the settings file and reopen the application')

    #Format the phone number contact info entry field to have dashes if it is a 10 digit number 
    def format_phone_number(self, new_value):
        if self.contact_radio_value.get() == "Phone #":   
            # Strip any non-digit characters from the new value
            stripped_value = "".join(filter(str.isdigit, new_value))
            # Format the stripped value as a phone number if necessary
            if len(stripped_value) == 10:
                formatted_value = "{}-{}-{}".format(stripped_value[:3], stripped_value[3:6], stripped_value[6:])
                MainApplication.formatted_phone_number = formatted_value
            else:   
                MainApplication.formatted_phone_number = new_value

#THIS FUNCTION MAY NOT BE NEEDED AS USER NOW HAS TO FILL OUT SETTINGS FILE ON FIRST TIME LAUNCH OF NO SETTINGS
    #Check if the settings file is completed. If not, delete it. 
    def check_settings_completed(self):
        # Load the ServiceEventGeneratorSettings.ini file
        config = ConfigParser()
        config.read('ServiceEventGeneratorSettings.ini')
    
        # Check if there are any sections other than the main section, if not delete the config file
        if len(config.options('main')) == 0:
            os.remove('ServiceEventGeneratorSettings.ini')
        root.destroy()  
        
    #Updates the contact info field depending on the radiobutton selected
    def contact_update(self, event = None):

        radio_value = self.contact_radio_value.get()
        contact_entry = self.contact_info.get()  # get the contact info string
        phone_start = contact_entry.find("Phone:")  # find the index of the start of the phone number
        email_start = contact_entry.find("Email:")  # find the index of the start of the email address
        phone_number_slice = contact_entry[phone_start+len("Phone:"):email_start].replace(",","").replace(" ","").strip()   # slice the phone number
        email_address_slice = contact_entry[email_start+len("Email:"):].strip()  # slice the email address
        MainApplication.bothcopy = f"Phone: {MainApplication.phonecopy}, Email: {MainApplication.emailcopy}"

        #If the previously selected radio button was the Phone # button
        if MainApplication._last_radio_value == 'Phone':

            #If the currently selected radio button is the Phone # button
            if radio_value == 'Phone #':
                if MainApplication.phonecopy == '' and contact_entry != '':
                    MainApplication.phonecopy = contact_entry
                else:
                    self.contact_info.set(MainApplication.phonecopy)
                MainApplication._last_radio_value = 'Phone'

            #If the currently selected radio button is the Email Address button
            if radio_value == 'Email Address':
                MainApplication.phonecopy = contact_entry
                if MainApplication.emailcopy != '':
                    self.contact_info.set(MainApplication.emailcopy)
                else:
                    self.contact_info.set('')
                MainApplication._last_radio_value = 'Email'

            #If the currently selected radio button is the Both button
            if radio_value == 'Both':
                #If phone copy and email copy variables are both emptY
                if MainApplication.phonecopy  == '' and MainApplication.emailcopy == '':
                    #If the entry field is not empty set the phone copy variable to the what was in the entry field and ask for an email
                    if contact_entry != '':
                        MainApplication.phonecopy = contact_entry
                        messagebox.showerror("Data Input Error", "Please enter an email address")
                        self.contact_radio_value.set('Email Address')
                        self.contact_info.set('')
                        MainApplication._last_radio_value = 'Email'
                    
                    #If the entry field is blank error and ask for both fields
                    else:
                        messagebox.showerror("Data Input Error", "Please enter a phone number and an email address")
                        self.contact_radio_value.set('Phone #')
                        MainApplication._last_radio_value = 'Phone'
                        return
                    return
                
                #If phone copy variable is empty and email copy variable is not empty
                elif MainApplication.phonecopy == '' and MainApplication.emailcopy != '':
                    #if the entry field is not blank and there is not a period or at sign in the entry field, set the phone copy variable to the entry
                    if contact_entry != '' and not ("." in contact_entry and "@" in contact_entry):
                        MainApplication.phonecopy = contact_entry

                    #else ask for a phone number
                    else:
                        messagebox.showerror("Data Input Error", "Please enter a phone number")
                        self.contact_radio_value.set('Phone #')
                        MainApplication._last_radio_value = 'Phone'
                        self.contact_info.set('')

                #if the phone copy variable is not empty
                elif MainApplication.phonecopy != '':
                    #if the entry field is not empty
                    if contact_entry != '':
                        #if the phone copy equals the entry and the email copy is blank, error and ask for email
                        if MainApplication.phonecopy == contact_entry and MainApplication.emailcopy == '':
                            messagebox.showerror("Data Input Error", "Please enter an email address")
                            self.contact_radio_value.set('Email Address')
                            MainApplication._last_radio_value = 'Email'
                            self.contact_info.set('')
                        
                        #else if the phone copy is not equal to the entry field and the is not a period and at symbol in the entry set the phone copy to the contact and ask for email
                        elif MainApplication.phonecopy != contact_entry and not ("." in contact_entry and "@" in contact_entry):
                            MainApplication.phonecopy = contact_entry
                            messagebox.showerror("Data Input Error", "Please enter an email address")
                            self.contact_radio_value.set("Email Address")
                            MainApplication._last_radio_value = 'Email'
                            self.contact_info.set('')

                        #else if there is a period and at in the entry set the email copy to the entry
                        elif "." in contact_entry and "@" in contact_entry:
                            MainApplication.emailcopy = contact_entry
                    else:
                        pass

                #else if the phone copy is not equal to the contact entry, set the phone copy to the contact entry and ask for email
                elif MainApplication.phonecopy != contact_entry:
                    MainApplication.phonecopy = contact_entry
                    messagebox.showerror("Data Input Error", "Please enter an email address")
                    self.contact_radio_value.set('Email Address')
                    MainApplication._last_radio_value = 'Email'
                    self.contact_info.set('')

                #if the phone copy and email copy are both not empty format the string and set the entry to the string
                if MainApplication.phonecopy != '' and MainApplication.emailcopy != '':
                    MainApplication.bothcopy = f"Phone: {MainApplication.phonecopy}, Email: {MainApplication.emailcopy}"
                    self.contact_info.set(MainApplication.bothcopy)
                    MainApplication._last_radio_value = 'Both'
                
        #If the previously selected radio button was the Email Address button
        elif MainApplication._last_radio_value == 'Email':

            #If the currently selected radio button is the Phone # button
            if radio_value == 'Phone #':
                MainApplication.emailcopy = contact_entry
                if MainApplication.phonecopy != '':
                    self.contact_info.set(MainApplication.phonecopy)
                else:
                    self.contact_info.set('')
                MainApplication._last_radio_value = 'Phone'

            #If the currently selected radio button is the Email Address button
            if radio_value == 'Email Address':
                if MainApplication.emailcopy == '' and contact_entry != '':
                    MainApplication.emailcopy = contact_entry
                else:
                    self.contact_info.set(MainApplication.emailcopy)
                MainApplication._last_radio_value = 'Email'

            #If the currently selected radio button is the Both button
            if radio_value == 'Both':
                #If phone copy and email copy variables are both empty
                if MainApplication.phonecopy  == '' and MainApplication.emailcopy == '':
                    if contact_entry != '':
                        MainApplication.emailcopy = contact_entry
                        messagebox.showerror("Data Input Error", "Please enter a phone number")
                        self.contact_radio_value.set('Phone #')
                        self.contact_info.set('')
                        MainApplication._last_radio_value = 'Phone'
                    
                    #else error and ask for email
                    else:
                        messagebox.showerror("Data Input Error", "Please enter a phone number and an email address")
                        self.contact_radio_value.set('Email Address')
                        MainApplication._last_radio_value = 'Email'
                        self.contact_info.set('')
                        return
                    return
                
                #If phone copy variable is empty and email copy variable is not empty
                elif MainApplication.phonecopy != '' and MainApplication.emailcopy == '':
                    #if the contact entry is not empty and there is a period and at in contact field, set the email copy to the contact entry
                    if contact_entry != '' and ("." in contact_entry and "@" in contact_entry):
                        MainApplication.emailcopy = contact_entry

                    #else, error and ask for email
                    else:
                        messagebox.showerror("Data Input Error", "Please enter an email address")
                        self.contact_radio_value.set('Email Address')
                        MainApplication._last_radio_value = 'Email'
                        self.contact_info.set('')

                #else if the email copy is not blank and the phone copy is blank
                elif MainApplication.emailcopy != '' and MainApplication.phonecopy == '':
                    #if the contact entry is not empty and there is a period and at symbol in the entry 
                    if contact_entry != '' and ("." in contact_entry and "@" in contact_entry):
                        #if the email copy is what is in the entry, show error and ask for phone
                        if MainApplication.emailcopy == contact_entry:
                            messagebox.showerror("Data Input Error", "Please enter a phone number")
                            self.contact_radio_value.set('Phone #')
                            MainApplication._last_radio_value = 'Phone'
                            self.contact_info.set('')

                        #else if the email copy is not what is in the contact entry and there is a period and at symbol in the entry, set the email copy to the contact entry and ask for a phone number
                        elif MainApplication.emailcopy != contact_entry and ("." in contact_entry and "@" in contact_entry):
                            MainApplication.emailcopy = contact_entry
                            messagebox.showerror("Data Input Error", "Please enter a phone number")
                            self.contact_radio_value.set('Phone #')
                            MainApplication._last_radio_value = 'Phone'
                            self.contact_info.set('')

                        #else if there is not a period and at symbol in the entry set the phone copy to the entry
                        elif not ("." in contact_entry and "@" in contact_entry):
                            MainApplication.phonecopy = contact_entry
                    else:
                        pass

                #else if the email copy is not the entry, set the email copy to the contact entry and ask for phone
                elif MainApplication.emailcopy != contact_entry:
                    MainApplication.emailcopy = contact_entry
                    messagebox.showerror("Data Input Error", "Please enter a phone number")
                    self.contact_radio_value.set('Phone #')
                    MainApplication._last_radio_value = 'Phone'
                    self.contact_info.set('')

                #if both phone and email copy variables are empty, format the string and insert it in to the entry
                if MainApplication.phonecopy != '' and MainApplication.emailcopy != '':
                    MainApplication.bothcopy = f"Phone: {MainApplication.phonecopy}, Email: {MainApplication.emailcopy}"
                    self.contact_info.set(MainApplication.bothcopy)
                    MainApplication._last_radio_value = 'Both'
                
        #If the previously selected radio button was the Both button
        elif MainApplication._last_radio_value == 'Both':
            #If the currently selected radio button is the Phone # button slice the phone and email if they are different and set them to the variables
            if radio_value == 'Phone #':
                if phone_number_slice != MainApplication.phonecopy:
                    MainApplication.phonecopy = phone_number_slice
                    self.contact_info.set(MainApplication.phonecopy)
                if email_address_slice != MainApplication.emailcopy:
                    MainApplication.emailcopy = email_address_slice
                    self.contact_info.set(MainApplication.phonecopy)
                else:
                    self.contact_info.set(phone_number_slice)
                MainApplication._last_radio_value = 'Phone'

            #If the currently selected radio button is the Email Address button slice the phone and email if they are different and set them to the variables
            if radio_value == 'Email Address':
                if phone_number_slice != MainApplication.phonecopy:
                    MainApplication.phonecopy = phone_number_slice
                    self.contact_info.set(MainApplication.emailcopy)
                if email_address_slice != MainApplication.emailcopy:
                    MainApplication.emailcopy = email_address_slice
                    self.contact_info.set(MainApplication.emailcopy)
                else:
                    self.contact_info.set(email_address_slice)
                MainApplication._last_radio_value = 'Email'

            #If the currently selected radio button is the Both button
            if radio_value == 'Both':
                MainApplication._last_radio_value = 'Both'
    
    #Combines the various entry and text fields in to one combined field
    def combine_text(self, event=None):
        config = ConfigParser()
        if os.path.exists('ServiceEventGeneratorSettings.ini'):
            ini_file_path = os.path.abspath("ServiceEventGeneratorSettings.ini")
            #config.read("config.ini")
            with codecs.open(ini_file_path, 'r', encoding='utf-8-sig') as f:
                config.read_file(f)
        
        agentType = config.get('main', 'agent_type')
        if agentType == 'Credit Union':
            MainApplication.customer_name_label.config(text='Member Name:*')
            MainApplication.accountnum_label.config(text="Member #")

        elif agentType == 'Bank':
            MainApplication.customer_name_label.config(text='Customer Name:*')
            MainApplication.accountnum_label.config(text="Account #")
        if agentType == 'Credit Union' or agentType == 'CU':
            self.combined_text = ""
            reason = self.reason_entry.get('1.0', tk.END)
            transactions = self.transactions_entry.get('1.0', tk.END)
            
            #Add the name
            if self.customer_name.get() != '':
                self.combined_text = ("Member Name: " + self.customer_name.get() + self.combined_text)
            #Add the reason for calling
            if reason.isspace():
                pass
            else:
                self.combined_text = (self.combined_text + "\n" + f"{self.reason_entry.get('1.0', tk.END)}\nThank you")
            #Add the reference number
            if self.reference_number.get() != '':
                self.combined_text = (self.combined_text + "\n" + f"{self.reference_radio_value.get()}: " + self.reference_number.get())
            #Add the contact info
            if self.contact_info.get() != '':
                if self.contact_radio_value.get() == 'Phone #':
                    self.combined_text = (self.combined_text + "\n" + f"{self.contact_radio_value.get()}: " + MainApplication.formatted_phone_number)
                elif self.contact_radio_value.get() == 'Email Address':
                    self.combined_text = (self.combined_text + "\n" + f"{self.contact_radio_value.get()}: " + self.contact_info.get())
                elif self.contact_radio_value.get() == 'Both':
                    self.combined_text = (self.combined_text + "\n" + MainApplication.bothcopy)
            #Add the last 4 of the debit card
            if self.debit_card_number.get() != '':
                self.combined_text = (self.combined_text + "\n" + f"Last 4 of Card: {self.debit_card_number.get()}")
            #Add the transactions
            if transactions.isspace():
                pass
            else:
                self.combined_text = (self.combined_text + "\n" + f"Transactions:\n{self.transactions_entry.get('1.0', tk.END)}")

            MainApplication.event_entry.delete('1.0', tk.END)
            MainApplication.event_entry.insert('1.0', self.combined_text)

        if agentType == 'Bank':
            self.combined_text = ""
            reason = self.reason_entry.get('1.0', tk.END)
            transactions = self.transactions_entry.get('1.0', tk.END)
            
            #Add the name
            if self.customer_name.get() != '':
                self.combined_text = ("Customer Name: " + self.customer_name.get() + self.combined_text)
            #Add the reason for calling
            if reason.isspace():
                pass
            else:
                self.combined_text = (self.combined_text + "\n" + f"{self.reason_entry.get('1.0', tk.END)}\nThank you")
            #Add the reference number
            if self.reference_number.get() != '':
                self.combined_text = (self.combined_text + "\n" + f"{self.reference_radio_value.get()}: " + self.reference_number.get())
            #Add the contact info
            if self.contact_info.get() != '':
                if self.contact_radio_value.get() == 'Phone #':
                    self.combined_text = (self.combined_text + "\n" + f"{self.contact_radio_value.get()}: " + MainApplication.formatted_phone_number)
                elif self.contact_radio_value.get() == 'Email Address':
                    self.combined_text = (self.combined_text + "\n" + f"{self.contact_radio_value.get()}: " + self.contact_info.get())
                elif self.contact_radio_value.get() == 'Both':
                    self.combined_text = (self.combined_text + "\n" + MainApplication.bothcopy)
            #Add the last 4 of the debit card
            if self.debit_card_number.get() != '':
                self.combined_text = (self.combined_text + "\n" + f"Last 4 of Card: {self.debit_card_number.get()}")
            #Add the transactions
            if transactions.isspace():
                pass
            else:
                self.combined_text = (self.combined_text + "\n" + f"Transactions:\n{self.transactions_entry.get('1.0', tk.END)}")


            MainApplication.event_entry.delete('1.0', tk.END)
            MainApplication.event_entry.insert('1.0', self.combined_text)

    #Restrict contact info field to number if the radio button selected is the Phone #        
    def restrict_contact_field(self, P):
        if self.contact_radio_value.get() == 'Phone #':
            if str.isdigit(P) or P == '':
                return True
            else:
                return False
        else:
            return

    #Restrict debit card field to numbers only    
    def restrict_debit_card_field(self, P):
        if str.isdigit(P) or P == '':
            return True
        else:
            return False

# - Popup window called when selecting set extension from File Menu - #
class AgentSettings():
    def __init__(self, master, show_window = True, *args, **kwargs):
        self.master = master
        #tk.Frame.__init__(self, self.master, *args, **kwargs)
        self.run_flag = 0
        AgentSettings.agentType = tk.StringVar()
        AgentSettings.extension = tk.StringVar()
        #self.request_settings()
        



            
    # - Creates a new top level window for setting the extension with the Agent Setting class- #    
    def configure_window(self):
        config = ConfigParser()
        self.settings_request_window = tk.Toplevel(self.master)
        self.settings_request_window.attributes('-topmost', True)
        self.settings_request_window.iconphoto(False, image)
        self.settings_request_window.winfo_toplevel().title("Agent Setting")
        self.settings_request_window.configure(bg=jhblue)
        self.settings_request_window.geometry('300x200')
        self.settings_request_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        AgentSettings.extension = tk.StringVar()
        AgentSettings.agentType = tk.StringVar()
        self.info = tk.Label(self.settings_request_window, text= "Please enter your extension and set your agent type", font=('Poppins 12'), bg=jhblue, fg="white", wraplength=280)
        self.extensionEntry = tk.Entry(self.settings_request_window, textvariable=AgentSettings.extension, width=5, font=("Poppins 12"))
        self.extension_label = tk.Label(self.settings_request_window, text= "Extension:", font=('Poppins 12'), bg=jhblue, fg="white")
        self.bank_agentType = tk.Radiobutton(self.settings_request_window, variable=AgentSettings.agentType, value = "Bank", bg = jhblue, indicatoron=1)
        self.bank_agent_label = tk.Label(self.settings_request_window, text= "Bank Agent", font=('Poppins 12'), bg=jhblue, fg="white")
        self.cu_agentType = tk.Radiobutton(self.settings_request_window, variable=AgentSettings.agentType, value = "Credit Union", bg = jhblue, indicatoron=1)
        self.cu_agent_label = tk.Label(self.settings_request_window, text= "CU Agent", font=('Poppins 12'), bg=jhblue, fg="white")
        self.save = tk.Button(self.settings_request_window, text="Save", command = lambda: self.save_settings(self.settings_request_window))
        self.info.place(x=20,y=5)
        self.extensionEntry.place(x=115, y=68, height=25)
        self.extension_label.place(x=25, y=67)
        self.bank_agentType.place(x=30, y=110, width=20, height=20)
        self.cu_agentType.place(x=165, y=110, width=20, height=20)
        self.bank_agent_label.place(x=50, y=105)
        self.cu_agent_label.place(x=185, y=105)
        self.save.place(x=115,y=145)
        if AgentSettings.agentType.get() == 'Credit Union':
            MainApplication.customer_name_label.config(text='Member Name:*')
            MainApplication.accountnum_label.config(text="Member #")

        elif AgentSettings.agentType.get() == 'Bank':
            MainApplication.customer_name_label.config(text='Customer Name:*')
            MainApplication.accountnum_label.config(text="Account #")
        

    def save_settings(self, settings_window_request):
            ext = str(self.extension.get())
            agent = self.agentType
            self.config=ConfigParser()
            ini_file_path = os.path.abspath("ServiceEventGeneratorSettings.ini")
            with codecs.open(ini_file_path, 'r', encoding='utf-8-sig') as f:
                self.config.read_file(f)
            
            # Check if extension is valid
            if len(ext) != 4 or not ext.isdigit() or (ext[0] != '4' and ext != '5000'):
                messagebox.showwarning("Data Input Error", "Please check extension for accuracy")
                return

            # Check if agent type is selected
            elif not agent.get():
                messagebox.showwarning("Data Input Error", "Please select an agent type")
                return
                    
            if not self.config.has_section('main'):
                self.config.add_section('main')

            if agent.get() == 'Credit Union':
                MainApplication.customer_name_label.config(text='Member Name:*')
                MainApplication.accountnum_label.config(text="Member #")

            elif agent.get() == 'Bank':
                MainApplication.customer_name_label.config(text='Customer Name:*')
                MainApplication.accountnum_label.config(text="Account #")

            with open('ServiceEventGeneratorSettings.ini', 'w') as f:
                self.config.set('main', "agent_type", agent.get())
                self.config.set('main', 'extension', ext)
                self.config.write(f)
                settings_window_request.destroy()
                AgentSettings.agentType = self.config.get('main', 'agent_type')
                if self.config.get('main', 'agent_type') == 'CU':
                    MainApplication.customer_name_label.config(text='Member Name:*')
                    MainApplication.accountnum_label.config(text="Member #")
                     
                elif self.config.get('main', 'agent_type') == 'Bank':
                    MainApplication.customer_name_label.config(text='Customer Name:*')
                    MainApplication.accountnum_label.config(text="Account #")
                messagebox.showinfo("Settings File Updated", f'Extension has been set to {ext}, and agent type has been set to {agent.get()} in the settings file!')
                return self.agentType
            
            
    def on_closing(self):
        ext = self.extension.get()
        agent_type = self.agentType.get()

        if not ext or not agent_type or len(ext) != 4 or not ext.isdigit() or (ext[0] != '4' and ext != '5000'):
            messagebox.showwarning("Data Input Error", "Please fill in the required fields before closing the window.")
        else:
            self.settings_request_window.destroy()
    
    def request_settings(self):
        self.config=ConfigParser()
        
        # Define the main section name
        main_section = 'main'
        
        if os.path.exists('ServiceEventGeneratorSettings.ini'):
            ini_file_path = os.path.abspath("ServiceEventGeneratorSettings.ini")
            with codecs.open(ini_file_path, 'r', encoding='utf-8-sig') as f:
                self.config.read_file(f)
            # Check if the main section contains the 'agent type' key
            if self.config.has_option(main_section, 'agent_type'):
                agent_type = self.config.get(main_section, 'agent_type')
                if agent_type == 'Credit Union':
                    MainApplication.customer_name_label.config(text='Member Name:*')
                    MainApplication.accountnum_label.config(text="Member #")
                elif agent_type == 'Bank':
                    MainApplication.customer_name_label.config(text='Customer Name:*')
                    MainApplication.accountnum_label.config(text="Account #")

            if self.config.has_option(main_section, 'extension'):
                ext = self.config.get('main', 'extension')


        else:
            self.settings_request_window = tk.Toplevel(self.master)
            self.settings_request_window.attributes('-topmost', True)
            self.settings_request_window.iconphoto(False, image)
            self.settings_request_window.winfo_toplevel().title("Agent Setting")
            self.settings_request_window.configure(bg=jhblue)
            self.settings_request_window.geometry('300x200')
            self.settings_request_window.protocol("WM_DELETE_WINDOW", self.on_closing)
            AgentSettings.extension = tk.StringVar()
            AgentSettings.agentType = tk.StringVar()
            self.info = tk.Label(self.settings_request_window, text= "Please enter your extension and set your agent type", font=('Poppins 14 bold'), bg=jhblue, fg="white", wraplength=280)
            self.extensionEntry = tk.Entry(self.settings_request_window, textvariable=AgentSettings.extension, width=5, font=("Poppins 14 bold"))
            self.extension_label = tk.Label(self.settings_request_window, text= "Extension:", font=('Poppins 14 bold'), bg=jhblue, fg="white")
            self.bank_agentType = tk.Radiobutton(self.settings_request_window, variable=AgentSettings.agentType, value = "Bank", bg = jhblue, indicatoron=1)
            self.bank_agent_label = tk.Label(self.settings_request_window, text= "Bank Agent", font=('Poppins 14 bold'), bg=jhblue, fg="white")
            self.cu_agentType = tk.Radiobutton(self.settings_request_window, variable=AgentSettings.agentType, value = "Credit Union", bg = jhblue, indicatoron=1)
            self.cu_agent_label = tk.Label(self.settings_request_window, text= "CU Agent", font=('Poppins 14 bold'), bg=jhblue, fg="white")
            self.save = tk.Button(self.settings_request_window, text="Save", command = lambda: self.save_settings())
            self.info.place(x=20,y=5)
            self.extensionEntry.place(x=115, y=53, height=25)
            self.extension_label.place(x=25, y=55)
            self.bank_agentType.place(x=30, y=90, width=20, height=20)
            self.cu_agentType.place(x=165, y=90, width=20, height=20)
            self.bank_agent_label.place(x=50, y=90)
            self.cu_agent_label.place(x=185, y=90)
            self.save.place(x=115,y=120)

    def update_settings(self):
        self.configure_window()
        if os.path.exists('ServiceEventGeneratorSettings.ini') and self.run_flag == 0:
            ini_file_path = os.path.abspath("ServiceEventGeneratorSettings.ini")


# - Sets up File Menu with drop down options - #
class FileMenu(tk.Menu):


    def __init__(self, master, main_app, agent_settings):
        self.master = master
        self.main_app = main_app
        self.agent_settings = agent_settings
        tk.Menu.__init__(self, self.master)
        self.menu = tk.Menu(self.master)
        self.fileMenu = tk.Menu(self.menu)
        self.fi_select_menu = tk.Menu(self.menu) 
        self.menu.add_cascade(label="Settings", menu=self.fileMenu)
        self.fileMenu.add_command(label="Open Welcome Message...", command=lambda: welcome_message(1))
        self.fileMenu.add_command(label="Settings...", command=lambda: AgentSettings.update_settings(self.agent_settings))                

# - For clearing text from the entry fields. Saves text from those fields to variables and changes Clear Text button to Undo Clear button to undo the clear if needed - #
class ClearUndo():
    # Use a class variable to keep track of how many times instance has been run
    _instance_count = 0

    
    def __init__(self):
        # Initialize the class attributes to None
        self.customernamecopy = None
        self.reasoncopy = None
        self.referencecopy = None
        self.contactinfocopy = None
        self.debitcardcopy = None
        self.transactionscopy = None
        
        # Set self.clear based on the value of the _first_run flag
        ClearUndo._instance_count += 1

        if ClearUndo._instance_count % 2 == 1:
            self.clear = True
        else:
            self.clear = False
            
        self.clear_undo()
    
    def clear_undo(self):
        
        if self.clear == True:
            # Assign values to the class attributes
            ClearUndo.customernamecopy = MainApplication.customer_name.get()
            ClearUndo.referencecopy = MainApplication.reference_number.get()
            ClearUndo.contactinfocopy = MainApplication.contact_info.get()
            ClearUndo.debitcardcopy = MainApplication.debit_card_number.get()
            ClearUndo.transactionscopy = MainApplication.transactions_entry.get("1.0", tk.END)
            ClearUndo.reasoncopy = MainApplication.reason_entry.get("1.0", tk.END)
            ClearUndo.evententrycopy = MainApplication.event_entry.get("1.0", tk.END)
            ClearUndo.contactradiocopy = MainApplication.contact_radio_value.get()

            def clear_fields():
                MainApplication.customer_name.set("")
                MainApplication.reference_number.set("")
                MainApplication.contact_info.set("")
                MainApplication.debit_card_number.set("")
                MainApplication.transactions_entry.delete("1.0", tk.END)
                MainApplication.reason_entry.delete("1.0", tk.END)
                MainApplication.event_entry.delete("1.0", tk.END)
                MainApplication.phonecopy = ''
                MainApplication.emailcopy = ''
                MainApplication.bothcopy = ''
                if MainApplication.contact_radio_value.get() == "Both":
                    MainApplication.contact_radio_value.set("Phone #")
                MainApplication._last_radio_value = "Phone"
                return

            clear_fields()
            self.clear = False
            MainApplication.clearundobtntxt.set("Undo Clear")
            return

        if self.clear == False:
            MainApplication.clearundobtntxt.set("Clear Text")
            # Use the class attributes in the second if statement
            MainApplication.customer_name.set(ClearUndo.customernamecopy)
            MainApplication.reference_number.set(ClearUndo.referencecopy)
            MainApplication.contact_info.set(ClearUndo.contactinfocopy)
            MainApplication.debit_card_number.set(ClearUndo.debitcardcopy)
            MainApplication.transactions_entry.insert("1.0", ClearUndo.transactionscopy)
            MainApplication.reason_entry.insert("1.0", ClearUndo.reasoncopy)
            MainApplication.event_entry.insert("1.0", ClearUndo.evententrycopy)
            MainApplication.contact_radio_value.set(ClearUndo.contactradiocopy)
            self.clear = True
            return


#Creates a custom dialog window for going through multiple spell check corrections at once
class SpellCheckDialog(tk.Toplevel):
    def __init__(self, parent, word, suggestions):
        super().__init__(parent)
        self.title("Choose an option")
        self.word = word
        self.suggestions = suggestions
        self.result = None
        self.combobox_clicked = False

        #Creates a label with the misspelled word currently being prompted for reply from user on
        message = f"Misspelled: {word}\n"
        msg_label = ttk.Label(self, text=message, wraplength=300)
        msg_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        #set suggested spellings to a string and add them from SymSpell to the string
        self.suggestion_var = tk.StringVar(self)
        if suggestions:
            self.suggestion_var.set(suggestions[0])

        #Create a dropdown with the suggested words
        self.suggestion_menu = ttk.Combobox(self, textvariable=self.suggestion_var, values=suggestions)
        self.suggestion_menu.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        #Create an entry for the user to enter the proper spelling if it does not appear
        self.custom_spelling = ttk.Entry(self)
        self.custom_spelling.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        #Check if suggestions isn't empty and if the combo box has not been checked. If it has not been clicked do not set the dropdown value to the entry box, 
        #otherwise set the entry to the dropdown value selected
        if suggestions:
            if self.combobox_clicked == False:
                pass
            else:
                self.custom_spelling.delete(0, tk.END)
                self.custom_spelling.insert(0, suggestions[0])

        #Create label to instruct user to enter word if correct spelling is not available
        self.custom_spelling_label = ttk.Label(self, text="If the correct word is not listed in the drop down please type it manually.", wraplength=300)
        self.custom_spelling_label.grid(row=2, column=1, padx=10, pady=10)

        #Call the create buttons function and close the window if the user ignores the spelling recommendation
        self.create_buttons()
        self.geometry("590x300")
        self.protocol("WM_DELETE_WINDOW", self.ignore)
        self.iconphoto(False, image)
        
    #function to create our custom buttons for our custom dialog, commands are set appropriately depending on the button selected
    def create_buttons(self):
        correct_button = ttk.Button(self, text="Correct it", command=self.correct)
        correct_button.grid(row=4, column=0, padx=10, pady=10)

        add_button = ttk.Button(self, text="Add to dictionary", command=self.add)
        add_button.grid(row=4, column=1, padx=10, pady=10)

        ignore_button = ttk.Button(self, text="Ignore", command=self.ignore)
        ignore_button.grid(row=4, column=2, padx=10, pady=10)

        # Update the entry widget with the selected value from the dropdown menu
        def update_entry(event):
            self.custom_spelling.delete(0, tk.END)
            self.custom_spelling.insert(0, self.suggestion_var.get())

        #bind the combobox being selected to calling the update entry function that will take the dropdown value selected and input it in to the entry
        self.suggestion_menu.bind("<<ComboboxSelected>>", update_entry)

    #If the user presses the correct button, check if there is anything typed in the custom entry field and use that, otherwise use the selected suggestion and 
    #close the window
    def correct(self):
        if self.custom_spelling.get():
            self.result = ("correct", self.custom_spelling.get())
        else:
            self.result = ("correct", self.suggestion_var.get())
        self.destroy()

    #Add the word misspelled to the dictionary and close the window
    def add(self):
        self.result = ("add", )
        self.destroy()

    #Ignore the spelling recommendation and close the window
    def ignore(self):
        self.result = ("ignore", )
        self.destroy()
    
    #function for updating the text entry if the combobox is selected, not sure if this is needed here?
    def update_entry(self, event):
        self.custom_spelling.delete(0, tk.END)
        self.custom_spelling.insert(0, self.suggestion_var.get())

#Smartsheet Window Class
class CustomSmartsheet(smartsheet.Smartsheet):
    run_flag = 0
    sheet_id = 2320617425921924
    event_details_copy = str('test')

    picklist_column_name = 'Banks'
    picklist_column_name_2 = 'Credit Unions'        
    def __init__(self, master, api_token):
        super().__init__(api_token)
        self.master = master
        self.sheet_id = 2320617425921924
        

    def send_event (self, event, sheet_id, row_values):
        columns = self.Sheets.get_columns(sheet_id).to_dict()
        column_name_to_id = {col['title']: col['id'] for col in columns['data']}
        
        new_row = smartsheet.models.Row()
        new_row.to_top = True

        cells = []
        for column_name, value in row_values.items():
            column_id = column_name_to_id[column_name]
            new_cell = smartsheet.models.Cell()
            new_cell.column_id = column_id
            new_cell.value = value
            cells.append(new_cell)

        new_row.cells = cells
        result = self.Sheets.add_rows(sheet_id, [new_row])
        self.smartsheet_event_window.destroy()
        
        tech_error_box = messagebox.askyesno("Warning", "Do you need to send a tech error form to report that you are not able to access synapsys?")
        if not tech_error_box:
            return
        else:
            if AgentSettings.agentType == 'Credit Union':

                url = "https://app.smartsheet.com/b/form/b09da0f620d04c45aeae3db44606d335"
                webbrowser.open(url)
            elif AgentSettings.agentType == 'Bank':
                url = "https://app.smartsheet.com/b/form/01581776b2564281b36ba9fc96f213c8"
                webbrowser.open(url)

    def get_picklist_values(self, sheet_id, column_name):
        columns = self.Sheets.get_columns(sheet_id).to_dict()

        for column in columns['data']:
            if column['title'] == column_name:
                if 'options' in column:
                    return column['options']
                
                else:
                    raise ValueError(f"The specified column '{column_name}' is not a picklist (dropdown) column.")
        
    
        raise ValueError(f"Column '{column_name}' not found in the sheet.")
    
    def check_if_time_elapsed(self, event, start_time, duration):
        current_time = time.time()
        return current_time - start_time <= duration
    
#Will need popup window form for these fields: Inquiry or Call Back?, FI depending on Agent Type (Bank or CU), 

    
    def smartsheet_event_options(self, event, sheet_id):      
        if self.run_flag == 0:
            self.start_time = time.time()
            self.run_flag += 1
        if self.run_flag > 0:
            self.current_time = time.time()
        #Set the duration that will trigger the next if
        duration = 180
        if self.check_if_time_elapsed(self, self.start_time, duration):
            if self.event_details_copy == MainApplication.event_entry.get("1.0", tk.END):
                result = messagebox.askyesno("Warning", "It's not been 3 minutes since the last event was sent and the event you are trying to send now is the same as the last event, are you sure you want to send this current event?")
                if not result:
                    return
                else:
                    pass
                
        self.smartsheet_event_window = tk.Toplevel(self.master)
        self.smartsheet_event_frame = tk.Frame(self.smartsheet_event_window)
        self.smartsheet_event_window.iconphoto(False, image)
        self.smartsheet_event_window.winfo_toplevel().title("Service Event Submission")
        self.smartsheet_event_window.configure(bg=jhblue)
        self.smartsheet_event_window.geometry('425x300')
        CustomSmartsheet.selected_fi = tk.StringVar()
        CustomSmartsheet.fi_list = tk.StringVar()
        if AgentSettings.agentType == 'Credit Union':
            CustomSmartsheet.fi_list = self.get_picklist_values(self.sheet_id, 'Credit Unions')
        elif AgentSettings.agentType == 'Bank':
            CustomSmartsheet.fi_list = self.get_picklist_values(self.sheet_id, 'Banks')
        self.label = tk.Label(self.smartsheet_event_window, text="If you are needing to send this Service Event to be submitted for you due to a Synapsys access issue please provide the following information", font=('Poppins 12'), bg=jhblue, fg="white", wraplength=375)
        self.label.place(x = 35, y = 25)
        self.start_time = time.time()
        if MainApplication.phonecopy == '':
            phone_num = MainApplication.contact_info.get()
        elif MainApplication.phonecopy != '':
            phone_num = MainApplication.phonecopy
        def on_combobox_change(event):
            CustomSmartsheet.selected_fi.set(self.combobox.get()) 
            if AgentSettings.agentType == 'Credit Union':
                CustomSmartsheet.row_values = {
                    'Agent Extension': f'{AgentSettings.extension.get()}',
                    'Bank or Credit Union?': f'{AgentSettings.agentType}',
                    'Inquiry or Call Back?' : f'{CustomSmartsheet.se_type.get()}',
                    'Credit Unions' : f'{CustomSmartsheet.selected_fi.get()}',
                    'CIT/Account Number/Member Number' : f'{MainApplication.reference_number.get()}', 
                    #need to adjust this for a phone number?
                    'Call Back Number' : f'{MainApplication.contact_info.get()}', 
                    'Service Event Details' : f'{MainApplication.event_entry.get("1.0", tk.END)}\nThis event is being wrapped for Agent {AgentSettings.extension.get()}', 
                    'Customer Name' : f'{MainApplication.customer_name.get()}'
                    }   
            elif AgentSettings.agentType == 'Bank':
                CustomSmartsheet.row_values = {
                    'Agent Extension': f'{AgentSettings.extension.get()}',
                    'Bank or Credit Union?': f'{AgentSettings.agentType}',
                    'Inquiry or Call Back?' : f'{CustomSmartsheet.se_type.get()}',
                    'Banks' : f'{CustomSmartsheet.selected_fi.get()}',
                    'CIT/Account Number/Member Number' : f'{MainApplication.reference_number.get()}', 
                    #need to adjust this for a phone number?
                    'Call Back Number' : f'{MainApplication.contact_info.get()}', 
                    'Service Event Details' : f'{MainApplication.event_entry.get("1.0", tk.END)}\nThis event is being wrapped for Agent {AgentSettings.extension.get()}', 
                    'Customer Name' : f'{MainApplication.customer_name.get()}'
                    }   
        CustomSmartsheet.se_type = tk.StringVar()
        self.inquiry_radio = tk.Radiobutton(self.smartsheet_event_window, value = "Inquiry", variable = CustomSmartsheet.se_type, bg = jhblue, indicatoron = 1)
        self.inquiry_label = tk.Label(self.smartsheet_event_window, bg = jhblue, fg = 'white', text = "Inquiry", font = "Poppins 12")
        self.callback_radio = tk.Radiobutton(self.smartsheet_event_window, value = "Call Back", variable = CustomSmartsheet.se_type, bg = jhblue, indicatoron = 1)
        self.callback_label = tk.Label(self.smartsheet_event_window, bg = jhblue, fg = 'white', text = "Callback", font = "Poppins 12")
        self.combobox = ttk.Combobox(self.smartsheet_event_window, textvariable = CustomSmartsheet.selected_fi, height = 20, width = 40)
        self.financial_institution_label = tk.Label(self.smartsheet_event_window, bg = jhblue, fg = 'white', text = "Financial\n Institution", font = "Poppins 12")
        self.combobox['values'] = CustomSmartsheet.fi_list
        self.combobox.bind("<<ComboboxSelected>>", lambda event: on_combobox_change(None))
        self.inquiry_radio.place(x = 40, y = 110)
        self.inquiry_label.place(x = 70, y = 113)
        self.callback_radio.place(x = 230, y = 110)
        self.callback_label.place(x=250, y = 113)
        self.combobox.place(x = 130, y = 180)
        self.financial_institution_label.place(x = 20, y = 160)
        if AgentSettings.agentType == 'Credit Union':
            CustomSmartsheet.row_values = {
                'Agent Name': 'Chris Richardson', #this can be formula'ed from extension
                'Agent Extension': f'{AgentSettings.extension.get()}',
                'Bank or Credit Union?': f'{AgentSettings.agentType}',
                'Inquiry or Call Back?' : f'{CustomSmartsheet.se_type.get()}',
                'Credit Unions' : f'{CustomSmartsheet.selected_fi.get()}',
                'CIT/Account Number/Member Number' : f'{MainApplication.reference_number.get()}', 
                'Call Back Number' : f'{phone_num}', 
                'Service Event Details' : f'{MainApplication.event_entry.get("1.0", tk.END)}\nThis event is being wrapped for Agent {AgentSettings.extension.get()}', 
                'Customer Name' : f'{MainApplication.customer_name.get()}'
                }   
        elif AgentSettings.agentType == 'Bank':
            CustomSmartsheet.row_values = {
                'Agent Name': 'Chris Richardson', #this can be formula'ed from extension
                'Agent Extension': f'{AgentSettings.extension.get()}',
                'Bank or Credit Union?': f'{AgentSettings.agentType}',
                'Inquiry or Call Back?' : f'{CustomSmartsheet.se_type.get()}',
                'Banks' : f'{CustomSmartsheet.selected_fi.get()}',
                'CIT/Account Number/Member Number' : f'{MainApplication.reference_number.get()}', 
                #need to adjust this for a phone number?
                'Call Back Number' : f'{phone_num}', 
                'Service Event Details' : f'{MainApplication.event_entry.get("1.0", tk.END)}\nThis event is being wrapped for Agent {AgentSettings.extension.get()}', 
                'Customer Name' : f'{MainApplication.customer_name.get()}'
                }   
        self.send_event_button = tk.Button(self.smartsheet_event_window, text = "Send Event", font = ('Poppins', 12), fg = jhblue, command = lambda: self.send_event(self, sheet_id, CustomSmartsheet.row_values))
        self.send_event_button.place(x = 150, y = 230)
        self.event_details_copy = MainApplication.event_entry.get("1.0", tk.END) 


# - Main program - #
if __name__ == '__main__':
    root = tk.Tk()
    window_icon()
    agent_settings = AgentSettings(root, show_window=False)
    SE_smartsheet = CustomSmartsheet(root, api_token)
    main_app = MainApplication(root, SE_smartsheet=SE_smartsheet)
    file_menu = FileMenu(root, main_app=main_app, agent_settings=agent_settings)
    welcome_message(None)
    check_settings()
    root.configure(menu=file_menu.menu)
    root.protocol("WM_DELETE_WINDOW", main_app.check_settings_completed)
    root.mainloop()

# Pyinstaller command (flags are one file, clean the cache, yes to overrwrite, set the icon file to the right file, add the png to the data for the tkinter windows)
# pyinstaller --clean -y -F --icon="jh.ico" -n "Service Event Generator" --add-data="jh.png;files" 'SE Generator V10.py'