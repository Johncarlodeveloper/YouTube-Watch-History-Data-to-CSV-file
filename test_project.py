import pytest

from project import clean_duration_time, process_datetime, get_category_name


def main():
    test_clean_duration_time()
    test_get_category_name()
    test_process_datetime()


def test_clean_duration_time():
    assert clean_duration_time("PT1H2M3S") == "01:02:03"
    assert clean_duration_time("PT15M25S") == "00:15:25"
    assert clean_duration_time("PT10M13S") == "00:10:13"

    with pytest.raises(ValueError):
        clean_duration_time("PT:1H:1M:3S")


def test_process_datetime():
    assert process_datetime("2017-11-13T06:06:22Z") == "2017-11-13 06:06:22"
    assert process_datetime("2020-04-10T05:36:02Z") == "2020-04-10 05:36:02"

    with pytest.raises(ValueError):
        process_datetime("11-13-2017T06:06:22Z")


def test_get_category_name():
    assert get_category_name("10") == "Music"
    assert get_category_name("20") == "Gaming"
    assert get_category_name("27") == "Education"
    assert get_category_name("100") is None
    assert get_category_name("010") is None
