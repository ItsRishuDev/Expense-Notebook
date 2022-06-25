from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(200), nullable=False)
    amount_type = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Expense %r>" % self.id


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        expense_content = request.form["content"]
        expense_amount = request.form["amount"]
        expense_type = request.form["type"]

        new_expense = Expense(
            amount=expense_amount, content=expense_content, amount_type=expense_type
        )

        try:
            db.session.add(new_expense)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return "Something went wrong"

    else:
        expenses = Expense.query.order_by(Expense.date_created).all()
        if expenses:
            balance = 0
            for expense in expenses:
                if expense.amount_type == "Expense":
                    balance -= expense.amount
                else:
                    balance += expense.amount
        else:
            balance = None

        print("Balance is : ", balance)

        return render_template("index.html", expenses=expenses, balance=balance)


@app.route("/delete/<int:id>")
def delete(id):
    expense_to_delete = Expense.query.get_or_404(id)

    try:
        db.session.delete(expense_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "Something went wrong."


@app.route("/update/<int:id>", methods=["POST", "GET"])
def update(id):
    try:
        expense = Expense.query.get_or_404(id)
    except:
        return "Something went wrong."

    if request.method == "POST":
        expense.content = request.form["content"]
        expense.amount = request.form["amount"]
        expense.amount_type = request.form["type"]

        try:
            db.session.commit()
            return redirect("/")

        except:
            return "Something went wrong."
    else:
        return render_template("update.html", expense=expense)


if __name__ == "__main__":
    app.run(debug=True)
