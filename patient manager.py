import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, QRadioButton, QTreeWidget, QTreeWidgetItem, QTextEdit, QFileDialog, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt, QDate
import sqlite3
from sqlite3 import Error
import os
import shutil
import pandas as pd
import openpyxl
import json


class PatientRecordApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Saifee Homeopathic Clinic")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.init_ui()

        self.display_text = QLabel()

        self.connection = self.create_connection()
        if self.connection:
            self.create_table(self.connection)

        self.periodic_backup()

    def init_ui(self):
        layout = QGridLayout()

        first_name_label = QLabel("First Name:")
        self.first_name_entry = QLineEdit()

        last_name_label = QLabel("Last Name:")
        self.last_name_entry = QLineEdit()

        age_label = QLabel("Age:")
        self.age_entry = QLineEdit()

        gender_label = QLabel("Gender:")
        self.gender_male_radio = QRadioButton("Male")
        self.gender_female_radio = QRadioButton("Female")

        address_label = QLabel("Address:")
        self.address_entry = QLineEdit()

        phone_label = QLabel("Phone:")
        self.phone_entry = QLineEdit()

        date_label = QLabel("Date:")
        self.date_entry = QLineEdit()
        self.date_entry.setText(QDate.currentDate().toString(Qt.ISODate))

        description_label = QLabel("Description:")
        self.description_entry = QTextEdit()

        prescription_label = QLabel("Prescription:")
        self.prescription_entry = QTextEdit()

        add_button = QPushButton("Add Record")
        add_button.clicked.connect(self.add_patient_record)

        search_label = QLabel("Search Patient:")
        self.search_entry = QLineEdit()

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_patient_record)

        edit_label = QLabel("Edit Record:")
        self.edit_entry = QLineEdit()

        edit_button = QPushButton("Re-visit")
        edit_button.clicked.connect(self.edit_patient_record)

        update_button = QPushButton("Update")
        update_button.clicked.connect(self.update_patient_record)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_patient_record)

        display_text = QLabel("")

        # Create a QTreeWidget for displaying records in a table
        self.tree = QTreeWidget()
        self.tree.setColumnCount(9)
        self.tree.setHeaderLabels(["First Name", "Last Name", "Age", "Gender", "Address", "Phone", "Date", "Description", "Prescription"])

        layout.addWidget(first_name_label, 0, 0 )
        layout.addWidget(self.first_name_entry, 0, 1)
        layout.addWidget(last_name_label, 1, 0)
        layout.addWidget(self.last_name_entry, 1, 1)
        layout.addWidget(age_label, 2, 0)
        layout.addWidget(self.age_entry, 2, 1)
        layout.addWidget(gender_label, 3, 0)
        layout.addWidget(self.gender_male_radio, 3, 1)
        layout.addWidget(self.gender_female_radio, 3, 2)
        layout.addWidget(address_label, 4, 0)
        layout.addWidget(self.address_entry, 4, 1)
        layout.addWidget(phone_label, 5, 0)
        layout.addWidget(self.phone_entry, 5, 1)
        layout.addWidget(date_label, 6, 0)
        layout.addWidget(self.date_entry, 6, 1)
        layout.addWidget(description_label, 7, 0)
        layout.addWidget(self.description_entry, 7, 1)
        layout.addWidget(prescription_label, 8, 0)
        layout.addWidget(self.prescription_entry, 8, 1)
        layout.addWidget(add_button, 9, 0)

        layout.addWidget(search_label, 10, 0)
        layout.addWidget(self.search_entry, 10, 1)
        layout.addWidget(search_button, 11, 0)

        layout.addWidget(edit_label, 12, 0)
        layout.addWidget(self.edit_entry, 12, 1)
        layout.addWidget(edit_button, 13, 0)
        layout.addWidget(update_button, 13, 1)
        layout.addWidget(delete_button, 13, 2)

        layout.addWidget(display_text, 14, 0, 1, 3)

        layout.addWidget(self.tree, 15, 0, 1, 3)

        import_button = QPushButton("Import Data")
        import_button.clicked.connect(self.import_data)
        layout.addWidget(import_button, 16, 0, 1, 3)

        self.central_widget.setLayout(layout)

    def create_connection(self):
        connection = None
        try:
            connection = sqlite3.connect("patient_records.db")
            print(f"Connected to SQLite version {sqlite3.version}")
            return connection
        except Error as e:
            print(f"Error: {e}")
            return connection

    def create_table(self, connection):
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

    def update_table(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM patient_records")
            records = cursor.fetchall()

            # Clear the existing entries in the table
            self.tree.clear()

            # Insert new records into the table
            for record in records:
                item = QTreeWidgetItem([str(field) for field in record[1:]])
                self.tree.addTopLevelItem(item)
        except Error as e:
            print(f"Error updating table: {e}")

    def update_backup(self):
        try:
            backup_folder = "backup"
            backup_db_path = os.path.join(backup_folder, "patient_records_backup.db")
            backup_excel_path = os.path.join(backup_folder, "patient_records_backup.xlsx")

            shutil.copy2("patient_records.db", backup_db_path)

            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM patient_records")
            records = cursor.fetchall()

            df = pd.DataFrame(records, columns=["ID", "First Name", "Last Name", "Age", "Gender", "Address", "Phone", "Date", "Description", "Prescription"])
            df.to_excel(backup_excel_path, index=False)

            QMessageBox.information(self, "Backup Updated", "Backup updated successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update backup: {e}")

    def add_patient_record(self):
        first_name = self.first_name_entry.text()
        last_name = self.last_name_entry.text()
        age = self.age_entry.text()
        gender = "Male" if self.gender_male_radio.isChecked() else "Female"
        address = self.address_entry.text()
        phone = self.phone_entry.text()
        date = self.date_entry.text()
        description = self.description_entry.toPlainText()
        prescription = self.prescription_entry.toPlainText()

        if not first_name or not last_name or not date or not description or not prescription:
            QMessageBox.warning(self, "Error", "Please fill in all required fields.")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO patient_records (first_name, last_name, age, gender, address, phone, date, description, prescription)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (first_name, last_name, age, gender, address, phone, date, description, prescription))
            self.connection.commit()
            QMessageBox.information(self, "Success", "Patient record added successfully.")
            self.clear_entry_fields()
            self.update_table()

            self.update_backup()
            self.create_backup()
        except Error as e:
            print(f"Error adding patient record: {e}")
            QMessageBox.critical(self, "Error", "Failed to add patient record.")

    def update_patient_record(self):
        selected_record = self.edit_entry.text()
        if not selected_record:
            QMessageBox.information(self, "No Selection", "Please enter a record to edit.")
            return

        first_name = self.first_name_entry.text()
        last_name = self.last_name_entry.text()
        age = self.age_entry.text()
        gender = "Male" if self.gender_male_radio.isChecked() else "Female"
        address = self.address_entry.text()
        phone = self.phone_entry.text()
        date = self.date_entry.text()
        description = self.description_entry.toPlainText()
        prescription = self.prescription_entry.toPlainText()

        if not first_name or not last_name or not date or not description or not prescription:
            QMessageBox.warning(self, "Error", "Please fill in all required fields.")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                UPDATE patient_records
                SET first_name=?, last_name=?, age=?, gender=?, address=?, phone=?, date=?, description=?, prescription=?
                WHERE LOWER(first_name) LIKE ? OR LOWER(last_name) LIKE ?
            ''', (first_name, last_name, age, gender, address, phone, date, description, prescription, f'%{selected_record}%', f'%{selected_record}%'))
            self.connection.commit()
            QMessageBox.information(self, "Success", "Patient record updated successfully.")
            self.clear_entry_fields()
            self.update_table()

            self.update_backup()
            self.create_backup()
        except Error as e:
            print(f"Error updating patient record: {e}")
            QMessageBox.critical(self, "Error", "Failed to update patient record.")

    def search_patient_record(self):
        search_query = self.search_entry.text().lower()
        if not search_query:
            QMessageBox.warning(self, "Empty Search", "Please enter a search query.")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT * FROM patient_records
                WHERE LOWER(first_name) LIKE ? OR LOWER(last_name) LIKE ?
            ''', (f'%{search_query}%', f'%{search_query}%'))
            records = cursor.fetchall()

            self.tree.clear()

            if records:
                for record in records:
                    item = QTreeWidgetItem([str(field) for field in record[1:]])
                    self.tree.addTopLevelItem(item)
            else:
                QMessageBox.information(self, "No Matches", "No matching patient records found.")

        except Error as e:
            print(f"Error searching patient records: {e}")

    def edit_patient_record(self):
        selected_record = self.edit_entry.text()
        if not selected_record:
            QMessageBox.information(self, "No Selection", "Please enter a record to edit.")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT * FROM patient_records
                WHERE LOWER(first_name) LIKE ? OR LOWER(last_name) LIKE ?
            ''', (f'%{selected_record}%', f'%{selected_record}%'))
            record = cursor.fetchone()

            if record:
                self.clear_entry_fields()

                _, first_name, last_name, age, gender, address, phone, date, description, prescription = record
                self.first_name_entry.setText(first_name)
                self.last_name_entry.setText(last_name)
                self.age_entry.setText(str(age))
                if gender.lower() == "male":
                    self.gender_male_radio.setChecked(True)
                else:
                    self.gender_female_radio.setChecked(True)
                self.address_entry.setText(address)
                self.phone_entry.setText(phone)
                self.date_entry.setText(date)
                self.description_entry.setPlainText(description)
                self.prescription_entry.setPlainText(prescription)
                QMessageBox.information(self, "Editing", "Editing selected record.")
            else:
                QMessageBox.information(self, "No Matches", "No matching patient records found to edit.")
                self.tree.clear()
        except Error as e:
            print(f"Error editing patient record: {e}")

    def delete_patient_record(self):
        selected_record = self.edit_entry.text()
        if not selected_record:
            QMessageBox.information(self, "No Selection", "Please enter a record to delete.")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                DELETE FROM patient_records
                WHERE LOWER(first_name) LIKE ? OR LOWER(last_name) LIKE ?
            ''', (f'%{selected_record}%', f'%{selected_record}%'))
            self.connection.commit()
            QMessageBox.information(self, "Success", "Patient record deleted successfully.")
            self.tree.clear()
        except Error as e:
            print(f"Error deleting patient record: {e}")
            QMessageBox.critical(self, "Error", "Failed to delete patient record.")

    def clear_entry_fields(self):
        self.first_name_entry.clear()
        self.last_name_entry.clear()
        self.age_entry.clear()
        self.gender_male_radio.setChecked(True) 
        self.address_entry.clear()
        self.phone_entry.clear()
        self.date_entry.setText(QDate.currentDate().toString(Qt.ISODate))  
        self.description_entry.clear()
        self.prescription_entry.clear()

    def periodic_backup(self):
        self.create_backup()
        self.startTimer(86400000)  # Set timer for 24 hours (in milliseconds)

    def timerEvent(self, event):
        self.create_backup()

    def get_backup_folder(self):
        try:
            with open("config.json", "r") as config_file:
                config = json.load(config_file)
                return config.get("backup_folder")
        except FileNotFoundError:
            return None

    def set_backup_folder(self, backup_folder):
        config = {"backup_folder": backup_folder}
        with open("config.json", "w") as config_file:
            json.dump(config, config_file)
    

    def ask_backup_folder(self):
        backup_folder = QFileDialog.getExistingDirectory(self, "Select Backup Folder")
        if backup_folder:
            self.set_backup_folder(backup_folder)
        return backup_folder

   # Function to create a backup of the SQLite database
    def create_backup(self):
        backup_folder_path = self.get_backup_folder()

        if not backup_folder_path:
            backup_folder_path = self.ask_backup_folder()
            if not backup_folder_path:
                return  # User canceled the backup

            self.set_backup_folder(backup_folder_path)  # Store the backup folder path

        try:
            os.makedirs(backup_folder_path, exist_ok=True)

            shutil.copy2("patient_records.db", os.path.join(backup_folder_path, "patient_records_backup.db"))

            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM patient_records")
            records = cursor.fetchall()

            df = pd.DataFrame(records, columns=["ID", "First Name", "Last Name", "Age", "Gender", "Address", "Phone", "Date", "Description", "Prescription"])
            df.to_excel(os.path.join(backup_folder_path, "patient_records_backup.xlsx"), index=False)

            QMessageBox.information(self, "Backup Created", f"Backup created successfully in {backup_folder_path}.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create backup: {e}")


    def import_data(self):
        try:
            backup_folder = "backup"

            import_file_path, _ = QFileDialog.getOpenFileName(self, "Select Import File", "", "Excel files (*.xlsx);;All files (*)")

            if not import_file_path:
                return 

            connection = self.create_connection()
            if connection:
                df = pd.read_excel(import_file_path)

                cursor = connection.cursor()
                cursor.execute("DELETE FROM patient_records")

                for _, row in df.iterrows():
                    cursor.execute('''
                        INSERT INTO patient_records (first_name, last_name, age, gender, address, phone, date, description, prescription)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (row["First Name"], row["Last Name"], row["Age"], row["Gender"], row["Address"], row["Phone"], row["Date"], row["Description"], row["Prescription"]))

                connection.commit()
                connection.close()

            self.display_text.setText("Data imported successfully.")
        except Exception as e:
            self.display_text.setText(f"Failed to import data: {e}")

    def periodic_backup(self):
        self.create_backup()
        self.startTimer(86400000, Qt.VeryCoarseTimer)  # Set timer for 24 hours (in milliseconds)

    def timerEvent(self, event):
        self.create_backup()

    def closeEvent(self, event):
        if self.connection:
            self.connection.close()


if __name__ == "__main__":
    app = QApplication([])
    window = PatientRecordApp()
    window.show()
    app.exec_()

    
