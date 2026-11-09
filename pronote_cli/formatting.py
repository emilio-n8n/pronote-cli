"""Mise en forme du texte de sortie."""
from datetime import datetime

JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


def hh(dt: datetime) -> str:
    return dt.strftime("%H:%M")


def lesson(line) -> str:
    """Une ligne de cours : horaires, matière, prof, salle, annulation."""
    flag = " [ANNULÉ]" if getattr(line, "canceled", False) else ""
    room = f" — {line.classroom}" if line.classroom else ""
    names = getattr(line, "teacher_names", None) or []
    prof = ", ".join(names) if names else (getattr(line, "teacher_name", "") or "")
    return f"{hh(line.start)}-{hh(line.end)}  {line.subject.name}  ({prof}){room}{flag}"
