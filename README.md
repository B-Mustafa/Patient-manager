# Patient Manager Software

Patient Manager is a comprehensive application designed to assist healthcare professionals in efficiently managing patient records. The software features an intuitive graphical user interface built with PyQt5 and utilizes SQLite for database management.

## Features

### 1. Intuitive Interface

The software provides a clean and user-friendly interface, ensuring easy navigation and a positive user experience.

### 2. Patient Information Management

Efficiently record and manage detailed patient information, including:
- First Name
- Last Name
- Age
- Gender
- Address
- Phone
- Date of Visit
- Medical Description
- Prescription Details

### 3. Search and Filter

Quickly search and filter patient records based on various criteria, making it easy to retrieve specific information when needed.

### 4. Appointment Scheduling

The application includes a feature for scheduling and managing patient appointments, helping healthcare professionals organize their workflow.

### 5. Data Security

Patient data is securely stored in a SQLite database, ensuring confidentiality and compliance with privacy regulations.

### 6. Backup and Restore

The software incorporates periodic backup functionality to safeguard patient data. This feature creates backups at regular intervals, providing an extra layer of protection against data loss.

## Getting Started

### Prerequisites

- [Python](https://www.python.org/) (version 3.12.0)
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/download) (version 5.15.10)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/B-Mustafa/patient-manager.git
   ```

2. Install dependencies:

   ```bash
   pip install PyQt5
   ```

### Usage

1. Navigate to the project directory:

   ```bash
   cd patient-manager
   ```

2. Run the Patient Manager:

   ```bash
   python "patient manager.py"
   ```

## Usage Guide

1. **Add Patient Record**: Enter patient information and click "Add Record" to save the record.

2. **Search Patient Record**: Enter a search query and click "Search" to find matching patient records.

3. **Edit Patient Record**: Enter the patient's name to edit the corresponding record. Click "Re-visit" to populate the fields for editing. Make changes and click "Update."

4. **Delete Patient Record**: Enter the patient's name and click "Delete" to remove the corresponding record.

5. **Import Data**: Click "Import Data" to import patient records from an Excel file.

6. **Periodic Backup**: The application automatically creates a backup every 24 hours.

## Preview
[(img.png)]

## Contributing

If you'd like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Create a new pull request.

## License

This project is licensed under the [MIT License](LICENSE.md).

## Acknowledgments

- Thanks to [PyQt](https://www.riverbankcomputing.com/software/pyqt/) for providing the GUI framework.

## Contact

For support or inquiries, please contact [bhikhapurmustafa@gmail.com].



