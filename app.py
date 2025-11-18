
from dotenv import load_dotenv
from datetime import datetime, date
import os



# ---------------- DATABASE CONNECTION ----------------

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


# Generate ClientCode: DOMUS<YEAR><SEQ>
def generate_client_code():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Client")
    seq_number = cursor.fetchone()[0] + 1
    cursor.close()
    conn.close()
    year = datetime.now().year
    return f"DOMUS{year}{seq_number}"

 #---------------- FETCH CASEWORKER IDs ----------------
def get_caseworker_ids():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT CaseworkerID FROM Caseworker")
    ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return ids

# ---------------- FETCH CASEWORKER NAMES ----------------
def get_caseworker_names():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT FirstName, LastName FROM Caseworker WHERE ActiveStatus = 1")
    names = [f"{row[0]} {row[1]}" for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return names


# ---------------- PAGE TITLE ----------------
st.markdown("<h1 style='text-align:center;'>AI DOMUS</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;color:gray;'>Caseworker Assessment System</h3>", unsafe_allow_html=True)

# ---------------- SIDEBAR NAVIGATION ----------------
page = st.sidebar.radio("Navigation", ["Client Info", "Household Members", "Assessments", "Case Management", "View Clients"])

# ---------------- CLIENT INFO ----------------
if page == "Client Info":
    st.markdown("<h4 style='color:#2E86C1;'>Step 1: Client Information</h4>", unsafe_allow_html=True)
    with st.form("client_form"):
        fname = st.text_input("First Name")
        lname = st.text_input("Last Name")
        dob = st.date_input("Date of Birth", min_value=date(1900,1,1), max_value=date.today())
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        phone = st.text_input("Phone Number")
        email = st.text_input("Email")
        nationality = st.text_input("Nationality")
        immigration_status = st.selectbox("Immigration Status", [
            "UK National", "Irish Citizen", "EU Settled Status", "EU Pre-Settled Status",
            "ILR", "Work Visa", "Family Visa", "Student Visa", "Asylum Seeker", "Refugee Status", "Other"
        ])
        marital_status = st.selectbox("Marital Status", ["Single", "Married", "Separated", "Divorced", "Widowed"])
        employment_status = st.selectbox("Employment Status", ["Employed", "Unemployed", "Student", "Retired", "Other"])
        reason_homelessness = st.text_area("Reason for Homelessness")
        specil_notes = st.text_area("Special Notes")
        education_needs = st.text_area("Education Needs")
        recreation_needs = st.text_area("Recreation Needs")
        medical_needs = st.text_area("Medical Needs")
        hospital_needs = st.text_area("Hospital Needs")
        other_needs = st.text_area("Other Needs")
        
        
        # Dropdown for Caseworker ID
        caseworker_ids = get_caseworker_ids()
        caseworker_id = st.selectbox("Select Caseworker ID", caseworker_ids)

        local_connection = st.checkbox("Local Connection to Borough")

        submit_client = st.form_submit_button("Save & Continue")

        if submit_client:
            client_code = generate_client_code()
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO Client (
                    ClientCode, FirstName, LastName, DateOfBirth, Gender, PhoneNumber, Email, Nationality,
                    ImmigrationStatus, MaritalStatus, EmploymentStatus, ReasonForHomelessness, SpecilNotes,
                    EducationNeeds, RecreationNeeds, MedicalNeeds, HospitalNeeds, OtherNeeds, CaseworkerID, LocalConnection
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                client_code, fname, lname, dob, gender, phone, email, nationality, immigration_status,
                marital_status, employment_status, reason_homelessness, specil_notes, education_needs,
                recreation_needs, medical_needs, hospital_needs, other_needs, caseworker_id, local_connection
            ))

            conn.commit()
            cursor.close()
            conn.close()
            st.session_state.client_id = client_code
            st.success(f"Client saved with ID: {client_code}")
            st.info("Please go to 'Household Members' in the sidebar to continue.")

# ---------------- HOUSEHOLD MEMBERS ----------------
elif page == "Household Members":
    st.markdown("<h4 style='color:#2E86C1;'>Step 2: Household Members</h4>", unsafe_allow_html=True)

    if "client_id" in st.session_state:
        st.info(f"Adding members for Client: {st.session_state.client_id}")

        num_members = st.number_input("Number of Household Members", min_value=1, max_value=10, step=1)

        with st.form("household_form"):
            members = []

            for i in range(num_members):
                st.markdown(f"### Member {i+1}")

                # Inputs
                name = st.text_input(f"Name{i+1}", key=f"name_{i}")
                relationship = st.selectbox(f"Relationship to Client{i+1}", ["Child", "Spouse", "Partner", "Other"], key=f"rel_{i}")
                gender = st.selectbox(f"Gender {i+1}", ["Male", "Female", "Other"], key=f"gender_{i}")
                dob = st.date_input(f"Date of Birth {i+1}", min_value=date(1900, 1, 1), max_value=date.today(), key=f"dob_{i}")
                vulnerabilities = st.text_area(f"Vulnerabilities{i+1}", key=f"vul_{i}")

                # Calculate Age
                today = date.today()
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

                # Determine Age Range
                if age < 10:
                    age_range = "Below 10"
                elif age < 16:
                    age_range = "Below 16"
                else:
                    age_range = "16 or Above"

                # Display Age Info
                st.write(f"**Calculated Age:** {age} years")
                st.write(f"**Age Range:** {age_range}")

                # Append member data
                members.append((name, relationship, gender, dob, age, age_range, vulnerabilities))

            # Submit Button
            submit_members = st.form_submit_button("Save & Continue")

            if submit_members:
                conn = get_connection()
                cursor = conn.cursor()

                for member in members:
                    cursor.execute("""
                        INSERT INTO HouseholdMemberstoClient
                        (ClientCode, Name, RelationshipToClient, Gender, DateOfBirth, Age, AgeRange, Vulnerabilities)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                    """, (st.session_state.client_id, member[0], member[1], member[2], member[3], member[4], member[5], member[6]))

                conn.commit()
                cursor.close()
                conn.close()

                st.success(f"{num_members} household members saved successfully!")
                st.info("Please go to 'Assessments' in the sidebar to continue.")
    else:
        st.warning("Please complete Client Info first.")

# ---------------- ASSESSMENTS ----------------
elif page == "Assessments":
    st.markdown("<h4 style='color:#2E86C1;'>Step 3: Assessment Details</h4>", unsafe_allow_html=True)
    if "client_id" in st.session_state:
        st.info(f"Adding assessment for Client: {st.session_state.client_id}")
        with st.form("assessment_form"):
            current_housing = st.selectbox("Current Housing Type", ["Sofa Surfing", "Temporary Accommodation", "Private Rent", "Family Home"])
            date_problem_started = st.date_input("Date Problem Started")
            safe_to_remain = st.checkbox("Safe to Remain?")
            notice_given = st.checkbox("Notice Given?")
            notice_type = st.text_input("Notice Type")
            physical_health = st.text_area("Physical Health Issues")
            mental_health = st.text_area("Mental Health Issues")
            children_special_needs = st.text_area("Children Special Needs")
            income_source = st.selectbox("Income Source", ["Job", "Benefits", "None"])
            weekly_income = st.number_input("Weekly Income (£)", min_value=0.0)
            rent_arrears = st.number_input("Rent Arrears (£)", min_value=0.0)
            debts = st.number_input("Debts (£)", min_value=0.0)
            emergency_needed = st.checkbox("Emergency Accommodation Needed?")
            submit_assessment = st.form_submit_button("Save & Continue")

            if submit_assessment:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO Assessments (
                        ClientCode, CurrentHousingType, DateProblemStarted, SafeToRemain, NoticeGiven,
                        NoticeType, PhysicalHealthIssues, MentalHealthIssues, ChildrenSpecialNeeds,
                        IncomeSource, WeeklyIncome, RentArrears, Debts, EmergencyAccommodationNeeded
                    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (
                    st.session_state.client_id, current_housing, date_problem_started, safe_to_remain,
                    notice_given, notice_type, physical_health, mental_health, children_special_needs,
                    income_source, weekly_income, rent_arrears, debts, emergency_needed
                ))
                conn.commit()
                cursor.close()
                conn.close()
                st.success("Assessment saved successfully!")
                st.info("Please go to 'Case Management' in the sidebar to continue.")
    else:
        st.warning("Please complete Client Info first.")


# ---------------- CASE MANAGEMENT ----------------
elif page == "Case Management":
    st.markdown("<h4 style='color:#2E86C1;'>Step 4: Case Management</h4>", unsafe_allow_html=True)
    if "client_id" in st.session_state:
        st.info(f"Managing case for Client: {st.session_state.client_id}")
        with st.form("case_form"):
           # Dropdown for Assigned Caseworker
            caseworker_names = get_caseworker_names()
            assigned_caseworker = st.selectbox("Assigned Caseworker", caseworker_names)
            personal_plan = st.text_area("Personal Housing Plan")
            emergency_provided = st.checkbox("Emergency Accommodation Provided?")
            case_status = st.selectbox("Case Status", ["Open", "In Progress", "Closed"])
            submit_case = st.form_submit_button("Save Case Management")

            if submit_case:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO CaseManagement (
                        ClientCode, AssignedCaseworker, PersonalHousingPlan,
                        EmergencyAccommodationProvided, CaseStatus
                    ) VALUES (%s,%s,%s,%s,%s)
                """, (
                    st.session_state.client_id, assigned_caseworker, personal_plan,
                    emergency_provided, case_status
                ))
                conn.commit()
                cursor.close()
                conn.close()
                st.success("Case management details saved successfully!")
    else:
        st.warning("Please complete Client Info first.")

# ---------------- VIEW CLIENTS ----------------
elif page == "View Clients":
    st.markdown("<h4 style='color:#2E86C1;'>All Client Records</h4>", unsafe_allow_html=True)

    # --- Fetch Data ---
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Client")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()

    df = pd.DataFrame(rows, columns=columns)

    # --- Search & Filter ---
    st.markdown("### Search & Filter")
    col1, col2, col3 = st.columns(3)
    with col1:
        search_name = st.text_input("Search by First Name")
    with col2:
        search_caseworker = st.text_input("Search by Caseworker ID")
    with col3:
        search_status = st.selectbox("Filter by Marital Status", ["All"] + df["MaritalStatus"].dropna().unique().tolist())

    filtered_df = df.copy()
    if search_name:
        filtered_df = filtered_df[filtered_df["FirstName"].str.contains(search_name, case=False)]
    if search_caseworker:
        filtered_df = filtered_df[filtered_df["CaseworkerID"].str.contains(search_caseworker, case=False)]
    if search_status != "All":
        filtered_df = filtered_df[filtered_df["MaritalStatus"] == search_status]

    # --- Display Table ---
    st.markdown("### Client Summary")
    st.dataframe(filtered_df[["ClientCode", "FirstName", "LastName", "PhoneNumber", "Email", "MaritalStatus", "EmploymentStatus", "DateCreated"]], use_container_width=True)

    # --- Expandable Details ---
    st.markdown("### View Full Details")
    selected_client = st.selectbox("Select Client Code", filtered_df["ClientCode"].tolist())
    if selected_client:
        details = df[df["ClientCode"] == selected_client].iloc[0].to_dict()
        with st.expander(f"Full Details for {selected_client}", expanded=True):
            for key, value in details.items():
                st.write(f"**{key}:** {value}")

    # --- Download Button ---
    st.markdown("### Download Data")
    st.download_button(
        label="Download Filtered Data as CSV",
        data=filtered_df.to_csv(index=False),
        file_name="clients_filtered.csv",
        mime="text/csv"
    )