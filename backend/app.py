from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db.models import CollegeDetails
from db.models import Branch

app = Flask(__name__)     #=========created flask app ie.created the backend server===

engine = create_engine("sqlite:///db/dse_compass.db")  #============conected to the database====


@app.route("/")  
def home():   #====defines API endpoint of home page ie.if someone go to this url it tells too run home function
    
    return jsonify({
        "message": "DSE Compass Backend is Running"
    })


@app.route("/api/colleges")
def get_colleges():    #====API endpoint of college deails page 

    with Session(engine) as session:  

        colleges = session.query(CollegeDetails).all()

        result = []

        for college in colleges:
            result.append({
                "college_id": college.college_id,
                "college_name": college.college_name,
                "city": college.city,
                "district": college.district,
                "college_type": college.college_type,
                "naac_grade": college.naac_grade
            })

        return jsonify({
            "success": True,
            "count": len(result),
            "data": result
        })



@app.route("/api/branches")
def get_branches():    #api endpoint of all branches  page 
     with Session(engine) as session:  

        branches = session.query(Branch).all()

        result = []

        for branch in branches:
            result.append({
                "college_id":branch.college_id,
                "branch_name":branch.branch_name,
                "branch_abbrv":branch.branch_abbrv,
                "intake_capacity":branch.intake_capacity
                })

        return jsonify({
            "success": True,
            "count": len(result),
            "data": result
         })




if __name__ == "__main__":
    app.run(debug=True)   #Runs the server