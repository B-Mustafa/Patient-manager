import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from sqlite3 import Error
from datetime import date

# Create SQLite database connection
def create_connection():
    connection = None
    try:
        connection = sqlite3.connect("patient_records.db")
        print(f"Connected to SQLite version {sqlite3.version}")
        return connection
    except Error as e:
        print(f"Error: {e}")
    return connection

# Create the patient_records table if not exists
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patient_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                address TEXT,
                phone TEXT,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                prescription TEXT NOT NULL
            )
        ''')
        connection.commit()
        print("Table created successfully")
    except Error as e:
        print(f"Error creating table: {e}")

# Function to update the table with patient records
def update_table(connection, tree):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM patient_records")
        records = cursor.fetchall()

        # Clear the existing entries in the table
        for row in tree.get_children():
            tree.delete(row)

        # Insert new records into the table
        for record in records:
            tree.insert("", "end", values=record[1:])
    except Error as e:
        print(f"Error updating table: {e}")

# Function to add a new patient record to SQLite database
def add_patient_record(connection, first_name_entry, last_name_entry, age_entry, gender_var, address_entry, phone_entry, date_entry, description_entry, prescription_entry, tree):
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    age = age_entry.get()
    gender = gender_var.get()
    address = address_entry.get()
    phone = phone_entry.get()
    date = date_entry.get()
    description = description_entry.get("1.0", "end-1c")  # Get all content in the description text area
    prescription = prescription_entry.get("1.0", "end-1c")  # Get all content in the prescription text area

    if not first_name or not last_name or not date or not description or not prescription:
        messagebox.showerror("Error", "Please fill in all required fields.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO patient_records (first_name, last_name, age, gender, address, phone, date, description, prescription)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, age, gender, address, phone, date, description, prescription))
        connection.commit()
        messagebox.showinfo("Success", "Patient record added successfully.")
        clear_entry_fields(first_name_entry, last_name_entry, age_entry, gender_var, address_entry, phone_entry, date_entry, description_entry, prescription_entry)
        update_table(connection, tree)
    except Error as e:
        print(f"Error adding patient record: {e}")
        messagebox.showerror("Error", "Failed to add patient record.")

# Function to search for a specific patient record in SQLite database
def search_patient_record(connection, tree, search_query):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            SELECT * FROM patient_records
            WHERE LOWER(first_name) LIKE ? OR LOWER(last_name) LIKE ?
        ''', (f'%{search_query}%', f'%{search_query}%'))
        records = cursor.fetchall()

        # Clear the existing entries in the table
        for row in tree.get_children():
            tree.delete(row)

        # Insert new records into the table
        for record in records:
            tree.insert("", "end", values=record[1:])
    except Error as e:
        print(f"Error searching patient records: {e}")

# Function to update an existing patient record in SQLite database
def update_patient_record(connection, selected_record, first_name_entry, last_name_entry, age_entry, gender_var, address_entry, phone_entry, date_entry, description_entry, prescription_entry, tree):
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    age = age_entry.get()
    gender = gender_var.get()
    address = address_entry.get()
    phone = phone_entry.get()
    date = date_entry.get()
    description = description_entry.get("1.0", "end-1c")  # Get all content in the description text area
    prescription = prescription_entry.get("1.0", "end-1c")  # Get all content in the prescription text area

    if not first_name or not last_name or not date or not description or not prescription:
        messagebox.showerror("Error", "Please fill in all required fields.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute('''
            UPDATE patient_records
            SET first_name=?, last_name=?, age=?, gender=?, address=?, phone=?, date=?, description=?, prescription=?
            WHERE LOWER(first_name) LIKE ? OR LOWER(last_name) LIKE ?
        ''', (first_name, last_name, age, gender, address, phone, date, description, prescription, f'%{selected_record}%', f'%{selected_record}%'))
        connection.commit()
        messagebox.showinfo("Success", "Patient record updated successfully.")
        clear_entry_fields(first_name_entry, last_name_entry, age_entry, gender_var, address_entry, phone_entry, date_entry, description_entry, prescription_entry)
        update_table(connection, tree)
    except Error as e:
        print(f"Error updating patient record: {e}")
        messagebox.showerror("Error", "Failed to update patient record.")

# Function to edit the selected patient record
def edit_patient_record(connection, selected_record, first_name_entry, last_name_entry, age_entry, gender_var, address_entry, phone_entry, date_entry, description_entry, prescription_entry, tree):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            SELECT * FROM patient_records
            WHERE LOWER(first_name) LIKE ? OR LOWER(last_name) LIKE ?
        ''', (f'%{selected_record}%', f'%{selected_record}%'))
        record = cursor.fetchone()

        if record:
            # Clear the existing record
            clear_entry_fields(first_name_entry, last_name_entry, age_entry, gender_var, address_entry, phone_entry, date_entry, description_entry, prescription_entry)

            # Unpack the record and populate entry fields
            _, first_name, last_name, age, gender, address, phone, date, description, prescription = record
            first_name_entry.insert(tk.END, first_name)
            last_name_entry.insert(tk.END, last_name)
            age_entry.insert(tk.END, age)
            gender_var.set(gender)
            address_entry.insert(tk.END, address)
            phone_entry.insert(tk.END, phone)
            date_entry.insert(tk.END, date)
            description_entry.insert(tk.END, description)
            prescription_entry.insert(tk.END, prescription)
            messagebox.showinfo("Editing", "Editing selected record.")
        else:
            messagebox.showinfo("No Matches", "No matching patient records found to edit.")
    except Error as e:
        print(f"Error editing patient record: {e}")

# Function to delete a patient record
def delete_patient_record(connection, selected_record, tree):
    if not selected_record:
        messagebox.showinfo("No Selection", "Please select a record to delete.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute('''
            DELETE FROM patient_records
            WHERE LOWER(first_name) LIKE ? OR LOWER(last_name) LIKE ?
        ''', (f'%{selected_record}%', f'%{selected_record}%'))
        connection.commit()
        messagebox.showinfo("Success", "Patient record deleted successfully.")
        update_table(connection, tree)
    except Error as e:
        print(f"Error deleting patient record: {e}")
        messagebox.showerror("Error", "Failed to delete patient record.")

# Function to clear entry fields
def clear_entry_fields(first_name_entry, last_name_entry, age_entry, gender_var, address_entry, phone_entry, date_entry, description_entry, prescription_entry):
    first_name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    gender_var.set("Male")  # Set default gender to Male
    address_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    date_entry.insert(0, date.today())  # Set default date to current date
    description_entry.delete("1.0", tk.END)
    prescription_entry.delete("1.0", tk.END)

# Main function
def main():
    # Initialize the SQLite connection and create the table
    connection = create_connection()
    if connection:
        create_table(connection)

    # Create a Tkinter window
    window = tk.Tk()
    window.title("Saifee Homeopathic Clinic")

    # Create a canvas to contain the entire content of the window
    canvas = tk.Canvas(window)
    canvas.pack(side="left", fill="both", expand=True)

    # Create a frame to place inside the canvas
    content_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    # Add a vertical scrollbar
    scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create labels and entry fields for patient information
    first_name_label = tk.Label(content_frame, text="First Name:")
    first_name_entry = tk.Entry(content_frame)

    last_name_label = tk.Label(content_frame, text="Last Name:")
    last_name_entry = tk.Entry(content_frame)

    age_label = tk.Label(content_frame, text="Age:")
    age_entry = tk.Entry(content_frame)

    gender_label = tk.Label(content_frame, text="Gender:")
    gender_var = tk.StringVar()
    gender_var.set("Male")  # Set default gender to Male
    gender_male_radio = tk.Radiobutton(content_frame, text="Male", variable=gender_var, value="Male")
    gender_female_radio = tk.Radiobutton(content_frame, text="Female", variable=gender_var, value="Female")

    address_label = tk.Label(content_frame, text="Address:")
    address_entry = tk.Entry(content_frame)

    phone_label = tk.Label(content_frame, text="Phone:")
    phone_entry = tk.Entry(content_frame)

    date_label = tk.Label(content_frame, text="Date:")
    date_entry = tk.Entry(content_frame)
    date_entry.insert(0, date.today())  # Set default date to current date

    description_label = tk.Label(content_frame, text="Description:")
    description_entry = tk.Text(content_frame, height=5, width=40, wrap="word")  # Use Text widget for multi-line input

    prescription_label = tk.Label(content_frame, text="Prescription:")
    prescription_entry = tk.Text(content_frame, height=5, width=40, wrap="word")  # Use Text widget for multi-line input

    add_button = tk.Button(content_frame, text="Add Record", command=lambda: add_patient_record(connection,
                                                                                        first_name_entry,
                                                                                        last_name_entry,
                                                                                        age_entry,
                                                                                        gender_var,
                                                                                        address_entry,
                                                                                        phone_entry,
                                                                                        date_entry,
                                                                                        description_entry,
                                                                                        prescription_entry,
                                                                                        tree))

    search_label = tk.Label(content_frame, text="Search Patient:")
    search_entry = tk.Entry(content_frame)

    search_button = tk.Button(content_frame, text="Search", command=lambda: search_patient_record(connection, tree, search_entry.get().lower()))

    edit_label = tk.Label(content_frame, text="Edit Record:")
    edit_entry = tk.Entry(content_frame)

    edit_button = tk.Button(content_frame, text="Re-visit", command=lambda: edit_patient_record(connection,
                                                                                  edit_entry.get(),
                                                                                  first_name_entry,
                                                                                  last_name_entry,
                                                                                  age_entry,
                                                                                  gender_var,
                                                                                  address_entry,
                                                                                  phone_entry,
                                                                                  date_entry,
                                                                                  description_entry,
                                                                                  prescription_entry,
                                                                                  tree))

    update_button = tk.Button(content_frame, text="Update", command=lambda: update_patient_record(connection,
                                                                                        edit_entry.get(),
                                                                                        first_name_entry,
                                                                                        last_name_entry,
                                                                                        age_entry,
                                                                                        gender_var,
                                                                                        address_entry,
                                                                                        phone_entry,
                                                                                        date_entry,
                                                                                        description_entry,
                                                                                        prescription_entry,
                                                                                        tree))

    delete_button = tk.Button(content_frame, text="Delete", command=lambda: delete_patient_record(connection,
                                                                                      edit_entry.get(),
                                                                                      tree))

    display_text = tk.Label(content_frame, text="", justify="left")

    # Create a Treeview widget for displaying records in a table
    tree = ttk.Treeview(content_frame, columns=("First Name", "Last Name", "Age", "Gender", "Address", "Phone", "Date", "Description", "Prescription"), show="headings")

    # Define the headings for the columns
    tree.heading("First Name", text="First Name")
    tree.heading("Last Name", text="Last Name")
    tree.heading("Age", text="Age")
    tree.heading("Gender", text="Gender")
    tree.heading("Address", text="Address")
    tree.heading("Phone", text="Phone")
    tree.heading("Date", text="Date")
    tree.heading("Description", text="Description")
    tree.heading("Prescription", text="Prescription")

    # Pack the Treeview widget
    tree.pack()

    # Pack the other widgets
    first_name_label.pack()
    first_name_entry.pack()
    last_name_label.pack()
    last_name_entry.pack()
    age_label.pack()
    age_entry.pack()
    gender_label.pack()
    gender_male_radio.pack()
    gender_female_radio.pack()
    address_label.pack()
    address_entry.pack()
    phone_label.pack()
    phone_entry.pack()
    date_label.pack()
    date_entry.pack()
    description_label.pack()
    description_entry.pack()
    prescription_label.pack()
    prescription_entry.pack()
    add_button.pack()
    search_label.pack()
    search_entry.pack()
    search_button.pack()
    edit_label.pack()
    edit_entry.pack()
    edit_button.pack()
    update_button.pack()
    delete_button.pack()
    display_text.pack()

    # Update the canvas scroll region when the content frame changes size
    content_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Main loop
    window.mainloop()

    # Close the SQLite connection when the application is closed
    if connection:
        connection.close()

if __name__ == "__main__":
    main()
