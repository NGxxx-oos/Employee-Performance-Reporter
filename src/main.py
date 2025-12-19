#!/usr/bin/env python3
import argparse
import sys
from tabulate import tabulate
from .report_generator import ReportFactory, CSVReader


def parse_arguments():
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description='Generate reports from employee CSV files'
    )
    
    parser.add_argument(
        '--files',
        nargs='+',
        required=True,
        help='Paths to CSV files with employee data'
    )
    
    parser.add_argument(
        '--report',
        required=True,
        help='Type of report to generate (performance)'
    )
    
    return parser.parse_args()


def main():
    """Основная функция скрипта."""
    args = parse_arguments()
    
    try:
        # Чтение данных из файлов
        employees = CSVReader.read_files(args.files)
        
        if not employees:
            print("No employee data found in the provided files.")
            return
        
        # Создание отчета
        report_generator = ReportFactory.create_report(args.report)
        report_data = report_generator.generate(employees)
        
        # Вывод отчета
        if not report_data:
            print("No data available for the report.")
            return
        
        headers = list(report_data[0].keys())
        rows = [[row[header] for header in headers] for row in report_data]
        
        print(f"\nReport: {report_generator.get_report_name()}\n")
        print(tabulate(rows, headers=headers, tablefmt='grid'))
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()