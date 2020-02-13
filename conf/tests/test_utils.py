import pytest

from conf.utils import account_warning_and_deletion_in_weeks_are_correct


@pytest.mark.parametrize(
    "deletion_weeks, warning_weeks",
    [
        [1, (52, 53)],
        [1, (1, 4)],
        [52, (0, 4)],
        [3, (2, 3)],
        [52, (4, 1)],
        [52, (4, 4)],
        [4, (4, 4)],
        [4, ("4", "4")],
        [None, (4, 4)],
        [52, (None, 4)],
        [52, (4)],
        [52, (0)],
        [52, (4,)],
        [52, (0,)],
        [52, ()],
        [52, (4, None)],
        [52, 0],
        [52, "0"],
        [0, None],
        [None, (0, 0)],
        ["52", (1, 4)],
    ],
)
def test_account_warning_and_deletion_in_weeks_are_correct_function_incorrect(
    settings, deletion_weeks, warning_weeks
):
    settings.INACTIVE_ACCOUNT_DELETION_IN_WEEKS = deletion_weeks
    settings.INACTIVE_ACCOUNT_WARNING_IN_WEEKS = warning_weeks
    assert not account_warning_and_deletion_in_weeks_are_correct(
        deletion_weeks, warning_weeks
    )


@pytest.mark.parametrize(
    "deletion_weeks, warning_weeks",
    [[52, (1, 4)], [None, (1, 4)], [52, None], [None, None]],
)
def test_account_warning_and_deletion_in_weeks_are_correct_function_correct(
    settings, deletion_weeks, warning_weeks
):
    settings.INACTIVE_ACCOUNT_DELETION_IN_WEEKS = deletion_weeks
    settings.INACTIVE_ACCOUNT_WARNING_IN_WEEKS = warning_weeks
    assert account_warning_and_deletion_in_weeks_are_correct(
        deletion_weeks, warning_weeks
    )
