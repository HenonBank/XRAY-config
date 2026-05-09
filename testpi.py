#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Xray VPN Proxy Checker v2.0
Тщательная проверка VLESS прокси ссылок на работоспособность
Поддерживает: одиночные ссылки, файлы со ссылками, пакетную проверку
Генерирует: JSON отчеты, HTML отчеты, статистику, мониторинг, TXT со списком рабочих прокси
"""

import asyncio
import subprocess
import json
import re
import os
import tempfile
import time
import sys
import argparse
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
import urllib.parse
import socket
import ssl
import hashlib
import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Цвета для вывода
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'
BOLD = '\033[1m'

class VlessProxyChecker:
    """Проверка VLESS прокси с реальными тестами"""
    
    def __init__(self, verbose: bool = False, timeout: int = 10, max_workers: int = 3):
        self.results = []
        self.verbose = verbose
        self.timeout = timeout
        self.max_workers = max_workers
        self.temp_dir = tempfile.mkdtemp(prefix="xray_check_")
        self.xray_binary = self._find_xray()
        self.test_urls = [
            "https://www.google.com/generate_204",
            "https://www.cloudflare.com/cdn-cgi/trace",
            "https://www.youtube.com",
            "https://www.github.com",
            "https://telegram.org",
            "https://www.microsoft.com",
            "https://api.ipify.org",
            "https://ipinfo.io/json",
            "https://speed.cloudflare.com/__down?bytes=1000000"
        ]
        self.results_file = f"proxy_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.html_report = f"proxy_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        self.working_txt = f"working_proxies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
    def _find_xray(self) -> Optional[str]:
        """Поиск Xray бинарника в системе"""
        possible_paths = [
            "/usr/local/bin/xray",
            "/usr/bin/xray",
            "./xray",
            "xray",
            "/opt/xray/xray",
            "/tmp/xray",
            os.path.expanduser("~/xray"),
            "/overlay/upper/usr/bin/xray"  # Для OpenWrt/FriendlyWrt
        ]
        
        for path in possible_paths:
            try:
                result = subprocess.run([path, "--version"], 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=2)
                if result.returncode == 0:
                    if self.verbose:
                        print(f"{GREEN}✓ Xray найден: {path}{RESET}")
                    return path
            except:
                continue
        
        print(f"{YELLOW}⚠ Xray не найден. Проверка будет ограничена (без реального прокси){RESET}")
        print(f"{YELLOW}  Скачайте Xray: https://github.com/XTLS/Xray-core/releases{RESET}")
        return None
    
    def parse_vless_link(self, link: str) -> Optional[Dict]:
        """Парсинг VLESS ссылки"""
        try:
            link = link.strip()
            if not link or not link.startswith('vless://'):
                return None
            
            # Удаляем vless://
            rest = link[8:]
            
            # Разделяем на UUID@host:port и параметры
            if '@' in rest:
                uuid_host, params_part = rest.split('@', 1)
                
                # UUID
                uuid = uuid_host
                
                # Host и Port
                if '?' in params_part:
                    host_port = params_part.split('?')[0]
                    query_part = params_part.split('?', 1)[1]
                else:
                    host_port = params_part
                    query_part = ""
                
                if ':' in host_port:
                    host = host_port.split(':')[0]
                    try:
                        port = int(host_port.split(':')[1])
                    except:
                        port = 443
                else:
                    host = host_port
                    port = 443
                
                # Параметры
                params = {}
                if query_part:
                    # Убираем якорь если есть
                    if '#' in query_part:
                        query_part, name_part = query_part.split('#', 1)
                        name = urllib.parse.unquote(name_part)
                    else:
                        name = "Xray Proxy"
                    
                    for param in query_part.split('&'):
                        if '=' in param:
                            key, value = param.split('=', 1)
                            params[key] = value
                else:
                    name = "Xray Proxy"
                
                # Название из якоря
                if '#' in link:
                    name_part = link.split('#', 1)[1]
                    name = urllib.parse.unquote(name_part)
                
                # Очищаем имя от лишних символов
                name = re.sub(r'[^\w\s\-\_\.,\(\)\[\]\{\}\@\#\&\*\+]', '', name)
                
                return {
                    'uuid': uuid,
                    'host': host,
                    'port': port,
                    'params': params,
                    'name': name or f"{host}:{port}",
                    'raw': link
                }
        except Exception as e:
            if self.verbose:
                print(f"{RED}Ошибка парсинга {link[:50]}...: {e}{RESET}")
        
        return None
    
    def create_xray_config(self, proxy_info: Dict) -> Dict:
        """Создание конфигурации Xray для прокси"""
        params = proxy_info['params']
        
        # Базовая конфигурация
        config = {
            "log": {
                "loglevel": "error" if not self.verbose else "debug",
                "access": "/dev/null",
                "error": "/dev/null"
            },
            "inbounds": [
                {
                    "port": 10808,
                    "protocol": "socks",
                    "settings": {
                        "auth": "noauth",
                        "udp": True
                    },
                    "sniffing": {
                        "enabled": True,
                        "destOverride": ["http", "tls"]
                    }
                },
                {
                    "port": 10809,
                    "protocol": "http",
                    "settings": {
                        "auth": "noauth",
                        "udp": True
                    },
                    "sniffing": {
                        "enabled": True,
                        "destOverride": ["http", "tls"]
                    }
                }
            ],
            "outbounds": [
                {
                    "protocol": "vless",
                    "settings": {
                        "vnext": [
                            {
                                "address": proxy_info['host'],
                                "port": proxy_info['port'],
                                "users": [
                                    {
                                        "id": proxy_info['uuid'],
                                        "encryption": params.get('encryption', 'none'),
                                        "flow": params.get('flow', '')
                                    }
                                ]
                            }
                        ]
                    },
                    "streamSettings": {
                        "network": params.get('type', 'tcp'),
                        "security": params.get('security', 'none')
                    }
                },
                {
                    "protocol": "freedom",
                    "tag": "direct"
                },
                {
                    "protocol": "blackhole",
                    "tag": "block"
                }
            ],
            "routing": {
                "rules": [
                    {
                        "type": "field",
                        "inboundTag": ["api"],
                        "outboundTag": "api"
                    },
                    {
                        "type": "field",
                        "outboundTag": "direct",
                        "ip": ["0.0.0.0/0", "::/0"]
                    }
                ]
            }
        }
        
        # Настройки streamSettings в зависимости от типа
        network = config['outbounds'][0]['streamSettings']['network']
        
        if network == 'ws' or params.get('type') == 'ws':
            config['outbounds'][0]['streamSettings']['network'] = 'ws'
            
            ws_settings = {}
            if params.get('path'):
                ws_settings['path'] = params['path']
            if params.get('host'):
                ws_settings['headers'] = {"Host": params['host']}
            
            config['outbounds'][0]['streamSettings']['wsSettings'] = ws_settings
        
        if params.get('security') == 'reality':
            config['outbounds'][0]['streamSettings']['security'] = 'reality'
            reality_settings = {
                "serverName": params.get('sni', proxy_info['host']),
                "fingerprint": params.get('fp', 'chrome'),
                "show": False,
                "publicKey": params.get('pbk', ''),
                "shortId": params.get('sid', '')
            }
            config['outbounds'][0]['streamSettings']['realitySettings'] = reality_settings
        
        elif params.get('security') == 'tls':
            config['outbounds'][0]['streamSettings']['security'] = 'tls'
            tls_settings = {
                "serverName": params.get('sni', proxy_info['host']),
                "fingerprint": params.get('fp', 'chrome'),
                "allowInsecure": True
            }
            config['outbounds'][0]['streamSettings']['tlsSettings'] = tls_settings
        
        return config
    
    def test_tcp_connect(self, host: str, port: int, timeout: int = 3) -> Tuple[bool, float]:
        """Быстрый TCP тест без прокси"""
        try:
            start = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                return True, time.time() - start
        except:
            pass
        return False, 0
    
    def test_tls_handshake(self, host: str, port: int = 443, sni: str = None) -> Tuple[bool, float]:
        """Проверка TLS рукопожатия"""
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            start = time.time()
            with socket.create_connection((host, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=sni or host) as ssock:
                    cert = ssock.getpeercert()
                    elapsed = time.time() - start
                    return True, elapsed
        except Exception as e:
            if self.verbose:
                print(f"TLS error: {e}")
        return False, 0
    
    def test_proxy_connection(self, proxy_info: Dict) -> Tuple[bool, float, Dict]:
        """Тестирование подключения через прокси"""
        if not self.xray_binary:
            return False, 0, {"error": "Xray не найден"}
        
        config = self.create_xray_config(proxy_info)
        config_hash = hashlib.md5(proxy_info['raw'].encode()).hexdigest()[:8]
        config_path = os.path.join(self.temp_dir, f"config_{config_hash}.json")
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Запускаем Xray
        process = None
        try:
            # Запуск в фоне
            process = subprocess.Popen(
                [self.xray_binary, '-c', config_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # Даем время на запуск
            time.sleep(1.5)
            
            # Проверяем запустился ли
            if process.poll() is not None:
                return False, 0, {"error": "Xray не запустился"}
            
            # Тестируем через SOCKS5 прокси
            socks5_proxy = "socks5://127.0.0.1:10808"
            
            results = {
                "direct": {"success": False, "time": 0, "ip": None, "country": None},
                "proxied": {"success": False, "time": 0, "ip": None, "country": None, "speed": 0},
                "tests": []
            }
            
            # 1. Проверка базового подключения
            for test_url in self.test_urls[:3]:
                try:
                    start_time = time.time()
                    
                    cmd = [
                        'curl', '-s', '-o', '/dev/null', '-w', '%{http_code}',
                        '--socks5-hostname', socks5_proxy,
                        '--connect-timeout', str(self.timeout),
                        '--max-time', str(self.timeout + 5),
                        test_url
                    ]
                    
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout + 10)
                    
                    if result.stdout.strip() in ['204', '200', '301', '302']:
                        elapsed = time.time() - start_time
                        results["proxied"]["success"] = True
                        results["proxied"]["time"] = elapsed
                        results["tests"].append({
                            "url": test_url,
                            "status": "success",
                            "time": elapsed
                        })
                        break
                except Exception as e:
                    results["tests"].append({
                        "url": test_url,
                        "status": "failed",
                        "error": str(e)[:50]
                    })
                    continue
            
            # 2. Определение IP и страны через прокси
            if results["proxied"]["success"]:
                try:
                    cmd = [
                        'curl', '-s', '--socks5-hostname', socks5_proxy,
                        '--connect-timeout', str(self.timeout),
                        '--max-time', str(self.timeout + 5),
                        'https://ipinfo.io/json'
                    ]
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout + 10)
                    
                    if result.returncode == 0 and result.stdout:
                        try:
                            ip_data = json.loads(result.stdout)
                            results["proxied"]["ip"] = ip_data.get('ip')
                            results["proxied"]["country"] = ip_data.get('country')
                            results["proxied"]["city"] = ip_data.get('city')
                            results["proxied"]["region"] = ip_data.get('region')
                            results["proxied"]["org"] = ip_data.get('org')
                            results["proxied"]["timezone"] = ip_data.get('timezone')
                        except:
                            pass
                except:
                    pass
                
                # Альтернативный метод определения IP
                if not results["proxied"].get("ip"):
                    try:
                        cmd = [
                            'curl', '-s', '--socks5-hostname', socks5_proxy,
                            '--connect-timeout', str(self.timeout),
                            'https://api.ipify.org'
                        ]
                        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                        if result.returncode == 0 and result.stdout:
                            results["proxied"]["ip"] = result.stdout.strip()
                    except:
                        pass
            
            # 3. Проверка без прокси для сравнения
            try:
                start_time = time.time()
                cmd = ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}',
                       '--connect-timeout', '3', '--max-time', '5',
                       'https://www.google.com']
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=8)
                if result.stdout.strip() in ['204', '200']:
                    results["direct"]["success"] = True
                    results["direct"]["time"] = time.time() - start_time
                    
                    # Получаем прямой IP
                    try:
                        cmd = ['curl', '-s', 'https://api.ipify.org']
                        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                        if result.returncode == 0:
                            results["direct"]["ip"] = result.stdout.strip()
                    except:
                        pass
            except:
                pass
            
            # 4. Тест скорости (скачивание небольшого файла)
            if results["proxied"]["success"]:
                try:
                    speed_test_url = "https://speed.cloudflare.com/__down?bytes=500000"
                    
                    start_time = time.time()
                    cmd = [
                        'curl', '-s', '-o', '/dev/null',
                        '--socks5-hostname', socks5_proxy,
                        '--connect-timeout', str(self.timeout),
                        '--max-time', '15',
                        speed_test_url
                    ]
                    result = subprocess.run(cmd, capture_output=True, timeout=20)
                    
                    if result.returncode == 0:
                        elapsed = time.time() - start_time
                        # 500KB / время в секундах = KB/s, конвертируем в kbps
                        speed_kbps = (500 / elapsed) * 8
                        results["proxied"]["speed"] = round(speed_kbps, 2)
                except:
                    pass
            
            # 5. Проверка стабильности (5 быстрых запросов)
            if results["proxied"]["success"]:
                stable_count = 0
                total_time = 0
                times = []
                
                for i in range(5):
                    try:
                        start_time = time.time()
                        cmd = [
                            'curl', '-s', '-o', '/dev/null', '-w', '%{http_code}',
                            '--socks5-hostname', socks5_proxy,
                            '--connect-timeout', '3',
                            '--max-time', '5',
                            'https://www.google.com/generate_204'
                        ]
                        result = subprocess.run(cmd, capture_output=True, text=True, timeout=8)
                        
                        if result.stdout.strip() == '204':
                            req_time = time.time() - start_time
                            stable_count += 1
                            total_time += req_time
                            times.append(req_time)
                    except:
                        times.append(None)
                
                results["stability"] = {
                    "success_rate": f"{(stable_count * 20)}%",
                    "success_count": stable_count,
                    "total_requests": 5,
                    "avg_time": round(total_time / stable_count, 3) if stable_count > 0 else 0,
                    "min_time": round(min(times), 3) if times and any(times) else 0,
                    "max_time": round(max(times), 3) if times and any(times) else 0,
                    "all_times": times
                }
            
            # 6. Дополнительная информация о прокси
            results["proxy_info"] = {
                "host": proxy_info['host'],
                "port": proxy_info['port'],
                "protocol": proxy_info['params'].get('type', 'tcp'),
                "security": proxy_info['params'].get('security', 'none'),
                "sni": proxy_info['params'].get('sni', ''),
                "flow": proxy_info['params'].get('flow', '')
            }
            
            return results["proxied"]["success"], results["proxied"]["time"], results
            
        except Exception as e:
            return False, 0, {"error": str(e)}
        finally:
            # Завершаем процесс Xray
            if process:
                process.terminate()
                try:
                    process.wait(timeout=3)
                except:
                    process.kill()
            
            # Удаляем конфиг
            try:
                os.remove(config_path)
            except:
                pass
    
    def check_proxy(self, link: str) -> Dict:
        """Полная проверка прокси"""
        if self.verbose:
            print(f"\n{BLUE}{'='*60}{RESET}")
            print(f"{CYAN}Проверка: {WHITE}{BOLD}{link[:80]}...{RESET}" if len(link) > 80 else f"{CYAN}Проверка: {WHITE}{BOLD}{link}{RESET}")
            print(f"{BLUE}{'='*60}{RESET}")
        
        result = {
            'link': link,
            'timestamp': datetime.now().isoformat(),
            'valid_format': False,
            'proxy_info': None,
            'tcp_check': False,
            'tcp_time': 0,
            'tls_check': False,
            'tls_time': 0,
            'proxy_test': False,
            'proxy_time': 0,
            'details': {},
            'score': 0,
            'status': 'INVALID'
        }
        
        # 1. Парсинг ссылки
        proxy_info = self.parse_vless_link(link)
        if not proxy_info:
            if self.verbose:
                print(f"{RED}✗ Неверный формат VLESS ссылки{RESET}")
            result['error'] = "Invalid VLESS link format"
            return result
        
        result['valid_format'] = True
        result['proxy_info'] = proxy_info
        
        if self.verbose:
            print(f"\n{YELLOW}Информация о прокси:{RESET}")
            print(f"  📌 Название: {WHITE}{proxy_info['name']}{RESET}")
            print(f"  🌍 Хост: {WHITE}{proxy_info['host']}{RESET}")
            print(f"  🔌 Порт: {WHITE}{proxy_info['port']}{RESET}")
            print(f"  🔑 UUID: {WHITE}{proxy_info['uuid'][:8]}...{RESET}")
            print(f"  ⚙️  Параметры: {WHITE}{len(proxy_info['params'])} шт.{RESET}")
        
        # 2. TCP проверка
        if self.verbose:
            print(f"\n{YELLOW}Тест 1/4: TCP подключение...{RESET}", end='')
        
        tcp_ok, tcp_time = self.test_tcp_connect(proxy_info['host'], proxy_info['port'])
        result['tcp_check'] = tcp_ok
        result['tcp_time'] = tcp_time
        
        if self.verbose:
            if tcp_ok:
                print(f" {GREEN}✓ Успешно ({tcp_time*1000:.1f}ms){RESET}")
            else:
                print(f" {RED}✗ Не удалось{RESET}")
        
        # 3. TLS проверка (если применимо)
        if proxy_info['port'] in [443, 8443, 2053, 2083, 2087, 2096, 4443, 6443, 9443]:
            if self.verbose:
                print(f"{YELLOW}Тест 2/4: TLS рукопожатие...{RESET}", end='')
            
            tls_ok, tls_time = self.test_tls_handshake(
                proxy_info['host'], 
                proxy_info['port'],
                proxy_info['params'].get('sni')
            )
            result['tls_check'] = tls_ok
            result['tls_time'] = tls_time
            
            if self.verbose:
                if tls_ok:
                    print(f" {GREEN}✓ Успешно ({tls_time*1000:.1f}ms){RESET}")
                else:
                    print(f" {RED}✗ Не удалось{RESET}")
        else:
            if self.verbose:
                print(f"{YELLOW}Тест 2/4: TLS рукопожатие... {CYAN}Пропущено (не TLS порт){RESET}")
            result['tls_check'] = None
        
        # 4. Реальный тест через Xray
        if self.verbose:
            print(f"{YELLOW}Тест 3/4: Проверка через Xray...{RESET}")
        
        if not self.xray_binary:
            if self.verbose:
                print(f"{RED}  ✗ Xray не найден, пропускаем{RESET}")
            result['proxy_test'] = False
            result['proxy_error'] = "Xray not found"
        else:
            proxy_ok, proxy_time, details = self.test_proxy_connection(proxy_info)
            result['proxy_test'] = proxy_ok
            result['proxy_time'] = proxy_time
            result['details'] = details
            
            if self.verbose:
                if proxy_ok:
                    print(f"  {GREEN}✓ Прокси работает!{RESET}")
                    print(f"    ⏱  Время отклика: {WHITE}{proxy_time*1000:.1f}ms{RESET}")
                    
                    if details.get("proxied", {}).get("ip"):
                        print(f"    🌍 IP через прокси: {WHITE}{details['proxied']['ip']}{RESET}")
                        if details['proxied'].get('country'):
                            print(f"    🏳️  Страна: {WHITE}{details['proxied']['country']}{RESET}")
                        if details['proxied'].get('city'):
                            print(f"    🏙️  Город: {WHITE}{details['proxied']['city']}{RESET}")
                        if details['proxied'].get('org'):
                            print(f"    🏢  Провайдер: {WHITE}{details['proxied']['org']}{RESET}")
                    
                    if details.get("proxied", {}).get("speed", 0) > 0:
                        speed = details['proxied']['speed']
                        color = GREEN if speed > 1000 else YELLOW if speed > 500 else RED
                        print(f"    ⚡ Скорость: {color}{speed} Kbps{RESET}")
                    
                    if details.get("stability"):
                        print(f"    📊 Стабильность: {WHITE}{details['stability']['success_rate']}{RESET}")
                        if details['stability'].get('avg_time'):
                            print(f"    ⏱  Среднее время: {WHITE}{details['stability']['avg_time']*1000:.1f}ms{RESET}")
                else:
                    print(f"  {RED}✗ Прокси не работает{RESET}")
                    if details.get("error"):
                        print(f"    Ошибка: {RED}{details['error']}{RESET}")
        
        # 5. Без прокси для сравнения
        if result.get('details') and result['details'].get("direct", {}).get("success"):
            direct_time = result['details']["direct"]["time"]
            if self.verbose:
                print(f"\n{YELLOW}Тест 4/4: Без прокси (для сравнения):{RESET}")
                print(f"  ⏱  Время: {WHITE}{direct_time*1000:.1f}ms{RESET}")
            
            if proxy_ok:
                ratio = proxy_time / direct_time
                if ratio < 1.5:
                    perf = f"{GREEN}Отлично{RESET}"
                elif ratio < 2.5:
                    perf = f"{YELLOW}Средне{RESET}"
                else:
                    perf = f"{RED}Медленно{RESET}"
                if self.verbose:
                    print(f"  📈 Производительность: {perf} ({ratio:.1f}x медленнее)")
        
        # 6. Оценка
        score = 0
        if result['tcp_check']: score += 15
        if result['tls_check']: score += 15
        if result['proxy_test']: 
            score += 40
            # Дополнительные баллы за качество
            if result['proxy_time'] < 1.0: score += 5
            if result['proxy_time'] < 0.5: score += 5
            if result['details'].get('proxied', {}).get('speed', 0) > 1000: score += 10
            if result['details'].get('proxied', {}).get('speed', 0) > 500: score += 5
            if result['details'].get('stability', {}).get('success_count', 0) >= 4: score += 10
        
        result['score'] = min(score, 100)  # Максимум 100
        
        if score >= 80:
            result['status'] = 'WORKING'
            status_color = GREEN
        elif score >= 50:
            result['status'] = 'QUESTIONABLE'
            status_color = YELLOW
        else:
            result['status'] = 'BROKEN'
            status_color = RED
        
        if self.verbose:
            print(f"\n{BLUE}{'='*60}{RESET}")
            print(f"ИТОГ: {status_color}{BOLD}{result['status']}{RESET} (оценка: {score}/100)")
            print(f"{BLUE}{'='*60}{RESET}")
        
        return result
    
    def save_working_proxies_to_txt(self, filename: str = None):
        """Сохранение только рабочих прокси (WORKING) в TXT файл"""
        if not filename:
            filename = self.working_txt
        
        # Фильтруем только WORKING прокси (исключаем BROKEN, QUESTIONABLE, ERROR, INVALID)
        working_proxies = [
            r for r in self.results 
            if r.get('status') == 'WORKING' and r.get('link')
        ]
        
        if working_proxies:
            with open(filename, 'w', encoding='utf-8') as f:
                for proxy in working_proxies:
                    f.write(f"{proxy['link']}\n")
            
            print(f"{GREEN}✅ Сохранено {len(working_proxies)} рабочих прокси в {filename}{RESET}")
        else:
            print(f"{YELLOW}⚠ Нет рабочих прокси для сохранения{RESET}")
    
    def check_multiple(self, links: List[str]) -> List[Dict]:
        """Проверка нескольких прокси"""
        print(f"\n{BOLD}{CYAN}Проверка {len(links)} прокси...{RESET}\n")
        
        self.results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.check_proxy, link): link for link in links}
            
            for i, future in enumerate(as_completed(futures), 1):
                try:
                    result = future.result(timeout=60)
                    self.results.append(result)
                    
                    # Прогресс
                    status = result['status']
                    color = GREEN if status == 'WORKING' else YELLOW if status == 'QUESTIONABLE' else RED
                    name = result['proxy_info']['name'][:30] if result['proxy_info'] else "Unknown"
                    print(f"[{i}/{len(links)}] {color}{status:12}{RESET} | {name} | {result['score']}/100")
                    
                except Exception as e:
                    print(f"{RED}Ошибка: {e}{RESET}")
                    self.results.append({
                        'link': futures[future],
                        'error': str(e),
                        'status': 'ERROR',
                        'score': 0
                    })
        
        # Сортировка по оценке
        self.results.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        # Сохраняем результаты
        self.save_results()
        self.save_working_proxies_to_txt()  # Автоматически сохраняем рабочие прокси в TXT
        
        # Вывод сводки
        self.print_summary()
        
        return self.results
    
    def check_from_file(self, filename: str) -> List[Dict]:
        """Проверка прокси из файла"""
        if not os.path.exists(filename):
            print(f"{RED}Файл {filename} не найден!{RESET}")
            return []
        
        links = []
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    links.append(line)
        
        print(f"{GREEN}Загружено {len(links)} ссылок из {filename}{RESET}")
        return self.check_multiple(links)
    
    def save_results(self, filename: str = None):
        """Сохранение результатов в JSON"""
        if not filename:
            filename = self.results_file
        
        # Подготовка данных для сохранения
        save_data = {
            'timestamp': datetime.now().isoformat(),
            'total': len(self.results),
            'working': len([r for r in self.results if r.get('status') == 'WORKING']),
            'questionable': len([r for r in self.results if r.get('status') == 'QUESTIONABLE']),
            'broken': len([r for r in self.results if r.get('status') == 'BROKEN']),
            'errors': len([r for r in self.results if r.get('status') == 'ERROR']),
            'results': self.results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n{GREEN}✅ Результаты сохранены в {filename}{RESET}")
        return filename
    
    def load_results(self, filename: str) -> List[Dict]:
        """Загрузка результатов из JSON"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.results = data.get('results', [])
                print(f"{GREEN}Загружено {len(self.results)} результатов из {filename}{RESET}")
                return self.results
        except Exception as e:
            print(f"{RED}Ошибка загрузки {filename}: {e}{RESET}")
            return []
    
    def print_summary(self):
        """Вывод сводки по результатам"""
        working = [r for r in self.results if r.get('status') == 'WORKING']
        questionable = [r for r in self.results if r.get('status') == 'QUESTIONABLE']
        broken = [r for r in self.results if r.get('status') == 'BROKEN']
        errors = [r for r in self.results if r.get('status') == 'ERROR']
        
        print(f"\n{CYAN}{'='*60}{RESET}")
        print(f"{BOLD}СВОДКА ПО ВСЕМ ПРОКСИ:{RESET}")
        print(f"{CYAN}{'='*60}{RESET}")
        print(f"✅ Рабочие:     {GREEN}{len(working):3}{RESET}")
        print(f"⚠️  Сомнительные: {YELLOW}{len(questionable):3}{RESET}")
        print(f"❌ Нерабочие:   {RED}{len(broken):3}{RESET}")
        print(f"💥 Ошибки:      {RED}{len(errors):3}{RESET}")
        print(f"{CYAN}{'='*60}{RESET}")
        
        # Топ 10 лучших
        if working:
            print(f"\n{GREEN}🏆 ТОП-5 ЛУЧШИХ ПРОКСИ:{RESET}")
            for i, r in enumerate(working[:5], 1):
                name = r['proxy_info']['name'][:40] if r.get('proxy_info') else "Unknown"
                speed = r.get('details', {}).get('proxied', {}).get('speed', 0)
                ping = r.get('proxy_time', 0) * 1000
                country = r.get('details', {}).get('proxied', {}).get('country', '??')
                print(f"  {i}. {name[:40]} | {country} | {ping:.0f}ms | {speed:.0f}Kbps | {r['score']}/100")
        
        # Худшие
        if broken:
            print(f"\n{RED}💔 ХУДШИЕ ПРОКСИ:{RESET}")
            for i, r in enumerate(broken[:3], 1):
                name = r['proxy_info']['name'][:40] if r.get('proxy_info') else "Unknown"
                print(f"  {i}. {name[:40]} | {r['score']}/100")
    
    def generate_html_report(self, filename: str = None) -> str:
        """Генерация красивого HTML отчета"""
        if not filename:
            filename = self.html_report
        
        working = [r for r in self.results if r.get('status') == 'WORKING']
        questionable = [r for r in self.results if r.get('status') == 'QUESTIONABLE']
        broken = [r for r in self.results if r.get('status') == 'BROKEN']
        errors = [r for r in self.results if r.get('status') == 'ERROR']
        
        # Статистика по странам
        countries = {}
        for r in working + questionable:
            country = r.get('details', {}).get('proxied', {}).get('country', 'Unknown')
            if country not in countries:
                countries[country] = 0
            countries[country] += 1
        
        countries_html = ""
        for country, count in sorted(countries.items(), key=lambda x: x[1], reverse=True)[:10]:
            countries_html += f"<li>{country}: {count} прокси</li>"
        
        # Генерация HTML
        html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Xray Proxy Check Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            background: rgba(255,255,255,0.95);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            color: #333;
            font-size: 32px;
            margin-bottom: 10px;
        }}
        .header p {{
            color: #666;
            font-size: 16px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }}
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        .stat-card.working {{
            border-left: 5px solid #4caf50;
        }}
        .stat-card.questionable {{
            border-left: 5px solid #ff9800;
        }}
        .stat-card.broken {{
            border-left: 5px solid #f44336;
        }}
        .stat-card.errors {{
            border-left: 5px solid #9c27b0;
        }}
        .stat-value {{
            font-size: 48px;
            font-weight: bold;
            margin: 10px 0;
        }}
        .stat-label {{
            color: #666;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .filters {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .filter-btn {{
            padding: 10px 20px;
            margin-right: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
        }}
        .filter-btn:hover {{
            opacity: 0.8;
        }}
        .filter-btn.active {{
            transform: scale(1.05);
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }}
        .proxy-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }}
        .proxy-card {{
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            transition: all 0.3s;
            border-left: 5px solid #ddd;
        }}
        .proxy-card.working {{
            border-left-color: #4caf50;
        }}
        .proxy-card.questionable {{
            border-left-color: #ff9800;
        }}
        .proxy-card.broken {{
            border-left-color: #f44336;
        }}
        .proxy-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        .proxy-name {{
            font-size: 16px;
            font-weight: bold;
            color: #333;
        }}
        .proxy-score {{
            font-size: 20px;
            font-weight: bold;
        }}
        .proxy-details {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 15px;
            font-size: 13px;
        }}
        .detail-item {{
            color: #666;
        }}
        .detail-label {{
            color: #999;
            font-size: 11px;
            text-transform: uppercase;
        }}
        .badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 3px;
            color: white;
            font-size: 11px;
            font-weight: bold;
        }}
        .badge-working {{
            background: #4caf50;
        }}
        .badge-questionable {{
            background: #ff9800;
        }}
        .badge-broken {{
            background: #f44336;
        }}
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 30px;
        }}
        .progress-bar {{
            width: 100%;
            height: 30px;
            background: #f0f0f0;
            border-radius: 15px;
            overflow: hidden;
            margin: 10px 0;
        }}
        .progress-fill {{
            height: 100%;
            transition: width 0.5s;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: rgba(255,255,255,0.8);
        }}
        @media (max-width: 768px) {{
            .proxy-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Xray Proxy Check Report</h1>
            <p>Сгенерировано: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Всего проверено: {len(self.results)} прокси</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card working">
                <div class="stat-label">✅ Рабочие</div>
                <div class="stat-value">{len(working)}</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {len(working)/len(self.results)*100 if self.results else 0}%; background: #4caf50;"></div>
                </div>
            </div>
            <div class="stat-card questionable">
                <div class="stat-label">⚠️ Сомнительные</div>
                <div class="stat-value">{len(questionable)}</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {len(questionable)/len(self.results)*100 if self.results else 0}%; background: #ff9800;"></div>
                </div>
            </div>
            <div class="stat-card broken">
                <div class="stat-label">❌ Нерабочие</div>
                <div class="stat-value">{len(broken)}</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {len(broken)/len(self.results)*100 if self.results else 0}%; background: #f44336;"></div>
                </div>
            </div>
            <div class="stat-card errors">
                <div class="stat-label">💥 Ошибки</div>
                <div class="stat-value">{len(errors)}</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {len(errors)/len(self.results)*100 if self.results else 0}%; background: #9c27b0;"></div>
                </div>
            </div>
        </div>
        
        <div class="chart-container">
            <h3>🌍 Распределение по странам</h3>
            <ul>
                {countries_html}
            </ul>
        </div>
        
        <div class="filters">
            <button class="filter-btn" onclick="filterProxies('all')" style="background: #4caf50; color: white;">Все</button>
            <button class="filter-btn" onclick="filterProxies('working')" style="background: #4caf50; color: white;">Рабочие</button>
            <button class="filter-btn" onclick="filterProxies('questionable')" style="background: #ff9800; color: white;">Сомнительные</button>
            <button class="filter-btn" onclick="filterProxies('broken')" style="background: #f44336; color: white;">Нерабочие</button>
        </div>
        
        <div class="proxy-grid" id="proxyGrid">
"""
        
        for result in self.results:
            if result.get('status') == 'WORKING':
                card_class = "working"
                badge_class = "badge-working"
                badge_text = "РАБОЧИЙ"
            elif result.get('status') == 'QUESTIONABLE':
                card_class = "questionable"
                badge_class = "badge-questionable"
                badge_text = "СОМНИТЕЛЬНЫЙ"
            elif result.get('status') == 'BROKEN':
                card_class = "broken"
                badge_class = "badge-broken"
                badge_text = "НЕРАБОЧИЙ"
            else:
                card_class = "broken"
                badge_class = "badge-broken"
                badge_text = "ОШИБКА"
            
            proxy_info = result.get('proxy_info', {})
            details = result.get('details', {})
            proxied = details.get('proxied', {})
            
            name = proxy_info.get('name', 'Unknown')[:40]
            host = proxy_info.get('host', 'N/A')
            port = proxy_info.get('port', 'N/A')
            score = result.get('score', 0)
            
            ping = result.get('proxy_time', 0) * 1000
            speed = proxied.get('speed', 0)
            country = proxied.get('country', 'N/A')
            ip = proxied.get('ip', 'N/A')
            city = proxied.get('city', '')
            org = proxied.get('org', 'N/A')[:30]
            
            stability = details.get('stability', {})
            success_rate = stability.get('success_rate', 'N/A')
            
            html += f"""
            <div class="proxy-card {card_class}" data-status="{result.get('status', 'UNKNOWN')}">
                <div class="proxy-header">
                    <span class="proxy-name">{name}</span>
                    <span class="badge {badge_class}">{badge_text}</span>
                </div>
                <div style="font-size: 24px; font-weight: bold; margin: 10px 0;">{score}/100</div>
                <div class="proxy-details">
                    <div>
                        <div class="detail-label">Хост</div>
                        <div class="detail-item">{host}:{port}</div>
                    </div>
                    <div>
                        <div class="detail-label">Пинг</div>
                        <div class="detail-item">{ping:.0f}ms</div>
                    </div>
                    <div>
                        <div class="detail-label">Скорость</div>
                        <div class="detail-item">{speed:.0f} Kbps</div>
                    </div>
                    <div>
                        <div class="detail-label">Страна</div>
                        <div class="detail-item">{country}</div>
                    </div>
                    <div>
                        <div class="detail-label">IP</div>
                        <div class="detail-item">{ip}</div>
                    </div>
                    <div>
                        <div class="detail-label">Стабильность</div>
                        <div class="detail-item">{success_rate}</div>
                    </div>
                </div>
                <div style="margin-top: 10px; font-size: 11px; color: #999;">
                    {city} | {org}
                </div>
            </div>
            """
        
        html += f"""
        </div>
        
        <div class="footer">
            <p>Xray Proxy Checker v2.0 | Сгенерировано автоматически</p>
        </div>
    </div>
    
    <script>
        function filterProxies(status) {{
            const cards = document.querySelectorAll('.proxy-card');
            cards.forEach(card => {{
                if (status === 'all') {{
                    card.style.display = 'block';
                }} else {{
                    const cardStatus = card.dataset.status.toLowerCase();
                    if (cardStatus === status) {{
                        card.style.display = 'block';
                    }} else {{
                        card.style.display = 'none';
                    }}
                }}
            }});
            
            // Обновление активной кнопки
            document.querySelectorAll('.filter-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            event.target.classList.add('active');
        }}
    </script>
</body>
</html>
        """
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"{GREEN}✅ HTML отчет сохранен в {filename}{RESET}")
        return filename
    
    def get_working_links(self, min_score: int = 80) -> List[str]:
        """Получение списка рабочих ссылок"""
        return [
            r['link'] for r in self.results 
            if r.get('score', 0) >= min_score and r.get('status') == 'WORKING'
        ]
    
    def get_fastest_links(self, limit: int = 10) -> List[Dict]:
        """Получение самых быстрых прокси"""
        working = [r for r in self.results if r.get('status') == 'WORKING' and r.get('proxy_time', 999) > 0]
        return sorted(working, key=lambda x: x.get('proxy_time', 999))[:limit]
    
    def get_by_country(self, country_code: str) -> List[Dict]:
        """Получение прокси по стране"""
        return [
            r for r in self.results 
            if r.get('details', {}).get('proxied', {}).get('country') == country_code
        ]
    
    def cleanup(self):
        """Очистка временных файлов"""
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
            if self.verbose:
                print(f"{GREEN}✓ Временные файлы удалены{RESET}")
        except:
            pass

def scan_vpn_config_folder(folder_path: str = "/mnt/extra/vpn/config") -> List[str]:
    """
    Сканирование папки с конфигами VPN и извлечение VLESS ссылок из всех файлов
    """
    all_links = []
    
    if not os.path.exists(folder_path):
        print(f"{YELLOW}Папка {folder_path} не найдена{RESET}")
        return all_links
    
    print(f"{CYAN}Сканирование папки {folder_path}...{RESET}")
    
    # Рекурсивно обходим все файлы в папке
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Пропускаем бинарные файлы и слишком большие
            if os.path.getsize(file_path) > 1024 * 1024:  # > 1MB
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Ищем VLESS ссылки в тексте
                    vless_links = re.findall(r'vless://[^\s"\'<>]+', content)
                    
                    if vless_links:
                        print(f"  {GREEN}✓ Найдено {len(vless_links)} ссылок в {file_path}{RESET}")
                        all_links.extend(vless_links)
            except Exception as e:
                if args.verbose:
                    print(f"  {RED}Ошибка чтения {file_path}: {e}{RESET}")
                continue
    
    # Удаляем дубликаты, сохраняя порядок
    seen = set()
    unique_links = []
    for link in all_links:
        if link not in seen:
            seen.add(link)
            unique_links.append(link)
    
    print(f"\n{GREEN}Всего найдено уникальных ссылок: {len(unique_links)}{RESET}")
    return unique_links

def print_banner():
    """Вывод баннера"""
    banner = f"""
{CYAN}{BOLD}
╔══════════════════════════════════════════════════════════════╗
║              XRAY VLESS PROXY CHECKER v2.0                   ║
║     Тщательная проверка прокси + отчеты + мониторинг         ║
╚══════════════════════════════════════════════════════════════╝
{RESET}
"""
    print(banner)

def main():
    """Основная функция"""
    parser = argparse.ArgumentParser(description='Xray VLESS Proxy Checker')
    parser.add_argument('links', nargs='*', help='VLESS ссылки для проверки')
    parser.add_argument('-f', '--file', help='Файл со ссылками (по одной на строку)')
    parser.add_argument('--scan-folder', action='store_true', help='Сканировать папку /mnt/extra/vpn/config')
    parser.add_argument('--scan-path', help='Сканировать указанную папку (вместо стандартной)')
    parser.add_argument('-o', '--output', help='Выходной JSON файл')
    parser.add_argument('--html', help='HTML отчет файл')
    parser.add_argument('--working-txt', help='TXT файл для рабочих прокси (по умолчанию working_proxies_ДатаВремя.txt)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Подробный вывод')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='Таймаут в секундах')
    parser.add_argument('-w', '--workers', type=int, default=3, help='Количество параллельных проверок')
    parser.add_argument('--min-score', type=int, default=80, help='Минимальный балл для рабочего прокси')
    parser.add_argument('--export-working', help='Экспортировать только рабочие ссылки в файл')
    parser.add_argument('--stats', action='store_true', help='Показать статистику по последней проверке')
    parser.add_argument('--monitor', help='Режим мониторинга (интервал в минутах)')
    
    global args
    args = parser.parse_args()
    
    print_banner()
    
    # Проверка наличия curl
    try:
        subprocess.run(['curl', '--version'], capture_output=True, check=True)
    except:
        print(f"{RED}ОШИБКА: curl не найден. Установите curl:{RESET}")
        print("  Ubuntu/Debian: sudo apt install curl")
        print("  CentOS/RHEL: sudo yum install curl")
        print("  macOS: brew install curl")
        sys.exit(1)
    
    checker = VlessProxyChecker(
        verbose=args.verbose,
        timeout=args.timeout,
        max_workers=args.workers
    )
    
    try:
        # Определяем источник ссылок
        links_to_check = []
        
        if args.scan_folder:
            # Сканируем стандартную папку
            links_to_check = scan_vpn_config_folder()
        elif args.scan_path:
            # Сканируем указанную папку
            links_to_check = scan_vpn_config_folder(args.scan_path)
        elif args.file:
            # Загружаем из файла
            if os.path.exists(args.file):
                with open(args.file, 'r', encoding='utf-8') as f:
                    links_to_check = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                print(f"{GREEN}Загружено {len(links_to_check)} ссылок из {args.file}{RESET}")
            else:
                print(f"{RED}Файл {args.file} не найден!{RESET}")
                return
        elif args.links:
            # Используем ссылки из аргументов командной строки
            links_to_check = args.links
        elif args.monitor:
            # В режиме мониторинга нужно знать что проверять
            print(f"{YELLOW}Для режима мониторинга укажите источник ссылок (--file или --scan-folder){RESET}")
            return
        elif args.stats:
            # Просто показать статистику
            latest_json = max(Path('.').glob('proxy_check_*.json'), key=os.path.getctime)
            if latest_json:
                checker.load_results(str(latest_json))
                checker.print_summary()
            else:
                print(f"{RED}Нет сохраненных результатов{RESET}")
            return
        else:
            # Интерактивный режим - сначала спросим про сканирование папки
            print(f"{YELLOW}Выберите источник ссылок:{RESET}")
            print(f"  1) {CYAN}Сканировать папку /mnt/extra/vpn/config{RESET}")
            print(f"  2) {CYAN}Указать путь к папке{RESET}")
            print(f"  3) {CYAN}Загрузить из файла{RESET}")
            print(f"  4) {CYAN}Ввести ссылки вручную{RESET}")
            
            choice = input(f"\n{BOLD}Ваш выбор (1-4): {RESET}").strip()
            
            if choice == '1':
                links_to_check = scan_vpn_config_folder()
            elif choice == '2':
                folder_path = input(f"{YELLOW}Введите путь к папке: {RESET}").strip()
                if folder_path:
                    links_to_check = scan_vpn_config_folder(folder_path)
                else:
                    print(f"{RED}Путь не указан{RESET}")
                    return
            elif choice == '3':
                file_path = input(f"{YELLOW}Введите путь к файлу: {RESET}").strip()
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        links_to_check = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                    print(f"{GREEN}Загружено {len(links_to_check)} ссылок из {file_path}{RESET}")
                else:
                    print(f"{RED}Файл {file_path} не найден!{RESET}")
                    return
            elif choice == '4':
                print(f"{YELLOW}Введите VLESS ссылки для проверки (по одной на строку):{RESET}")
                print(f"{CYAN}Для завершения ввода введите пустую строку или 'q'{RESET}\n")
                
                links_to_check = []
                while True:
                    try:
                        line = input(f"{BOLD}> {RESET}").strip()
                        if not line or line.lower() == 'q':
                            break
                        if line.startswith('vless://'):
                            links_to_check.append(line)
                        else:
                            print(f"{RED}Не VLESS ссылка, пропущено{RESET}")
                    except KeyboardInterrupt:
                        print(f"\n{YELLOW}Прервано пользователем{RESET}")
                        break
            else:
                print(f"{RED}Неверный выбор{RESET}")
                return
        
        # Проверяем ссылки
        if links_to_check:
            if args.monitor:
                # Режим мониторинга
                interval = int(args.monitor) * 60
                print(f"{CYAN}Режим мониторинга запущен (интервал {args.monitor} мин){RESET}")
                
                while True:
                    print(f"\n{YELLOW}{'='*60}{RESET}")
                    print(f"{YELLOW}Проверка {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
                    print(f"{YELLOW}{'='*60}{RESET}")
                    
                    checker.check_multiple(links_to_check)
                    
                    # Сохраняем отчет с меткой времени
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    checker.save_results(f"monitor_{timestamp}.json")
                    checker.generate_html_report(f"monitor_{timestamp}.html")
                    
                    # Сохраняем рабочие прокси
                    if args.working_txt:
                        working_filename = f"monitor_working_{timestamp}.txt"
                    else:
                        working_filename = f"monitor_working_{timestamp}.txt"
                    checker.save_working_proxies_to_txt(working_filename)
                    
                    print(f"\n{CYAN}Следующая проверка через {args.monitor} мин...{RESET}")
                    time.sleep(interval)
            else:
                # Обычный режим проверки
                checker.check_multiple(links_to_check)
                
                if args.output:
                    checker.save_results(args.output)
                else:
                    checker.save_results()
                
                if args.html:
                    checker.generate_html_report(args.html)
                else:
                    checker.generate_html_report()
                
                # Сохраняем рабочие прокси в TXT
                if args.working_txt:
                    checker.save_working_proxies_to_txt(args.working_txt)
                else:
                    checker.save_working_proxies_to_txt()
                
                if args.export_working:
                    working = checker.get_working_links(args.min_score)
                    with open(args.export_working, 'w', encoding='utf-8') as f:
                        for link in working:
                            f.write(f"{link}\n")
                    print(f"{GREEN}✅ Экспортировано {len(working)} рабочих ссылок в {args.export_working}{RESET}")
        else:
            print(f"{YELLOW}Нет ссылок для проверки{RESET}")
    
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Программа прервана{RESET}")
    except Exception as e:
        print(f"{RED}Критическая ошибка: {e}{RESET}")
        import traceback
        traceback.print_exc()
    finally:
        checker.cleanup()

if __name__ == "__main__":
    main()
