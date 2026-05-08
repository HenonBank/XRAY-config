import os
import sys
import re
import json
import requests
import zipfile
from typing import List, Dict, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
import time
import base64
import asyncio
import socket
import ssl
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlparse

import aiofiles
import aiohttp
from loguru import logger
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.table import Table

# ============================================================================
# CONFIGURATION
# ============================================================================

OUTPUT_DIR = "tor_bridges"
HISTORY_FILE = os.path.join(OUTPUT_DIR, "bridge_history.json")
SOURCES_DIR = "sources"
RECENT_HOURS = 72
HISTORY_RETENTION_DAYS = 30
MAX_WORKERS = 20
DOWNLOAD_TIMEOUT = 15

GITHUB_MIRROR_BASE = "https://raw.githubusercontent.com/Delta-Kronecker/Tor-Bridges-Collector/refs/heads/main/bridge"

# GitHub Settings (DISABLED)
GITHUB_TOKEN = "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"
GITHUB_REPO = "HenonBank/XRAY-config"
GITHUB_BRANCH = "main"
GITHUB_TOR_FOLDER = "tor"

# Gitea Settings
GITEA_URL = "http://192.168.1.200:3002"
GITEA_TOKEN = "e7ee3591eb617b7444f64bc86584a0ffd754f941"
GITEA_REPO = "yarikpawe/Parser"
GITEA_BRANCH = "main"
GITEA_TOR_FOLDER = "tor"

# Parser settings (for VLESS configs)
PARSER_SOURCES_FILE = "sources.txt"
PARSER_RAW_FILE = "url_raw.txt"
PARSER_NAMED_FILE = "url_named.txt"
PARSER_WORK_FILE = "url_work.txt"
PARSER_DEAD_FILE = "url_dead.txt"
PARSER_STATS_FILE = "stats.log"

PARSER_CYCLE_SLEEP = 3600
PARSER_DOWNLOAD_CONC = 60
PARSER_CHECK_WORKERS = 40
PARSER_TCP_TIMEOUT = 2.5
PARSER_RETRY_COUNT = 3
PARSER_RETRY_DELAY = 1.5

# ============================================================================
# BRIDGE FILES
# ============================================================================

BRIDGE_FILES = {
    "obfs4.txt": f"{GITHUB_MIRROR_BASE}/obfs4.txt",
    "obfs4_72h.txt": f"{GITHUB_MIRROR_BASE}/obfs4_72h.txt",
    "obfs4_tested.txt": f"{GITHUB_MIRROR_BASE}/obfs4_tested.txt",
    "obfs4_ipv6.txt": f"{GITHUB_MIRROR_BASE}/obfs4_ipv6.txt",
    "obfs4_ipv6_72h.txt": f"{GITHUB_MIRROR_BASE}/obfs4_ipv6_72h.txt",
    "obfs4_ipv6_tested.txt": f"{GITHUB_MIRROR_BASE}/obfs4_ipv6_tested.txt",
    "webtunnel.txt": f"{GITHUB_MIRROR_BASE}/webtunnel.txt",
    "webtunnel_72h.txt": f"{GITHUB_MIRROR_BASE}/webtunnel_72h.txt",
    "webtunnel_tested.txt": f"{GITHUB_MIRROR_BASE}/webtunnel_tested.txt",
    "webtunnel_ipv6.txt": f"{GITHUB_MIRROR_BASE}/webtunnel_ipv6.txt",
    "webtunnel_ipv6_72h.txt": f"{GITHUB_MIRROR_BASE}/webtunnel_ipv6_72h.txt",
    "webtunnel_ipv6_tested.txt": f"{GITHUB_MIRROR_BASE}/webtunnel_ipv6_tested.txt",
    "vanilla.txt": f"{GITHUB_MIRROR_BASE}/vanilla.txt",
    "vanilla_72h.txt": f"{GITHUB_MIRROR_BASE}/vanilla_72h.txt",
    "vanilla_tested.txt": f"{GITHUB_MIRROR_BASE}/vanilla_tested.txt",
    "vanilla_ipv6.txt": f"{GITHUB_MIRROR_BASE}/vanilla_ipv6.txt",
    "vanilla_ipv6_72h.txt": f"{GITHUB_MIRROR_BASE}/vanilla_ipv6_72h.txt",
    "vanilla_ipv6_tested.txt": f"{GITHUB_MIRROR_BASE}/vanilla_ipv6_tested.txt",
}

EXTRA_SOURCES = {}

# ============================================================================
# VLESS PARSER COMPONENTS
# ============================================================================

console = Console()

LABELS: dict[str, str] = {
    "sber.ru":             "Сбер",
    "online.sberbank.ru":  "Сбер Онлайн",
    "tbank.ru":            "Т-Банк",
    "tinkoff.ru":          "Т-Банк",
    "alfabank.ru":         "Альфа",
    "vtb.ru":              "ВТБ",
    "ozon.ru":             "Ozon",
    "wildberries.ru":      "WB",
    "wb.ru":               "WB",
    "avito.ru":            "Avito",
    "avito.st":            "Avito",
    "vk.com":              "VK",
    "vk.ru":               "VK",
    "userapi.com":         "VK",
    "yandex.ru":           "Яндекс",
    "ya.ru":               "Яндекс",
    "dzen.ru":             "Дзен",
    "yastatic.net":        "Яндекс",
    "gosuslugi.ru":        "Госуслуги",
    "esia.gosuslugi.ru":   "Госуслуги",
    "mts.ru":              "МТС",
    "megafon.ru":          "МегаФон",
    "beeline.ru":          "Билайн",
    "tele2.ru":            "Tele2",
    "rt.ru":               "Ростелеком",
    "rutube.ru":           "Rutube",
    "ivi.ru":              "Иви",
    "okko.tv":             "Okko",
    "fasssst.ru":          "Fasssst",
    "tree-top.cc":         "TreeTop",
    "maviks.ru":           "Maviks",
    "connect-iskra.ru":    "Iskra",
    "speedload.ru":        "Speedload",
    "tcp-reset-club.net":  "TCP-Reset",
}

def get_label(host: str) -> str:
    if not host:
        return "Unknown"
    h = host.lower().strip("[]")
    if h in LABELS:
        return LABELS[h]
    parts = h.split(".")
    for i in range(1, len(parts) + 1):
        sub = ".".join(parts[-i:])
        if sub in LABELS:
            return LABELS[sub]
    return parts[-2].capitalize() if len(parts) >= 2 else h.upper()

@dataclass(slots=True)
class Vless:
    raw:     str
    uuid:    str
    host:    str
    port:    int
    params:  dict
    remark:  str   = ""
    latency: float = -1.0

    @property
    def sni(self) -> str:
        return self.params.get("sni") or self.params.get("host") or self.host

    @property
    def proto(self) -> str:
        t   = self.params.get("type", "tcp").lower()
        sec = self.params.get("security", "").lower()
        if sec == "reality":               return "reality"
        if sec in ("tls", "xtls"):         return "tls"
        if t in ("ws", "websocket"):       return "ws"
        if t in ("grpc", "gun"):           return "grpc"
        if t in ("httpupgrade", "xhttp"):  return "xhttp"
        if t == "h2":                      return "h2"
        return "tcp"

    @property
    def dedup_key(self) -> str:
        return f"{self.uuid}@{self.host}:{self.port}"

VLESS_PAT = re.compile(r"vless://[^\s#\"'<>]+", re.IGNORECASE)

def _try_base64_decode(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("data:"):
        stripped = stripped.split(",", 1)[-1]
    try:
        padded  = stripped + "=" * (-len(stripped) % 4)
        decoded = base64.b64decode(padded).decode("utf-8", errors="ignore")
        if "vless://" in decoded.lower():
            return decoded
    except Exception:
        pass
    return text

def validate_sni(hostname: str) -> Optional[str]:
    """Validate and clean SNI hostname, return None if invalid"""
    if not hostname:
        return None
    cleaned = re.sub(r'[^\x20-\x7E]', '', hostname.strip())
    if not cleaned or len(cleaned) > 255:
        return None
    if re.match(r'^[\w\.\-]+$', cleaned):
        try:
            cleaned.encode('idna')
            return cleaned
        except (UnicodeError, UnicodeEncodeError):
            return None
    ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(ip_pattern, cleaned):
        return cleaned
    if cleaned.startswith('[') and cleaned.endswith(']'):
        return cleaned
    return None

def parse_vless(line: str) -> Optional[Vless]:
    line = line.strip()
    if not line.lower().startswith("vless://"):
        return None
    try:
        u = urlparse(line)
        if "@" not in u.netloc:
            return None

        uuid_part, netloc_rest = u.netloc.split("@", 1)
        netloc_rest = netloc_rest.split("#")[0]

        if "?" in netloc_rest:
            host_port, query_str = netloc_rest.split("?", 1)
        else:
            host_port, query_str = netloc_rest, u.query or ""

        if host_port.startswith("["):
            bracket_end = host_port.index("]")
            host     = host_port[: bracket_end + 1]
            port_str = host_port[bracket_end + 1:].lstrip(":")
        elif ":" in host_port:
            host, port_str = host_port.rsplit(":", 1)
        else:
            host, port_str = host_port, "443"

        params: dict[str, str] = {}
        if query_str:
            for k, vs in parse_qs(query_str).items():
                if vs:
                    value = unquote(vs[0])
                    if k in ("sni", "host"):
                        value = re.sub(r'[^\x20-\x7E]', '', value.strip())
                    params[k] = value

        params = {k: v for k, v in params.items() if v}

        remark = unquote(u.fragment) if u.fragment else ""

        return Vless(
            raw    = line,
            uuid   = uuid_part,
            host   = host,
            port   = int(port_str),
            params = params,
            remark = remark,
        )
    except Exception:
        return None

def normalize_url(v: Vless) -> str:
    SAFE_KEYS = {"security", "type", "fp", "pbk", "sid", "flow", "spx", "mode"}
    q_parts = [
        f"{k}={v.params[k]}" if k in SAFE_KEYS else f"{k}={quote(v.params[k])}"
        for k in sorted(v.params)
    ]
    base = f"vless://{v.uuid}@{v.host}:{v.port}"
    if q_parts:
        base += "?" + "&".join(q_parts)
    if v.remark:
        base += "#" + quote(v.remark, safe="/ ")
    return base

async def fetch_with_retry(
    session: aiohttp.ClientSession,
    url: str,
    sem: asyncio.Semaphore,
    *,
    retries: int = PARSER_RETRY_COUNT,
) -> Optional[str]:
    delay = PARSER_RETRY_DELAY
    async with sem:
        for attempt in range(1, retries + 1):
            try:
                async with session.get(url, ssl=False) as resp:
                    if resp.status == 200:
                        text = await resp.text(encoding="utf-8", errors="ignore")
                        return _try_base64_decode(text)
                    if 400 <= resp.status < 500:
                        return None
            except (aiohttp.ClientError, asyncio.TimeoutError):
                pass
            if attempt < retries:
                await asyncio.sleep(delay)
                delay *= 2
    return None

async def parser_download_phase(progress: Progress) -> int:
    sources_file = Path(PARSER_SOURCES_FILE)
    if not sources_file.is_file():
        console.print(f"[red]{PARSER_SOURCES_FILE} не найден[/red]")
        return 0

    urls: list[str] = []
    async with aiofiles.open(sources_file, encoding="utf-8") as f:
        async for line in f:
            line = line.strip()
            if line and not line.startswith(("#", "//")):
                urls.append(line)

    if not urls:
        return 0

    task = progress.add_task(f"[cyan]Скачивание VLESS[/cyan] [dim]({len(urls)} источников)[/dim]", total=len(urls))
    sem = asyncio.Semaphore(PARSER_DOWNLOAD_CONC)
    timeout = aiohttp.ClientTimeout(total=15, connect=5)
    links: set[str] = set()

    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [fetch_with_retry(session, u, sem) for u in urls]
        for coro in asyncio.as_completed(tasks):
            result = await coro
            if isinstance(result, str):
                links.update(VLESS_PAT.findall(result))
            progress.advance(task)

    if links:
        async with aiofiles.open(PARSER_RAW_FILE, "w", encoding="utf-8") as f:
            for ln in sorted(links):
                await f.write(ln + "\n")

    progress.remove_task(task)
    logger.info(f"VLESS download: {len(links)} raw links")
    return len(links)

async def parser_clean_and_rename(progress: Progress) -> list[Vless]:
    raw_file = Path(PARSER_RAW_FILE)
    if not raw_file.is_file():
        return []

    task = progress.add_task("[cyan]Парсинг VLESS[/cyan]", total=None)

    configs: list[Vless] = []
    async with aiofiles.open(raw_file, encoding="utf-8") as f:
        async for line in f:
            v = parse_vless(line)
            if v:
                configs.append(v)

    seen_keys: set[str] = set()
    unique: list[Vless] = []
    for v in configs:
        k = v.dedup_key
        if k not in seen_keys:
            seen_keys.add(k)
            unique.append(v)

    for v in unique:
        v.remark = f"{v.proto.upper()} • {get_label(v.sni)}"

    if unique:
        async with aiofiles.open(PARSER_NAMED_FILE, "w", encoding="utf-8") as f:
            for v in unique:
                await f.write(normalize_url(v) + "\n")

    progress.remove_task(task)
    logger.info(f"VLESS clean: {len(configs)} -> {len(unique)} unique")
    return unique

def tcp_check(v: Vless) -> float:
    t0 = time.perf_counter()
    try:
        host = v.host.strip("[]")
        with socket.create_connection((host, v.port), timeout=PARSER_TCP_TIMEOUT) as sock:
            if v.proto in ("tls", "reality"):
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                
                sni = validate_sni(v.sni)
                if sni is None:
                    sni = validate_sni(v.host)
                    if sni is None:
                        return -1.0
                
                try:
                    with ctx.wrap_socket(sock, server_hostname=sni) as tls_sock:
                        tls_sock.do_handshake()
                except ssl.SSLError as e:
                    if "UNRECOGNIZED_NAME" in str(e):
                        with ctx.wrap_socket(sock) as tls_sock:
                            tls_sock.do_handshake()
                    else:
                        raise
        return (time.perf_counter() - t0) * 1000
    except (socket.timeout, ConnectionRefusedError, OSError, ssl.SSLError):
        return -1.0

async def parser_check_phase(
    configs: list[Vless],
    progress: Progress,
) -> tuple[list[Vless], list[Vless]]:
    if not configs:
        return [], []

    task = progress.add_task(f"[cyan]Проверка VLESS[/cyan] [dim]({len(configs)} конфигов)[/dim]", total=len(configs))
    loop = asyncio.get_running_loop()
    sem = asyncio.Semaphore(PARSER_CHECK_WORKERS)

    async def _run(v: Vless) -> Vless:
        async with sem:
            v.latency = await loop.run_in_executor(None, tcp_check, v)
            progress.advance(task)
            return v

    results = await asyncio.gather(*[_run(v) for v in configs])
    progress.remove_task(task)

    alive = sorted([v for v in results if v.latency >= 0], key=lambda x: x.latency)
    dead = [v for v in results if v.latency < 0]

    if alive:
        async with aiofiles.open(PARSER_WORK_FILE, "w", encoding="utf-8") as f:
            for v in alive:
                await f.write(normalize_url(v) + "\n")
    if dead:
        async with aiofiles.open(PARSER_DEAD_FILE, "w", encoding="utf-8") as f:
            for v in dead:
                await f.write(normalize_url(v) + "\n")

    logger.info(f"VLESS check: alive={len(alive)} dead={len(dead)}")
    return alive, dead

def parser_print_stats(alive: list[Vless], dead: list[Vless], elapsed: float) -> None:
    total = len(alive) + len(dead)
    pct_alive = (len(alive) / total * 100) if total else 0

    summary = Table(box=box.ROUNDED, title="Результаты VLESS цикла", title_style="bold cyan")
    summary.add_column("Метрика", style="bold")
    summary.add_column("Значение", justify="right")

    summary.add_row("Всего конфигов", f"[white]{total}[/white]")
    summary.add_row("Живые", f"[green]{len(alive)}[/green]  ({pct_alive:.1f}%)")
    summary.add_row("Мёртвые", f"[red]{len(dead)}[/red]")
    if alive:
        lats = [v.latency for v in alive]
        summary.add_row("Лучший latency", f"[bold green]{min(lats):.0f} ms[/bold green]")
        summary.add_row("Средний latency", f"[yellow]{sum(lats)/len(lats):.0f} ms[/yellow]")
        summary.add_row("Худший latency", f"[red]{max(lats):.0f} ms[/red]")
    summary.add_row("Время цикла", f"[dim]{elapsed:.1f}s[/dim]")
    console.print(summary)

    if alive:
        top = Table(box=box.SIMPLE_HEAD, title="Топ-15 самых быстрых VLESS", title_style="bold green", show_lines=False)
        top.add_column("#", width=4, justify="right", style="dim")
        top.add_column("Latency", width=10, justify="right")
        top.add_column("Протокол", width=10)
        top.add_column("Метка", width=16)
        top.add_column("Host", style="dim")

        for i, v in enumerate(alive[:15], 1):
            lat_color = "green" if v.latency < 300 else ("yellow" if v.latency < 700 else "red")
            top.add_row(
                str(i),
                f"[{lat_color}]{v.latency:.0f} ms[/{lat_color}]",
                f"[cyan]{v.proto.upper()}[/cyan]",
                get_label(v.sni),
                v.host,
            )
        console.print(top)

    if alive:
        proto_cnt = Counter(v.proto for v in alive)
        pt = Table(box=box.SIMPLE, title="Протоколы VLESS (живые)", title_style="bold magenta")
        pt.add_column("Протокол")
        pt.add_column("Кол-во", justify="right")
        pt.add_column("Доля", justify="right")
        for proto, cnt in proto_cnt.most_common():
            pt.add_row(
                f"[cyan]{proto.upper()}[/cyan]",
                str(cnt),
                f"{cnt/len(alive)*100:.1f}%",
            )
        console.print(pt)

def make_progress() -> Progress:
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=36),
        MofNCompleteColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console,
        transient=True,
    )

async def run_vless_parser_one_cycle() -> Dict:
    """Run one cycle of VLESS parser and return stats"""
    ts = time.time()
    
    console.rule("[bold magenta] VLESS Parser Cycle [/bold magenta]", style="magenta")
    
    with make_progress() as progress:
        await parser_download_phase(progress)
        configs = await parser_clean_and_rename(progress)
        alive, dead = await parser_check_phase(configs, progress)
    
    elapsed = time.time() - ts
    parser_print_stats(alive, dead, elapsed)
    
    return {
        "total": len(configs),
        "alive": len(alive),
        "dead": len(dead),
        "elapsed": elapsed,
        "alive_configs": alive
    }

# ============================================================================
# GIT UPLOADER
# ============================================================================

class GitUploader:
    def __init__(self):
        self.github_session = requests.Session()
        self.github_session.headers.update({
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Tor-Bridges-Parser"
        })
        
        self.gitea_session = requests.Session()
        self.gitea_session.headers.update({
            "Authorization": f"token {GITEA_TOKEN}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
    
    def upload_to_github(self, filepath: str, filename: str) -> bool:
        """Upload file to GitHub repository - DISABLED"""
        return False
    
    def upload_to_gitea(self, filepath: str, filename: str, remote_folder: str = None) -> bool:
        """Upload file to Gitea repository"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if remote_folder:
                gitea_path = f"{remote_folder}/{filename}"
            else:
                gitea_path = f"{GITEA_TOR_FOLDER}/{filename}"
            
            url = f"{GITEA_URL}/api/v1/repos/{GITEA_REPO}/contents/{gitea_path}"
            
            sha = None
            response = self.gitea_session.get(url)
            if response.status_code == 200:
                sha = response.json().get('sha')
            
            data = {
                "content": content,
                "message": f"Update Tor bridges: {filename}",
                "branch": GITEA_BRANCH
            }
            
            if sha:
                data["sha"] = sha
                response = self.gitea_session.put(url, json=data)
            else:
                response = self.gitea_session.post(url, json=data)
            
            if response.status_code in [200, 201]:
                return True
            else:
                return self.upload_to_gitea_base64(filepath, filename, remote_folder)
                
        except Exception:
            return self.upload_to_gitea_base64(filepath, filename, remote_folder)
    
    def upload_to_gitea_base64(self, filepath: str, filename: str, remote_folder: str = None) -> bool:
        """Upload file to Gitea using base64 encoding"""
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            
            encoded_content = base64.b64encode(content).decode('utf-8')
            
            if remote_folder:
                gitea_path = f"{remote_folder}/{filename}"
            else:
                gitea_path = f"{GITEA_TOR_FOLDER}/{filename}"
            
            url = f"{GITEA_URL}/api/v1/repos/{GITEA_REPO}/contents/{gitea_path}"
            
            sha = None
            response = self.gitea_session.get(url)
            if response.status_code == 200:
                sha = response.json().get('sha')
            
            data = {
                "content": encoded_content,
                "message": f"Update Tor bridges: {filename}",
                "branch": GITEA_BRANCH,
                "encoding": "base64"
            }
            
            if sha:
                data["sha"] = sha
                response = self.gitea_session.put(url, json=data)
            else:
                response = self.gitea_session.post(url, json=data)
            
            return response.status_code in [200, 201]
                
        except Exception:
            return False
    
    def upload_sources_folder_to_gitea(self, sources_path: str) -> Dict[str, bool]:
        """Upload all files from sources folder to Gitea"""
        results = {}
        
        if not os.path.exists(sources_path):
            print(f"⚠️ Folder {sources_path} not found")
            return results
        
        all_files = []
        for root, dirs, files in os.walk(sources_path):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, sources_path)
                all_files.append((full_path, rel_path))
        
        if not all_files:
            print(f"⚠️ No files found in {sources_path}")
            return results
        
        print(f"\n📁 Uploading {len(all_files)} files from 'sources' folder to Gitea...")
        print("-" * 60)
        
        success_count = 0
        for i, (full_path, rel_path) in enumerate(all_files, 1):
            rel_path_normalized = rel_path.replace('\\', '/')
            print(f"   [{i:2d}/{len(all_files)}] {rel_path_normalized}...", end=' ')
            
            remote_folder = f"{GITEA_TOR_FOLDER}/sources"
            dir_path = os.path.dirname(rel_path)
            if dir_path:
                dir_path_normalized = dir_path.replace('\\', '/')
                remote_folder = f"{GITEA_TOR_FOLDER}/sources/{dir_path_normalized}"
            
            success = self.upload_to_gitea(full_path, os.path.basename(full_path), remote_folder)
            results[rel_path] = success
            
            if success:
                success_count += 1
                print("✅")
            else:
                print("❌")
        
        print(f"\n📊 Sources folder upload summary: {success_count}/{len(all_files)} files uploaded")
        return results
    
    def upload_vless_files_to_gitea(self) -> Dict[str, bool]:
        """Upload VLESS parser result files to Gitea"""
        results = {}
        vless_files = [PARSER_RAW_FILE, PARSER_NAMED_FILE, PARSER_WORK_FILE, PARSER_DEAD_FILE]
        
        print("\n📤 Uploading VLESS parser files to Gitea...")
        print("-" * 60)
        
        for filename in vless_files:
            if os.path.exists(filename):
                print(f"   {filename}...", end=' ')
                success = self.upload_to_gitea(filename, filename, GITEA_TOR_FOLDER)
                results[filename] = success
                print("✅" if success else "❌")
            else:
                print(f"   {filename}... ⚠️ not found")
                results[filename] = False
        
        return results
    
    def upload_all_files(self, folder_path: str) -> Dict[str, Dict[str, bool]]:
        """Upload all tor bridge files to Gitea only"""
        results = {"github": {}, "gitea": {}}
        
        if not os.path.exists(folder_path):
            print(f"⚠️ Folder {folder_path} not found")
            return results
        
        files = [f for f in os.listdir(folder_path) 
                if f.endswith('.txt') and f != 'bridge_history.json']
        
        print(f"\n📤 Uploading {len(files)} files to Gitea only...")
        print("=" * 60)
        
        print("\n🦋 Uploading to Gitea...")
        gitea_success = 0
        for i, filename in enumerate(files, 1):
            filepath = os.path.join(folder_path, filename)
            print(f"   [{i:2d}/{len(files)}] {filename}...", end=' ')
            success = self.upload_to_gitea(filepath, filename)
            results["gitea"][filename] = success
            if success:
                gitea_success += 1
                print("✅")
            else:
                print("❌")
        
        print(f"\n📊 Upload Summary:")
        print(f"   Gitea: {gitea_success}/{len(files)} files uploaded (GitHub disabled)")
        
        return results

# ============================================================================
# TOR BRIDGES PARSER
# ============================================================================

class TorBridgesParser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/plain,text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9",
        })
        self.history = self._load_history()
        self.git_uploader = GitUploader()
        
    def _load_history(self) -> Dict:
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Ошибка загрузки истории: {e}")
        return {}
    
    def _save_history(self):
        try:
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Ошибка сохранения истории: {e}")
    
    def _cleanup_history(self):
        cutoff = datetime.now() - timedelta(days=HISTORY_RETENTION_DAYS)
        old_count = len(self.history)
        self.history = {
            k: v for k, v in self.history.items()
            if datetime.fromisoformat(v) > cutoff
        }
        removed = old_count - len(self.history)
        if removed > 0:
            print(f"   🗑️ Удалено {removed} старых записей из истории")
    
    def parse_bridge_line(self, line: str) -> Optional[Dict]:
        line = line.strip()
        if not line or line.startswith('#'):
            return None
        
        result = {
            'transport': None,
            'host': None,
            'port': None,
            'fingerprint': None,
            'url': None,
            'sni': None,
            'version': None,
            'is_ipv6': False,
            'raw': line
        }
        
        if line.startswith('obfs4'):
            result['transport'] = 'obfs4'
        elif line.startswith('webtunnel'):
            result['transport'] = 'webtunnel'
        elif line.startswith('vanilla'):
            result['transport'] = 'vanilla'
        else:
            if 'webtunnel' in line.lower() or 'url=' in line:
                result['transport'] = 'webtunnel'
            elif 'obfs4' in line.lower():
                result['transport'] = 'obfs4'
            else:
                result['transport'] = 'vanilla'
        
        ipv6_match = re.search(r'\[([0-9a-fA-F:]+)\]:(\d+)', line)
        if ipv6_match:
            result['host'] = ipv6_match.group(1)
            result['port'] = int(ipv6_match.group(2))
            result['is_ipv6'] = True
        
        if not result['host']:
            ipv4_match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d+)', line)
            if ipv4_match:
                result['host'] = ipv4_match.group(1)
                result['port'] = int(ipv4_match.group(2))
        
        if not result['host']:
            domain_match = re.search(r'([a-zA-Z0-9.-]+):(\d+)', line)
            if domain_match:
                result['host'] = domain_match.group(1)
                result['port'] = int(domain_match.group(2))
        
        fp_match = re.search(r'([A-F0-9]{40})', line, re.IGNORECASE)
        if fp_match:
            result['fingerprint'] = fp_match.group(1).upper()
        
        url_match = re.search(r'url=([^\s]+)', line)
        if url_match:
            result['url'] = url_match.group(1)
        
        sni_match = re.search(r'sni-imitation=([^\s]+)', line)
        if sni_match:
            result['sni'] = sni_match.group(1)
        
        ver_match = re.search(r'ver=([0-9.]+)', line)
        if ver_match:
            result['version'] = ver_match.group(1)
        
        return result if result['host'] or result['fingerprint'] else None
    
    def download_bridge_file(self, filename: str, url: str) -> Tuple[str, List[str], bool]:
        try:
            print(f"   📥 Загрузка {filename}...", end=' ')
            response = self.session.get(url, timeout=DOWNLOAD_TIMEOUT)
            
            if response.status_code == 200:
                lines = []
                new_bridges = 0
                
                for line in response.text.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        lines.append(line)
                        if line not in self.history:
                            self.history[line] = datetime.now().isoformat()
                            new_bridges += 1
                
                print(f"✅ {len(lines)} мостов (новых: {new_bridges})")
                return filename, lines, True
            else:
                print(f"❌ HTTP {response.status_code}")
                return filename, [], False
                
        except requests.exceptions.Timeout:
            print(f"❌ Таймаут")
            return filename, [], False
        except Exception as e:
            print(f"❌ Ошибка: {str(e)[:50]}")
            return filename, [], False
    
    def download_all_bridges(self) -> Dict[str, List[str]]:
        all_sources = {**BRIDGE_FILES, **EXTRA_SOURCES}
        
        print(f"\n🌐 Скачивание {len(all_sources)} файлов с мостами...")
        print("-" * 60)
        
        results = {}
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {
                executor.submit(self.download_bridge_file, name, url): name
                for name, url in all_sources.items()
            }
            
            for future in as_completed(futures):
                name, lines, success = future.result()
                if success:
                    results[name] = lines
        
        return results
    
    def save_bridges(self, bridges: Dict[str, List[str]]):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        for name, lines in bridges.items():
            filepath = os.path.join(OUTPUT_DIR, name)
            with open(filepath, 'w', encoding='utf-8') as f:
                for line in lines:
                    f.write(line + '\n')
        
        print(f"\n💾 Сохранено {len(bridges)} файлов в папку {OUTPUT_DIR}/")
    
    def create_zip_archive(self) -> Optional[str]:
        zip_path = os.path.join(OUTPUT_DIR, "tor_bridges_complete.zip")
        
        if os.path.exists(zip_path):
            os.remove(zip_path)
        
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for filename in os.listdir(OUTPUT_DIR):
                    if filename.endswith('.zip') or filename == "bridge_history.json":
                        continue
                    
                    filepath = os.path.join(OUTPUT_DIR, filename)
                    
                    if '_tested' in filename:
                        folder = "Tested"
                    elif '_72h' in filename:
                        folder = "Recent_72h"
                    elif '_ipv6' in filename:
                        folder = "IPv6"
                    else:
                        folder = "Full_Archive"
                    
                    arcname = os.path.join(folder, filename)
                    zipf.write(filepath, arcname)
            
            size_kb = os.path.getsize(zip_path) / 1024
            print(f"\n📦 Создан ZIP архив: {zip_path} ({size_kb:.1f} KB)")
            return zip_path
            
        except Exception as e:
            print(f"⚠️ Ошибка создания ZIP архива: {e}")
            return None
    
    def analyze_bridges(self, bridges: Dict[str, List[str]]) -> Dict:
        analysis = {
            'obfs4': {'total': 0, 'tested': 0, 'recent': 0, 'ipv6': 0},
            'webtunnel': {'total': 0, 'tested': 0, 'recent': 0, 'ipv6': 0},
            'vanilla': {'total': 0, 'tested': 0, 'recent': 0, 'ipv6': 0},
            'total_bridges': 0,
            'unique_fingerprints': set(),
            'unique_hosts': set()
        }
        
        for name, lines in bridges.items():
            count = len(lines)
            
            if 'obfs4' in name:
                if name == 'obfs4.txt':
                    analysis['obfs4']['total'] = count
                elif 'tested' in name:
                    analysis['obfs4']['tested'] = count
                elif '72h' in name:
                    analysis['obfs4']['recent'] = count
                elif 'ipv6' in name:
                    analysis['obfs4']['ipv6'] = count
            
            elif 'webtunnel' in name:
                if name == 'webtunnel.txt':
                    analysis['webtunnel']['total'] = count
                elif 'tested' in name:
                    analysis['webtunnel']['tested'] = count
                elif '72h' in name:
                    analysis['webtunnel']['recent'] = count
                elif 'ipv6' in name:
                    analysis['webtunnel']['ipv6'] = count
            
            elif 'vanilla' in name:
                if name == 'vanilla.txt':
                    analysis['vanilla']['total'] = count
                elif 'tested' in name:
                    analysis['vanilla']['tested'] = count
                elif '72h' in name:
                    analysis['vanilla']['recent'] = count
                elif 'ipv6' in name:
                    analysis['vanilla']['ipv6'] = count
            
            for line in lines:
                parsed = self.parse_bridge_line(line)
                if parsed:
                    if parsed['fingerprint']:
                        analysis['unique_fingerprints'].add(parsed['fingerprint'])
                    if parsed['host']:
                        analysis['unique_hosts'].add(parsed['host'])
        
        analysis['total_bridges'] = (
            analysis['obfs4']['total'] + 
            analysis['webtunnel']['total'] + 
            analysis['vanilla']['total']
        )
        analysis['total_unique_fingerprints'] = len(analysis['unique_fingerprints'])
        analysis['total_unique_hosts'] = len(analysis['unique_hosts'])
        
        return analysis
    
    def print_report(self, analysis: Dict) -> int:
        print("\n" + "=" * 70)
        print("📊 ОТЧЕТ О СОБРАННЫХ TOR МОСТАХ")
        print("=" * 70)
        
        print(f"\n{'Тип':<12} {'Всего':>8} {'Проверено':>10} {'Свежие 72ч':>10} {'IPv6':>8}")
        print("-" * 50)
        
        for t in ['obfs4', 'webtunnel', 'vanilla']:
            data = analysis[t]
            print(f"{t:<12} {data['total']:>8} {data['tested']:>10} {data['recent']:>10} {data['ipv6']:>8}")
        
        print("-" * 50)
        
        print(f"\n📈 ИТОГО:")
        print(f"   Всего уникальных мостов: {analysis['total_bridges']}")
        print(f"   Уникальных fingerprint'ов: {analysis['total_unique_fingerprints']}")
        print(f"   Уникальных хостов: {analysis['total_unique_hosts']}")
        
        total_tested = analysis['obfs4']['tested'] + analysis['webtunnel']['tested'] + analysis['vanilla']['tested']
        if analysis['total_bridges'] > 0:
            working_percent = (total_tested / analysis['total_bridges']) * 100
            print(f"   Процент проверенных: {working_percent:.1f}%")
        
        print("=" * 70)
        
        return total_tested
    
    def create_local_readme(self, analysis: Dict, total_tested: int):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        readme_content = f"""# Tor Bridges Collection

**Last update:** {timestamp}

## Statistics

| Type | Total | Tested | Recent (72h) | IPv6 |
|------|-------|--------|--------------|------|
| **obfs4** | {analysis['obfs4']['total']} | {analysis['obfs4']['tested']} | {analysis['obfs4']['recent']} | {analysis['obfs4']['ipv6']} |
| **WebTunnel** | {analysis['webtunnel']['total']} | {analysis['webtunnel']['tested']} | {analysis['webtunnel']['recent']} | {analysis['webtunnel']['ipv6']} |
| **Vanilla** | {analysis['vanilla']['total']} | {analysis['vanilla']['tested']} | {analysis['vanilla']['recent']} | {analysis['vanilla']['ipv6']} |

**Total bridges:** {analysis['total_bridges']}
**Tested working:** {total_tested}
**Unique hosts:** {analysis['total_unique_hosts']}

## Usage

For Tor Browser:
1. Open Tor Browser
2. Go to Settings → Tor Bridges
3. Select "Provide a bridge I know"
4. Copy a bridge line from `*_tested.txt` files

---
Generated by Tor Bridges Parser
"""
        
        readme_path = "README_TOR_BRIDGES.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"\n📝 Created local README: {readme_path}")
    
    def cleanup_old_files(self):
        if not os.path.exists(OUTPUT_DIR):
            return
        
        for filename in os.listdir(OUTPUT_DIR):
            if filename.endswith('.zip') and filename != "tor_bridges_complete.zip":
                filepath = os.path.join(OUTPUT_DIR, filename)
                try:
                    os.remove(filepath)
                except:
                    pass
    
    def upload_sources_to_gitea(self):
        """Upload entire sources folder to Gitea"""
        print("\n" + "=" * 60)
        print("📁 UPLOADING SOURCES FOLDER TO GITEA")
        print("=" * 60)
        
        if os.path.exists(SOURCES_DIR):
            results = self.git_uploader.upload_sources_folder_to_gitea(SOURCES_DIR)
            success_count = sum(1 for v in results.values() if v)
            print(f"\n✅ Sources uploaded: {success_count}/{len(results)} files")
        else:
            print(f"⚠️ Sources folder '{SOURCES_DIR}' not found, skipping...")
            print(f"   Create '{SOURCES_DIR}' folder and add files to upload them to Gitea")
    
    def run_tor_bridges(self):
        """Run only Tor bridges collection"""
        print("=" * 70)
        print("TOR BRIDGES PARSER - GitHub Mirror Version")
        print("=" * 70)
        print(f"Source: {GITHUB_MIRROR_BASE}")
        print(f"Local output: {OUTPUT_DIR}/")
        print("=" * 70)
        
        self._cleanup_history()
        
        bridges = self.download_all_bridges()
        
        if not bridges:
            print("\n❌ Failed to download any bridge files!")
            print("   Check internet connection or GitHub availability")
            return
        
        self.save_bridges(bridges)
        self._save_history()
        
        analysis = self.analyze_bridges(bridges)
        total_tested = self.print_report(analysis)
        self.create_local_readme(analysis, total_tested)
        self.create_zip_archive()
        
        self.git_uploader.upload_all_files(OUTPUT_DIR)
        
        self.cleanup_old_files()
        
        print("\n" + "=" * 70)
        print("✅ TOR BRIDGES COMPLETED!")
        print("=" * 70)
    
    def run_full(self):
        """Run both Tor bridges and VLESS parser"""
        # Run Tor bridges collection
        self.run_tor_bridges()
        
        # Run VLESS parser
        print("\n" + "=" * 70)
        print("🔄 STARTING VLESS PARSER")
        print("=" * 70)
        
        try:
            # Run one cycle of VLESS parser
            vless_result = asyncio.run(run_vless_parser_one_cycle())
            
            # Upload VLESS results to Gitea
            self.git_uploader.upload_vless_files_to_gitea()
            
            print(f"\n✅ VLESS Parser completed: {vless_result['alive']}/{vless_result['total']} alive")
        except Exception as e:
            print(f"⚠️ VLESS Parser error: {e}")
            import traceback
            traceback.print_exc()
        
        # Upload sources folder
        self.upload_sources_to_gitea()
        
        print("\n" + "=" * 70)
        print("✅ ALL PARSERS COMPLETED SUCCESSFULLY!")
        print("=" * 70)

# ============================================================================
# MAIN
# ============================================================================

def test_parser():
    print("=" * 70)
    print("TEST MODE - Tor Bridges")
    print("=" * 70)
    
    parser = TorBridgesParser()
    
    test_lines = [
        "obfs4 192.95.36.142:443 C7B7B7B7B7B7B7B7B7B7B7B7B7B7B7B7B7B7B7B",
        "webtunnel [2001:db8:1:1:1:1:1:1]:443 FINGERPRINT1234567890 url=https://example.com ver=0.0.3",
        "vanilla 192.95.36.142:443"
    ]
    
    print("\n📝 Parse test:")
    for line in test_lines:
        result = parser.parse_bridge_line(line)
        if result:
            print(f"  ✅ {line[:50]}... -> {result['transport']}: {result.get('host', 'N/A')}")
        else:
            print(f"  ❌ FAIL: {line[:50]}")
    
    print("\n🌐 Download test:")
    filename, lines, success = parser.download_bridge_file("obfs4.txt", BRIDGE_FILES["obfs4.txt"])
    
    if success and lines:
        print(f"  ✅ Downloaded {len(lines)} bridges")
        if lines:
            print(f"  First bridge: {lines[0][:100]}...")
    else:
        print("  ❌ Download failed")
    
    print("\n✅ Test completed")

def test_vless_parser():
    """Test VLESS parser only"""
    print("=" * 70)
    print("TEST MODE - VLESS Parser")
    print("=" * 70)
    
    try:
        result = asyncio.run(run_vless_parser_one_cycle())
        print(f"\n✅ VLESS test completed: {result['alive']}/{result['total']} alive")
    except Exception as e:
        print(f"❌ VLESS test error: {e}")
        import traceback
        traceback.print_exc()

def main():
    import argparse
    
    global SOURCES_DIR, OUTPUT_DIR, MAX_WORKERS
    
    parser = argparse.ArgumentParser(description="Unified Parser - Tor Bridges + VLESS")
    parser.add_argument("--test", action="store_true", help="Test Tor bridges parser")
    parser.add_argument("--test-vless", action="store_true", help="Test VLESS parser")
    parser.add_argument("--tor-only", action="store_true", help="Run only Tor bridges parser")
    parser.add_argument("--vless-only", action="store_true", help="Run only VLESS parser")
    parser.add_argument("--output", default=OUTPUT_DIR, help=f"Output folder (default: {OUTPUT_DIR})")
    parser.add_argument("--workers", type=int, default=MAX_WORKERS, help=f"Threads (default: {MAX_WORKERS})")
    parser.add_argument("--sources", default=SOURCES_DIR, help=f"Sources folder (default: {SOURCES_DIR})")
    
    args = parser.parse_args()
    
    SOURCES_DIR = args.sources
    OUTPUT_DIR = args.output
    MAX_WORKERS = args.workers
    
    if args.test:
        test_parser()
    elif args.test_vless:
        test_vless_parser()
    elif args.tor_only:
        try:
            collector = TorBridgesParser()
            collector.run_tor_bridges()
        except KeyboardInterrupt:
            print("\n\n⏹️ Interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    elif args.vless_only:
        try:
            result = asyncio.run(run_vless_parser_one_cycle())
            uploader = GitUploader()
            uploader.upload_vless_files_to_gitea()
        except KeyboardInterrupt:
            print("\n\n⏹️ Interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    else:
        try:
            collector = TorBridgesParser()
            collector.run_full()
        except KeyboardInterrupt:
            print("\n\n⏹️ Interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == "__main__":
    main()
