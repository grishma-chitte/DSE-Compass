from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import (
    CollegeDetails,
    Branch,
    PlacementStats,
    Cutoff,
    User,
    StudentProfile,
    StudentPreferredBranch,
    FavCollege,
)

engine = create_engine("sqlite:///dse_compass.db")

with Session(engine) as session:

    # College
    college = CollegeDetails(
        dte_code=123456,
        college_name="Sample Engineering College",
        college_abbrv="SEC",
        address="Sample Address",
        city="Nashik",
        district="Nashik",
        college_type="Private",
        autonomous=False,
        naac_grade="A",
        ugc_approved=True,
        contact_no="9876543210",
        hostel_available=True,
        transport_available=True,
        estimated_fees=400000,
        website_url="https://example.com",
        establishment_year=2000,
    )

    session.add(college)
    session.commit()

    # Branch
    branch = Branch(
        college_id=college.college_id,
        branch_name="Computer Engineering",
        branch_abbrv="COMP",
        intake_capacity=120,
    )

    session.add(branch)
    session.commit()

    # Placement
    placement = PlacementStats(
        college_id=college.college_id,
        year=2025,
        placement_percent=80,
        avg_package=4.5,
    )

    session.add(placement)

    # Cutoff
    cutoff = Cutoff(
        college_id=college.college_id,
        branch_id=branch.branch_id,
        year=2025,
        category="GOPEN",
        percentage=92.5,
    )

    session.add(cutoff)

    # User
    user = User(
        name="Test Student",
        email="test@example.com",
        gender="Male",
        password_hash="dummy_hash",
        role="Student",
    )

    session.add(user)
    session.commit()

    # Student Profile
    profile = StudentProfile(
        user_id=user.user_id,
        latest_percentile=85,
        category="GOPEN",
        preferred_city="Pune",
    )

    session.add(profile)

    # Preferred Branch
    pref_branch = StudentPreferredBranch(
        user_id=user.user_id,
        branch_id=branch.branch_id,
    )

    session.add(pref_branch)

    # Favourite College
    fav = FavCollege(
        user_id=user.user_id,
        college_id=college.college_id,
    )

    session.add(fav)

    session.commit()

print("Sample data inserted successfully!")