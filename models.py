from datetime import datetime

class Application:
    VALID_STATUSES = ["applied", "interviewing", "offer", "rejected"]

    def __init__(self, company, role, status="applied", date_applied=None, notes="", app_id=None):
        self.id = app_id
        self.company = company
        self.role = role
        self.status = status if status in self.VALID_STATUSES else "applied"
        self.date_applied = date_applied or datetime.now().strftime("%Y-%m-%d")
        self.notes = notes

    def days_since_applied(self):
        try:
            app_date = datetime.strptime(self.date_applied, "%Y-%m-%d")
            return (datetime.now() - app_date).days
        except ValueError:
            return 0