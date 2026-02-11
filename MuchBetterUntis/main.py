import webuntis
import datetime
import argparse
import time
import json
import os

# --- DEFAULTS ---
SERVER = 'cissa.webuntis.com'
SCHOOL = 'Georg-herwegh-gym'
USER = 'S4936'
PASSWORD = 'teny8.WebUntis'
# -------------------

def get_timetable(start_date, end_date):
    # Lade Zugangsdaten aus credentials.json falls vorhanden
    global SERVER, SCHOOL, USER, PASSWORD
    script_dir = os.path.dirname(os.path.abspath(__file__))
    creds_path = os.path.join(script_dir, "credentials.json")
    
    if os.path.exists(creds_path):
        try:
            with open(creds_path, 'r', encoding='utf-8') as f:
                creds = json.load(f)
                SERVER = creds.get('server', SERVER)
                SCHOOL = creds.get('school', SCHOOL)
                USER = creds.get('user', USER)
                PASSWORD = creds.get('password', PASSWORD)
                print(f"Zugangsdaten aus {creds_path} geladen.")
        except Exception as e:
            print(f"Fehler beim Laden von {creds_path}: {e}")

    s = webuntis.Session(
        username=USER,
        password=PASSWORD,
        server=SERVER,
        school=SCHOOL,
        useragent='Mozilla/5.0'
    )

    try:
        s.login()
        time.sleep(1)

        # Abfrage des eigenen Stundenplans
        # my_timetable() nutzt automatisch die ID des angemeldeten Nutzers
        timetable = s.my_timetable(start=start_date, end=end_date)
        timetable = sorted(timetable, key=lambda x: x.start)

        print(f"\nPlan für {USER}")
        print(f"Zeitraum: {start_date.strftime('%d.%m.')} - {end_date.strftime('%d.%m.')}")
        print("=" * 70)

        if not timetable:
            print("Keine Unterrichtsstunden gefunden.")
            return

        last_date = None
        for slot in timetable:
            curr_date = slot.start.date()
            if curr_date != last_date:
                print(f"\n--- {slot.start.strftime('%A, %d.%m.%Y')} ---")
                last_date = curr_date

            start = slot.start.strftime('%H:%M')
            end = slot.end.strftime('%H:%M')
            
            subj = slot.subjects[0].name if slot.subjects else "???"
            room = slot.rooms[0].name if slot.rooms else "---"
            teacher = slot.teachers[0].name if slot.teachers else "---"

            status_msg = ""
            if slot.code == 'cancelled':
                status_msg = " >> ENTFÄLLT <<"
            elif slot.code == 'irregular':
                status_msg = " >> ÄNDERUNG <<"

            print(f"{start}-{end} | {subj:12} | {room:10} | {teacher:8} {status_msg}")

        # JSON Export für das Dashboard
        export_data = []
        for slot in timetable:
            subj = slot.subjects[0].name if slot.subjects else "???"
            room = slot.rooms[0].name if slot.rooms else "---"
            teacher = slot.teachers[0].name if slot.teachers else "---"
            
            status_msg = ""
            if slot.code == 'cancelled':
                status_msg = "ENTFÄLLT"
            elif slot.code == 'irregular':
                status_msg = "ÄNDERUNG"

            export_data.append({
                "start": slot.start.isoformat(),
                "end": slot.end.isoformat(),
                "title": f"{subj} {'(' + status_msg + ')' if status_msg else ''}".strip(),
                "location": room,
                "description": f"{teacher}"
            })

        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "timetable.json")
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=4)
        print(f"\nDaten erfolgreich nach {json_path} exportiert.")

    except Exception as e:
        print(f"\nFehler aufgetreten: {e}")
    finally:
        try:
            s.logout()
        except:
            pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--all", action="store_true")
    args = parser.parse_args()

    today = datetime.date.today()

    if args.all:
        monday = today - datetime.timedelta(days=today.weekday())
        friday = monday + datetime.timedelta(days=4)
        get_timetable(monday, friday)
    else:
        get_timetable(today, today)

if __name__ == "__main__":
    main()