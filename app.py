from flask import Flask, request

app = Flask(__name__)

# الواجهة 1: تسجيل الاسم والمسار
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        track = request.form["track"]
        return grades_page(name, track)
    return login_page()

def login_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>نظام اقتراح التخصص</title>
        <style>
            body { font-family: Arial; background-color: #f0f8ff; text-align: center; padding: 50px;}
            input, select { padding: 8px; margin: 5px; width: 200px;}
            button { padding: 10px 20px; background-color: #007bff; color: white; border: none; cursor: pointer;}
            button:hover { background-color: #0056b3;}
            h3 { color: #333; }
        </style>
    </head>
    <body>
        <h3>تسجيل الطالب</h3>
        <form method="post">
            <input name="name" placeholder="اسم الطالب" required><br><br>
            <select name="track" required>
                <option value="">اختر المسار</option>
                <option value="علمي">علمي</option>
                <option value="أدبي">أدبي</option>
            </select><br><br>
            <button type="submit">التالي</button>
        </form>
    </body>
    </html>
    """

# الواجهة 2: إدخال الدرجات حسب المسار
def grades_page(name, track):
    if track == "علمي":
        fields = ["رياضيات", "فيزياء", "كيمياء", "أحياء"]
    else:
        fields = ["عربي", "إنجليزي", "تاريخ", "جغرافيا"]

    inputs = "".join([f'{f} <input type="number" name="{f}" required><br>' for f in fields])

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>إدخال الدرجات</title>
        <style>
            body {{ font-family: Arial; background-color: #f0f8ff; text-align: center; padding: 50px; }}
            input {{ padding: 8px; margin: 5px; width: 100px; }}
            button {{ padding: 10px 20px; background-color: #28a745; color: white; border: none; cursor: pointer; }}
            button:hover {{ background-color: #1e7e34; }}
            h3 {{ color: #333; }}
        </style>
    </head>
    <body>
        <h3>إدخال الدرجات ({track})</h3>
        <form method="post" action="/result">
            <input type="hidden" name="name" value="{name}">
            <input type="hidden" name="track" value="{track}">
            {inputs}<br>
            <button type="submit">تحليل</button>
        </form>
    </body>
    </html>
    """

# صفحة النتيجة: تقييم و اقتراح تخصص
@app.route("/result", methods=["POST"])
def result():
    name = request.form["name"]
    track = request.form["track"]

    # جمع الدرجات حسب المسار
    subjects = ["رياضيات", "فيزياء", "كيمياء", "أحياء"] if track=="علمي" else ["عربي", "إنجليزي", "تاريخ", "جغرافيا"]
    total = 0
    for s in subjects:
        total += int(request.form[s])

    # التقييم
    average = total / len(subjects)
    if average >= 90:
        grade = "ممتاز"
    elif average >= 75:
        grade = "جيد جداً"
    elif average >= 50:
        grade = "جيد"
    else:
        grade = "ضعيف"

    # اقتراح التخصصات حسب المسار والتقييم
    if track == "علمي":
        if average >= 85:
            majors = ["طب", "هندسة", "علوم حاسوب"]
        elif average >= 70:
            majors = ["صيدلة", "رياضيات", "فيزياء"]
        else:
            majors = ["علوم عامة", "تقانة حيوية"]
    else: # أدبي
        if average >= 85:
            majors = ["قانون", "إدارة أعمال", "إعلام"]
        elif average >= 70:
            majors = ["اقتصاد", "علوم سياسية"]
        else:
            majors = ["تعليم", "إعلام مساعد"]

    majors_list = "".join([f"<li>{m}</li>" for m in majors])

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>النتيجة</title>
        <style>
            body {{ font-family: Arial; background-color: #f0f8ff; text-align: center; padding: 50px; }}
            button {{ padding: 10px 20px; background-color: #007bff; color: white; border: none; cursor: pointer; margin-top: 20px; }}
            button:hover {{ background-color: #0056b3; }}
            h3 {{ color: #333; }}
        </style>
    </head>
    <body>
        <h3>النتيجة</h3>
        الاسم: {name}<br>
        المسار: {track}<br>
        المجموع: {total} | التقييم: {grade}<br><br>
        التخصصات المقترحة:
        <ul>
            {majors_list}
        </ul>
        <button onclick="window.location.href='/'">عودة</button>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)