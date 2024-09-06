from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with your own secret key

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Update with your DB host
            user="root",  # Update with your DB username
            password="",  # Update with your DB password
            database="thesocialsocre"  # Update with your DB name
        )
        print("Successfully connected to the database")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/activity', methods=["GET", "POST"])
def activity():
    if request.method == "POST":
        activity_id = request.form["activity_id"]
        print(activity_id)
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM student_activity WHERE activity_id = %s", (activity_id,))
            activity = cursor.fetchone()
            cursor.close()
            connection.close()

        if activity:
            return render_template("activity_detail.html", activity=activity)
        else:
            return "Activity not found", 404 
    return render_template("activity_form.html")  # Ensure this template exists

@app.route("/homepage", methods=["GET"])
def homepage():
    if 'username' in session:
        username = session['username']
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM student_login WHERE username = %s", (username,))
            user = cursor.fetchone()
            if user:
                cursor.execute("SELECT * FROM student_detail WHERE login_id = %s", (user["id"],))
                user_detail = cursor.fetchone()

                cursor.execute("SELECT activity_id, activity_name FROM student_activity ")
                activities = cursor.fetchall()

                cursor.execute("SELECT event_id, event_name FROM eventinfo")
                events = cursor.fetchall()

                cursor.close()
                connection.close()

                user_rank = 60
                images = []
                if user_rank > 10:
                    images.append(url_for("static", filename="level1.png"))
                
                if user_rank > 30:
                    images.append(url_for("static", filename="level2.png"))
                
                if user_rank > 50:
                    images.append(url_for("static", filename="level3.png"))
                
                if user_rank > 80:
                    images.append(url_for("static", filename="level4.png"))
                
                if user_rank > 100:
                    images.append(url_for("static", filename="level5.png"))
                
                if user_detail:
                    return render_template("HomePageUser.html", activities=activities, events=events, images=images, first_name=user_detail["first_name"], last_name=user_detail["last_name"], email=user_detail["email"])
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("login.html")
    
    username = request.form["username"]
    password = request.form["password"]

    print(f"Attempting to login with username: {username}")

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM student_login WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        print(f"User found: {user}")

        if user:
            cursor.execute("SELECT * FROM student_detail WHERE login_id = %s", (user["id"],))
            user_detail = cursor.fetchone()
            print(f"User details: {user_detail}")

            cursor.execute("SELECT activity_id, activity_name FROM student_activity ")
            activities = cursor.fetchall()

            cursor.execute("SELECT event_id, event_name FROM eventinfo")
            events = cursor.fetchall()

            cursor.close()
            connection.close()

            user_rank = 60
            images = []
            if user_rank > 10:
                images.append(url_for("static", filename="level1.png"))
            
            if user_rank > 30:
                images.append(url_for("static", filename="level2.png"))
            
            if user_rank > 50:
                images.append(url_for("static", filename="level3.png"))
            
            if user_rank > 80:
                images.append(url_for("static", filename="level4.png"))
            
            if user_rank > 100:
                images.append(url_for("static", filename="level5.png"))
            
            if user_detail:
                session['username'] = username  # Save username in session
                return render_template("HomePageUser.html", activities=activities, events=events, images=images, first_name=user_detail["first_name"], last_name=user_detail["last_name"], email=user_detail["email"])
    
    return render_template("login.html")


@app.route("/signUp", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signUp.html")
    
    username = request.form["username"]
    password = request.form["password"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]

    print(f"Attempting to sign up with username: {username}")

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM student_login WHERE username = %s", (username,))
        user = cursor.fetchone()
        print(f"User check: {user}")

        if not user:
            cursor.execute("INSERT INTO student_login (username, password) VALUES (%s, %s)", (username, password))
            connection.commit()
            print(f"Inserted user {username}")

            cursor.execute("SELECT id FROM student_login WHERE username = %s", (username,))
            login_id = cursor.fetchone()['id']
            print(f"Login ID: {login_id}")

            cursor.execute("INSERT INTO student_detail (login_id, first_name, last_name, email) VALUES (%s, %s, %s, %s)", 
                           (login_id, first_name, last_name, email))
            connection.commit()
            print(f"Inserted user details for {username}")

        cursor.close()
        connection.close()

        return redirect(url_for('index'))
    return render_template("signUp.html") 

# @app.route('/submitreport', methods=["POST"])
# def submitreport():
#     if request.method == "POST":
#         activityname = request.form["activity"]
#         report_description = request.form["report"]
#         studentname = request.form["studentname"]
#         teacher = request.form["teacher"]

#         connection = get_db_connection()
#         if connection:
#             cursor = connection.cursor()
#             try:
#                 cursor.execute("INSERT INTO reports (activityname, report_description, studentname, teacher) VALUES (%s, %s, %s, %s)", 
#                                (activityname, report_description, studentname, teacher))
#                 connection.commit()
#                 cursor.close()
#                 connection.close()
#                 return render_template("submitreport.html")
#             except Error as e:
#                 print(f"Error inserting data: {e}")
#                 return "Failed to submit report"
#         else:
#             return "Failed to connect to the database"

#     else:
#         return redirect(url_for("activity_report"))

@app.route('/submitreport', methods=["POST"])
def submitreport():
    if request.method == "POST":
        activityname = request.form["activity"]
        report_description = request.form["report"]
        studentname = request.form["studentname"]
        teacher = request.form["teacher"]

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("INSERT INTO reports (activityname, report_description, studentname, teacher) VALUES (%s, %s, %s, %s)", 
                               (activityname, report_description, studentname, teacher))
                cursor.execute("UPDATE points SET total_points = total_points + 100 WHERE first_name = %s", (studentname,))
                connection.commit()
                cursor.close()
                connection.close()
                return render_template("submitreport.html")
            except Error as e:
                print(f"Error inserting data: {e}")
                return "Failed to submit report"
        else:
            return "Failed to connect to the database"

# Add this route to your app.py file
@app.route("/submit-report", methods=["GET"])
def submit_report_page():
    return render_template("submitreport.html") 

# @app.route("/viewrecords", methods=["GET"])
# def view_records():
#     if 'username' in session:
#         studentname = session['username']
#         connection = get_db_connection()
#         if connection:
#             cursor = connection.cursor(dictionary=True)
#             cursor.execute("SELECT * FROM reports WHERE studentname = %s", (studentname,))
#             reports = cursor.fetchall()
#             cursor.close()
#             connection.close()
#             return render_template("viewreports.html", reports=reports)
#         else:
#             flash("Failed to connect to the database", "danger")
#             return render_template("viewreports.html", reports=[])
#     else:
#         return redirect(url_for('index'))

@app.route("/viewrecords", methods=["GET"])
def view_records():
    if 'username' in session:
        username = session['username']
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            # Join the student_login and student_detail tables to get the first name
            cursor.execute("""
                SELECT sd.first_name 
                FROM student_login sl
                JOIN student_detail sd ON sl.id = sd.login_id
                WHERE sl.username = %s
            """, (username,))
            result = cursor.fetchone()
            
            if result:
                first_name = result['first_name']
                cursor.execute("SELECT * FROM reports WHERE studentname = %s", (first_name,))
                reports = cursor.fetchall()
                cursor.close()
                connection.close()
                return render_template("viewreports.html", reports=reports)
            else:
                cursor.close()
                connection.close()
                flash("User details not found", "danger")
                return render_template("viewreports.html", reports=[])
        else:
            flash("Failed to connect to the database", "danger")
            return render_template("viewreports.html", reports=[])
    else:
        return redirect(url_for('index'))



# Add this route to your app.py file
@app.route("/submitcertificate", methods=["GET"])
def submit_certificate():
    return render_template("submitcertificate.html") 

@app.route('/submit_certificate_submission', methods=["POST"])
def submit_certificate_submission():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        organization = request.form["organization"]
        work_done = request.form["work-done"]
        hours = request.form["hours"]
        
        # Save the uploaded certificate file
        certificate_file = request.files["certificate"]
        
        # Create the uploads directory if it doesn't exist
        if not os.path.exists("uploads"):
            os.makedirs("uploads")
        
        certificate_path = os.path.join("uploads", certificate_file.filename)
        certificate_file.save(certificate_path)
        
        # Get the student ID from session
        student_id = session.get('student_id')
        
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("INSERT INTO certificate_submission (student_id, name, email, organization, work_done, hours, certificate_path) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                               (student_id, name, email, organization, work_done, hours, certificate_path))
                connection.commit()
                cursor.close()
                connection.close()
                return redirect(url_for("submit_certificate_success"))
            except Error as e:
                print(f"Error inserting data: {e}")
                return "Failed to submit certificate"
        else:
            return "Failed to connect to the database"

# Add this route to your app.py file
@app.route("/reportincident", methods=["GET"])
def report_incident():
    return render_template("ReportIncident.html")

@app.route('/report_incident_insertion', methods=["GET", "POST"])
def report_incident_insertion():
    if request.method == "POST":
        reporter_name = request.form["name"]
        reporter_email = request.form["email"]
        person_name = request.form["person-name"]
        cause = request.form["cause"]
        incident_date = request.form["incident-date"]
        incident_location = request.form["incident-location"]
        witnesses = request.form.get("witnesses", "")

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    INSERT INTO incident_reports 
                    (reporter_name, reporter_email, person_name, cause, incident_date, incident_location, witnesses)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (reporter_name, reporter_email, person_name, cause, incident_date, incident_location, witnesses))
                connection.commit()
                cursor.close()
                connection.close()
                return redirect(url_for("report_incident"))
            except Error as e:
                print(f"Error inserting data: {e}")
                return "Failed to submit report"
        else:
            return "Failed to connect to the database"
    return render_template("report_incident.html")


@app.route("/feedback", methods=["GET"])
def feedback():
    return render_template("feedback.html")

@app.route('/submit_feedback', methods=["GET", "POST"])
def submit_feedback():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        feedback = request.form["feedback"]
        rating = request.form["rating"]

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    INSERT INTO feedback (name, email, feedback, rating)
                    VALUES (%s, %s, %s, %s)
                """, (name, email, feedback, rating))
                connection.commit()
                cursor.close()
                connection.close()
                return redirect(url_for("feedback"))
            except Error as e:
                print(f"Error inserting data: {e}")
                return "Failed to submit feedback"
        else:
            return "Failed to connect to the database"
    return render_template("feedback.html")


@app.route('/event', methods=["GET", "POST"])
def event():
    if request.method == "POST":
        event_id = request.form["event_id"]
        print(event_id)
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM eventinfo WHERE event_id = %s", (event_id,))
            event = cursor.fetchone()
            cursor.close()
            connection.close()

        if event:
            return render_template("event_detail.html", event=event)
        else:
            return "Event not found", 404 
    # If the request method is GET, simply render the form to display event information
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM eventinfo")
        events = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template("event_list.html", events=events)
    else:
        return "Database connection error", 500



#admin
#admin
#admin
#admin
#admin
#admin
#admin
#admin
#admin
#admin
#admin
#admin
#admin
#admin
#admin 


@app.route("/loginadmin", methods=["GET"])
def loginadmin():
    return render_template("LoginAdmin.html")

@app.route("/signupadmin", methods=["GET"])
def signupadmin():
    return render_template("SignupAdmin.html")


@app.route("/signupadmin_proccess", methods=["GET", "POST"])
def signup_admin_proccess():
    if request.method == "GET":
        return render_template("SignupAdmin.html")
    
    username = request.form["username"]
    password = request.form["password"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]

    print(f"Attempting to sign up with username: {username}")

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM adminlogin WHERE username = %s", (username,))
        user = cursor.fetchone()
        print(f"User check: {user}")

        if not user:
            cursor.execute("INSERT INTO adminlogin (username, password, afirstname, alastname) VALUES (%s, %s, %s, %s)", (username, password, first_name, last_name))
            connection.commit()
            print(f"Inserted admin user {username}")

        cursor.close()
        connection.close()

        return redirect(url_for('loginadmin'))
    return render_template("SignupAdmin.html")

@app.route("/admin_homepage", methods=["GET"])
def admin_homepage():
    if 'admin_username' in session:
        admin_username = session['admin_username']
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM adminlogin WHERE username = %s", (admin_username,))
            admin = cursor.fetchone()
            if admin:
                admin_detail = admin  # Since adminlogin table contains first_name and last_name directly

                cursor.close()
                connection.close()

                if admin_detail:
                    return render_template("HomepageAdmin.html", first_name=admin_detail["afirstname"], last_name=admin_detail["alastname"])
        return redirect(url_for('loginadmin_proccess'))
    else:
        return redirect(url_for('loginadmin_proccess'))


@app.route("/loginadmin_proccess", methods=["GET", "POST"])
def loginadmin_proccess():
    if request.method == "GET":
        return render_template("login.html")
    
    username = request.form["username"]
    password = request.form["password"]

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        
        # Check for student login
        cursor.execute("SELECT * FROM student_login WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            cursor.execute("SELECT * FROM student_detail WHERE login_id = %s", (user["id"],))
            user_detail = cursor.fetchone()

            cursor.close()
            connection.close()

            if user_detail:
                session['username'] = username  # Save username in session
                return redirect(url_for('homepage'))

        # Check for admin login
        cursor.execute("SELECT * FROM adminlogin WHERE username = %s AND password = %s", (username, password))
        admin = cursor.fetchone()

        if admin:
            cursor.close()
            connection.close()

            if admin:
                session['admin_username'] = username  # Save admin username in session
                return redirect(url_for('admin_homepage'))
    
    return render_template("LoginAdmin.html")





# @app.route("/listactivity", methods=["GET"])
# def listactivity():
#     return render_template("ListActivityAdmin.html")

@app.route("/mystudents", methods=["GET"])
def mystudents():
    return render_template("HomePageAdmin.html")

# @app.route("/listevents", methods=["GET"])
# def listevents():
#     return render_template("ListEventsAdmin.html")

# @app.route("/reports", methods=["GET"])
# def reports():
#     return render_template("ReportsAdmin.html")

# @app.route("/violations", methods=["GET"])
# def violations():
#     return render_template("ViolationsAdmin.html")

# @app.route("/statistics", methods=["GET"])
# def statistics():
#     return render_template("StatisticsAdmin.html")

@app.route("/statistics", methods=["GET"])
def statistics():
    if 'username' in session:  # Ensure only admin can access this page
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT first_name, last_name, total_points FROM points ORDER BY total_points DESC")
            students = cursor.fetchall()
            cursor.close()
            connection.close()
            return render_template("StatisticsAdmin.html", students=students)
        else:
            flash("Failed to connect to the database", "danger")
            return render_template("StatisticsAdmin.html", students=[])
    else:
        return redirect(url_for('index'))
    
@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    if 'username' in session:  # Ensure only admin can access this page
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT first_name, last_name, total_points FROM points ORDER BY total_points DESC")
            students = cursor.fetchall()
            cursor.close()
            connection.close()
            return render_template("leaderboard.html", students=students)
        else:
            flash("Failed to connect to the database", "danger")
            return render_template("leaderboard.html", students=[])
    else:
        return redirect(url_for('index'))


@app.route("/reports", methods=["GET"])
def reports():
    if 'admin_username' in session:
        admin_username = session['admin_username']
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT * 
                FROM reports
            """)
            reports = cursor.fetchall()
            cursor.close()
            connection.close()
            return render_template("ReportsAdmin.html", reports=reports)
        else:
            flash("Failed to connect to the database", "danger")
            return render_template("ReportsAdmin.html", reports=[])
    else:
        return redirect(url_for('login'))
    
@app.route('/handle_violation', methods=['POST'])
def handle_violation():
    if request.method == 'POST':
        action = request.form['action']
        violation_id = request.form['violation_id']
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            try:
                if action == 'accept':
                    # Update the status of the violation in the database as accepted
                    cursor.execute("UPDATE incident_reports SET status = 'Accepted' WHERE id = %s", (violation_id,))
                elif action == 'reject':
                    # Update the status of the violation in the database as rejected
                    cursor.execute("UPDATE incident_reports SET status = 'Rejected' WHERE id = %s", (violation_id,))
                connection.commit()
                cursor.close()
                connection.close()
                # Redirect to the page showing all violations
                return redirect(url_for('violations'))
            except Exception as e:
                print(f"Error updating violation status: {e}")
                return "Failed to update violation status"
        else:
            return "Failed to connect to the database"

@app.route('/violations')
def violations():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM incident_reports")
            violations = cursor.fetchall()
            cursor.close()
            connection.close()
            return render_template('ViolationsAdmin.html', violations=violations)
        except Exception as e:
            print(f"Error fetching violations: {e}")
            return "Failed to fetch violations"
    else:
        return "Failed to connect to the database"
    


@app.route('/listactivity', methods=["GET"])
def listactivity():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT activity_id, activity_name, description, score FROM student_activity")
        activities = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template("ListActivityAdmin.html", activities=activities)
    else:
        return "Failed to connect to the database"

@app.route('/addactivity', methods=["POST"])
def addactivity():
    activity_name = request.form["activity"]
    description = request.form["description"]
    score = request.form["score"]

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO student_activity (activity_name, description, score,student_username) VALUES (%s, %s, %s,'prasadbelure07@gmail.com')", 
                           (activity_name, description, score))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('listactivity'))
        except Error as e:
            print(f"Error inserting data: {e}")
            return "Failed to add activity"
    else:
        return "Failed to connect to the database"
    
@app.route('/listevents', methods=["GET"])
def listevents():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT event_id, event_name, event_description, event_type, points FROM eventinfo")
        events = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template("ListEventsAdmin.html", events=events)
    else:
        return "Failed to connect to the database"

@app.route('/addevent', methods=["POST"])
def addevent():
    event_name = request.form["event_name"]
    event_description = request.form["event_description"]
    event_type = request.form["event_type"]
    points = request.form["points"]

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO eventinfo (event_name, event_description, event_type, points) VALUES (%s, %s, %s, %s)", 
                           (event_name, event_description, event_type, points))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('listevents'))
        except Error as e:
            print(f"Error inserting data: {e}")
            return "Failed to add event"
    else:
        return "Failed to connect to the database"


if __name__ == "__main__":
    app.run(port=8000)
