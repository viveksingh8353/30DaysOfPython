from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


contacts = []

def norm(s: str) -> str:
    return s.strip()

@app.route("/", methods=["GET"])
def home():
    q = norm(request.args.get("q", ""))
    if q:
        qlow = q.lower()
        filtered = [
            c for c in contacts
            if (qlow in c["name"].lower() or q in c["phone"] or qlow in c["email"].lower())
        ]
    else:
        filtered = contacts
    return render_template("index.html", contacts=filtered, q=q)

@app.route("/add", methods=["POST"])
def add_contact():
    name = norm(request.form.get("name", "")).title()
    phone = norm(request.form.get("phone", ""))
    email = norm(request.form.get("email", ""))

    if not (name and phone and email):
        return redirect(url_for("home"))

    # if same name exists → update; else add new
    for c in contacts:
        if c["name"] == name:
            c["phone"] = phone
            c["email"] = email
            break
    else:
        contacts.append({"name": name, "phone": phone, "email": email})

    return redirect(url_for("home"))

@app.route("/delete/<int:index>", methods=["POST"])
def delete_contact(index: int):
    if 0 <= index < len(contacts):
        contacts.pop(index)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
