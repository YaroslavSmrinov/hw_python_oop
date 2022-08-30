from typing import Dict, Any


class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f"Тип тренировки: {self.training_type}; "
                f"Длительность: {self.duration:.3f} ч.; "
                f"Дистанция: {self.distance:.3f} км; "
                f"Ср. скорость: {self.speed:.3f} км/ч; "
                f"Потрачено ккал: {self.calories:.3f}.")


class Training:
    action: int
    duration: float
    weight: float
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        dist: float = self.get_distance()
        return dist / self.duration

    def get_spent_calories(self) -> float:
        pass

    def show_training_info(self) -> InfoMessage:
        training_type: str = self.__class__.__name__
        duration: float = self.duration
        distance: float = self.get_distance()
        speed: float = self.get_mean_speed()
        calories: float = self.get_spent_calories()
        return InfoMessage(training_type, duration, distance, speed, calories)


class Running(Training):

    def get_spent_calories(self) -> float:
        coef_1: int = 18
        coef_2: int = 20
        time_in_minutes: float = self.duration * 60
        mid_speed: float = self.get_mean_speed()
        interim_res: float = (coef_1 * mid_speed - coef_2)
        return interim_res * self.weight / self.M_IN_KM * time_in_minutes


class SportsWalking(Training):
    height: int

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        weight_inx_1: float = 0.035 * self.weight
        weight_inx_2: float = 0.029 * self.weight
        time_in_minutes: float = self.duration * 60
        mean_speed: float = self.get_mean_speed()
        multiplier: int = 2
        interim_res: float = mean_speed ** multiplier // self.height
        return (weight_inx_1 + interim_res * weight_inx_2) * time_in_minutes


class Swimming(Training):
    LEN_STEP: float = 1.38
    M_IN_KM: int = 1000
    length_pool: int
    count_pool: int

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        dist = self.length_pool * self.count_pool / self.M_IN_KM
        return dist / self.duration

    def get_spent_calories(self) -> float:
        multiplier: int = 2
        calory_rate: float = 1.1
        mean_speed: float = self.get_mean_speed()
        return (mean_speed + calory_rate) * multiplier * self.weight


def read_package(workout_type: str, data: list) -> Training:
    sport_types: Dict[str, Any] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return sport_types[workout_type](*data)


def main(training: Training) -> None:
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
