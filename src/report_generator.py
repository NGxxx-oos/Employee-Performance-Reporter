import csv
from typing import List, Dict, Any
from abc import ABC, abstractmethod
from .models import Employee


class BaseReport(ABC):
    """Базовый класс для всех отчетов."""
    
    @abstractmethod
    def generate(self, employees: List[Employee]) -> List[Dict[str, Any]]:
        """Генерирует отчет на основе списка сотрудников."""
        pass
    
    @abstractmethod
    def get_report_name(self) -> str:
        """Возвращает название отчета."""
        pass


class PerformanceReport(BaseReport):
    """Отчет по средней эффективности по должностям."""
    
    def generate(self, employees: List[Employee]) -> List[Dict[str, Any]]:
        """Генерирует отчет по эффективности."""
        position_data = {}
        
        for employee in employees:
            if employee.position not in position_data:
                position_data[employee.position] = {
                    'performance_sum': 0,
                    'count': 0
                }
            
            position_data[employee.position]['performance_sum'] += employee.performance
            position_data[employee.position]['count'] += 1
        
        report = []
        for position, data in position_data.items():
            avg_performance = data['performance_sum'] / data['count']
            report.append({
                'position': position,
                'avg_performance': round(avg_performance, 2)
            })
        
        # Сортировка по убыванию эффективности
        report.sort(key=lambda x: x['avg_performance'], reverse=True)
        return report
    
    def get_report_name(self) -> str:
        return "performance"


class ReportFactory:
    """Фабрика для создания отчетов."""
    
    _reports = {
        'performance': PerformanceReport
    }
    
    @classmethod
    def create_report(cls, report_type: str) -> BaseReport:
        """Создает отчет указанного типа."""
        if report_type not in cls._reports:
            raise ValueError(f"Unknown report type: {report_type}. "
                           f"Available reports: {list(cls._reports.keys())}")
        return cls._reports[report_type]()
    
    @classmethod
    def register_report(cls, report_type: str, report_class):
        """Регистрирует новый тип отчета."""
        if not issubclass(report_class, BaseReport):
            raise TypeError("Report class must inherit from BaseReport")
        cls._reports[report_type] = report_class


class CSVReader:
    """Класс для чтения CSV-файлов."""
    
    @staticmethod
    def read_files(file_paths: List[str]) -> List[Employee]:
        """Читает несколько CSV-файлов и возвращает список сотрудников."""
        employees = []
        
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        employees.append(Employee.from_csv_row(row))
            except FileNotFoundError:
                raise FileNotFoundError(f"File not found: {file_path}")
            except Exception as e:
                raise IOError(f"Error reading file {file_path}: {str(e)}")
        
        return employees