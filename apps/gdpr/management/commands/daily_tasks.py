from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = """Daily tasks"""

    def handle(self, **options):
        self.run_daily_tasks()

    def run_daily_tasks(self):
        print("--- Running daily tasks... ---")
        call_command("delete_inactive_users")
        call_command("remove_deleted_users")
        call_command("send_account_info")
        print("--- Done ---")
