# AI-DOMUS Project App

A Streamlit web application integrated with MySQL for managing client information and caseworker assessments under the **Newham Project** initiative.

---

## Overview
AI DOMUS (Latin for "home") is designed to support housing and community services through digital tools. This app enables:
- Adding new client records with a unique `ClientCode` format: `DOMUS<YEAR><SEQ>`.
- Collecting detailed client information via user-friendly forms.
- Viewing all client records in a sortable, filterable table.
- Managing household members, assessments, and case management.

---

## Features
✅ Auto-generate unique ClientCode  
✅ Multi-step forms for client details, household members, and assessments  
✅ Interactive data table with search and filter options  
✅ Download filtered data as CSV  

---

## Tech Stack
- **Frontend:** Streamlit
- **Backend:** Python, MySQL
- **Libraries:** Pandas, mysql-connector-python, python-dotenv

---

## Project Structure
```
AI-DOMUS_Project_app/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .gitignore          # Ignore .env and cache files
└── README.md           # Project documentation
```

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/RamyaShrawan/AI-DOMUS_Project_app.git
cd AI-DOMUS_Project_app
```

### 2. Create Virtual Environment (Optional)
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=newham_project
```

### 5. Set Up MySQL Database
Run these commands in MySQL:
```sql
CREATE DATABASE newham_project;
USE newham_project;

CREATE TABLE Client (
    ClientCode VARCHAR(50) NOT NULL PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    DateOfBirth DATE,
    PhoneNumber VARCHAR(20),
    Email VARCHAR(100),
    Nationality VARCHAR(50),
    ImmigrationStatus VARCHAR(100),
    MaritalStatus VARCHAR(30),
    EmploymentStatus VARCHAR(50),
    ReasonForHomelessness VARCHAR(200),
    LocalConnection TINYINT(1),
    SpecilNotes VARCHAR(255)
);
```

### 6. Run the App
```bash
streamlit run app.py
```
Access the app at: `http://localhost:8501`

---

## Next Steps
- Add forms for Household Members, Assessments, and Case Management.
- Deploy on **Streamlit Cloud** or **Docker** for easy access.

---

## License
This project is for educational and community purposes under the Newham Project initiative.
