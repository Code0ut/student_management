from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.staticfiles import StaticFiles
import models, schemas, crud
from database import engine
from dependencies import get_db

app = FastAPI()

@app.on_event("startup")
async def startup():
    pass # Migrations handled by Alembic

@app.post("/students/", response_model=schemas.StudentResponse)
async def create_student(student: schemas.StudentCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_student(db, student)

@app.get("/students/{student_id}", response_model=schemas.StudentResponse)
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    student = await crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.post("/courses/", response_model=schemas.CourseResponse)
async def create_course(course: schemas.CourseCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_course(db, course)

@app.get("/courses/{course_id}", response_model=schemas.CourseResponse)
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await crud.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.post("/enrollments")
async def enroll(enrollment: schemas.EnrollmentCreate, db: AsyncSession = Depends(get_db)):
    await crud.enroll_student(db, enrollment)
    return {"message": "Enrollment successful"}

@app.get("/students/{student_id}/courses/")
async def get_courses(student_id: int, db: AsyncSession = Depends(get_db)):
    courses = await crud.get_student_courses(db, student_id)
    return {"enrolled_courses": courses}

@app.get("/students/", response_model=list[schemas.StudentResponse])
async def get_all_students(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_students(db)

@app.put("/students/{student_id}", response_model=schemas.StudentResponse)
async def update_student(student_id: int, student: schemas.StudentCreate, db: AsyncSession = Depends(get_db)):
    updated = await crud.update_student(db, student_id, student)
    if not updated:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated

@app.delete("/students/{student_id}")
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_student(db, student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
    return deleted

@app.get("/courses/", response_model=list[schemas.CourseResponse])
async def get_all_courses(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_courses(db)

@app.put("/courses/{course_id}", response_model=schemas.CourseResponse)
async def update_course(course_id: int, course: schemas.CourseCreate, db: AsyncSession = Depends(get_db)):
    updated = await crud.update_course(db, course_id, course)
    if not updated:
        raise HTTPException(status_code=404, detail="Course not found")
    return updated

@app.delete("/courses/{course_id}")
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_course(db, course_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Course not found")
    return deleted

@app.get("/enrollments/")
async def get_all_enrollments(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_enrollments(db)

app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
