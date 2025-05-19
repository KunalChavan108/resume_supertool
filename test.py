import os

resume_path = r"C:\Desktop\resume_screener\resumes\sample_resume.pdf"

if os.path.exists(resume_path):
    print("✅ File found!")
else:
    print("❌ File NOT found!")
