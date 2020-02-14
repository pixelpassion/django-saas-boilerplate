def change_date_format(date):
    return date.strftime("%d/%m/%Y %H:%m:%S")


def account_info_handler(user):

    return {
        "email": user.email,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "privacy_policy": user.privacy_policy,
        "warning_sent_email": user.warning_sent_email,
        "account_info_link": user.account_info_link,
        "last_account_info_created": change_date_format(user.last_account_info_created)
        if user.last_account_info_created
        else None,
        "is_staff": user.is_staff,
        "is_active": user.is_active,
        "date_joined": change_date_format(user.date_joined)
        if user.date_joined
        else None,
        "last_login": change_date_format(user.last_login) if user.last_login else None,
        "last_password_change_date": change_date_format(user.last_password_change_date)
        if user.last_password_change_date
        else None,
    }
