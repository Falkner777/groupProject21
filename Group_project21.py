import fnmatch
import sqlite3 as sql
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from tkcalendar import  DateEntry
from datetime import date

import re

PROGRAM_NAME = 'TourstDB Application'
helv36 = ("Verdana", 36, "bold")
BUTTON_COLOR_RIGHT = "#43cea2"
BUTTON_COLOR_LEFT = "#185b9d"
TEXT_COLOR = '#ddfbfe'
BUTTON_FONT = 'Verdana 12 bold'
LABEL_FONT = 'Verdana 12 bold underline'


class Application:

    def __init__(self, root):
        self.root = root
        self.root.title(PROGRAM_NAME)
        self.root.resizable(False,False)
        self.imageData = None
        self.isOPEN = 0
        self.init_gui()
        self.topWidgets = []
        self.bindings()

    def bindings(self):
        # Συνάρτηση για όλα τα shortcuts
        self.root.bind('<Control-O>', lambda event: self.openDB())
        self.root.bind('<Control-o>', lambda event: self.openDB())

    def openDB(self):
        # Συνάρτηση για το άνοιγμα της βάσης δεδομένων , αρχικοποιήση του cursor
        if self.isOPEN:
            messagebox.showerror("Database Error", "A database is already open")
            return
        # Prompt για τον χρήστη για να ανοίξει το αρχείο της βάσης
        fname = tk.filedialog.askopenfilename(
            filetypes=[("SQLite database files", ("*.db", "*.sqlite", "*.sqlite3", "*.db3")), ("All Files", "*.*")])
        if fname:
            try:
                # Δημιουργία σύνδεσης με την βάση
                self.con = sql.connect(fname)
                self.con.row_factory = sql.Row
                self.cur = self.con.cursor()
                sqlite_select_Query = "SELECT count(*) FROM sqlite_master WHERE type='table'"
                self.isOPEN = 1
                # Dummy querry για να πάρουμε error , αν το αρχείο δεν είναι βάση δεδομένων
                self.cur.execute(sqlite_select_Query)
                # Αλλαγή τίτλου ανοιχτής DB
                self.updateTitle(fname[fname.rfind("/") + 1:])
                # Messabox για την επιτυχή σύνδεση με την βάση

                messagebox.showinfo(title="Database Info", message=f'Database {fname[fname.rfind("/") + 1:]} '
                                                                   f'successfully connected')

            except sql.Error:
                # Throw error στην περίπτωση που δεν κατάφερε να ανοίξη η βάση
                self.isOPEN = 0
                self.dbLoaderror(1)
        else:
            pass

    def dbLoaderror(self, errorType=0):
        # Ανάλογα με το errorType πετάει διαφορετικό error μήνυμα
        if not self.isOPEN and errorType == 0:
            messagebox.showerror("Database Error", "No database is open")
        elif errorType == 1:
            messagebox.showerror("Database Error", "Not a database")
        else:
            pass

    def closeDB(self):
        # Διακοπή της σύνδεσης με την βάση χωρίς να κάνει save
        if self.isOPEN:
            self.con.close()
            self.isOPEN = 0
            self.updateTitle("No open database!")
        else:
            self.dbLoaderror()

    def create_top_menu(self):
        self.menu_bar = tk.Menu(self.root)  # Δημιουργία του πάνω μενού ίσως βάλουμε και αλλα πραγματα
        self.open_menu = tk.Menu(self.menu_bar, tearoff=0)  #
        self.open_menu.add_command(label="Open ", accelerator='Ctrl+Ο',
                                   compound='left', command=self.openDB)  # Εισαγωγή της επιλογής Open
        self.open_menu.add_command(label="Close ", accelerator='Ctrl+K',
                                   compound='left', command=self.closeDB)  # Εισαγωγή της επιλογής Close
        self.menu_bar.add_cascade(label="File", menu=self.open_menu)
        self.root.config(menu=self.menu_bar)  # Εισαγωγή το menu πάνω στο root

    def createFrames(self):
        # Πάνω frame για τον τίτλο διαστάσεις 640χ70
        self.titleFrame = tk.Frame(self.root, width=640, height=70)
        self.titleFrame.grid(row=0, column=0, columnspan=2)
        self.titleFrame.grid_propagate(0)
        # Αριστερό frame για τον sql widget διαστάσεις 320χ400
        self.canvaFrame = tk.Frame(self.root)
        self.canvaFrame.config(width=320, height=400)
        self.canvaFrame.grid(row=1, column=0, ipadx=0, ipady=0)
        self.canvaFrame.grid_propagate(0)
        # Δεξί frame με τα κουμπιά διαστάσεις 320χ400
        self.buttonFrame = tk.Frame(self.root)
        self.buttonFrame.config(width=320, height=400)
        self.buttonFrame.grid(row=1, column=1, ipadx=0, ipady=0)
        self.buttonFrame.grid_propagate(0)

    def topPanel(self, frame):
        self.canvaTitle = tk.Canvas(frame, width=640, height=70)  # Δημιουργία του canva για να μπει πάνω η εικόνα
        self.canvaTitle.pack()
        self.canvaTitle.pack_propagate(0)

        self.image1 = Image.open('topCard.png')  # Ανοιγμα της εικόνας με την βιβλιοθήκη Pillow
        self.background1 = ImageTk.PhotoImage(self.image1)  # Μετραπή σε εικόνα που διαβάζει η tkinter
        self.canvaTitle.create_image(0, 0, anchor=tk.NW, image=self.background1)  # Ειαγωγή της εικόνας canva

        self.canvaTitle.create_text(320, 10, text="Database Manager", anchor=tk.N, font='Verdana 25 bold',
                                    fill=TEXT_COLOR)  # Δημιουργία του τίτλου

    def rightPanel(self, frame):
        # Δημιουργία canva για να μπει η εικόνα
        self.canvaButton = tk.Canvas(frame, width=320, height=400)
        self.canvaButton.pack()
        self.canvaButton.pack_propagate(0)

        self.image2 = Image.open('rightCard.png')  # Ανοιγμα της εικόνας με την βιβλιοθήκη Pillow
        self.background2 = ImageTk.PhotoImage(self.image2)  # Μετραπή σε εικόνα που διαβάζει η tkinter
        self.canvaButton.create_image(0, 0, anchor=tk.NW, image=self.background2)  # Ειαγωγή της εικόνας canva

        self.dbTitleLabel = tk.Label(self.canvaButton, text="No open database!")  # Τίτλος ανοιχτής βάσης
        self.dbTitleLabel.configure(width=15, activebackground="#33B5E5",
                                    background=BUTTON_COLOR_LEFT, fg=TEXT_COLOR,
                                    anchor=tk.CENTER, relief=tk.FLAT, font=LABEL_FONT)
        self.title_window = self.canvaButton.create_window(80, 10, anchor=tk.NW, window=self.dbTitleLabel)

        self.updateDBbutton = tk.Button(self.canvaButton,
                                        text="Insert")  # Κουμπί υπεύθυνο για την εισαγωγή στοιχείων στους πίνακες
        self.updateDBbutton.configure(width=15, activebackground="#33B5E5", relief=tk.FLAT, font=BUTTON_FONT,
                                      anchor=tk.CENTER, background=BUTTON_COLOR_RIGHT,
                                      fg=TEXT_COLOR, command=lambda: self.updateDB())  # Συνάρτηση updateDB()
        self.button1_window = self.canvaButton.create_window(80, 70, anchor=tk.NW, window=self.updateDBbutton)
        # Τοποθέτηση του κουμπιού στον canva

        self.browseDB = tk.Button(self.canvaButton, text="Browse Tables")
        self.browseDB.configure(width=15, activebackground="#33B5E5", relief=tk.FLAT, font=BUTTON_FONT,
                                anchor=tk.CENTER, background=BUTTON_COLOR_RIGHT, fg=TEXT_COLOR,
                                command=lambda: self.browseButton())
        self.button2_window = self.canvaButton.create_window(80, 190, anchor=tk.NW, window=self.browseDB)

        self.showExcel = tk.Button(self.canvaButton, text="Update")  # TO BE MADE
        self.showExcel.configure(width=15, activebackground="#33B5E5", relief=tk.FLAT, font=BUTTON_FONT,
                                 anchor=tk.CENTER, background=BUTTON_COLOR_RIGHT, fg=TEXT_COLOR,
                                 command=self.createExcel)
        self.button3_window = self.canvaButton.create_window(80, 130, anchor=tk.NW, window=self.showExcel)

        self.deleteButton = tk.Button(self.canvaButton, text="Delete Row")  # Κουμπί για την έξοδο από το πρόγραμμα λογικά
        self.deleteButton.configure(width=15, activebackground="#33B5E5", relief=tk.FLAT, font=BUTTON_FONT,
                                  anchor=tk.CENTER, background=BUTTON_COLOR_RIGHT, fg=TEXT_COLOR, command=lambda :self.deleteRow())
        self.button4_window = self.canvaButton.create_window(80, 250, anchor=tk.NW, window=self.deleteButton)
        self.exitButton = tk.Button(self.canvaButton, text="Exit")  # Κουμπί για την έξοδο από το πρόγραμμα λογικά
        self.exitButton.configure(width=15, activebackground="#33B5E5", relief=tk.FLAT, font=BUTTON_FONT,
                                  anchor=tk.CENTER, background=BUTTON_COLOR_RIGHT, fg=TEXT_COLOR, command=self.exit)
        self.button5_window = self.canvaButton.create_window(80, 310, anchor=tk.NW, window=self.exitButton)
        # Τοποθέτηση του κουμπιού στον canva

    def createExcel(self):
        if self.isOPEN == 0:
            self.dbLoaderror(0)
            return
        cursor = self.cur
        # Επιλογή των ονομάτων των πινάκων της βάσης μεσω query
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_name = []  # Λιστα για την αποθήκευση των ονομάτων
        res = cursor.fetchall()
        for name in res:
            table_name.append(name[0])
        # Προσθήκη του αποτελέσματος του query στην λίστα table_names
        window = tk.Toplevel(self.root)

        self.table_combo = ttk.Combobox(window,
                                        values=table_name)  # Δημιουργία combobox για τα ονοματα των πινάκων
        self.table_combo.current(0)
        self.table_combo.grid(row=0, column=2)
        self.getID = tk.Button(window, text="Select",
                               command=lambda: self.PKWidget(window, cursor)).grid(row=0,
                                                                                   column=0)  # Δημιουργία του κουμπιού select για την εμφάνιση του primary key του εκάστοτε πίνακα
        self.clearWidgetButton = tk.Button(window,
                                           text="Clear",
                                           command=lambda: self.clearWidgets(
                                               self.tempwidgets,
                                               self.topWidgets))  # Δημιουργία του κουμπιου clear για την διαγραφή των υπαρχοντων widgets στο top window
        self.clearWidgetButton.grid(row=0, column=1)

    def getPrimaryKeys(self, cursor):
        # query για την λήψη των primary keys του κάθε πίνακα (η εφαρμογή εχει μεχρι 2 οπότε περιοριστήκαμε σε αυτό)
        query = f'SELECT l.name FROM pragma_table_info("{self.table_combo.get()}") as l WHERE l.pk = 1  or l.pk =2;'
        keys = []
        # εκτέλεση του query με try except και αποθηκευση των αποτελεσμάτων στην λιστα keys
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            for res in results:
                keys.append(res[0])
        except sql.Error as error:
            messagebox.showerror("Error", error)
        return keys

    def PKWidget(self, window, cursor, delete =0):
        keys = self.getPrimaryKeys(cursor)  # λήψη των primary keys μεσω της μεθόδου της κλασσης
        self.tempwidgets = []  # λίστα για την αποθήκευση των προσωρινών widgets
        # βρόχος για την δημιουργία label - entry ζευγαριού για την εμφάνιση των primary keys
        for ind, key in enumerate(keys):
            label = tk.Label(window, text=key)
            label.grid(row=ind + 1, column=0)
            entry = tk.Entry(window)
            entry.grid(row=ind + 1, column=2)
            self.tempwidgets.append(label)
            self.tempwidgets.append(entry)
            # κουμπί υπεύθυνο για την εκτέλεση της φόρτωσης των δεδομένων απο την βάση και διαγραφή των widgets που υπάρχουν ήδη

        tempButton = tk.Button(window, text="Ok", command=lambda: self.doubleCommand(window, 1,
                                                                                     [self.tempwidgets[x].get() for x in
                                                                                      range(1, len(self.tempwidgets),
                                                                                            2)]))
        tempButton.grid(row=1, column=3)
        self.tempwidgets.append(tempButton)
        if delete:
            self.tempwidgets[-1].destroy()
            tempButton = tk.Button(window, text="Ok", command=lambda: self.deleteData(keys, [self.tempwidgets[x].get() for x in
                                                                                      range(1, len(self.tempwidgets),
                                                                                            2)]))
            tempButton.grid(row=1, column=3)

    def updateTitle(self, name):
        self.dbTitleLabel.config(text=name)

    def leftPanel(self, frame):
        # Δημιουργία canva για να μπει η εικόνα
        self.canvaQuerry = tk.Canvas(frame, width=320, height=400)
        self.canvaQuerry.pack()
        self.canvaQuerry.pack_propagate(0)

        self.image3 = Image.open('LeftCard.png')  # Ανοιγμα της εικόνας με την βιβλιοθήκη Pillow
        self.background3 = ImageTk.PhotoImage(self.image3)  # Μετραπή σε εικόνα που διαβάζει η tkinter
        self.canvaQuerry.create_image(0, 0, anchor=tk.NW, image=self.background3)  # Ειαγωγή της εικόνας canva

        self.querryText = tk.Text(self.canvaQuerry, width=35, height=18,
                                  highlightthickness=0)  # Δημιουργία του text box για τα SQL querries
        self.querryText.config(state=tk.NORMAL)
        self.querry_window = self.canvaQuerry.create_window(18, 30, anchor=tk.NW, window=self.querryText)

        self.execSQlButton = tk.Button(self.canvaQuerry,
                                       text="ExequteSql")  # Κουμπί για να εκτελεστεί το περιεχόμενο του text box
        self.execSQlButton.configure(width=11, activebackground="#33B5E5", relief=tk.FLAT, font=BUTTON_FONT,
                                     anchor=tk.CENTER, background=BUTTON_COLOR_LEFT, fg=TEXT_COLOR,
                                     command=lambda: self.exeqSQL(self.cur))
        self.execSQlButton = self.canvaQuerry.create_window(18, 323, anchor=tk.NW, window=self.execSQlButton)

        self.clearButton = tk.Button(self.canvaQuerry, text="Clear")  # Κουμπί για να καθαρίσει το text box
        self.clearButton.configure(width=11, activebackground="#33B5E5", relief=tk.FLAT, font=BUTTON_FONT,
                                   anchor=tk.CENTER, background=BUTTON_COLOR_LEFT, fg=TEXT_COLOR,
                                   command=lambda: self.querryText.delete(1.0, tk.END))
        self.clearButton = self.canvaQuerry.create_window(171, 323, anchor=tk.NW, window=self.clearButton)

    def updateDB(self):
        # 'Ελεγχος για το αν η βάση ειναι ανοιχτή
        if self.isOPEN == 0:
            self.dbLoaderror(0)
            return
        cursor = self.cur
        # Επιλογή των ονομάτων των πινάκων της βάσης μεσω query
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_name = []  # Λιστα για την αποθήκευση των ονομάτων
        res = cursor.fetchall()
        for name in res:
            table_name.append(name[0])
        # Προσθήκη του αποτελέσματος του query στην λίστα table_names
        newWindow = tk.Toplevel(self.root)
        newWindow.title("Update")
        newWindow.geometry("300x320")

        self.table_combo = ttk.Combobox(newWindow,
                                        values=table_name)  # Δημιουργία combobox για τα ονοματα των πινάκων
        self.table_combo.current(0)
        self.table_combo.grid(row=0, column=2)

        self.selectButton = tk.Button(newWindow, text="Select",
                                      command=lambda: self.createTableData(newWindow)).grid(row=0,
                                                                                                      column=0)  # Δημιουργία του κουμπιού select για την δημιουργιά των rows με τα ονόματα
        self.clearWidgetButton = tk.Button(newWindow,
                                           text="Clear",
                                           command=lambda: self.clearWidgets(
                                               self.topWidgets))  # Δημιουργία του κουμπιου clear για την διαγραφή των υπαρχοντων widgets στο top window
        self.clearWidgetButton.grid(row=0, column=1)

    def appendDB(self):
        cursor = self.cur
        table_name = self.table_combo.get()  # το όνομα του πίνακα που θα κάνουμε ενημέρωση
        data = []  # λίστα για την τοποθέτηση των δεδομένων της πλειάδας
        names = []  # λίστα με τα ονόματα των στηλών της πλειάδας

        pks = self.getPrimaryKeys(self.cur)  # λήψη των primary keys
        # βρόχος με σκοπό τον διαχωρισμό των διαφόρων ειδών των widgets και των δεδομένων που πρεπει να λάβουμε τα δεδομένα στην
        # σωστή μορφή για την τοποθέτηση στην βάση
        for widget in self.topWidgets:
            if fnmatch.fnmatch(str(widget), '*dateentry*', ):
                date = widget.get_date()
                data.append(f'"{date.year}-{date.month}-{date.day}"')
            elif fnmatch.fnmatch(str(widget), '*entry*'):
                try:
                    value = int(widget.get())
                    data.append(value)
                except:
                    data.append(f'"{widget.get()}"')
            elif fnmatch.fnmatch(str(widget), '*combobox*', ):
                data.append(widget.get())
            elif fnmatch.fnmatch(str(widget), "*label*"):
                names.append(widget.cget("text"))
        # αφαιρούμε τις στήλες με τα πρωτεύοντα γνωρίσματα και τα ονόματα των στηλών αυτών
        # για να εκτελέσουμε το update query
        if len(pks) > 1:
            primary = f'{names[0]}={data[0]} and {names[1]}={data[1]}'
            names.remove(names[0])
            names.remove(names[1])
            data.remove(data[0])
            data.remove(data[1])
        else:
            primary = f'{names[0]}={data[0]}'
            names.remove(names[0])
            data.remove(data[0])

        # matching του κάθε ονόματος με το σωστό δεδομένο
        query_List = [f"{name}={data}" for name, data in zip(names, data)]
        # δημιουργία του query
        query = f'UPDATE {table_name} SET {",".join(query_List)} WHERE {primary};'
        # ενημέρωση της βάσης με try except
        try:
            cursor.execute(query)
            messagebox.showinfo("Succes", table_name + ' has been updated successfully!')
        except sql.Error as error:
            messagebox.showerror("Error", error)

    def setImage(self):
        fname = tk.filedialog.askopenfilename(
            filetypes=[("Image Files", ("*.jpg", "*.jpeg", "*.gif", "*.png")), ("All Files", "*.*")])
        if fname:
            with open(fname, "rb") as image:
                img_file = image.read()
                byte_stream = bytearray(img_file)
                self.imageData = byte_stream

    def getImage(self):
        return self.imageData

    def doubleCommand(self, master, fill, keys):
        self.clearWidgets(self.tempwidgets)
        self.createTableData(master, fill, keys)

    def createTableData(self, master=None, fill=0, pkeys=None):
        cursor = self.cur
        self.topWidgets = []  # λίστα με όλα τα widgets του top window
        self.stringEntries = []  # λίστα με τα stringvars του κάθε entry λογικά θα έχει κάθε τύπο Var
        self.rowData = []  # ονόματα των στηλών του πίνακα
        #  λεξικό με τους τύπους δεδομένων στην βάση χρησιμοποιώντας την ανώνυμη συνάρτηση lambda
        #  με σκοπό να τοποθετηθεί το σωστό textvariable σε κάθε δεδομένο όταν αυτό χρειάζεται
        widg_dict = {"INTEGER": lambda x: tk.Entry(master),
                     "BOOLEAN": lambda x: ttk.Combobox(master, value=("True", "False")),
                     "VARCHAR": lambda x: tk.Entry(master),
                     "TEXT": lambda x: tk.Entry(master),
                     "STRING": lambda x: tk.Entry(master),
                     "BLOB": lambda x: tk.Button(master, text="Choose", command=self.setImage),
                     "DECIMAL": lambda x: tk.Entry(master),
                     "DATE": lambda x: DateEntry(master, text="Pick Date", date_pattern='yyyy-mm-dd',
                                                 year=datetime.today().year, month=datetime.today().month,
                                                 day=datetime.today().day, textvariable=x),
                     "FLOAT": lambda x: tk.Entry(master),
                     }
        # λεξικό με τον τύπο του textvariable που θα χρησιμοποιθεί για την δημιουργία των widgets
        var_dict = {"INTEGER": lambda x: tk.IntVar(),
                    "BOOLEAN": lambda x: tk.BooleanVar(),
                    "VARCHAR": lambda x: tk.StringVar(),
                    "TEXT": lambda x: tk.StringVar(),
                    "STRING": lambda x: tk.StringVar(),
                    "BLOB": lambda x: None,
                    "DECIMAL": lambda x: tk.DoubleVar(),
                    "DATE": lambda x: x,
                    "FLOAT": lambda x: tk.DoubleVar(),
                    }

        try:
            curr_table = self.table_combo.get()
            querry = f"PRAGMA table_info({curr_table});"  # query για να πάρει τα ονόματα των rows του πίνακα
            cursor.execute(querry)  # κάνουμε το query
            res = cursor.fetchall()  # λαμβάνουμε τα δεδομένα
            for label in res:
                self.rowData.append(label)  # τοποθετούμε τα ονόματα των στηλών
        except sql.Error as error:
            messagebox.showerror("Error", error)
            return

        # Βρόχο για την δημιουργία των Labels και των Entries για τον κάθε πίνακα
        # Επίσης βολεύει να κρατάω χωριστά τα field names
        field_names = []
        ind = 0
        for ind, name in enumerate(self.rowData):

            if name[1] == 'reg_date':
                continue  # Skip reg_date δεν εισάγεται από τον χρήστη

            field_names.append(name[1])
            # name[1] είναι τα ονόματα των fields πχ. username, fname

            tempLabel = tk.Label(master, text=name[1])
            self.topWidgets.append(tempLabel)
            tempLabel.grid(row=2 + ind, column=0, columnspan=2, sticky='w')

            tempType = name[2].upper()
            finalType = tempType if tempType.find("(") == -1 else tempType[:tempType.find("(")]

            tempVar = var_dict[finalType](0)
            self.stringEntries.append(tempVar)
            temp = widg_dict[finalType](tempVar)
            self.topWidgets.append(temp)
            temp.grid(row=2 + ind, column=1, columnspan=2, sticky='e')
            ind += 2
            # Δημιουργία του κουμπιού updateSQL που λαμβάνει τα δεδομένα και τα στέλνει σην μέθοδο updateSQL

        insertButton = tk.Button(master, text="InsertSQL",
                                 command=lambda: self.fillDB(curr_table, field_names, self.topWidgets))
        insertButton.grid(row=ind + 2, column=0, columnspan=3)

        self.topWidgets.append(insertButton)
        # τα περιττά topWidgets είναι τα EntryObjects
        if fill == 1:
            self.setTableData(cursor, self.table_combo.get(), pkeys)
            self.topWidgets[-1].destroy()
            updateButton = tk.Button(master, text="UpdateSQL",
                                     command=self.appendDB)
            updateButton.grid(row=ind + 2, column=0, columnspan=3)
            self.topWidgets.append(updateButton)

    def setTableData(self, cursor, tableName, keys):
        # μέθοδος για την τοποθέτηση των δεδομένων στα κατάλληλα entry boxes η datentries όταν με σκοπό την ενημέρωση
        # της πλειάδας
        pks = self.getPrimaryKeys(cursor)
        # κάνουμε την ερώτηση στην βάση ανάλογα με τα πόσα primary keys έχει ο πίνακας
        if len(keys) > 1:
            query = f'select * from {tableName} where {pks[0]}={keys[0]} and {pks[1]}={keys[1]}'
        else:
            query = f'select * from {tableName} where {pks[0]}={keys[0]} '
        # με try except εκτελούμε το query  και λαμβάνουμε όλα τα δεδομένα του πίνακα,
        try:
            cursor.execute(query)
            results = cursor.fetchone()
            values = []
            if results is None:
                messagebox.showerror("Error", "No id matches your search!")
                return
            # τοποθετούμε τα αποτελέσματα του query στην λίστα values και αντικαθιστούμε το None με empty string
            for res in results:
                if res is None:
                    values.append("")
                else:
                    values.append(res)
            # στην περίπτωση που η πλειάδα ανήκει στον πίνακα User αγνοούμε την στήλη regdate γιατί υπολογίζεται από την βάση
            if tableName == 'User':
                values.remove(values[6])
            count = 0
            # τοποθετούμε τα δεδομένα ανάλογα με το είδος τους στα entries του topLevel παραθύρου
            for box_index in range(1, len(self.topWidgets), 2):

                if re.search('.+dateentry', str(self.topWidgets[box_index])):

                    temp = values[count].replace("-", "/").split("/")[::-1]
                    dt = datetime.strptime("/".join(temp), '%d/%m/%Y')
                    self.topWidgets[box_index].set_date(dt)
                else:
                    self.topWidgets[box_index].insert(tk.END, values[count])

                count += 1
        except sql.Error as error:
            messagebox.showerror("Error", error)

    def fillDB(self, curr_table, field_names, topWidgets):
        data = self.getWidgEntries(topWidgets)
        # εκτέλεση της μεθόδου για την λήψη των δεδομένων απο τα entries

        data_dict = {} # λεξικό για τα δεδομένα

        for i in range(len(data)):
            data_dict[field_names[i]] = data[i] # τοποθέτηση των δεδομένων σε μορφή λεξικού

        self.insData(self.cur, curr_table, data_dict) # μέθοδος για την εισαγωγή των δεδομένων στην βάση

    def getWidgEntries(self, topWidgets):
        # συνάρτηση για την λήψη δεδομένων απο τα entries
        data = []
        # επειδή τα δεδομένα στην λίστα με τα widgets είναι σε περιττή θέση λαμβάνουμε μόνο αυτά
        for box_index in range(1, len(topWidgets), 2):
            try:
                single_data = topWidgets[box_index].get()
            except:
                single_data = topWidgets[box_index].get_date()
            data.append(single_data)
        return data

    def buildQuery(self, table_name, data):
        '''
        :param table_name: όνομα του κάθε πίνακα
        :param data: δεδομένα σε μορφή λεξικού
        :return:
        '''
        query = '''INSERT INTO ''' + table_name + '''('''
        data_query = '''VALUES('''

        for key, value in data.items():

            if value == 'True':
                value = 1
            elif value == 'False':
                value = 0

            try:
                value = int(value)
            except:
                if self.checkNull(value):
                    continue
                value = '\'' + value + '\''

            query += key + ', '
            data_query += str(value) + ', '

        # μη - ντιτερμινιστικο reg_date omegalul
        if table_name == 'User':
            query += 'reg_date, '
            reg_date = date.today()
            data_query += '\'' + str(reg_date) + '\', '

        query = query[:-2]
        query += ''')'''
        data_query = data_query[:-2]
        data_query += ''');'''
        query += '''\n''' + data_query

        return query

    def insData(self, cur, table_name, data):
        '''
        :param cur: cursor object για την επικοινωνία με την βάση
        :param table_name: όνομα του πίνακα
        :param data: δεδομένα σε μορφή λίστας
        :return:
        '''
        query = self.buildQuery(table_name, data)
        # δημιουργία του query

        try:
            #εκτέλεση του query ενημέρωση της βάσης και διαγραφή των widgets στο παράθυο
            cur.execute(query)
            messagebox.showinfo('Success', 'Insertion  Complete')

            self.con.commit()
            self.clearWidgets(self.topWidgets)


        except sql.Error as error:
            messagebox.showerror("error", error)

        return 1

    def checkNull(self, value):
        if (value == 'NULL') or (value.replace(" ", "") == ""):
            return 1
        else:
            return 0

    def exeqSQL(self, cursor=None):

        if self.isOPEN == 0:
            self.dbLoaderror(0)
            return

        query = self.querryText.get("1.0", 'end-1c')
        first_word = query[:query.find(" ")]
        if first_word.upper() == "SELECT":
            self.queryBox(cursor)
            return
        else:
            try:
                cursor.execute(query)
                messagebox.showinfo("Success", "Query has been executed successfully")
            except sql.Error as error:
                messagebox.showerror("Querry Error", error)

    def queryBox(self, cursor):
        query = self.querryText.get("1.0", 'end-1c')
        self.queryResults(cursor, query)

    def queryResults(self, cursor, query):
        self.treeViewWindow = tk.Toplevel(self.root)
        self.treeViewWindow.title("SQL Results")
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) == 0:
                messagebox.showinfo("Empty Query", "The selection you have executed yielded no results")
                return

            # Treeview Style
            self.treeViewStyle = ttk.Style()
            self.treeViewStyle.theme_use('winnative')
            self.treeViewStyle.configure('myStyle.myTreeview.Heading', background="#33B5E5", foreground="black")
            self.treeViewStyle.layout("myStyle.myTreeview", [('myStyle.myTreeview.treearea', {'sticky': 'nswe'})])

            # Αρχικοποίηση TreeView
            self.treeView = ttk.Treeview(self.treeViewWindow, style='myStyle.myTreeview', show='headings')
            self.treeView.heading('#0', text='', anchor=tk.CENTER)
            self.treeView.column('#0', width=0, stretch=tk.YES)

            column_names = result[0].keys()

            self.treeView['columns'] = tuple(column_names)
            for name in column_names:
                self.treeView.column(name, anchor=tk.CENTER, width=150)
                self.treeView.heading(name, text=name, anchor=tk.CENTER)
            for ind, row in enumerate(result):
                temp = dict(row)

                self.treeView.insert("", tk.END, text=f'test{ind}', values=tuple(temp.values()))

            # Δημιουργία scrollbar
            self.scbar = ttk.Scrollbar(self.treeViewWindow, orient='vertical', command=self.treeView.yview)
            self.scbar.pack(side='right', fill='y')
            self.treeView.configure(yscrollcommand=self.scbar.set)

            # Κάνω τελευταίο pack το treeView για να πάρει τον υπόλοιπο χώρο
            self.treeView.pack(expand=True, fill='y')


        except sql.Error as error:
            messagebox.showerror("Querry Error", error)

    def browseButton(self):
        # 'Ελεγχος για το αν η βάση ειναι ανοιχτή
        if self.isOPEN == 0:
            self.dbLoaderror(0)
            return
        cursor = self.cur
        browseWindow = tk.Toplevel(self.root)
        browseWindow.title("Table Browser")
        browseWindow.geometry("300x100+400+400")

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = []  # Λιστα για την αποθήκευση των ονομάτων
        res = cursor.fetchall()
        for name in res:
            table_names.append(name[0])

        selected_table = tk.StringVar()
        self.table_combo = ttk.Combobox(browseWindow,
                                        values=table_names, textvariable=selected_table)
        self.table_combo.current(0)
        self.table_combo.pack(expand=tk.TRUE)

        self.selectBrowseButton = tk.Button(browseWindow, text="Select",
                                            command=lambda: self.browseTable(cursor, selected_table.get()))
        self.selectBrowseButton.pack(expand=tk.TRUE)

    def browseTable(self, cursor, table_name):
        query = 'SELECT * FROM ' + table_name
        self.queryResults(cursor, query)

    def deleteRow(self):
        if self.isOPEN == 0:
            self.dbLoaderror(0)
            return
        cursor = self.cur
        # Επιλογή των ονομάτων των πινάκων της βάσης μεσω query
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_name = []  # Λιστα για την αποθήκευση των ονομάτων
        res = cursor.fetchall()
        for name in res:
            table_name.append(name[0])
        # Προσθήκη του αποτελέσματος του query στην λίστα table_names
        window = tk.Toplevel(self.root)

        self.table_combo = ttk.Combobox(window,
                                        values=table_name)  # Δημιουργία combobox για τα ονοματα των πινάκων
        self.table_combo.current(0)
        self.table_combo.grid(row=0, column=2)
        self.getID = tk.Button(window, text="Select",
                               command=lambda: self.PKWidget(window, cursor,1)).grid(row=0,
                                                                                   column=0)  # Δημιουργία του κουμπιού select για την εμφάνιση του primary key του εκάστοτε πίνακα
        self.clearWidgetButton = tk.Button(window,
                                           text="Clear",
                                           command=lambda: self.clearWidgets(
                                               self.tempwidgets,
                                               self.topWidgets))  # Δημιουργία του κουμπιου clear για την διαγραφή των υπαρχοντων widgets στο top window
        self.clearWidgetButton.grid(row=0, column=1)

    def deleteData(self,keys,data):
        tableName = self.table_combo.get()

        if len(keys) > 1:
            query = f'delete from {tableName} where {keys[0]}={data[0]} and {keys[1]}={data[1]}'
        else:
            query = f'delete from {tableName} where {keys[0]}={data[0]} '
        try:
            self.cur.execute(query)
            messagebox.showinfo("Success", "Successful deletion")
        except sql.Error as error:
            messagebox.showerror("Error",error)

    def clearWidgets(self, *args):
        # Μέθοδος για το κουμπί clear , διαγράφει όλα τα widgets
        for widg_list in args:
            for widget in widg_list:
                widget.destroy()


    def exit(self):

        MsgBox = tk.messagebox.askquestion('Exit Application', 'Do you want to exit the application?',
                                           icon='warning')
        if MsgBox == 'yes':
            self.root.destroy()
        else:
            pass

    def init_gui(self):
        self.create_top_menu()
        self.createFrames()
        self.topPanel(self.titleFrame)
        self.rightPanel(self.buttonFrame)
        self.leftPanel(self.canvaFrame)


root = tk.Tk()
Application(root)
root.mainloop()

