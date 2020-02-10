def account_warning_and_deletion_in_weeks_are_correct(  # noqa
    deletion_weeks: int, warning_weeks: tuple
) -> bool:
    """ Validates variables INACTIVE_ACCOUNT_DELETION_IN_WEEKS
        and INACTIVE_ACCOUNT_WARNING_IN_WEEKS.
        INACTIVE_ACCOUNT_DELETION_IN_WEEKS must not be
        zero or less than one of INACTIVE_ACCOUNT_WARNING_IN_WEEKS.
        Check if INACTIVE_ACCOUNT_DELETION_IN_WEEKS is an integer.
        Also check if INACTIVE_ACCOUNT_WARNING_IN_WEEKS is a tuple with two integers.
        If one of the conditions is not satisfied, returns False else True.
    """
    if deletion_weeks is not None and (
        type(deletion_weeks) != int or deletion_weeks == 0
    ):
        return False

    if warning_weeks is not None:
        if type(warning_weeks) == tuple and len(warning_weeks) == 2:
            first_week_warning = warning_weeks[0]
            second_week_warning = warning_weeks[1]
            if (
                (not first_week_warning or not second_week_warning)
                or first_week_warning >= second_week_warning
                or (type(first_week_warning) != int or type(second_week_warning) != int)
            ):
                return False
        else:
            return False

        if deletion_weeks is not None:
            if (
                deletion_weeks <= first_week_warning
                or deletion_weeks <= second_week_warning
            ):
                return False
    return True
