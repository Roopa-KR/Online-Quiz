class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

    def __str__(self):
        return f"{self.username} ({self.role})"