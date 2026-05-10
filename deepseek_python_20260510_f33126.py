import re
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
        return
    
    # Создаём имя выходного файла: исходное имя.html -> исходное имя.txt
    output_filename = html_path.stem + ".txt"
    output_path = output_dir / output_filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for msg in messages:
            f.write(msg + "\n")
    
    print(f"  Записано {len(messages)} сообщений в {output_path.name}")

def main():
    # Путь к папке со скриптом (или можно указать конкретную)
    script_dir = Path(__file__).parent
    
    # Ищем все .html файлы в текущей папке
    html_files = list(script_dir.glob("*.html"))
    
    if not html_files:
        print("HTML-файлы не найдены в текущей директории.")
        return
    
    # Создаём папку для результатов
    output_dir = script_dir / "parsed_chats"
    output_dir.mkdir(exist_ok=True)
    
    for html_file in html_files:
        process_html_file(html_file, output_dir)
    
    print(f"\nГотово! Все текстовые файлы сохранены в папке: {output_dir}")

if __name__ == "__main__":
    main()