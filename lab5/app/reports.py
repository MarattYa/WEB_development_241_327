from flask import Blueprint, render_template, request, make_response
from flask_login import login_required, current_user
from models import VisitLog, User, db
from sqlalchemy import func
import csv, io

reports = Blueprint('reports', __name__, url_prefix="/logs")

# ----------------- Журнал посещений -----------------
@reports.route("/")
@login_required
def visit_log():
    page = request.args.get('page', 1, type=int)

    if current_user.role.name == "Администратор":
        pagination = VisitLog.query.order_by(VisitLog.created_at.desc())\
            .paginate(page=page, per_page=10)
    else:
        pagination = VisitLog.query.filter_by(user_id=current_user.id)\
            .order_by(VisitLog.created_at.desc())\
            .paginate(page=page, per_page=10)

    logs = []
    for log in pagination.items:
        if log.user:
            full_name = f"{log.user.last_name} {log.user.first_name} {log.user.patronymic or ''}".strip()
        else:
            full_name = "Неаутентифицированный пользователь"
        logs.append({
            "id": log.id,
            "user": full_name,
            "path": log.path,
            "created_at": log.created_at.strftime("%d.%m.%Y %H:%M:%S")
        })

    return render_template("logs/index.html", logs=logs, pagination=pagination)

# ----------------- Отчёт по страницам -----------------
@reports.route("/pages")
@login_required
def report_pages():
    data = db.session.query(
        VisitLog.path,
        func.count(VisitLog.id).label("visits_count")
    ).group_by(VisitLog.path).order_by(func.count(VisitLog.id).desc()).all()

    return render_template("logs/pages.html", data=data)

@reports.route("/pages/csv")
@login_required
def pages_csv():
    data = db.session.query(
        VisitLog.path,
        func.count(VisitLog.id).label("visits_count")
    ).group_by(VisitLog.path).order_by(func.count(VisitLog.id).desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Страница", "Количество посещений"])
    for row in data:
        writer.writerow(row)

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=pages_report.csv"
    response.headers["Content-type"] = "text/csv"
    return response

# ----------------- Отчёт по пользователям -----------------
@reports.route("/users")
@login_required
def report_users():
    # Считаем посещения по пользователям, включая возможность отсутствия user_id
    data = db.session.query(
        User.id,
        User.last_name,
        User.first_name,
        User.patronymic,
        func.count(VisitLog.id).label("visits_count")
    ).join(VisitLog, VisitLog.user_id == User.id)\
     .group_by(User.id)\
     .order_by(func.count(VisitLog.id).desc()).all()

    # Формируем список для шаблона с ФИО или "Неаутентифицированный пользователь"
    formatted_data = []
    for u_id, last, first, patronymic, count in data:
        full_name = f"{last} {first} {patronymic or ''}".strip() if u_id else "Неаутентифицированный пользователь"
        formatted_data.append((full_name, count))

    return render_template("logs/users.html", data=formatted_data)

@reports.route("/users/csv")
@login_required
def users_csv():
    data = db.session.query(
        User.id,
        User.last_name,
        User.first_name,
        User.patronymic,
        func.count(VisitLog.id).label("visits_count")
    ).join(VisitLog, VisitLog.user_id == User.id)\
     .group_by(User.id)\
     .order_by(func.count(VisitLog.id).desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Пользователь", "Количество посещений"])
    for u_id, last, first, patronymic, count in data:
        full_name = f"{last} {first} {patronymic or ''}".strip() if u_id else "Неаутентифицированный пользователь"
        writer.writerow([full_name, count])

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=users_report.csv"
    response.headers["Content-type"] = "text/csv"
    return response