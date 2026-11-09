"""Commandes de lecture."""
import re
from datetime import date, timedelta

from .auth import connect
from .formatting import JOURS, lesson


def today() -> None:
    c = connect()
    d = date.today()
    print(f"{JOURS[d.weekday()]} {d:%d/%m/%Y} — semaine {c.get_week(d)}")
    courses = sorted(c.lessons(d), key=lambda x: x.start)
    if not courses:
        print("  Aucun cours.")
    for line in courses:
        print("  " + lesson(line))


def week(offset: int = 0) -> None:
    c = connect()
    monday = date.today() - timedelta(days=date.today().weekday()) + timedelta(weeks=offset)
    print(f"Semaine du {monday:%d/%m} (semaine {c.get_week(monday)})")
    for i in range(5):
        day = monday + timedelta(days=i)
        print(f"\n{JOURS[day.weekday()].upper()} {day:%d/%m}")
        courses = sorted(c.lessons(day), key=lambda x: x.start)
        if not courses:
            print("  —")
        for line in courses:
            print("  " + lesson(line))


def homework(days: int = 14) -> None:
    c = connect()
    start = date.today()
    items = c.homework(start, start + timedelta(days=days))
    if not items:
        print("Aucun devoir sur la période.")
        return
    for h in items:
        subject = h.subject.name if h.subject else "?"
        print(f"\n{h.date:%d/%m} — {subject}")
        for raw in (h.description or "").split("\n"):
            if raw.strip():
                print("   " + raw.strip()[:200])


def grades() -> None:
    """Moyennes par matière, calculées depuis les notes détaillées.

    pronotepy n'expose pas de moyennes par matière directes sur un compte élève :
    on agrège les notes de chaque matière (note ramenée sur 20, pondérée par le
    coefficient de l'évaluation).
    """
    c = connect()
    period = c.current_period
    grades_list = period.grades
    if not grades_list:
        print(f"Aucune note sur {period.name}.")
        return

    def as_float(value):
        """Les notes arrivent en texte, virgule française incluse."""
        return float(str(value).replace(",", "."))

    subjects = {}
    for g in grades_list:
        if g.grade is None or not g.out_of:
            continue
        name = g.subject.name if g.subject else "?"
        normalized = as_float(g.grade) / as_float(g.out_of) * 20
        subjects.setdefault(name, []).append((normalized, as_float(g.coefficient or 1)))

    print(f"=== {period.name} ===")
    for name in sorted(subjects):
        values = subjects[name]
        total_coef = sum(coef for _, coef in values)
        if not total_coef:
            continue
        average = sum(v * coef for v, coef in values) / total_coef
        nb = len(values)
        print(f"  {name:24} {average:5.2f}/20   ({nb} note{'s' if nb > 1 else ''})")


def links(days: int = 3) -> None:
    """Liens (Teams, sites) déposés par les profs dans le cahier de textes."""
    c = connect()
    start = date.today()
    found = False
    for line in sorted(c.lessons(start, start + timedelta(days=days)), key=lambda x: x.start):
        content = getattr(line, "content", None)
        if not content:
            continue
        blob = " ".join(str(x) for x in (content.title, content.description) if x)
        urls = re.findall(r"https?://[^\s<\"']+", blob)
        if urls:
            found = True
            print(f"{line.start:%d/%m %H:%M}  {line.subject.name}")
            for url in urls:
                print("   " + url.rstrip(".,)"))
    if not found:
        print("Aucun lien déposé pour les prochains jours.")


def messages(n: int = 5) -> None:
    c = connect()
    discussions = c.discussions() if callable(c.discussions) else c.discussions
    if not discussions:
        print("Aucun message.")
        return
    for d in discussions[:n]:
        head = getattr(d, "subject", None) or getattr(d, "creator", "") or "?"
        print(f"\n--- {head}")
        for m in d.messages[:3]:
            print("   " + (m.content or "").strip()[:250])
