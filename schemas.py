from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    age: int
    email: str

class StudentResponse(StudentCreate):
    id: int

    class Config:
        orm_mode = True

class CourseCreate(BaseModel):
    title: str
    description: str

class CourseResponse(CourseCreate):
    id: int

    class Config:
        orm_mode = True

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int