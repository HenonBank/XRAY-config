import re
import os
from pathlib import Path
from html import unescape
from datetime import datetime

def parse_html_chat_fast(html_content):
    """
    Быстрый парсинг HTML-контента экспортированного чата.
    Использует построчный анализ вместо тяжёлых регулярных выражений.
    """
    results = []
    
    # Ищем все блоки сообщений по простому шаблону
    # Разбиваем на строки и ищем маркеры
    lines = html_content.split('\n')
    
    i = 0
    total_lines = len(lines)
    
    while i < total_lines:
        line = lines[i]
        
        # Ищем начало блока сообщения
        if 'class="message default clearfix' in line:
            # Начинаем собирать блок
            block_lines = [line]
            i += 1
            # Собираем блок до закрывающих div'ов
            div_count = 1
            while i < total_lines and div_count > 0:
                block_lines.append(lines[i])
                div_count += lines[i].count('<div')
                div_count -= lines[i].count('</div>')
                i += 1
            
            block = '\n'.join(block_lines)
            
            # Извлекаем время
            time_match = re.search(r'<div class="pull_right date details".*?>(.*?)</div>', block)
            if not time_match:
                continue
            time_str = time_match.group(1).strip()
            
            # Извлекаем имя
            name_match = re.search(r'<div class="from_name">(.*?)</div>', block)
            if not name_match:
                continue
            name = unescape(name_match.group(1).strip())
            
            # Извлекаем текст
            text_match = re.search(r'<div class="text">(.*?)</div>', block, re.DOTALL)
            if text_match:
                raw_text = text_match.group(1)
                cleaned_text = re.sub(r'<.*?>', '', raw_text)
                cleaned_text = unescape(cleaned_text.strip())
                if cleaned_text:
                    results.append(f"{time_str}: {name}: {cleaned_text}")
        else:
            i += 1
    
    return results

def process_html_file_fast(html_path, output_dir):
    """
    Быстрая обработка одного HTML-файла.
    """
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(html_path, 'r', encoding='cp1251') as f:
            content = f.read()
    
    messages = parse_html_chat_fast(content)
    
    if not messages:
        return False
    
    output_filename = html_path.stem + ".txt"
    output_path = output_dir / output_filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for msg in messages:
            f.write(msg + "\n")
    
    return True

def delete_html_files(html_files):
    """
    Удаляет все переданные HTML-файлы.
    """
    print("\n" + "="*50)
    print("УДАЛЕНИЕ HTML-ФАЙЛОВ")
    print("="*50)
    
    deleted_count = 0
    for html_file in html_files:
        try:
            os.remove(html_file)
            print(f"✓ Удалён: {html_file.name}")
            deleted_count += 1
        except Exception as e:
            print(f"✗ Ошибка при удалении {html_file.name}: {e}")
    
    print(f"\nУдалено файлов: {deleted_count} из {len(html_files)}")

def main():
    script_dir = Path(__file__).parent
    html_files = sorted(script_dir.glob("*.html"))
    
    if not html_files:
        print("HTML-файлы не найдены.")
        return
    
    total_files = len(html_files)
    print(f"Найдено HTML-файлов: {total_files}")
    print("="*50)
    
    output_dir = script_dir / "parsed_chats"
    output_dir.mkdir(exist_ok=True)
    
    successful_files = []
    start_time = datetime.now()
    
    for idx, html_file in enumerate(html_files, 1):
        # Показываем прогресс
        percent = (idx / total_files) * 100
        print(f"[{idx:3}/{total_files}] ({percent:5.1f}%) Обработка: {html_file.name}")
        
        if process_html_file_fast(html_file, output_dir):
            successful_files.append(html_file)
    
    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()
    
    print(f"\n{'='*50}")
    print(f"Обработано успешно: {len(successful_files)} из {total_files}")
    print(f"Затраченное время: {elapsed:.2f} секунд")
    
    if successful_files:
        print("\n" + "="*50)
        print("ВНИМАНИЕ! БУДУТ УДАЛЕНЫ HTML-ФАЙЛЫ:")
        print("="*50)
        
        # Показываем первые 10 и последние 10 файлов для экономии места
        if len(successful_files) > 20:
            for f in successful_files[:10]:
                print(f"  - {f.name}")
            print(f"  ... и ещё {len(successful_files) - 20} файлов ...")
            for f in successful_files[-10:]:
                print(f"  - {f.name}")
        else:
            for f in successful_files:
                print(f"  - {f.name}")
        
        confirm = input("\nУдалить эти HTML-файлы? (да/нет): ").strip().lower()
        
        if confirm in ['да', 'yes', 'д', 'y']:
            delete_html_files(successful_files)
        else:
            print("Удаление отменено. HTML-файлы сохранены.")
    
    print(f"\n✅ Готово! Текстовые файлы сохранены в папке: {output_dir}")

if __name__ == "__main__":
    main()