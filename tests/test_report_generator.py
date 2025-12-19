import pytest
import tempfile
import csv
from src.report_generator import PerformanceReport, ReportFactory, CSVReader
from src.models import Employee


@pytest.fixture
def sample_employees():
    """Фикстура с тестовыми данными сотрудников."""
    return [
        Employee(
            name="Alex Ivanov",
            position="Backend Developer",
            completed_tasks=45,
            performance=4.8,
            skills=["Python", "Django", "PostgreSQL", "Docker"],
            team="API Team",
            experience_years=5
        ),
        Employee(
            name="Maria Petrova",
            position="Frontend Developer",
            completed_tasks=38,
            performance=4.7,
            skills=["React", "TypeScript", "Redux", "CSS"],
            team="Web Team",
            experience_years=4
        ),
        Employee(
            name="John Smith",
            position="Data Scientist",
            completed_tasks=29,
            performance=4.6,
            skills=["Python", "ML", "SQL", "Pandas"],
            team="AI Team",
            experience_years=3
        ),
        Employee(
            name="Another Backend",
            position="Backend Developer",
            completed_tasks=50,
            performance=4.9,
            skills=["Java", "Spring"],
            team="API Team",
            experience_years=6
        )
    ]


def test_performance_report_generate(sample_employees):
    """Тест генерации отчета по эффективности."""
    report = PerformanceReport()
    result = report.generate(sample_employees)
    
    assert len(result) == 3  # 3 разные должности
    
    # Проверяем сортировку (по убыванию эффективности)
    assert result[0]['avg_performance'] >= result[1]['avg_performance']
    assert result[1]['avg_performance'] >= result[2]['avg_performance']
    
    # Проверяем расчет средней эффективности для Backend Developer
    backend_data = [e for e in result if e['position'] == 'Backend Developer'][0]
    expected_avg = (4.8 + 4.9) / 2
    assert backend_data['avg_performance'] == round(expected_avg, 2)


def test_performance_report_get_name():
    """Тест получения названия отчета."""
    report = PerformanceReport()
    assert report.get_report_name() == "performance"


def test_report_factory():
    """Тест фабрики отчетов."""
    report = ReportFactory.create_report('performance')
    assert isinstance(report, PerformanceReport)
    
    with pytest.raises(ValueError):
        ReportFactory.create_report('unknown_report')


def test_csv_reader():
    """Тест чтения CSV файлов."""
    # Создаем временный CSV файл
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        writer = csv.DictWriter(f, fieldnames=[
            'name', 'position', 'completed_tasks', 'performance', 
            'skills', 'team', 'experience_years'
        ])
        writer.writeheader()
        writer.writerow({
            'name': 'Test User',
            'position': 'Test Position',
            'completed_tasks': '100',
            'performance': '5.0',
            'skills': 'Python, Testing',
            'team': 'Test Team',
            'experience_years': '10'
        })
        temp_file = f.name
    
    try:
        employees = CSVReader.read_files([temp_file])
        assert len(employees) == 1
        assert employees[0].name == 'Test User'
        assert employees[0].position == 'Test Position'
        assert employees[0].performance == 5.0
        assert employees[0].skills == ['Python', 'Testing']
    finally:
        import os
        os.unlink(temp_file)


def test_csv_reader_file_not_found():
    """Тест обработки отсутствующего файла."""
    with pytest.raises(FileNotFoundError):
        CSVReader.read_files(['nonexistent_file.csv'])


def test_employee_from_csv_row():
    """Тест создания Employee из CSV строки."""
    row = {
        'name': 'Test Name',
        'position': 'Test Position',
        'completed_tasks': '50',
        'performance': '4.5',
        'skills': 'Python, Java, Go',
        'team': 'Test Team',
        'experience_years': '3'
    }
    
    employee = Employee.from_csv_row(row)
    
    assert employee.name == 'Test Name'
    assert employee.position == 'Test Position'
    assert employee.completed_tasks == 50
    assert employee.performance == 4.5
    assert employee.skills == ['Python', 'Java', 'Go']
    assert employee.team == 'Test Team'
    assert employee.experience_years == 3