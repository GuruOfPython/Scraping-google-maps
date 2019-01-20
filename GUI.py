try:
    import tkinter as tk
    from tkinter import messagebox as msg, filedialog
    from tkinter import *
except:
    import Tkinter as tk
    import tkMessageBox as msg
    from Tkinter import *

import ttk

class main_GUI(tk.Frame):
    def __init__(self, master, queue, endCommand):
        self.master = master
        self.queue = queue
        self.endCommand = endCommand
        
        self.start_url = 'https://www.google.com/maps/search/'
        self.i = 0
        self.total_data = []
        self.url_dict = []
        self.company_names = []
        self.start = False
        self.keyword = ''

        self.initialize_user_interface()

    def initialize_user_interface(self):
        """Draw a user interface allowing the user to type
        items and insert them into the treeview
        """
        self.master.title("Google Maps")
        self.master.grid_rowconfigure(0,weight=1)
        self.master.grid_columnconfigure(0,weight=1)
        self.master.config(background="lavender")


        # Define the different GUI widgets
        self.search_label = tk.Label(self.master, text = "Search Word")
        self.search_entry = tk.Entry(self.master)
        self.search_label.grid(row = 0, column = 1, sticky = tk.W)
        self.search_entry.grid(row = 0, column = 2)

        self.search_button = tk.Button(self.master, text = "Search", command = self.start_running)
        self.search_button.grid(row = 1, column = 2, sticky = tk.W)
        self.exit_button = tk.Button(self.master, text = "Exit", command = self.endCommand)
        self.exit_button.grid(row = 1, column = 3)

        # Set the treeview
        self.tree = ttk.Treeview(self.master, columns=('Company Name', 'Address',
                                                        'Category', 'Star Rating',
                                                        'Reviews', 'Phone Number',
                                                        'Website'
                                                        ))
        treeScroll = ttk.Scrollbar(self.master, orient='vertical')
        treeScroll.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=treeScroll.set)
        treeScroll.place(x=1400, y=47, height=225)

        self.tree.heading('#0', text='No')
        self.tree.heading('#1', text='Company Name')
        self.tree.heading('#2', text='Address')
        self.tree.heading('#3', text='Category')
        self.tree.heading('#4', text='Star Rating')
        self.tree.heading('#5', text='Reviews')
        self.tree.heading('#6', text='Phone Number')
        self.tree.heading('#7', text='Website')

        self.tree.column('#0', stretch=tk.YES, width=40)
        self.tree.column('#1', stretch=tk.YES, width=300)
        self.tree.column('#2', stretch=tk.YES, width=350)
        self.tree.column('#3', stretch=tk.YES, width=250)
        self.tree.column('#4', stretch=tk.YES, width=80)
        self.tree.column('#5', stretch=tk.YES, width=80)
        self.tree.column('#6', stretch=tk.YES, width=100)
        self.tree.column('#7', stretch=tk.YES, width=200)


        self.tree.grid(row=10, columnspan=1, sticky='nsew')
        self.treeview = self.tree
        # Initialize the counter
        self.i = 1

    def start_running(self):
        self.keyword = self.search_entry.get()
        if self.keyword == '':
            msg.showerror("Error", "You must enter 'Search Word'!!!")
        else:
            self.start = True

    def insert_data(self):
        while self.queue:
            element = self.queue.pop()
            try:
                self.treeview.insert('', 'end', text = str(self.i),
                                     values=(element['company_name'], element['address'],
                                             element['category'], element['star_rating'],
                                             element['review_numbers'], element['phone'],
                                             element['websites']))

                self.i += 1
            except:
                pass


def main():
    root = tk.Tk()
    app = main_GUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()