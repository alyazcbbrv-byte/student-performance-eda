"""
Clean the course workbook "13 Student Performance.xlsx" and save data/student_performance.csv.

    python src/prepare_data.py "path/to/13 Student Performance.xlsx"

- keeps the 10 original data columns, renames them to snake_case
- drops student names (not needed for the analysis) and the helper columns added during the course
- runs data-quality checks and stops if one fails
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parents[1] / "data" / "student_performance.csv"
COLS = {"Student ID": "student_id", "Gender": "gender", "Department / Major": "major", "Semester": "semester",
        "Course Name": "course", "Credit Hours": "credits", "Grade": "grade", "GPA (Semester)": "grade_points",
        "Attendance %": "attendance_pct"}


def main(src: str) -> int:
    df = pd.read_excel(src)[list(COLS)].rename(columns=COLS)
    checks = {
        "no missing values": df.isna().sum().sum() == 0,
        "no duplicate rows": not df.duplicated().any(),
        "attendance within 0-100": df.attendance_pct.between(0, 100).all(),
        "grade points within 0-4": df.grade_points.between(0, 4).all(),
        "grades are A-F": set(df.grade) <= set("ABCDF"),
        "each student has exactly one major": df.groupby("student_id").major.nunique().max() == 1,
    }
    for k, ok in checks.items():
        print(("OK   " if ok else "FAIL ") + k)
    if not all(checks.values()):
        return 1
    OUT.parent.mkdir(exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"{len(df)} rows, {df.student_id.nunique()} students -> {OUT.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
