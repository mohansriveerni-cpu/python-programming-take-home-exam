grades = {
    "math": {
        "anna": 1.7,
        "ben": 2.3,
        "clara": 1.0
    },
    "physics": {
        "ben": 3.0,
        "clara": 1.3,
        "david": 2.0
    },
    "art": {
        "anna": 1.0,
        "david": 1.7
    }
}


def subjects_of(student) -> set:
    subjects = set()

    for subject, students in grades.items():
        if student in students:
            subjects.add(subject)

    return subjects


def takes_all(grades) -> set:
    if not grades:
        return set()

    subject_students = [
        set(students.keys())
        for students in grades.values()
    ]

    result = subject_students[0]

    for students in subject_students[1:]:
        result = result.intersection(students)

    return result


def student_average(grades, student) -> float:
    total = 0
    number_of_subjects = 0

    for students in grades.values():
        if student in students:
            total += students[student]
            number_of_subjects += 1

    if number_of_subjects == 0:
        return 0.0

    return round(total / number_of_subjects, 2)


def honor_roll(grades, limit=1.5) -> list:
    all_students = set()

    for students in grades.values():
        all_students.update(students.keys())

    result = [
        student
        for student in all_students
        if student_average(grades, student) <= limit
    ]

    return sorted(result)


# Demo
if __name__ == "__main__":
    print("Subjects of anna:", subjects_of("anna"))
    print("Students taking all subjects:", takes_all(grades))
    print("Average of clara:", student_average(grades, "clara"))
    print("Average of unknown:", student_average(grades, "unknown"))
    print("Honor roll:", honor_roll(grades))
