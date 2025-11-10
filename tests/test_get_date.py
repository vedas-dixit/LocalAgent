from tools.getDate import get_current_date
from datetime import datetime
import re


def test_get_current_date_format():
    res = get_current_date.run({})
    assert isinstance(res, str)
    assert re.match(r"^\d{4}-\d{2}-\d{2}$", res)


def test_get_current_date_today():
    res = get_current_date.run({})
    assert res == datetime.now().strftime("%Y-%m-%d")
