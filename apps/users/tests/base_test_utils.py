def mock_users_email_service_function(mocker, func_name):
    return mocker.patch(f"apps.users.email_service.UsersSaasyEmailService.{func_name}")
