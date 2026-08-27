from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_pdf(filename, title, content_lines):
    path = os.path.join("data", "raw", filename)
    c = canvas.Canvas(path, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, title)
    
    c.setFont("Helvetica", 12)
    y = 700
    for line in content_lines:
        c.drawString(100, y, line)
        y -= 20
        if y < 100:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = 750
            
    c.save()

def main():
    docs = {
        "Academic Regulations.pdf": (
            "Academic Regulations and Guidelines",
            [
                "1. Attendance Policy:",
                "Students require 75% attendance in all courses to be eligible for the end-semester exams.",
                "Medical leaves must be accompanied by a valid medical certificate.",
                "",
                "2. Grading System:",
                "A grade (90-100%): Outstanding performance.",
                "B grade (80-89%): Excellent performance.",
                "C grade (70-79%): Good performance.",
                "D grade (60-69%): Average performance.",
                "F grade (<60%): Fail. Must retake the course.",
                "",
                "3. Examinations:",
                "Mid-term exams account for 30% of the final grade.",
                "End-semester exams account for 50%.",
                "Assignments and quizzes make up the remaining 20%."
            ]
        ),
        "Hostel Guidelines.pdf": (
            "Hostel Rules and Regulations",
            [
                "1. Curfew Timings:",
                "All students must be inside the hostel premises by 9:30 PM.",
                "Late entries will be recorded and reported to the warden.",
                "",
                "2. Visitors:",
                "Visitors are allowed only in the reception area between 4 PM and 7 PM.",
                "No overnight guests are permitted under any circumstances.",
                "",
                "3. Mess Timings:",
                "Breakfast: 7:30 AM - 9:00 AM",
                "Lunch: 12:30 PM - 2:00 PM",
                "Dinner: 7:30 PM - 9:00 PM"
            ]
        ),
        "Library Rules.pdf": (
            "Library Policies",
            [
                "1. Borrowing Rules:",
                "Students can borrow up to 3 books at a time for a maximum of 14 days.",
                "A late fee of $1 per day will be charged for overdue books.",
                "",
                "2. Quiet Zones:",
                "The second floor is a designated quiet zone. No talking allowed.",
                "Group study is permitted only in the ground floor discussion rooms.",
                "",
                "3. Digital Resources:",
                "Students have access to IEEE and ACM digital libraries through the college network.",
                "Credentials can be requested from the librarian."
            ]
        )
    }

    for filename, (title, content) in docs.items():
        create_pdf(filename, title, content)
        print(f"Created {filename}")

if __name__ == "__main__":
    main()
