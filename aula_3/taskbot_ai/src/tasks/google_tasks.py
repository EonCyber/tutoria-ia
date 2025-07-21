from googleapiclient.discovery import build

class GoogleTasks:
    def __init__(self, credentials):
        self.service = build('tasks', 'v1', credentials=credentials)

    def create_task(self, title: str, due_iso: str):
        task = {
            'title': title,
            'due': due_iso,
        }
        created_task = self.service.tasks().insert(tasklist='@default', body=task).execute()
        return created_task