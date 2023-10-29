from pydantic import ValidationError
from datetime import date, datetime, timezone, timedelta
from unic.utils import config_parser, validators
from typing import Union


class DatetimeModel:
    def convert(self, data: int, **kwargs: any) -> Union[date, datetime]:
        try:
            self.check_parameter_name(kwargs)

            tz = kwargs.get("tz", None)

            target = kwargs["target"]

            input_data = validators.DatetimeModelValidator(
                data=data, target=target, tz=tz
            )
        except ValidationError as e:
            raise ValueError(e.errors()[0]["msg"])

        timezone_hour = 0

        if tz:
            parameter = config_parser.parse_toml("timezone")
            timezone_hour = parameter[tz]["value"]

        dt_timestamp = self.convert_timestamp_by_digits(input_data.data, timezone_hour)

        actions = {
            "datetime": lambda: dt_timestamp,
            "date": lambda: dt_timestamp.date(),
        }

        return actions.get(target, lambda: None)()

    def convert_timestamp_by_digits(self, data: int, timezone_hour: int) -> datetime:
        digits = len(str(abs(data)))

        actions = {
            10: lambda: datetime.fromtimestamp(
                data,
                timezone(timedelta(hours=timezone_hour)),
            ),
            13: lambda: datetime.fromtimestamp(
                data / 1000,
                timezone(timedelta(hours=timezone_hour)),
            ),
        }

        return actions.get(digits, lambda: None)()

    def check_parameter_name(self, parameter_name: dict) -> None:
        if (len(parameter_name) == 1) and ("target" in parameter_name):
            return
        elif (
            (len(parameter_name) == 2)
            and ("target" in parameter_name)
            and ("tz" in parameter_name)
        ):
            return
        else:
            raise ValueError("Invalid parameter name.")
