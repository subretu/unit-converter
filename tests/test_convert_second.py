import pytest
from unicorn.unit import timeunit


class TestConverterSecond:
    def test_convert_second_msec(self):
        test_timeunit = timeunit.TimeUnit()
        result = test_timeunit.convert_second(8, "msec")

        assert result == 0.008

    @pytest.mark.parametrize(
        "msec, unit, expect",
        [(8, "msec", 0.008), (9, "msec", 0.009), (10, "msec", 0.01)],
    )
    def test_convert_second_msec2(self, msec, unit, expect):
        test_timeunit = timeunit.TimeUnit()
        result = test_timeunit.convert_second(msec, unit)

        assert result == expect

    def test_convert_second_sec(self):
        test_timeunit = timeunit.TimeUnit()
        result = test_timeunit.convert_second(200, "sec")

        assert result == 200

    def test_convert_second_min(self):
        test_timeunit = timeunit.TimeUnit()
        result = test_timeunit.convert_second(19, "min")

        assert result == 1140

    def test_convert_second_hour(self):
        test_timeunit = timeunit.TimeUnit()
        result = test_timeunit.convert_second(4, "hour")

        assert result == 14400

    def test_convert_second_fail(self):
        with pytest.raises(Exception) as e:
            test_timeunit = timeunit.TimeUnit()
            _ = test_timeunit.convert_second(35, "second")

        error_msg = """1 validation error for TimeUnitrModel
unit
  Undefined unit. (type=value_error)"""
        assert str(e.value) == error_msg
