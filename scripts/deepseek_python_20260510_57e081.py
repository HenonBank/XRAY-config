# Быстрая версия с lxml (нужно установить: pip install lxml)
try:
    from lxml import html
    USE_LXML = True
except ImportError:
    USE_LXML = False
    print("Для максимальной скорости установите lxml: pip install lxml")

def parse_html_chat_lxml(html_content):
    """Супер-быстрый парсинг с использованием lxml"""
    tree = html.fromstring(html_content)
    results = []
    
    # Ищем все блоки сообщений
    messages = tree.xpath('//div[contains(@class, "message") and contains(@class, "default")]')
    
    for msg in messages:
        # Время
        time_elem = msg.xpath('.//div[contains(@class, "pull_right") and contains(@class, "date")]')
        if not time_elem:
            continue
        time_str = time_elem[0].text_content().strip()
        
        # Имя
        name_elem = msg.xpath('.//div[contains(@class, "from_name")]')
        if not name_elem:
            continue
        name = name_elem[0].text_content().strip()
        
        # Текст
        text_elem = msg.xpath('.//div[contains(@class, "text")]')
        if not text_elem:
            continue
        text = text_elem[0].text_content().strip()
        
        if text:
            results.append(f"{time_str}: {name}: {text}")
    
    return results