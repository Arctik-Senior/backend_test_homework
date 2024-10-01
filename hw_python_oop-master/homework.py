from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {"{:.3f}".format(self.duration)} ч.; '
            f'Дистанция: {"{:.3f}".format(self.distance)} км; '
            f'Ср. скорость: {"{:.3f}".format(self.speed)} км/ч; '
            f'Потрачено ккал: {"{:.3f}".format(self.calories)}.'
        )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ):

        self.action = action
        self.duration = duration
        self.weight = weight

    def distance(self) -> float:
        """Получить пройденную дистанцию"""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.distance() / self.duration

    def spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        ...

    def show_training_info(self):
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            training_type=type(self).__name__,
            duration=self.duration,
            distance=self.distance(),
            speed=self.mean_speed(),
            calories=self.spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (
                self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight
                + (
                    (
                        self.mean_speed()
                        * self.KMH_IN_MSEC)
                    ** 2
                    / (
                        self.height
                        / self.CM_IN_M))
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight)
            * self.duration * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_WEIGHT_MULTIPLIER: int = 2
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 ) -> None:

        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration)

    def spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (
                self.mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.CALORIES_WEIGHT_MULTIPLIER
            * self.weight
            * self.duration)


def read_package(workout_type: str, data: list):
    trainigs = {
        "RUN": Running,
        "SWM": Swimming,
        "WLK": SportsWalking,
    }

    assert workout_type in trainigs, "Не верно указан тип тренировки"
    return trainigs[workout_type](*data)


def main(training: Training):
    """Главная функция."""
    info = training.show_training_info()
    print(info.message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
