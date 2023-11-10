from typing import Optional
from numbers import Real

from lsm_project.event_logger.event_logger import EventLogger

from lsm_project.lsm.enumerations import MismatchStrategies
from lsm_project.lsm.models import (
    LSMDescription,
    LSMStatistics,
    LSMLines,
)
import os


PRECISION = 3
event_logger = EventLogger()


def get_lsm_description(
        abscissa: list[float], ordinates: list[float],
        mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL
        ) -> LSMDescription:

    # проверка и приведение к list если все ок
    abscissa = _validate_measurments(abscissa)
    ordinates = _validate_measurments(ordinates)

    # длины не равны
    if len(abscissa) != len(ordinates):
        abscissa, ordinates = _process_mismatch(abscissa, ordinates, mismatch_strategy)

    global event_logger
    event_logger._logger.info("lsm description is got")  # logging

    return _get_lsm_description(abscissa, ordinates)


def get_lsm_lines(
    abscissa: list[float], ordinates: list[float],
    lsm_description: Optional[LSMDescription] = None
) -> LSMLines:

    if lsm_description is None:
        lsm_description = get_lsm_description(abscissa, ordinates)
    elif type(lsm_description) is not LSMDescription:
        raise TypeError
    x = abscissa
    n = len(x)
    a = lsm_description.incline
    b = lsm_description.shift
    a_err = lsm_description.incline_error
    b_err = lsm_description.shift_error

    line_pred = [(a*x[i] + b) for i in range(n)]
    line_ab = []
    line_und = []
    for i in range(n):
        line_ab.append((a+a_err)*x[i] + b + b_err)
        line_und.append((a-a_err)*x[i] + b - b_err)

    global event_logger
    event_logger._logger.info("lsm lines is got")  # logging

    return LSMLines(
        abscissa=abscissa,
        ordinates=ordinates,
        line_predicted=line_pred,
        line_above=line_ab,
        line_under=line_und
    )


def get_report(lsm_description: LSMDescription, path_to_save: str = '') -> str:

    global PRECISION
    incline = lsm_description.incline
    shift = lsm_description.shift
    incline_err = lsm_description.incline_error
    shift_err = lsm_description.shift_error

    report = '\n'.join([
        'LSM computing result'.center(100, "="), '',
        f'[INFO]: incline: {incline:.{PRECISION}f};',
        f'[INFO]: shift: {shift:.{PRECISION}f};',
        f'[INFO]: incline error: {incline_err:.{PRECISION}f};',
        f'[INFO]: shift error: {shift_err:.{PRECISION}f};',
        '', ''.center(100, "=")
    ])

    if path_to_save:
        abs_path = os.path.abspath(path_to_save)
        if os.path.exists(os.path.dirname(abs_path)):
            f = open(path_to_save, "w")
            f.write(report)
            f.close()
        else:
            print(report)
            raise RuntimeError("Directory cant be found")

    global event_logger
    event_logger.info("report is got")  # logging

    return report


# служебная функция для валидации (бывшая _is_valid_measurments)
def _validate_measurments(measurments: list[float]) -> list:

    # проверка типа measure
    if type(measurments) is not (list or tuple):
        raise TypeError

    # проверка типа каждого значения
    for i in measurments:
        if not isinstance(i, Real):
            raise ValueError

    # проверка длины списка
    if len(measurments) <= 2:
        raise ValueError

    global event_logger
    event_logger._logger.info("validation is made")  # logging

    return list(measurments)


# служебная функция для обработки несоответствия размеров
def _process_mismatch(
        abscissa: list[float], ordinates: list[float],
        mismatch_strategy: MismatchStrategies = MismatchStrategies.FALL
        ) -> tuple[list[float], list[float]]:

    if mismatch_strategy == MismatchStrategies.FALL:
        raise RuntimeError
    elif mismatch_strategy == MismatchStrategies.CUT:
        min_len = min(len(abscissa), len(ordinates))
    else:
        raise ValueError

    global event_logger
    event_logger._logger.info("mismatch is processed")  # logging

    return abscissa[:min_len], ordinates[:min_len]


# служебная функция для получения статистик
def _get_lsm_statistics(
        abscissa: list[float], ordinates: list[float]
        ) -> LSMStatistics:
    global PRECISION

    n = len(abscissa)
    x = abscissa
    y = ordinates
    xy = [x[i] * y[i] for i in range(n)]
    x_kv = [i**2 for i in x]

    av_xy = sum(xy)/n
    av_x = sum(x)/n
    av_y = sum(y)/n
    av_x_kv = sum(x_kv)/n

    global event_logger
    event_logger._logger.info("lsm statistics is got")  # logging

    return LSMStatistics(
        abscissa_mean=av_x,
        ordinate_mean=av_y,
        product_mean=av_xy,
        abs_squared_mean=av_x_kv
    )


# служебная функция для получения описания МНК
def _get_lsm_description(
    abscissa: list[float], ordinates: list[float]
) -> LSMDescription:
    global PRECISION

    avarages = _get_lsm_statistics(abscissa, ordinates)
    av_x = avarages.abscissa_mean
    av_y = avarages.ordinate_mean
    av_xy = avarages.product_mean
    av_x_kv = avarages.abs_squared_mean

    n = len(abscissa)
    a = (av_xy-av_x*av_y)/(av_x_kv - av_x**2)
    b = av_y - a*av_x

    y_err = 0
    for i in range(n):
        y_err += (ordinates[i] - a*abscissa[i] - b)**2
    y_err = (y_err/(n-2)) ** 0.5

    a_err = (y_err**2) / (n*(av_x_kv - av_x**2))
    a_err = a_err**0.5

    b_err = (y_err**2 * av_x_kv) / (n*(av_x_kv - av_x**2))
    b_err = b_err**0.5

    global event_logger
    event_logger._logger.info("lsm description is got")  # logging

    return LSMDescription(
        incline=a,
        shift=b,
        incline_error=a_err,
        shift_error=b_err
    )
