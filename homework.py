from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: classmethod
    duration: float
    distance: float
    speed: float
    calories: float

    def __str__(self):
        return self.get_message()

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f"Длительность: {format(self.duration, '.3f')} ч.; "
                f"Дистанция: {format(self.distance, '.3f')} км; "
                f"Ср. скорость: {format(self.speed, '.3f')} км/ч; "
                f"Потрачено ккал: {format(self.calories, '.3f')}.")


@dataclass
class Training:
    """Общий класс тренировок"""
    action: int
    duration: float
    weight: float

    M_IN_KM: float = 1000
    MIN_IN_H: float = 60
    CM_IN_M: float = 100
    LEN_STEP: float = 0.65

    def __str__(self):
        return self.__class__.__name__

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения км/ч."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # raise NotImplementedError('Не определен метод
        # подсчета калорий для данного вида спорта')
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        distance = self.get_distance()
        training_type = self.__class__.__name__
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type,
                           self.duration,
                           distance,
                           speed,
                           calories)


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    KMH_IN_MSEC: float = 0.278

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                 + ((self.get_mean_speed() * self.KMH_IN_MSEC) ** 2)
                 / (self.height / self.CM_IN_M)
                 * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                 * self.weight) * self.duration * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    CALORIES_WEIGHT_MULTIPLIER = 2
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    LEN_STEP: float = 1.38

    def __str__(self):
        return self.__class__.__name__

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        self.LEN_STEP: float = 1.38
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainings = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type not in trainings:
        raise ValueError('Неожиданный способ тренировки')
    try:
        trainings[workout_type](*data)
    except TypeError:
        print('TypeError: Неожиданные данные')
    class_type = trainings[workout_type](*data)
    return class_type


def main(training: Training) -> None:
    """Главная функция."""
    info = Training.show_training_info(training)
    print(info)
    return


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
