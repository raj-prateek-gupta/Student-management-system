from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import Base, engine
import models
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import UploadFile, File
from pathlib import Path
import shutil

Base.metadata.create_all(bind=engine)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# ==================================================
# DATABASE DEPENDENCY
# ==================================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

app = FastAPI(version="2.0")


# ==================================================
# JINJA2 CONFIGURATION
# ==================================================

templates = Jinja2Templates(
    directory="templates"
)


# ==================================================
# STATIC FILES
# ==================================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# ==================================================
# HOME PAGE
# ==================================================

@app.get("/")
def home(request: Request,
         db: Session = Depends(get_db)):

    students = db.query(models.Student).all()

    return templates.TemplateResponse(
        request=request,
        name="students.html",
        context={
            "students": students
        }
    )


# ==================================================
# ADD STUDENT PAGE
# ==================================================

@app.get("/add-student")
def add_student_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="add_student.html",
        context={}
    )


# ==================================================
# CREATE STUDENT
# ==================================================

@app.post("/add-student")
def add_student(
    first_name: str = Form(...),
    last_name: str = Form(...),
    age: int = Form(...),
    course: str = Form(...),
    db: Session = Depends(get_db)
):

   
    # Create new student
    new_student = models.Student(
        first_name=first_name,
        last_name=last_name,
        age=age,
        course=course,
    )


    # Add student to list
    db.add(new_student)

    db.commit()

    db.refresh(new_student)

    # Redirect to students page
    return RedirectResponse(
        "/",
        status_code=303
    )


# ==================================================
# EDIT STUDENT PAGE
# ==================================================

@app.get('/students/{student_id}/edit')
def edit_student_page(request:Request, 
                      student_id:int,
                      db: Session = Depends(get_db)):

    student = db.query(models.Student).filter(
        models.Student.id == student_id).first()

    
    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    
    return templates.TemplateResponse(request=request,   
                                    name="edit_student.html", 
                                    context={"student":student})

# ==================================================
# UPDATE STUDENT
# ==================================================

@app.post("/students/{student_id}/update")
def update_student(
    student_id: int,
    first_name: str = Form(...),
    last_name: str = Form(...),
    age: int = Form(...),
    course: str = Form(...),
    db: Session = Depends(get_db)
):


    student = db.query(models.Student).filter(models.Student.id == student_id).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    student.first_name = first_name
    student.last_name=last_name
    student.age=age
    student.course=course

    db.commit()

    return RedirectResponse(
        "/",
        status_code=303
    )

# ==================================================
# DELETE STUDENT
# ==================================================

@app.post("/student/{student_id}/delete")
def delete_student(student_id:int,
                   db: Session = Depends(get_db)):

    student = db.query(models.Student).filter(models.Student.id == student_id).first()

    if not student:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)

    db.commit()

    return RedirectResponse(
        "/",
        status_code=303
    )

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):

    file_path = UPLOAD_DIR/file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file,buffer)

        return{
            "message":"File Uploaded Successfully",
            "filename":file.filename
        }


@app.get("/upload")
def upload_page(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="upload.html",
        context={}
    )