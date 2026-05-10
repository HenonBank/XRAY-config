import re
import os
from pathlib import Path
from html import unescape

def parse_html_chat(html_content):
    """
    Парсит HTML-контент экспортированного чата и возвращает список строк вида "ВРЕМЯ: ИМЯ: ТЕКСТ".
    """
    results = []
    
    # Ищем каждый блок сообщения с классом "message default clearfix"
    # Используем DOTALL, чтобы . мог сопоставлять переводы строк
    message_pattern = re.compile(
        r'<div class="message default clearfix.*?<div class="pull_right date details".*?>(.*?)</div>.*?<div class="from_name">(.*?)</div>.*?<div class="text">(.*?)</div>',
        re.DOTALL
    )
    
    # Также учитываем сообщения, где может быть класс "joined" (продолжение переписки от того же пользователя)
    # Просто расширим поиск, добавив optional "joined"
    message_pattern_extended = re.compile(
        r'<div class="message default clearfix(?: joined)?.*?<div class="pull_right date details".*?>(.*?)</div>.*?<div class="from_name">(.*?)</div>.*?<div class="text">(.*?)</div>',
        re.DOTALL
    )
    
    # Пробуем более гибкий подход: ищем блоки от message default clearfix и внутри уже ищем детали
    # Проще: найти все блоки message
    blocks = re.findall(r'<div class="message default clearfix(?: joined)?.*?</div>\s*</div>\s*</div>', html_content, re.DOTALL)
    
    for block in blocks:
        # Извлекаем время
        time_match = re.search(r'<div class="pull_right date details".*?>(.*?)</div>', block, re.DOTALL)
        if not time_match:
            continue
        time_str = time_match.group(1).strip()
        
        # Извлекаем имя
        name_match = re.search(r'<div class="from_name">(.*?)</div>', block, re.DOTALL)
        if not name_match:
            continue
        name = unescape(name_match.group(1).strip())  # unescape для HTML-сущностей
        
        # Извлекаем текст
        text_match = re.search(r'<div class="text">(.*?)</div>', block, re.DOTALL)
        if not text_match:
            continue
        
        raw_text = text_match.group(1)
        # Убираем HTML-теги внутри текста (например, <a>), но оставляем содержимое
        cleaned_text = re.sub(r'<.*?>', '', raw_text)
        cleaned_text = unescape(cleaned_text.strip())
        
        if cleaned_text:  # Игнорируем пустые сообщения
            results.append(f"{time_str}: {name}: {cleaned_text}")
    
    # Если первый метод не сработал (мало блоков), попробуем альтернативный
    if len(results) < 3:  # Порог срабатывания
        results = []
        # Ищем все сообщения по другому шаблону
        alt_pattern = re.compile(
            r'<div class="message[^>]*>.*?<div class="pull_right date details[^>]*>(.*?)</div>.*?<div class="from_name">(.*?)</div>.*?<div class="text">(.*?)</div>',
            re.DOTALL
        )
        matches = alt_pattern.findall(html_content)
        for time_str, name, raw_text in matches:
            name = unescape(name.strip())
            cleaned_text = re.sub(r'<.*?>', '', raw_text)
            cleaned_text = unescape(cleaned_text.strip())
            if cleaned_text:
                results.append(f"{time_str.strip()}: {name}: {cleaned_text}")
    
    return results

def process_html_file(html_path, output_dir):
    """
    Обрабатывает один HTML-файл и создаёт соответствующий .txt файл с диалогом.
    """
    print(f"Обработка: {html_path.name}")
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Пробуем другую кодировку
        with open(html_path, 'r', encoding='cp1251') as f:
            content = f.read()
    
    messages = parse_html_chat(content)
    
    if not messages:
        print(f"  Предупреждение: Не найдено сообщений в {html_path.name}")
        return False
    
    # Создаём имя выходного файла: исходное имя.html -> исходное имя.txt
    output_filename = html_path.stem + ".txt"
    output_path = output_dir / output_filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for msg in messages:
            f.write(msg + "\n")
    
    print(f"  Записано {len(messages)} сообщений в {output_path.name}")
    return True

def delete_html_files(html_files, dry_run=False):
    """
    Удаляет все переданные HTML-файлы.
    Если dry_run=True, только выводит список файлов для удаления, не удаляя их.
    """
    print("\n" + "="*50)
    print("УДАЛЕНИЕ HTML-ФАЙЛОВ")
    print("="*50)
    
    deleted_count = 0
    for html_file in html_files:
        try:
            if dry_run:
                print(f"[DRY RUN] Будет удалён: {html_file.name}")
            else:
                os.remove(html_file)
                print(f"Удалён: {html_file.name}")
                deleted_count += 1
        except Exception as e:
            print(f"Ошибка при удалении {html_file.name}: {e}")
    
    if not dry_run:
        print(f"\nУдалено файлов: {deleted_count} из {len(html_files)}")

def main():
    # Путь к папке со скриптом (или можно указать конкретную)
    script_dir = Path(__file__).parent
    
    # Ищем все .html файлы в текущей папке
    html_files = list(script_dir.glob("*.html"))
    
    if not html_files:
        print("HTML-файлы не найдены в текущей директории.")
        return
    
    print(f"Найдено HTML-файлов: {len(html_files)}")
    
    # Создаём папку для результатов
    output_dir = script_dir / "parsed_chats"
    output_dir.mkdir(exist_ok=True)
    
    # Обрабатываем все HTML-файлы
    successful_files = []
    for html_file in html_files:
        if process_html_file(html_file, output_dir):
            successful_files.append(html_file)
    
    print(f"\nОбработано успешно: {len(successful_files)} из {len(html_files)}")
    
    # Запрос подтверждения на удаление HTML-файлов
    if successful_files:
        print("\n" + "="*50)
        print("ВНИМАНИЕ!")
        print("="*50)
        print(f"Будут удалены следующие HTML-файлы ({len(successful_files)} шт.):")
        for f in successful_files:
            print(f"  - {f.name}")
        
        confirm = input("\nУдалить эти HTML-файлы? (да/нет): ").strip().lower()
        
        if confirm == 'да' or confirm == 'yes' or confirm == 'д':
            delete_html_files(successful_files, dry_run=False)
        else:
            print("Удаление отменено. HTML-файлы сохранены.")
    
    print(f"\nГотово! Все текстовые файлы сохранены в папке: {output_dir}")

if __name__ == "__main__":
    main()