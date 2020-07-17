from abc import abstractmethod


# Methods to convert to SQL
class ConvertSQL:
    @abstractmethod
    def to_sql(self) -> str:
        pass
