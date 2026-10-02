from openpyxl import Workbook


def create_registration_report(data, filename):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Registration Report"

    headers = [
        "Student ID",
        "Name",
        "Branch",
        "CGPA",
        "Status"
    ]

    sheet.append(headers)

    for student in data:
        sheet.append([
            student["student_id"],
            student["name"],
            student["branch"],
            student["cgpa"],
            student["status"]
        ])

    workbook.save(filename)