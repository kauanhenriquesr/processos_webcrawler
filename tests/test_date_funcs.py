import pytest
from src import date_funcs
from datetime import date

def test_str_to_date():
    assert date_funcs.str_to_date("01/02/2004") == date(2004, 2, 1)

def test_date_to_str():
    assert date_funcs.date_to_str(date(2004, 2, 1)) == "01/02/2004"