from abc import ABC, abstractmethod

DEFAULT_HOURS = 8
BONUS = 0.15


class Department:
    def __init__(self, name, code):
        self.name = name
        self.code = code


class Employee(ABC):
    def __init__(self, code, name, salary, department):
        self.__department = department
        self.code = code
        self.name = name
        self.salary = salary

    def get_department(self):
        return self.__department.name

    def set_department(self, department_name):
        self.__department.name = department_name

    @abstractmethod
    def calc_bonus(self):
        pass

    def get_hours(self):
        return DEFAULT_HOURS


class Manager(Employee):
    def __init__(self, code, name, salary):
        super().__init__(code, name, salary, Department('managers', 1))

    def calc_bonus(self):
        return self.salary * BONUS


class Seller(Employee):
    def __init__(self, code, name, salary):
        super().__init__(code, name, salary, Department('sellers', 2))
        self.__sales = 0

    def get_sales(self):
        return self.__sales

    def put_sales(self, sales):
        self.__sales += sales

    def calc_bonus(self):
        return self.__sales * BONUS
