import pytest

from project import clean_duration_time, process_datetime, get_category_name


def main():
    test_clean_duration_time()
    test_process_datetime()
    test_get_category_name()


def test_clean_duration_time():
    assert clean_duration_time('PT1H2M3S') == '01:02:03'
    assert clean_duration_time('PT15M25S') == '00:15:25'
    assert clean_duration_time('PT10M13S') == '00:10:13'


def test_process_datetime():
    assert process_datetime('2017-11-13T06:06:22Z') == '2017-11-13 06:06:22'
    assert process_datetime('2020-04-10T05:36:02Z') == '2020-04-10 05:36:02'


def test_get_category_name():
    assert get_category_name('10') == 'Music'
    assert get_category_name('20') == 'Gaming'
    assert get_category_name('27') == 'Education'



