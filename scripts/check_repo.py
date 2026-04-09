#!/usr/bin/env python3
"""
Скрипт для проверки и валидации конфигурационных файлов в репозитории.
Проверяет наличие необходимых файлов, их размер и базовую структуру.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

def check_directory_structure():
    """Проверка структуры директорий."""
    required_dirs = ['data', 'blacklists', 'whitelists', 'tor_bridges', 'clients', 'mirrors', 'assets']
    base_path = Path(__file__).parent.parent
    
    print(f"📁 Проверка структуры директорий в: {base_path}")
    print("-" * 50)
    
    for dir_name in required_dirs:
        dir_path = base_path / dir_name
        if dir_path.exists() and dir_path.is_dir():
            files_count = len(list(dir_path.iterdir()))
            print(f"✅ {dir_name}/ - найдено файлов: {files_count}")
        else:
            print(f"❌ {dir_name}/ - отсутствует")
    print()

def validate_json_files():
    """Валидация JSON файлов в папке data."""
    data_path = Path(__file__).parent.parent / 'data'
    
    if not data_path.exists():
        print("⚠️ Папка data не найдена")
        return
    
    print(f"📄 Валидация JSON файлов в: {data_path}")
    print("-" * 50)
    
    json_files = list(data_path.glob('*.json'))
    
    if not json_files:
        print("ℹ️ JSON файлы не найдены")
        return
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            size_kb = json_file.stat().st_size / 1024
            keys_count = len(data) if isinstance(data, dict) else len(data) if isinstance(data, list) else 0
            
            print(f"✅ {json_file.name} - размер: {size_kb:.2f} KB, элементов: {keys_count}")
        except json.JSONDecodeError as e:
            print(f"❌ {json_file.name} - ошибка JSON: {e}")
        except Exception as e:
            print(f"❌ {json_file.name} - ошибка: {e}")
    print()

def check_txt_files_stats():
    """Статистика по TXT файлам."""
    data_path = Path(__file__).parent.parent / 'data'
    
    if not data_path.exists():
        return
    
    print(f"📝 Статистика TXT файлов в: {data_path}")
    print("-" * 50)
    
    txt_files = list(data_path.glob('*.txt'))
    
    if not txt_files:
        print("ℹ️ TXT файлы не найдены")
        return
    
    for txt_file in txt_files:
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            size_kb = txt_file.stat().st_size / 1024
            non_empty_lines = sum(1 for line in lines if line.strip())
            
            print(f"📄 {txt_file.name} - размер: {size_kb:.2f} KB, строк: {len(lines)}, непустых: {non_empty_lines}")
        except Exception as e:
            print(f"❌ {txt_file.name} - ошибка: {e}")
    print()

def generate_report():
    """Генерация отчета о состоянии репозитория."""
    print("=" * 50)
    print("📊 ОТЧЕТ О СОСТОЯНИИ РЕПОЗИТОРИЯ")
    print(f"🕒 Дата проверки: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    print()
    
    check_directory_structure()
    validate_json_files()
    check_txt_files_stats()
    
    print("✨ Проверка завершена!")

if __name__ == "__main__":
    try:
        generate_report()
    except KeyboardInterrupt:
        print("\n⚠️ Прервано пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1)
