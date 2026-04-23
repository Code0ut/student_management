from sqlalchemy import select
from models import Student, Course, Enrollment

async def create_student(db, student):
    new_student = Student(**student.dict())
    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)
    return new_student

async def get_student(db, student_id):
    result = await db.execute(select(Student).where(Student.id == student_id))
    return result.scalar_one_or_none()

async def create_course(db, course):
    new_course = Course(**course.dict())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course

async def get_course(db, course_id):
    result = await db.execute(select(Course).where(Course.id == course_id))
    return result.scalar_one_or_none()

async def enroll_student(db, enrollment):
    new_enroll = Enrollment(**enrollment.dict())
    db.add(new_enroll)
    await db.commit()
    await db.refresh(new_enroll)
    return new_enroll

async def get_student_courses(db, student_id):
    result = await db.execute(
        select(Enrollment.course_id).where(Enrollment.student_id == student_id)
    )
    return result.scalars().all()

async def get_all_students(db):
    result = await db.execute(select(Student))
    return result.scalars().all()

async def get_all_courses(db):
    result = await db.execute(select(Course))
    return result.scalars().all()

async def get_all_enrollments(db):
    result = await db.execute(select(Enrollment))
    return result.scalars().all()

async def update_student(db, student_id, updated_data):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()

    if not student:
        return None

    for key, value in updated_data.model_dump().items():
        setattr(student, key, value)

    await db.commit()
    await db.refresh(student)
    return student

async def update_course(db, course_id, updated_data):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()

    if not course:
        return None

    for key, value in updated_data.model_dump().items():
        setattr(course, key, value)

    await db.commit()
    await db.refresh(course)
    return course

async def delete_student(db, student_id):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()

    if not student:
        return None

    await db.delete(student)
    await db.commit()
    return {"message": "Student deleted"}

async def delete_course(db, course_id):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()

    if not course:
        return None

    await db.delete(course)
    await db.commit()
    return {"message": "Course deleted"}