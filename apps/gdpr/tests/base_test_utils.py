def mock_gdpr_email_service_function(mocker, func_name):
    return mocker.patch(f"apps.gdpr.email_service.GDPRSaasyEmailService.{func_name}")
