import os
import uuid
import pdfplumber
import spacy
from flask import Flask, request, render_template, send_file
from spacy.matcher import PhraseMatcher
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = "oneeyedeagle"

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Upload folder
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Skill list (same as before)
SKILL_LIST = [
    "Python", "R", "MySQL", "Excel", "Word", "PowerPoint", "Machine Learning", "Deep Learning",
    "Statistics", "Data Analysis", "Data Visualization", "SQL", "HTML", "CSS", "JavaScript",
    "Flask", "Django", "Pandas", "Numpy", "Matplotlib", "Seaborn", "Tableau", "Power BI",
    "Natural Language Processing", "Git", "Github", "Big Data", "Cloud Computing", "AWS",
    "React", "Node.js", "CI/CD", "Java", "OOP", "Algorithms", "Data Structures"
]

# Import job descriptions (unchanged - keep your full dict here)
JOB_DESCRIPTIONS = {
    # TECHNICAL JOBS
    "software_developer": """
        Hiring a Software Developer with experience in Java, Python, OOP, algorithms, and Git. Familiarity with databases, cloud environments, and CI/CD is a bonus.
    """,
    "web_developer": """
        Looking for a Web Developer skilled in HTML, CSS, JavaScript, React, Node.js, and responsive design. Experience with Git is preferred.
    """,
    "data_analyst": """
        We need a Data Analyst with skills in Python, R, SQL, Excel, statistics, and visualization tools like Seaborn and Matplotlib.
    """,
    "cybersecurity_analyst": """
        Seeking a Cybersecurity Analyst with expertise in firewalls, network security, threat detection, and vulnerability assessment.
    """,
    "it_support_specialist": """
        Looking for an IT Support Specialist with experience in troubleshooting, software/hardware support, and technical documentation.
    """,
    "cloud_engineer": """
        Hiring a Cloud Engineer skilled in AWS, Azure, Kubernetes, cloud architecture, and DevOps tools like CI/CD.
    """,
    "devops_engineer": """
        DevOps Engineer with experience in CI/CD pipelines, cloud infrastructure, automation, and monitoring tools required.
    """,
    "database_administrator": """
        We need a Database Administrator with proficiency in MySQL, SQL Server, database tuning, and backup management.
    """,
    "ai_ml_engineer": """
        AI/ML Engineer experienced in machine learning algorithms, deep learning frameworks, Python, and model deployment.
    """,
    "network_engineer": """
        Network Engineer with knowledge of routing/switching, network security, and network troubleshooting is required.
    """,
    "mechanical_engineer": """
        Hiring a Mechanical Engineer experienced in CAD tools, thermodynamics, product design, and mechanical systems.
    """,
    "electrical_engineer": """
        Electrical Engineer with experience in circuit design, power systems, and embedded systems development.
    """,
    "civil_engineer": """
        Seeking a Civil Engineer skilled in structural analysis, AutoCAD, construction planning, and project estimation.
    """,
    "chemical_engineer": """
        Chemical Engineer with knowledge in process design, thermodynamics, and safety regulations is needed.
    """,
    "aerospace_engineer": """
        Aerospace Engineer skilled in flight mechanics, propulsion systems, and aerospace materials.
    """,
    "industrial_engineer": """
        Industrial Engineer with process optimization, lean manufacturing, and production planning experience preferred.
    """,
    "robotics_engineer": """
        Robotics Engineer needed with skills in automation, control systems, and C/C++ or Python.
    """,
    "biomedical_engineer": """
        Biomedical Engineer experienced in medical device design, clinical research, and data analysis is required.
    """,
    "lab_technician": """
        Lab Technician with experience in handling lab equipment, sample testing, and data recording.
    """,
    "research_scientist": """
        Research Scientist needed for experimental research, data analysis, and scientific reporting.
    """,
    "environmental_scientist": """
        Environmental Scientist required with experience in environmental assessments, GIS, and sustainability practices.
    """,
    "biotechnologist": """
        Biotechnologist with molecular biology, lab techniques, and bioinformatics experience needed.
    """,
    "physicist": """
        Physicist skilled in theoretical modeling, experimental physics, and computational simulations preferred.
    """,
    "electrician": """
        Hiring a certified Electrician experienced in residential/commercial wiring and troubleshooting.
    """,
    "hvac_technician": """
        HVAC Technician required for maintenance and installation of HVAC systems and equipment.
    """,
    "cnc_machine_operator": """
        CNC Machine Operator skilled in machine setup, tool programming, and part inspection is needed.
    """,
    "auto_mechanic": """
        Auto Mechanic experienced in vehicle diagnostics, repair, and routine maintenance.
    """,
    "elevator_technician": """
        Elevator Technician required for installation, repair, and safety inspections of elevator systems.
    """,

    # NON-TECHNICAL JOBS
    "project_manager": """
        Project Manager with experience in project planning, risk management, Agile/Scrum, and team leadership is required.
    """,
    "hr_specialist": """
        HR Specialist skilled in recruitment, onboarding, employee relations, and HR compliance needed.
    """,
    "operations_manager": """
        Operations Manager needed with experience in process optimization, logistics, and team supervision.
    """,
    "business_analyst": """
        Business Analyst with knowledge in requirements gathering, stakeholder communication, and documentation is preferred.
    """,
    "executive_assistant": """
        Executive Assistant with calendar management, travel coordination, and administrative skills required.
    """,
    "office_manager": """
        Office Manager with operations coordination, vendor management, and employee support experience needed.
    """,
    "marketing_manager": """
        Marketing Manager skilled in SEO, digital marketing, content strategy, and campaign analytics.
    """,
    "sales_representative": """
        Sales Representative with strong communication, CRM skills, and lead generation experience needed.
    """,
    "copywriter": """
        Copywriter required for writing compelling content, product descriptions, and marketing copy.
    """,
    "seo_specialist": """
        SEO Specialist with experience in keyword research, technical SEO, and analytics is preferred.
    """,
    "social_media_manager": """
        Social Media Manager skilled in platform strategy, content creation, and analytics.
    """,
    "brand_strategist": """
        Brand Strategist required to develop brand identity, campaigns, and audience engagement.
    """,
    "accountant": """
        Accountant with bookkeeping, financial reporting, tax prep, and audit support experience is needed.
    """,
    "financial_analyst": """
        Financial Analyst with experience in forecasting, budgeting, and financial modeling required.
    """,
    "bookkeeper": """
        Bookkeeper with experience in ledgers, reconciliation, and QuickBooks preferred.
    """,
    "loan_officer": """
        Loan Officer with knowledge of lending policies, client evaluations, and credit assessments needed.
    """,
    "administrative_assistant": """
        Administrative Assistant with calendar management, filing, and document preparation skills.
    """,
    "teacher": """
        Teacher with lesson planning, classroom management, and curriculum development experience required.
    """,
    "school_counselor": """
        School Counselor with experience in student advising, emotional support, and career guidance.
    """,
    "academic_advisor": """
        Academic Advisor needed to support students with course selection, degree planning, and progression.
    """,
    "corporate_trainer": """
        Corporate Trainer with skills in employee training, presentation design, and performance evaluation.
    """,
    "graphic_designer": """
        Graphic Designer with Adobe Creative Suite experience, branding, and layout design needed.
    """,
    "content_writer": """
        Content Writer with skills in SEO writing, blogs, and technical documentation is preferred.
    """,
    "video_editor": """
        Video Editor required with editing software skills, storytelling, and post-production knowledge.
    """,
    "photographer": """
        Photographer needed for commercial, portrait, or event photography and editing.
    """,
    "interior_designer": """
        Interior Designer with experience in space planning, AutoCAD, and client presentations.
    """,
    "customer_service_representative": """
        Customer Service Representative with CRM, troubleshooting, and communication skills needed.
    """,
    "call_center_agent": """
        Call Center Agent required for handling inbound/outbound calls, issue resolution, and call tracking.
    """,
    "technical_support": """
        Tier 1 Technical Support agent with communication, problem-solving, and customer handling skills.
    """,
    "client_relationship_manager": """
        Client Relationship Manager needed to maintain long-term client satisfaction and resolve issues.
    """,
    "medical_secretary": """
        Medical Secretary required with scheduling, records management, and insurance billing experience.
    """,
    "hospital_administrator": """
        Hospital Administrator with operations coordination, patient services, and compliance oversight experience.
    """,
    "medical_biller": """
        Medical Biller needed with CPT/ICD coding, claims processing, and insurance liaison skills.
    """,
    "health_insurance_specialist": """
        Health Insurance Specialist with knowledge of benefits, policies, and claims processes is required.
    """
}



@app.route('/how-it-works')
def how_it_works():
    return render_template('works.html')


# Extract text from PDF file
def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        return ""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


# Extract skills using spaCy PhraseMatcher
def extract_skills(text):
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(skill) for skill in SKILL_LIST]
    matcher.add("SKILLS", patterns)
    doc = nlp(text)
    matches = matcher(doc)
    extracted = list(set([doc[start:end].text for _, start, end in matches]))
    return extracted


# Match skills with job description
def match_skills(candidate_skills, job_description):
    job_doc = nlp(job_description.lower())
    job_keywords = {token.text.capitalize() for token in job_doc if token.is_alpha}
    matched = [skill for skill in candidate_skills if skill in job_keywords]
    match_percentage = (len(matched) / len(candidate_skills)) * 100 if candidate_skills else 0
    return matched, round(match_percentage, 2)


@app.route("/", methods=["GET", "POST"])
def upload_resume():
    job_roles = list(JOB_DESCRIPTIONS.keys())

    if request.method == "POST":
        if "resume" not in request.files or "job_role" not in request.form:
            return "❌ Resume and job role are required!", 400

        file = request.files["resume"]
        job_role = request.form["job_role"]

        if file.filename == "":
            return "❌ No selected file!", 400
        if not file.filename.lower().endswith(".pdf"):
            return "❌ Only PDF files are allowed!", 400
        if job_role not in JOB_DESCRIPTIONS:
            return "❌ Invalid job role selected!", 400

        unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
        resume_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
        file.save(resume_path)

        resume_text = extract_text_from_pdf(resume_path)
        skills = extract_skills(resume_text)
        matched_skills, match_percentage = match_skills(skills, JOB_DESCRIPTIONS[job_role])

        return render_template(
            "result.html",
            filename=unique_filename,
            job_role_display=job_role.replace("_", " ").title(),
            job_role=job_role,
            skills=skills,
            matched_skills=matched_skills,
            match_percentage=match_percentage
        )

    return render_template("index.html", job_roles=job_roles)


@app.route("/download/<filename>/<job_role>")
def download_report(filename, job_role):
    resume_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if not os.path.exists(resume_path):
        return "❌ Resume file not found!", 404

    if job_role not in JOB_DESCRIPTIONS:
        return "❌ Invalid job role!", 400

    resume_text = extract_text_from_pdf(resume_path)
    skills = extract_skills(resume_text)
    matched_skills, match_percentage = match_skills(skills, JOB_DESCRIPTIONS[job_role])

    pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], f"{uuid.uuid4().hex}_report.pdf")

    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 90, f"Filename: {filename}")
    c.drawString(50, height - 110, f"Job Role: {job_role.replace('_', ' ').title()}")
    c.drawString(50, height - 130, f"Match Percentage: {match_percentage}%")

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 160, "Extracted Skills:")
    c.setFont("Helvetica", 12)
    y = height - 180
    for skill in skills:
        c.drawString(70, y, f"- {skill}")
        y -= 15
        if y < 100:
            c.showPage()
            y = height - 50

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y - 10, "Matched Skills:")
    c.setFont("Helvetica", 12)
    y -= 30
    for skill in matched_skills:
        c.drawString(70, y, f"- {skill}")
        y -= 15
        if y < 100:
            c.showPage()
            y = height - 50

    c.save()

    return send_file(pdf_path, as_attachment=True)


@app.route("/create-resume", methods=["GET", "POST"])
def create_resume():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        skills = request.form.get("skills")

        if not name or not email or not skills:
            return "❌ Please fill in all fields!", 400

        # Save the generated resume PDF with a unique filename to avoid overwrite
        pdf_filename = f"{uuid.uuid4().hex}_resume.pdf"
        pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], pdf_filename)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Resume", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
        pdf.cell(200, 10, txt=f"Email: {email}", ln=True)
        pdf.multi_cell(0, 10, txt=f"Skills: {skills}")

        pdf.output(pdf_path)

        return send_file(pdf_path, as_attachment=True)

    return render_template("create_resume.html")


if __name__ == "__main__":
    print("🌐 Starting Flask Web App... Visit: http://127.0.0.1:5001")
    app.run(debug=True, port=5001)
