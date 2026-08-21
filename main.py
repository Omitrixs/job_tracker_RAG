from models import Application
from database import Tracker
from ai_service import analyze_job_match
from agents import generate_cover_letter

def main():
    tracker = Tracker()

    while True:
        print("\n===================================")
        print("   JOB TRACKER v4 (Full Suite)    ")
        print("===================================")
        print("1. Add Application")
        print("2. View All Applications")
        print("3. Check Follow-Up Reminders")
        print("4. Local AI Resume Matcher")
        print("5. Generate Cover Letter (Agent)")
        print("6. Exit")

        choice = input("\nSelect Option (1-6): ").strip()

        if choice == "1":
            company = input("Company Name: ").strip()
            role = input("Role / Title: ").strip()
            status = input("Status (applied/interviewing/offer/rejected): ").strip()
            date_app = input("Date Applied (YYYY-MM-DD): ").strip()
            notes = input("Notes: ").strip()

            app = Application(company=company, role=role, status=status, date_applied=date_app, notes=notes)
            tracker.add_application(app)

        elif choice == "2":
            apps = tracker.get_all_applications()
            if not apps:
                print("\nNo applications found.")
            else:
                for app in apps:
                    print(f"ID #{app.id} | {app.role} at {app.company} | Status: {app.status}")

        elif choice == "3":
            reminders = tracker.get_followup_reminders(threshold_days=14)
            if not reminders:
                print("\nNo applications currently need follow-up.")
            else:
                for app in reminders:
                    print(f"[!] ID #{app.id}: {app.role} at {app.company} ({app.days_since_applied()} days ago)")

        elif choice == "4":
            resume = input("Paste resume text: ").strip()
            job_desc = input("Paste job description: ").strip()
            if resume and job_desc:
                analyze_job_match(resume, job_desc)

        elif choice == "5":
            apps = tracker.get_all_applications()
            if not apps:
                print("\nNo applications in database. Add one first!")
                continue

            print("\nSelect an application by ID to generate a cover letter for:")
            for app in apps:
                print(f"  [{app.id}] {app.role} at {app.company}")

            try:
                app_id = int(input("\nEnter Application ID: "))
                selected_app = next((a for a in apps if a.id == app_id), None)

                if selected_app:
                    resume = input("Paste your core resume summary: ").strip()
                    tone = input("Select tone (e.g., Professional / Enthusiastic / Concise): ").strip() or "Professional"
                    generate_cover_letter(selected_app, resume, tone)
                else:
                    print("[!] ID not found.")
            except ValueError:
                print("[!] Invalid input.")

        elif choice == "6":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()