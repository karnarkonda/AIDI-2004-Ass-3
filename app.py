from flask import Flask
from flask import request
from flask import jsonify
import sqlite3

app = Flask(__name__)
DBPATH = "students.db"

@app.route("/create", methods=["POST"])
def create_record():
    """
    This API endpoint creates a student record 
    when given the student details.
    """
    params = request.get_json()
    if params:
        with sqlite3.connect(DBPATH) as conn:
            mssg = conn.execute("""
            INSERT INTO student_record (first_name, last_name, dob, amount_due) VALUES (?,?,?,?) """, 
            (params.get('first_name', ''), params.get('last_name', ''), 
            params.get('dob', None), params.get('amount_due', 0.00))
            )
            return jsonify('Created Record Successful'), 200

    return jsonify('Pls. provide student details'), 200

@app.route("/read", methods=['GET'])
def read_record():
    """
    This API endpoint reads the details of a student record 
    when given the student id.
    """
    student_id = request.args.get('student_id', None)
    response = []
    if student_id:
        with sqlite3.connect(DBPATH) as conn:
            records = conn.execute("""
            select * from student_record where student_id = ? """, 
            (student_id)
            )
            response = [{'student_id':res[0], 'first_name':res[1], 'last_name':res[2], 'dob':res[3], 'amount_due':res[4]} for res in records]
    
    return jsonify(response), 200

@app.route('/update', methods=["POST"])
def update_record():
    """
    This API endpoint creates a student record 
    when given the student details.
    """
    params = request.get_json()
    if params:
        with sqlite3.connect(DBPATH) as conn:
            if params.get('student_id', 0) == 0:
                return jsonify('Pls. provide student id'), 200
            
            mssg = conn.execute("""
            UPDATE student_record SET first_name = ?, last_name = ?, dob = ?, amount_due = ? WHERE student_id = ?""", 
            (params.get('first_name', ''), params.get('last_name', ''), 
            params.get('dob', None), params.get('amount_due', 0.00), params.get('student_id', 0))
            )
            return jsonify('Updated Record Successful'), 200

    return jsonify('Pls. provide student details'), 200
    

@app.route('/delete', methods=["GET"])
def delete_record():
    """
    This API endpoint deletes the details of a student record 
    when given the student id.
    """
    student_id = request.args.get('student_id', None)
    response = 'pls provide student_id to be deleted'
    if student_id:
        with sqlite3.connect(DBPATH) as conn:
            records = conn.execute("""
            delete from student_record where student_id = ? """, 
            (student_id)
            )
            response = 'Record deleted succesfully.'
    
    return jsonify(response), 200

@app.route('/all')
def return_all_records():
    # fetch all records.
    response = []
    with sqlite3.connect(DBPATH) as conn:
        records = conn.execute("select * from student_record")
        response = [{'student_id':res[0], 'first_name':res[1], 'last_name':res[2], 'dob':res[3], 'amount_due':res[4]} for res in records]
    
    return jsonify(response), 200

@app.route('/createdb')
def create_database():
    try:
        conn = sqlite3.connect('students.db')
        conn.execute("""CREATE TABLE IF NOT EXISTS student_record (
                    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name VARCHAR(500),
                    last_name VARCHAR(500),
                    dob DATE, amount_due DECIMAL(10,5)
                    )"""
                     )
        conn.close()
        return 'Done'

    except Exception as err:
        return ("Error Initialising database: {}".format(str(err)))

# Application Initialization starts here
if __name__ == "__main__":
    app.run(debug=True)
    