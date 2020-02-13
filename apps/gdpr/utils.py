def change_date_format(date):
    if date:
        return date.strftime("%d/%m/%Y %H:%m:%S")
    return None


def account_info_handler(user):
    return {
        "email": user.email,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "privacy_policy": user.privacy_policy,
        "warning_sent_email": user.warning_sent_email,
        "account_info_link": user.account_info_link,
        "last_account_info_created": change_date_format(user.last_account_info_created),
        "is_staff": user.is_staff,
        "is_active": user.is_active,
        "date_joined": change_date_format(user.date_joined),
        "last_login": change_date_format(user.last_login),
        "last_password_change_date": change_date_format(user.last_password_change_date),
    }
