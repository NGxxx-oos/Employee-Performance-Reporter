from dataclasses import dataclass
from typing import List


@dataclass
class Employee:
    """Модель сотрудника для хранения данных из CSV."""
    name: str
    position: str
    completed_tasks: int
    performance: float
    skills: List[str]
    team: str
    experience_years: int

    @classmethod
    def from_csv_row(cls, row: dict) -> 'Employee':
        """Создает объект Employee из строки CSV."""
        return cls(
            name=row['name'],
            position=row['position'],
            completed_tasks=int(row['completed_tasks']),
            performance=float(row['performance']),
            skills=[skill.strip() for skill in row['skills'].split(',')],
            team=row['team'],
            experience_years=int(row['experience_years'])
        )