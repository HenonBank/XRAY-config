import asyncio
import aiohttp
import aiofiles
import re
import os
import time
import json
import subprocess
import tempfile
import requests
import threading
import hashlib
import socket
import random
import urllib.parse
import ssl
import sys
import platform
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# ========= ДИАГНОСТИКА =========
print(f"🚀 Запуск парсера...")
print(f"📂 Текущая директория: {os.getcwd()}")
print(f"🐍 Python версия: {sys.version}")
print(f"🖥️ Платформа: {platform.system()} {platform.machine()}")

# ========= ФАЙЛЫ =========
SOURCES_FILE = "sources.txt"
OUTPUT_FILE = "url.txt"
CLEAN_FILE = "url_clean.txt"
FILTERED_FILE = "url_filtered.txt"
NAMED_FILE = "url_named.txt"
ENCODED_FILE = "url_encoded.txt"
WORK_FILE = "url_work.txt"
LOG_FILE = "log.txt"
PROCESSED_FILE = "processed.json"
CACHE_FILE = "cache_results.json"
DEBUG_FILE = "debug_failed.txt"
XRAY_LOG_FILE = "xray_errors.log"
COUNTRY_CACHE_FILE = "country_cache.json"

# ========= НАСТРОЙКИ =========
THREADS_DOWNLOAD = 50
CYCLE_DELAY = 3600
LOG_CLEAN_INTERVAL = 86400
CYCLES_BEFORE_DEBUG_CLEAN = 5

XRAY_MAX_WORKERS = 10
XRAY_TEST_URL = "https://www.gstatic.com/generate_204"
XRAY_TIMEOUT = 5
MAX_RETRIES = 2
RETRY_DELAY = 1
MAX_PING_MS = 2700  # МАКСИМАЛЬНЫЙ ПИНГ В МИЛЛИСЕКУНДАХ

print(f"⚡ Настройки: XRAY_MAX_WORKERS={XRAY_MAX_WORKERS}, TIMEOUT={XRAY_TIMEOUT}, MAX_PING={MAX_PING_MS}ms")

# ========= СЧЕТЧИК ЦИКЛОВ =========
cycle_counter = 0

# ========= РЕГУЛЯРКИ =========
VLESS_REGEX = re.compile(r"vless://[^\s]+", re.IGNORECASE)
UUID_REGEX = re.compile(
    r"[0-9a-fA-F]{8}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{12}"
)

# ========= ПОЛНЫЙ СПИСОК ДОМЕНОВ (сокращенная версия для экономии места) =========
DOMAIN_NAMES = {
    # X5 Retail Group
    'x5.ru': 'Пятёрочка',
    '5ka.ru': 'Пятёрочка',
    'perekrestok.ru': 'Перекрёсток',
    'dixy.ru': 'Дикси',
    
    # VK
    'vk.com': 'VK',
    'vk.ru': 'VK',
    'vkontakte.ru': 'VK',
    'userapi.com': 'VK',
    
    # Яндекс
    'yandex.ru': 'Яндекс',
    'ya.ru': 'Яндекс',
    'dzen.ru': 'Дзен',
    'kinopoisk.ru': 'Кинопоиск',
    'yastatic.net': 'Яндекс',
    
    # Mail.ru
    'mail.ru': 'Mail.ru',
    'bk.ru': 'Mail.ru',
    'inbox.ru': 'Mail.ru',
    'list.ru': 'Mail.ru',
    
    # Государственные
    'gosuslugi.ru': 'Госуслуги',
    'nalog.ru': 'ФНС',
    'kremlin.ru': 'Кремль',
    
    # Соцсети
    'ok.ru': 'Одноклассники',
    'odnoklassniki.ru': 'Одноклассники',
    
    # Маркетплейсы
    'ozon.ru': 'Ozon',
    'wildberries.ru': 'Wildberries',
    'wb.ru': 'Wildberries',
    'avito.ru': 'Avito',
    
    # Банки
    'sberbank.ru': 'Сбербанк',
    'sber.ru': 'Сбербанк',
    'tinkoff.ru': 'Тинькофф',
    'tbank.ru': 'Тинькофф',
    'vtb.ru': 'ВТБ',
    'alfabank.ru': 'Альфа-Банк',
    
    # Телеком
    'rostelecom.ru': 'Ростелеком',
    'mts.ru': 'МТС',
    'megafon.ru': 'Мегафон',
    'beeline.ru': 'Билайн',
    'tele2.ru': 'Tele2',
}

print(f"📋 Загружено {len(DOMAIN_NAMES)} доменов в словарь")

# ========= ФУНКЦИИ ДЛЯ ОПРЕДЕЛЕНИЯ СТРАНЫ =========
def get_country_flag(country_code: str) -> str:
    if not country_code or len(country_code) != 2:
        return "🏳️"
    flag = ""
    for char in country_code.upper():
        flag += chr(ord(char) + 0x1F1E6 - ord('A'))
    return flag

def get_country_name(country_code: str) -> str:
    country_names = {
        'RU': 'Россия', 'US': 'США', 'DE': 'Германия', 'NL': 'Нидерланды',
        'GB': 'Великобритания', 'FR': 'Франция', 'CA': 'Канада', 'JP': 'Япония',
        'SG': 'Сингапур', 'HK': 'Гонконг', 'FI': 'Финляндия', 'SE': 'Швеция',
        'NO': 'Норвегия', 'DK': 'Дания', 'PL': 'Польша', 'CZ': 'Чехия',
    }
    return country_names.get(country_code.upper(), country_code)

def save_country_cache(country_info: dict, host: str):
    cache = {}
    if os.path.exists(COUNTRY_CACHE_FILE):
        try:
            with open(COUNTRY_CACHE_FILE, 'r', encoding='utf-8') as f:
                cache = json.load(f)
        except:
            pass
    cache[host] = {
        'country': country_info.get('country'),
        'ip': country_info.get('ip'),
        'city': country_info.get('city'),
        'org': country_info.get('org'),
        'timestamp': datetime.now().isoformat()
    }
    try:
        with open(COUNTRY_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
    except:
        pass

def check_tcp_connection(host: str, port: int, timeout: int = 2) -> bool:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def get_country_info_direct(host: str, port: int) -> dict:
    country_info = {'ip': host, 'country': None, 'city': None, 'region': None, 'org': None, 'timezone': None, 'success': False}
    try:
        is_ip = re.match(r'^(\d{1,3}\.){3}\d{1,3}$', host) is not None
        if is_ip:
            target_ip = host
        else:
            try:
                target_ip = socket.gethostbyname(host)
                country_info['ip'] = target_ip
            except:
                target_ip = host
        try:
            import urllib.request
            url = f"https://ipapi.co/{target_ip}/json/"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                if data.get('country_code'):
                    country_info['country'] = data.get('country_code')
                    country_info['success'] = True
                    return country_info
        except:
            pass
        try:
            url = f"http://ip-api.com/json/{target_ip}?fields=status,countryCode,city,region,org,timezone"
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode())
                if data.get('status') == 'success' and data.get('countryCode'):
                    country_info['country'] = data.get('countryCode')
                    country_info['success'] = True
                    return country_info
        except:
            pass
    except:
        pass
    return country_info

def get_country_info_fallback(host: str, port: int) -> dict:
    country_info = get_country_info_direct(host, port)
    if not country_info.get('country'):
        if port == 443:
            try:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                with socket.create_connection((host, port), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=host) as ssock:
                        cert = ssock.getpeercert()
                        if cert and 'subject' in cert:
                            for item in cert['subject']:
                                for key, value in item:
                                    if key == 'countryName':
                                        country_info['country'] = value
                                        country_info['success'] = True
                                        return country_info
            except:
                pass
    return country_info

def parse_vless_host(url: str) -> str:
    try:
        if not url.startswith('vless://'):
            return None
        content = url[8:]
        at_pos = content.find('@')
        if at_pos == -1:
            return None
        after_at = content[at_pos+1:]
        q_pos = after_at.find('?')
        if q_pos != -1:
            host_part = after_at[:q_pos]
        else:
            host_part = after_at
        hash_pos = host_part.find('#')
        if hash_pos != -1:
            host_part = host_part[:hash_pos]
        if ':' in host_part:
            host = host_part.split(':', 1)[0]
        else:
            host = host_part
        return host
    except:
        return None

# ========= ЛОГ =========
async def log(message: str):
    try:
        now = datetime.now()
        async with aiofiles.open(LOG_FILE, "a", encoding="utf-8") as f:
            await f.write(f"[{now}] {message}\n")
    except:
        pass

def log_xray_error(message: str):
    try:
        with open(XRAY_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
    except:
        pass

# ========= ВАЛИДАЦИЯ =========
def validate_vless(url: str) -> bool:
    if not url.startswith("vless://"):
        return False
    if not UUID_REGEX.search(url):
        return False
    if "@" not in url:
        return False
    if ":" not in url:
        return False
    return True

# ========= WHITELIST =========
def load_whitelist_domains():
    domains = set()
    suffixes = []
    if os.path.exists("whitelist.txt"):
        try:
            with open("whitelist.txt", "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    d = line.strip().lower()
                    if not d or d.startswith('#'):
                        continue
                    domains.add(d)
                    suffixes.append("." + d)
            print(f"📋 Загружено {len(domains)} доменов из whitelist.txt")
        except:
            print("⚠️ Ошибка загрузки whitelist.txt")
    else:
        print("⚠️ Файл whitelist.txt не найден, использую DOMAIN_NAMES")
    return domains, suffixes

# ========= ПРОТОКОЛ / SNI / НАЗВАНИЕ =========
def detect_protocol(vless_url: str) -> str:
    try:
        no_scheme = vless_url[len("vless://"):]
        after_at = no_scheme.split("@", 1)[1]
        query = after_at.split("?", 1)[1] if "?" in after_at else ""
        params = {}
        for part in query.split("&"):
            if "=" in part:
                k, v = part.split("=", 1)
                params[k.lower()] = v.lower()
        transport = params.get("type", "").lower()
        security = params.get("security", "").lower()
        if transport in ("ws", "websocket"):
            return "WS"
        if transport in ("grpc", "gun"):
            return "gRPC"
        if transport in ("xhttp", "httpupgrade"):
            return "XHTTP"
        if transport in ("h2", "http2"):
            return "H2"
        if transport == "tcp":
            return "TCP"
        if security == "reality":
            return "Reality"
        if security in ("tls", "xtls"):
            return "TLS"
        return "TCP"
    except:
        return "Неизвестно"

def extract_all_possible_domains(vless_url: str) -> list:
    domains = set()
    try:
        if not vless_url.startswith("vless://"):
            return []
        content = vless_url[8:]
        at_pos = content.find('@')
        if at_pos == -1:
            return []
        after_at = content[at_pos+1:]
        q_pos = after_at.find('?')
        if q_pos != -1:
            host_part = after_at[:q_pos]
            query_part = after_at[q_pos+1:]
        else:
            host_part = after_at
            query_part = ""
        if ':' in host_part:
            host = host_part.split(':', 1)[0]
        else:
            host = host_part
        if host and '.' in host:
            domains.add(host.lower())
        if query_part:
            if '#' in query_part:
                query_part = query_part.split('#', 1)[0]
            for param in query_part.split('&'):
                if '=' in param:
                    k, v = param.split('=', 1)
                    try:
                        v_decoded = urllib.parse.unquote(v).lower()
                    except:
                        v_decoded = v.lower()
                    if k.lower() == 'sni' and '.' in v_decoded:
                        domains.add(v_decoded)
                    elif k.lower() == 'host' and '.' in v_decoded:
                        domains.add(v_decoded)
        return list(domains)
    except Exception as e:
        return []

def get_human_name(domain: str) -> str:
    if not domain:
        return "Неизвестно"
    d = domain.lower()
    if d in DOMAIN_NAMES:
        return DOMAIN_NAMES[d]
    parts = d.split('.')
    for i in range(len(parts) - 1):
        sub = ".".join(parts[i:])
        if sub in DOMAIN_NAMES:
            return DOMAIN_NAMES[sub]
    if len(parts) >= 2:
        base = ".".join(parts[-2:])
        if base in DOMAIN_NAMES:
            return DOMAIN_NAMES[base]
    return "Неизвестно"

def filter_by_sni(vless_url: str, whitelist_domains: set, whitelist_suffixes: list) -> bool:
    domains = extract_all_possible_domains(vless_url)
    for domain in domains:
        if domain in whitelist_domains:
            return True
        for suffix in whitelist_suffixes:
            if domain.endswith(suffix):
                return True
        parts = domain.split('.')
        if len(parts) >= 2:
            base_domain = '.'.join(parts[-2:])
            if base_domain in whitelist_domains:
                return True
    if not whitelist_domains:
        for domain in domains:
            if domain in DOMAIN_NAMES:
                return True
    return False

# ========= СКАЧИВАНИЕ =========
async def fetch(session, url, sem):
    async with sem:
        try:
            print(f"📥 Скачиваю: {url[:80]}...")
            async with session.get(url, timeout=15) as resp:
                if resp.status == 200:
                    return await resp.text()
        except Exception as e:
            await log(f"Ошибка при скачивании {url}: {e}")
    return None

async def process_url(session, url, sem, output_lock, stats):
    content = await fetch(session, url, sem)
    stats["processed"] += 1
    if not content:
        return
    matches = VLESS_REGEX.findall(content)
    if matches:
        async with output_lock:
            async with aiofiles.open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                for m in matches:
                    await f.write(m + "\n")
        stats["found"] += len(matches)
    print(f"📊 Обработано: {stats['processed']} | Найдено VLESS: {stats['found']}", end="\r")

# ========= ОЧИСТКА =========
async def clean_vless():
    print("\n🧹 Очищаю дубликаты и проверяю валидность...")
    if not os.path.exists(OUTPUT_FILE):
        print("Нет файла url.txt — пропускаю очистку.")
        return
    try:
        async with aiofiles.open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            lines = await f.readlines()
    except:
        print("Ошибка чтения файла")
        return
    unique = set()
    valid = []
    for line in lines:
        url = line.strip()
        if url and url not in unique and validate_vless(url):
            unique.add(url)
            valid.append(url)
    async with aiofiles.open(CLEAN_FILE, "w", encoding="utf-8") as f:
        for url in valid:
            await f.write(url + "\n")
    print(f"✅ Очистка завершена. Итоговых конфигов: {len(valid)}")

# ========= ФИЛЬТРАЦИЯ =========
async def filter_vless():
    print("\n=== ФИЛЬТРАЦИЯ ПО WHITELIST ===")
    if not os.path.exists(CLEAN_FILE):
        print("Нет файла url_clean.txt — пропускаю фильтрацию.")
        return
    domains, suffixes = load_whitelist_domains()
    try:
        with open(CLEAN_FILE, "r", encoding="utf-8", errors="ignore") as f:
            total = sum(1 for _ in f)
    except:
        total = 0
    passed = 0
    processed = 0
    async with aiofiles.open(CLEAN_FILE, "r", encoding="utf-8") as f_in, \
               aiofiles.open(FILTERED_FILE, "w", encoding="utf-8") as f_out:
        async for line in f_in:
            processed += 1
            url = line.strip()
            if not url:
                continue
            if filter_by_sni(url, domains, suffixes):
                await f_out.write(url + "\n")
                passed += 1
            if processed % 100 == 0 and total > 0:
                print(f"Фильтрация: {processed}/{total} | Подошло: {passed}", end="\r")
    print(f"\n✅ Фильтрация завершена. Итог: {passed} конфигов.")

# ========= ПЕРЕИМЕНОВАНИЕ =========
async def rename_configs():
    print("\n=== ПЕРЕИМЕНОВАНИЕ КОНФИГОВ ===")
    if not os.path.exists(FILTERED_FILE):
        print("Нет файла url_filtered.txt — пропускаю переименование.")
        return
    try:
        with open(FILTERED_FILE, "r", encoding="utf-8", errors="ignore") as f:
            total = sum(1 for _ in f)
    except:
        total = 0
    processed = 0
    async with aiofiles.open(FILTERED_FILE, "r", encoding="utf-8") as f_in, \
               aiofiles.open(NAMED_FILE, "w", encoding="utf-8") as f_out:
        async for line in f_in:
            processed += 1
            url = line.strip()
            if not url:
                continue
            protocol = detect_protocol(url)
            domains = extract_all_possible_domains(url)
            human_name = "Неизвестно"
            if domains:
                for domain in domains:
                    name = get_human_name(domain)
                    if name != "Неизвестно":
                        human_name = name
                        break
                if human_name == "Неизвестно" and domains:
                    human_name = domains[0].split('.')[-2].capitalize() if len(domains[0].split('.')) >= 2 else domains[0]
            title = f"{protocol}, {human_name} [#РКП]"
            base = url.split("#", 1)[0]
            new_url = f"{base}#{title}"
            await f_out.write(new_url + "\n")
            if processed % 500 == 0 and total > 0:
                print(f"Переименовано: {processed}/{total}", end="\r")
    print(f"\n✅ Переименование завершено. Итог: {processed} конфигов.")

# ========= НОРМАЛИЗАЦИЯ URL =========
def encode_vless_url(url: str) -> str:
    try:
        if not url.startswith("vless://"):
            return url
        content = url[8:]
        at_pos = content.find('@')
        if at_pos == -1:
            return url
        uuid = content[:at_pos]
        after_at = content[at_pos+1:]
        q_pos = after_at.find('?')
        if q_pos != -1:
            host_part = after_at[:q_pos]
            params_part = after_at[q_pos+1:]
        else:
            host_part = after_at
            params_part = ""
        hash_pos = host_part.find('#')
        if hash_pos != -1:
            host_only = host_part[:hash_pos]
            fragment = host_part[hash_pos+1:]
        else:
            host_only = host_part
            fragment = ""
        if not fragment and params_part:
            hash_pos = params_part.find('#')
            if hash_pos != -1:
                params_only = params_part[:hash_pos]
                fragment = params_part[hash_pos+1:]
                params_part = params_only
        return f"vless://{uuid}@{host_only}"
    except Exception as e:
        return url

async def encode_all_configs():
    print("\n=== КОДИРОВАНИЕ КОНФИГОВ ===")
    if not os.path.exists(NAMED_FILE):
        print("Нет файла url_named.txt — пропускаю кодирование.")
        return
    try:
        with open(NAMED_FILE, 'r', encoding='utf-8') as f:
            configs = [line.strip() for line in f if line.strip()]
    except:
        print("Ошибка чтения файла")
        return
    total = len(configs)
    changed = 0
    async with aiofiles.open(ENCODED_FILE, "w", encoding="utf-8") as f_out:
        for i, url in enumerate(configs, 1):
            encoded_url = encode_vless_url(url)
            await f_out.write(encoded_url + "\n")
            if encoded_url != url:
                changed += 1
            if i % 500 == 0:
                print(f"Закодировано: {i}/{total} | Изменено: {changed}", end="\r")
    print(f"\n✅ Кодирование завершено. Всего: {total}, изменено: {changed}")

# ========= XRAY-ТЕСТЕР =========
class SimpleProgress:
    def __init__(self, total):
        self.total = total
        self.current = 0
        self.start_time = time.time()
        self.lock = threading.Lock()
        self.working_count = 0
        self.retry_count = 0
        self.rejected_count = 0
    
    def update(self, status='', working=False, retry=False, rejected=False):
        with self.lock:
            self.current += 1
            if working:
                self.working_count += 1
            if retry:
                self.retry_count += 1
            if rejected:
                self.rejected_count += 1
            if self.current % 10 == 0 or self.current == self.total:
                elapsed = time.time() - self.start_time
                speed = self.current / elapsed if elapsed > 0 else 0
                print(f"\r📊 [{self.current}/{self.total}] ✅:{self.working_count} ❌:{self.rejected_count} 🔄:{self.retry_count} {speed:.1f} к/с {status}", end='', flush=True)
    
    def finish(self):
        elapsed = time.time() - self.start_time
        print(f"\n✅ Готово! {self.current} конфигов за {elapsed:.1f}с, рабочих: {self.working_count}, отклонено: {self.rejected_count}")

class PortManager:
    def __init__(self, start=20000, end=25000):
        self.ports = list(range(start, end + 1))
        self.used = set()
        self.lock = threading.Lock()
    
    def get_port(self):
        with self.lock:
            available = [p for p in self.ports if p not in self.used]
            if not available:
                return None
            port = random.choice(available)
            self.used.add(port)
            return port
    
    def release_port(self, port):
        with self.lock:
            self.used.discard(port)

class XrayTester:
    def __init__(self, input_file='url_encoded.txt', output_file='url_work.txt', max_workers=10, max_ping_ms=8000):
        self.input_file = input_file
        self.output_file = output_file
        self.max_workers = max_workers
        self.max_ping_ms = max_ping_ms
        self.test_url = XRAY_TEST_URL
        self.timeout = XRAY_TIMEOUT
        self.max_retries = MAX_RETRIES
        self.retry_delay = RETRY_DELAY
        
        if platform.system() == 'Windows':
            self.xray_path = Path('./xray_bin/xray.exe')
        else:
            possible_paths = ['/usr/bin/xray', '/usr/local/bin/xray', './xray_bin/xray']
            self.xray_path = None
            for path in possible_paths:
                if Path(path).exists():
                    self.xray_path = Path(path)
                    break
            if not self.xray_path:
                self.xray_path = Path('./xray_bin/xray')
        
        self.port_manager = PortManager()
        self.debug_file = DEBUG_FILE
        self.xray_log_file = XRAY_LOG_FILE
        
        self.country_cache = {}
        if os.path.exists(COUNTRY_CACHE_FILE):
            try:
                with open(COUNTRY_CACHE_FILE, 'r', encoding='utf-8') as f:
                    self.country_cache = json.load(f)
                print(f"📋 Загружено {len(self.country_cache)} записей из кэша стран")
            except:
                pass
        
        self.saved_urls = set()
        if os.path.exists(output_file):
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        url = line.strip()
                        if url:
                            self.saved_urls.add(url)
                print(f"📋 Загружено {len(self.saved_urls)} уже сохраненных конфигов")
            except:
                pass
        
        print(f"🔍 XrayTester инициализирован")
        print(f"   ⚡ Потоков: {self.max_workers}")
        print(f"   ⏱️ Максимальный пинг: {self.max_ping_ms}ms")
        
        self.xray_available = self.check_xray()
    
    def check_xray(self):
        if not self.xray_path or not self.xray_path.exists():
            print(f"⚠️ Xray не найден по пути: {self.xray_path}")
            return False
        try:
            result = subprocess.run([str(self.xray_path), '-version'], 
                                  capture_output=True, text=True, timeout=5)
            version = result.stdout.split('\n')[0] if result.stdout else 'Unknown'
            print(f"✅ Xray готов: {version}")
            return True
        except Exception as e:
            print(f"⚠️ Ошибка Xray: {e}")
            return False

    def parse_vless_url(self, url):
        try:
            if not url.startswith('vless://'):
                return None
            content = url[8:]
            at_pos = content.find('@')
            if at_pos == -1:
                return None
            uuid = content[:at_pos]
            after_at = content[at_pos+1:]
            q_pos = after_at.find('?')
            if q_pos != -1:
                host_part = after_at[:q_pos]
            else:
                host_part = after_at
            hash_pos = host_part.find('#')
            if hash_pos != -1:
                host_part = host_part[:hash_pos]
            if ':' in host_part:
                host, port_str = host_part.split(':', 1)
                try:
                    port = int(port_str)
                except:
                    port = 443
            else:
                host = host_part
                port = 443
            return {
                'uuid': uuid,
                'host': host,
                'port': port,
                'url': url
            }
        except Exception as e:
            return None

    def create_xray_config(self, parsed, port):
        try:
            config = {
                "log": {"loglevel": "error"},
                "inbounds": [{
                    "port": port,
                    "protocol": "socks",
                    "settings": {"auth": "noauth", "udp": False},
                    "tag": "socks-in"
                }],
                "outbounds": [{
                    "protocol": "vless",
                    "settings": {
                        "vnext": [{
                            "address": parsed['host'],
                            "port": parsed['port'],
                            "users": [{
                                "id": parsed['uuid'],
                                "encryption": "none"
                            }]
                        }]
                    },
                    "streamSettings": {
                        "network": "tcp",
                        "security": "none"
                    },
                    "tag": "proxy"
                }]
            }
            return config
        except Exception as e:
            return None

    def get_country_for_host(self, host, port):
        if host in self.country_cache:
            cached = self.country_cache[host]
            if cached.get('country'):
                return cached.get('country')
        
        country_info = get_country_info_fallback(host, port)
        if country_info.get('country'):
            country_code = country_info['country']
            save_country_cache(country_info, host)
            self.country_cache[host] = country_info
            return country_code
        return None

    def add_country_flag_to_url(self, url, country_code, protocol, ping_ms, service_name=""):
        try:
            if '#' in url:
                base = url.split("#", 1)[0]
                existing_fragment = url.split("#", 1)[1]
            else:
                base = url
                existing_fragment = ""
            
            if country_code:
                flag = get_country_flag(country_code)
                country_name = get_country_name(country_code)
                new_fragment = f"{flag} {protocol}, {country_name} | {ping_ms:.0f}ms | {service_name} [#РКП]" if service_name else f"{flag} {protocol}, {country_name} | {ping_ms:.0f}ms [#РКП]"
            else:
                new_fragment = f"{protocol}, {service_name} | {ping_ms:.0f}ms [#РКП]" if service_name else f"{protocol} | {ping_ms:.0f}ms [#РКП]"
            
            return f"{base}#{new_fragment}"
        except:
            return url

    def save_working_config(self, url, ping, country_code, protocol, service_name=""):
        if ping > self.max_ping_ms:
            return False
        
        final_url = self.add_country_flag_to_url(url, country_code, protocol, ping, service_name)
        
        if final_url in self.saved_urls:
            return False
        
        try:
            with open(self.output_file, 'a', encoding='utf-8') as f:
                f.write(final_url + '\n')
            self.saved_urls.add(final_url)
            return True
        except Exception as e:
            return False

    def test_with_xray(self, parsed, port, attempt=1):
        if not self.xray_available:
            return None
        
        config_file = None
        process = None
        
        try:
            config = self.create_xray_config(parsed, port)
            if not config:
                return None
            
            fd, config_file = tempfile.mkstemp(suffix='.json')
            os.close(fd)
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f)
            
            if platform.system() == 'Windows':
                creationflags = subprocess.CREATE_NO_WINDOW
            else:
                creationflags = 0
                
            process = subprocess.Popen(
                [str(self.xray_path), '-c', config_file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=creationflags
            )
            
            time.sleep(1.0)
            
            if process.poll() is not None:
                return "CRASH"
            
            start = time.time()
            proxies = {'http': f'socks5://127.0.0.1:{port}', 'https': f'socks5://127.0.0.1:{port}'}
            
            try:
                r = requests.get(self.test_url, proxies=proxies, timeout=self.timeout)
                if r.status_code in [200, 204]:
                    ping = (time.time() - start) * 1000
                    return {'working': True, 'ping': ping, 'method': 'xray'}
                else:
                    return "FAIL"
            except requests.exceptions.Timeout:
                return "TIMEOUT"
            except requests.exceptions.ConnectionError:
                return "CONN_ERROR"
            except Exception:
                return "ERROR"
            
        except Exception as e:
            return "EXCEPTION"
        finally:
            if process:
                try: 
                    process.terminate()
                    time.sleep(0.2)
                    if process.poll() is None:
                        process.kill()
                except: 
                    pass
            if config_file and os.path.exists(config_file):
                try: 
                    os.remove(config_file)
                except: 
                    pass

    def test_one(self, url, progress=None):
        parsed = self.parse_vless_url(url)
        if not parsed:
            if progress:
                progress.update('❌ парсинг', working=False)
            return None
        
        protocol = detect_protocol(url)
        domains = extract_all_possible_domains(url)
        service_name = "Неизвестно"
        if domains:
            for domain in domains:
                name = get_human_name(domain)
                if name != "Неизвестно":
                    service_name = name
                    break
        
        port = self.port_manager.get_port()
        if port:
            try:
                for attempt in range(1, self.max_retries + 1):
                    result = self.test_with_xray(parsed, port, attempt)
                    
                    if isinstance(result, dict) and result.get('working'):
                        ping = result.get('ping', 0)
                        
                        if ping > self.max_ping_ms:
                            if progress:
                                progress.update('⏱️ пинг', working=False, rejected=True)
                            self.port_manager.release_port(port)
                            return None
                        
                        country_code = self.get_country_for_host(parsed['host'], parsed['port'])
                        
                        saved = self.save_working_config(url, ping, country_code, protocol, service_name)
                        
                        self.port_manager.release_port(port)
                        if progress:
                            progress.update('✅', working=True)
                        return {'url': url, 'ping': ping, 'method': 'xray', 'country': country_code}
                    
                    elif result in ["TIMEOUT", "FAIL", "CONN_ERROR", "CRASH"]:
                        if attempt < self.max_retries:
                            time.sleep(self.retry_delay)
                            continue
                    
                    else:
                        break
                
                self.port_manager.release_port(port)
            except:
                self.port_manager.release_port(port)
        
        if progress:
            progress.update('❌', working=False)
        return None

    def test_all(self):
        if not os.path.exists(self.input_file):
            print(f"\n❌ Нет файла {self.input_file}")
            return
        
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                all_urls = [line.strip() for line in f if line.strip()]
        except:
            print(f"❌ Ошибка чтения файла {self.input_file}")
            return
        
        if not all_urls:
            print(f"\n📭 Нет конфигов для тестирования")
            return
        
        print(f"\n{'='*60}")
        print(f"🔍 Тестирование {len(all_urls)} конфигов")
        print(f"⚡ Потоков: {self.max_workers}")
        print(f"⏱️ Максимальный пинг: {self.max_ping_ms}ms")
        print('='*60)
        
        working = []
        progress = SimpleProgress(len(all_urls))
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.test_one, url, progress): url for url in all_urls}
            for future in as_completed(futures):
                try:
                    result = future.result(timeout=self.timeout + 5)
                    if result:
                        working.append(result)
                except Exception as e:
                    progress.update('⚠️', working=False)
        
        progress.finish()
        
        print(f"\n📊 Результаты:")
        print(f"   ✅ Работает и добавлено: {len(working)}")
        print(f"   📁 Всего сохранено: {len(self.saved_urls)} уникальных конфигов")
        
        return working

    def run(self):
        self.test_all()

# ========= ОСНОВНОЙ ЦИКЛ =========
async def main_cycle():
    global cycle_counter
    cycle_counter += 1
    
    print(f"\n{'='*60}")
    print(f"=== ЦИКЛ #{cycle_counter} ===")
    print(f"{'='*60}")
    
    # Очистка предыдущих результатов
    for file in [OUTPUT_FILE, CLEAN_FILE, FILTERED_FILE, NAMED_FILE, ENCODED_FILE]:
        if os.path.exists(file):
            os.remove(file)
            print(f"🧹 Удален {file}")
    
    if not os.path.exists(SOURCES_FILE):
        print(f"❌ Нет файла {SOURCES_FILE}")
        return
    
    try:
        with open(SOURCES_FILE, "r", encoding="utf-8", errors="ignore") as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except:
        print(f"❌ Ошибка чтения {SOURCES_FILE}")
        return
    
    if not urls:
        print("⚠️ Нет URL для скачивания")
        return
    
    print(f"📥 Загружаю {len(urls)} источников...")
    
    sem = asyncio.Semaphore(THREADS_DOWNLOAD)
    output_lock = asyncio.Lock()
    stats = {"processed": 0, "found": 0}
    
    async with aiohttp.ClientSession() as session:
        tasks = [process_url(session, url, sem, output_lock, stats) for url in urls]
        await asyncio.gather(*tasks)
    
    print(f"\n✅ Скачивание завершено. Найдено VLESS: {stats['found']}")
    await log(f"Скачивание завершено. Найдено VLESS: {stats['found']}")
    
    if stats['found'] > 0:
        await clean_vless()
        await filter_vless()
        await rename_configs()
        await encode_all_configs()
        
        print("\n=== ЗАПУСК Xray ПРОВЕРКИ ===")
        
        tester = XrayTester(
            input_file=ENCODED_FILE, 
            output_file=WORK_FILE, 
            max_workers=XRAY_MAX_WORKERS,
            max_ping_ms=MAX_PING_MS
        )
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, tester.run)
        
        if os.path.exists(WORK_FILE):
            with open(WORK_FILE, 'r', encoding='utf-8') as f:
                total_working = sum(1 for line in f if line.strip())
            print(f"\n📊 ИТОГО РАБОЧИХ КОНФИГОВ: {total_working}")
    else:
        print("⏭️ Нет новых конфигов для обработки")

async def run_once():
    """Однократный запуск для GitHub Actions"""
    print("🚀 Запуск в режиме однократного выполнения")
    await main_cycle()

async def run_forever():
    """Бесконечный цикл для локального запуска"""
    print("\n🔄 Запуск бесконечного цикла...")
    while True:
        try:
            cycle_start = time.time()
            await main_cycle()
            cycle_time = time.time() - cycle_start
            print(f"✅ Цикл завершен за {cycle_time:.1f}с")
            print(f"⏳ Ожидание {CYCLE_DELAY//3600} час до следующего цикла...")
            await asyncio.sleep(CYCLE_DELAY)
        except KeyboardInterrupt:
            print("\n👋 Остановка по запросу пользователя")
            break
        except Exception as e:
            print(f"\n❌ Ошибка в цикле: {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='VLESS парсер конфигов')
    parser.add_argument('--once', action='store_true', help='Выполнить один цикл и завершить')
    parser.add_argument('--forever', action='store_true', help='Запустить в бесконечном цикле')
    
    args = parser.parse_args()
    
    if args.once:
        asyncio.run(run_once())
    elif args.forever:
        asyncio.run(run_forever())
    else:
        # По умолчанию однократный запуск для GitHub Actions
        asyncio.run(run_once())
