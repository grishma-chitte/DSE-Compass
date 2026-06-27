from sqlalchemy import (
    Boolean,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


# =========================
# COLLEGE DETAILS
# =========================

class CollegeDetails(Base):
    __tablename__ = "college_details"

    college_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    dte_code: Mapped[int | None] = mapped_column(
        Integer,
        unique=True
    )

    college_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    college_abbrv: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    participates_in_cap: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    address: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    district: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    college_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    autonomous: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    naac_grade: Mapped[str | None] = mapped_column(
        String(20)
    )

    aicte_approved: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    ugc_recognized: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    ugc_approved_section: Mapped[str | None] = mapped_column(
        String(50)
    )

    contact_no: Mapped[str | None] = mapped_column(
        String(20)
    )

    hostel_available: Mapped[bool | None] = mapped_column(
        Boolean
    )

    transport_available: Mapped[bool | None] = mapped_column(
        Boolean
    )

    estimated_fees: Mapped[float | None] = mapped_column(
        Float
    )

    website_url: Mapped[str | None] = mapped_column(
        String(255)
    )

    establishment_year: Mapped[int | None] = mapped_column(
        Integer
    )

    branches = relationship(
        "Branch",
        back_populates="college"
    )

    cutoffs = relationship(
        "Cutoff",
        back_populates="college"
    )

    placements = relationship(
        "PlacementStats",
        back_populates="college"
    )


# =========================
# BRANCHES
# =========================

class Branch(Base):
    __tablename__ = "branches"

    __table_args__ = (
        UniqueConstraint(
            "college_id",
            "branch_name",
            name="uq_college_branch"
        ),
    )

    branch_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    college_id: Mapped[int] = mapped_column(
        ForeignKey("college_details.college_id"),
        nullable=False
    )

    branch_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    branch_abbrv: Mapped[str | None] = mapped_column(
        String(50)
    )

    regular_intake: Mapped[int | None] = mapped_column(
        Integer
    )

    estimated_dse_intake: Mapped[int | None] = mapped_column(
        Integer
    )

    dse_intake_2025: Mapped[int | None] = mapped_column(
        Integer
    )

    college = relationship(
        "CollegeDetails",
        back_populates="branches"
    )

    cutoffs = relationship(
        "Cutoff",
        back_populates="branch"
    )


# =========================
# CUTOFFS
# =========================

class Cutoff(Base):
    __tablename__ = "cutoffs"

    __table_args__ = (
        UniqueConstraint(
            "college_id",
            "branch_id",
            "year",
            "category",
            name="uq_cutoff_record"
        ),
    )

    cutoff_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    college_id: Mapped[int] = mapped_column(
        ForeignKey("college_details.college_id"),
        nullable=False
    )

    branch_id: Mapped[int] = mapped_column(
        ForeignKey("branches.branch_id"),
        nullable=False
    )

    year: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    category: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    percentage: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    college = relationship(
        "CollegeDetails",
        back_populates="cutoffs"
    )

    branch = relationship(
        "Branch",
        back_populates="cutoffs"
    )


# =========================
# PLACEMENT STATS
# =========================

class PlacementStats(Base):
    __tablename__ = "placement_stats"

    __table_args__ = (
        UniqueConstraint(
            "college_id",
            "year",
            name="uq_placement_year"
        ),
    )

    placement_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    college_id: Mapped[int] = mapped_column(
        ForeignKey("college_details.college_id"),
        nullable=False
    )

    year: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    placement_percent: Mapped[float | None] = mapped_column(
        Float
    )

    avg_package: Mapped[float | None] = mapped_column(
        Numeric(10, 2)
    )

    college = relationship(
        "CollegeDetails",
        back_populates="placements"
    )


# =========================
# USERS
# =========================

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    gender: Mapped[str | None] = mapped_column(
        String(20)
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    profile = relationship(
        "StudentProfile",
        back_populates="user",
        uselist=False
    )

    preferred_branches = relationship(
        "StudentPreferredBranch",
        back_populates="user"
    )

    favorites = relationship(
        "FavCollege",
        back_populates="user"
    )


# =========================
# STUDENT PROFILES
# =========================

class StudentProfile(Base):
    __tablename__ = "student_profiles"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"),
        primary_key=True
    )

    latest_percentage: Mapped[float | None] = mapped_column(
        Float
    )

    category: Mapped[str | None] = mapped_column(
        String(20)
    )

    preferred_city: Mapped[str | None] = mapped_column(
        String(100)
    )

    user = relationship(
        "User",
        back_populates="profile"
    )


# =========================
# STUDENT PREFERRED BRANCHES
# =========================

class StudentPreferredBranch(Base):
    __tablename__ = "student_preferred_branches"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "branch_id",
            name="uq_user_branch_preference"
        ),
    )

    branch_preference_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False
    )

    branch_id: Mapped[int] = mapped_column(
        ForeignKey("branches.branch_id"),
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="preferred_branches"
    )

    branch = relationship("Branch")


# =========================
# FAVOURITE COLLEGES
# =========================

class FavCollege(Base):
    __tablename__ = "fav_college"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "college_id",
            name="uq_user_favorite_college"
        ),
    )

    fav_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False
    )

    college_id: Mapped[int] = mapped_column(
        ForeignKey("college_details.college_id"),
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="favorites"
    )

    college = relationship("CollegeDetails")