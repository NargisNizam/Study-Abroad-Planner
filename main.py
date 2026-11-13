
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from pydantic import BaseModel, Field

app = FastAPI(
    title="Study Abroad Planner",
    description="A single-agent study abroad planning application",
    version="1.0.0"
)

# Static files and HTML templates
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


# Student information model
class StudentData(BaseModel):
    country: str
    degree: str
    budget: float = Field(gt=0)
    field: str


# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

# Study plan endpoint
@app.post("/plan")
async def generate_plan(student: StudentData):

    try:
        # Demo Mode: no paid API required
        budget = student.budget

        tuition = budget * 0.50
        accommodation = budget * 0.30
        living_and_travel = budget * 0.20

        plan = f"""
STUDY ABROAD PLANNER
====================

YOUR STUDENT PROFILE

Destination: {student.country}
Degree Level: {student.degree}
Study Field: {student.field}
Annual Budget: {budget:,.2f}

ILLUSTRATIVE BUDGET PLAN
========================

Tuition Budget (50%): {tuition:,.2f}
Accommodation (30%): {accommodation:,.2f}
Living & Travel (20%): {living_and_travel:,.2f}

YOUR STUDY PLAN
===============

1. UNIVERSITY RESEARCH
Research universities in {student.country} offering
programs related to {student.field}.

2. DEGREE OPTIONS
Explore {student.degree} programs matching your
academic background and career goals.

3. SCHOLARSHIPS
Check university scholarship pages and official
government scholarship opportunities.

4. ACCOMMODATION
Compare university accommodation and other
student housing options.

5. DOCUMENTS
Prepare your academic transcripts, passport,
statement of purpose and recommendation letters.

6. NEXT STEPS
Shortlist universities, check admission deadlines,
confirm tuition fees and review visa requirements.

IMPORTANT NOTE
==============

This is an illustrative DEMO plan.
The budget percentages are estimates, not verified
country-specific costs.

No university, scholarship or admission availability
has been verified yet.

Live AI planning will be connected later when
API access is available.
"""

        return {
            "success": True,
            "mode": "demo",
            "plan": plan
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to generate plan: {str(error)}"
        )


