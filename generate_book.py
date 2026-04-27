import os
import random
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

AGE_GROUP = os.getenv("AGE_GROUP", "5-8")
PAGES = int(os.getenv("PAGES", "80"))

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

pdf_path = f"{output_dir}/Kids_Math_Activity_Book_Age_{AGE_GROUP}.pdf"

width, height = 8.5 * inch, 11 * inch
c = canvas.Canvas(pdf_path, pagesize=(width, height))

answers = []

def get_problem(topic, level, number):
    if topic == "Addition":
        max_num = 10 if level == 1 else 20 if level == 2 else 50
        a, b = random.randint(1, max_num), random.randint(1, max_num)
        return f"{number}. {a} + {b} = ______", a + b

    if topic == "Subtraction":
        max_num = 10 if level == 1 else 30 if level == 2 else 60
        a = random.randint(5, max_num)
        b = random.randint(1, a)
        return f"{number}. {a} - {b} = ______", a - b

    if topic == "Multiplication":
        max_num = 5 if level == 1 else 8 if level == 2 else 12
        a, b = random.randint(1, max_num), random.randint(1, max_num)
        return f"{number}. {a} × {b} = ______", a * b

    if topic == "Division":
        divisor = random.randint(2, 10)
        answer = random.randint(1, 10)
        dividend = divisor * answer
        return f"{number}. {dividend} ÷ {divisor} = ______", answer

    topics = ["Addition", "Subtraction", "Multiplication", "Division"]
    return get_problem(random.choice(topics), level, number)

def title_page():
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width / 2, height - 2 * inch, "Kids Math Activity Book")
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 2.8 * inch, "Ages 5–8")
    c.setFont("Helvetica", 15)
    c.drawCentredString(width / 2, height - 3.5 * inch, "Addition • Subtraction • Multiplication • Division")
    c.drawCentredString(width / 2, height - 4.0 * inch, "Easy to Hard Practice Worksheets")
    c.showPage()

def draw_fun_header(title, page_num):
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 0.65 * inch, title)

    c.setFont("Helvetica", 10)
    c.drawRightString(width - 0.7 * inch, height - 0.4 * inch, f"Page {page_num}")

    c.setFont("Helvetica", 12)
    c.drawString(0.7 * inch, height - 1.05 * inch, "Name: ____________________")
    c.drawRightString(width - 0.7 * inch, height - 1.05 * inch, "Date: ____________")

def worksheet(topic, level, page_num):
    draw_fun_header(f"{topic} Practice", page_num)

    c.setFont("Helvetica", 16)

    if level == 1:
        sums_per_page = 12
        spacing = 0.55 * inch
    elif level == 2:
        sums_per_page = 15
        spacing = 0.45 * inch
    else:
        sums_per_page = 18
        spacing = 0.38 * inch

    y = height - 1.7 * inch
    page_answers = []

    for i in range(1, sums_per_page + 1):
        q, a = get_problem(topic, level, i)
        c.drawString(1 * inch, y, q)
        page_answers.append(f"{i}. {a}")
        y -= spacing

    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(width / 2, 0.55 * inch, "Great job! Keep practicing!")
    answers.append((page_num, topic, page_answers))
    c.showPage()

def section_page(title):
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(width / 2, height - 3 * inch, title)
    c.setFont("Helvetica", 15)
    c.drawCentredString(width / 2, height - 3.7 * inch, "Let’s practice and have fun!")
    c.showPage()

def answer_key():
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 0.8 * inch, "Answer Key")

    y = height - 1.4 * inch
    c.setFont("Helvetica", 10)

    for page_num, topic, ans in answers:
        if y < 1.2 * inch:
            c.showPage()
            y = height - 1 * inch

        c.setFont("Helvetica-Bold", 11)
        c.drawString(0.7 * inch, y, f"Page {page_num} - {topic}")
        y -= 0.25 * inch

        c.setFont("Helvetica", 9)
        c.drawString(1 * inch, y, "   ".join(ans))
        y -= 0.45 * inch

title_page()

page_num = 1

plan = [
    ("Addition", 1, 10),
    ("Subtraction", 1, 10),
    ("Addition", 2, 8),
    ("Subtraction", 2, 8),
    ("Multiplication", 1, 10),
    ("Multiplication", 2, 8),
    ("Division", 1, 8),
    ("Mixed Practice", 3, 18),
]

for topic, level, count in plan:
    section_page(topic)
    for _ in range(count):
        if page_num <= PAGES:
            worksheet(topic, level, page_num)
            page_num += 1

answer_key()
c.save()

print(f"Generated: {pdf_path}")
