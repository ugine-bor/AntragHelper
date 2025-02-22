from datetime import datetime


def log(note, message):
    dat = datetime.fromisoformat(str(message.date)).utcnow()
    with open(f"UserFiles/U_{message.from_user.id}/DataNotToShow/U_log_{message.from_user.id}.txt", "a",
              encoding="utf-8") as log_file:
        log_file.write(
            f"|{dat.strftime('%d.%m.%Y %H:%M:%S')}| {message.from_user.first_name} {message.from_user.last_name} ({message.from_user.id}): {note}\n")
