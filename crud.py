from sqlalchemy.future import select
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
    return new_enroll

async def get_student_courses(db, student_id):
    result = await db.execute(
        select(Enrollment.course_id).where(Enrollment.student_id == student_id)
    )
    return [row[0] for row in result.fetchall()]