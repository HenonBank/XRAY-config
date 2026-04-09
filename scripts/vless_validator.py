#!/usr/bin/env python3
"""
Скрипт для валидации и очистки VLESS конфигураций
Удаляет дубликаты, проверяет формат и сортирует конфиги
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

class VlessValidator:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.stats = {
            "total": 0,
            "valid": 0,
            "invalid": 0,
            "duplicates": 0
        }
    
    def validate_vless(self, config: str) -> bool:
        """Проверяет корректность формата VLESS ссылки"""
        if not config.startswith("vless://"):
            return False
        
        try:
            # Базовая проверка структуры
            uuid_part = config[8:].split('@')[0]
            if len(uuid_part) != 36:
                return False
            
            # Проверка UUID формата
            uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
            if not re.match(uuid_pattern, uuid_part, re.IGNORECASE):
                return False
            
            return True
        except Exception:
            return False
    
    def process_file(self, filepath: Path) -> tuple[list[str], list[str]]:
        """Обрабатывает файл: удаляет дубликаты и невалидные записи"""
        valid_configs = []
        invalid_configs = []
        seen = set()
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                configs = f.readlines()
            
            self.stats["total"] += len(configs)
            
            for config in configs:
                config = config.strip()
                if not config:
                    continue
                
                if config in seen:
                    self.stats["duplicates"] += 1
                    continue
                
                seen.add(config)
                
                if self.validate_vless(config):
                    valid_configs.append(config)
                    self.stats["valid"] += 1
                else:
                    invalid_configs.append(config)
                    self.stats["invalid"] += 1
            
            return valid_configs, invalid_configs
        
        except Exception as e:
            print(f"❌ Ошибка чтения файла {filepath}: {e}")
            return [], []
    
    def save_results(self, valid: list[str], invalid: list[str], output_dir: Path):
        """Сохраняет результаты обработки"""
        output_dir.mkdir(exist_ok=True)
        
        # Сохраняем валидные конфиги
        if valid:
            valid_file = output_dir / f"vless_clean_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(valid_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(valid))
            print(f"✅ Валидные конфиги сохранены: {valid_file} ({len(valid)} шт.)")
        
        # Сохраняем невалидные (для анализа)
        if invalid:
            invalid_file = output_dir / f"vless_invalid_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(invalid_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(invalid))
            print(f"⚠️ Невалидные конфиги сохранены: {invalid_file} ({len(invalid)} шт.)")
    
    def run(self):
        """Запускает обработку всех VLESS файлов"""
        print("🔍 Поиск VLESS конфигураций...")
        
        vless_files = list(self.data_dir.glob("vless*.txt"))
        
        if not vless_files:
            print("❌ Файлы с VLESS конфигурациями не найдены")
            return
        
        print(f"📁 Найдено файлов: {len(vless_files)}")
        
        all_valid = []
        all_invalid = []
        
        for file in vless_files:
            print(f"\n📄 Обработка: {file.name}")
            valid, invalid = self.process_file(file)
            all_valid.extend(valid)
            all_invalid.extend(invalid)
        
        # Удаляем дубликаты между файлами
        final_valid = list(dict.fromkeys(all_valid))
        final_invalid = list(dict.fromkeys(all_invalid))
        
        print("\n" + "="*50)
        print("📊 СТАТИСТИКА:")
        print(f"   Всего обработано: {self.stats['total']}")
        print(f"   ✅ Валидные: {len(final_valid)}")
        print(f"   ❌ Невалидные: {len(final_invalid)}")
        print(f"   🔄 Дубликаты удалены: {self.stats['duplicates']}")
        print("="*50)
        
        # Сохраняем результаты
        output_dir = self.data_dir / "processed"
        self.save_results(final_valid, final_invalid, output_dir)
        
        print("\n✨ Обработка завершена!")


if __name__ == "__main__":
    validator = VlessValidator()
    validator.run()
