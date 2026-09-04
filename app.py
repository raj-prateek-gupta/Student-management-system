from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from data import students


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
def home(request: Request):

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
    course: str = Form(...)
):

    # Generate new ID
    new_id = max(
        [student["id"] for student in students],   
        default=0
    ) + 1


    # Create new student
    new_student = {
        "id": new_id,
        "first_name": first_name,
        "last_name": last_name,
        "age": age,
        "course": course
    }


    # Add student to list
    students.append(new_student)


    # Redirect to students page
    return RedirectResponse(
        "/",
        status_code=303
    )

@app.get('/students/{student_id}/edit')
def edit_student_page(request:Request, student_id:int):

    for student in students:
        if student["id"] == student_id:
            return templates.TemplateResponse(request=request, name="edit_student.html", context={"student":student})

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )

@app.post("/students/{student_id}/update")
def update_student(
    student_id: int,

    first_name: str = Form(...),
    last_name: str = Form(...),
    age: int = Form(...),
    course: str = Form(...)
):

    for student in students:

        if student["id"] == student_id:

            student["first_name"] = first_name
            student["last_name"] = last_name
            student["age"] = age
            student["course"] = course

            return RedirectResponse(
                "/",
                status_code=303
            )

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )

@app.post("/student/{student_id}/delete")
def delete_student(student_id:int):

    for index,student in enumerate(students):
        if student["id"] == student_id:
            students.pop(index)                           # [s1, s2]

            return RedirectResponse("/", status_code=303)

    
    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )

            
            
            

