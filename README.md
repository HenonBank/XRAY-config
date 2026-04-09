# XRAY Config Collection

[![Update](https://github.com/HenonBank/XRAY-config/actions/workflows/update.yml/badge.svg)](https://github.com/HenonBank/XRAY-config/actions/workflows/update.yml)
[![Last Updated](https://img.shields.io/github/last-commit/HenonBank/XRAY-config)](https://github.com/HenonBank/XRAY-config/commits)

Коллекция рабочих конфигураций XRAY/VLESS для обхода блокировок. Данные обновляются автоматически.

## 📁 Структура репозитория

```
├── data/              # Основные данные (конфиги, кэши, источники)
│   ├── url_*.txt      # URL конфиги (работчие, кодированные, фильтрованные)
│   ├── vless_*.txt    # VLESS конфиги
│   ├── sources.txt    # Источники сбора
│   └── country_cache.json  # Кэш стран
├── blacklists/        # Черные списки для фильтрации
├── whitelists/        # Белые списки CIDR и SNI
├── tor_bridges/       # Мосты Tor (webtunnel, obfs4)
├── clients/           # Инструкции для клиентов
├── mirrors/           # Зеркала
└── assets/            # Дополнительные ресурсы
```

## 📥 Быстрый старт

### Основные файлы для использования:

| Файл | Описание |
|------|----------|
| [data/url_work.txt](data/url_work.txt) | **Рабочие конфиги с названиями стран** |
| [data/url_encoded.txt](data/url_encoded.txt) | Закодированные конфиги |
| [data/vless_configs.txt](data/vless_configs.txt) | VLESS конфиги |

### Использование:
1. Скопируйте содержимое файла `data/url_work.txt`
2. Вставьте в ваш клиент (Xray, v2rayN, Nekoray, v2rayNG и т.д.)

## 🗂️ Детальная структура

### Data (`/data`)
Основные рабочие файлы:
- `url_work.txt` — проверенные рабочие конфиги
- `url_encoded.txt` — URL в закодированном формате
- `url_filtered.txt` — отфильтрованные конфиги
- `url_named.txt` — конфиги с понятными именами
- `vless_configs.txt` — VLESS конфигурации
- `sources.txt` — источники сбора конфигов

### Blacklists (`/blacklists`)
Списки для блокировки нежелательных доменов и IP:
- `VLESS_full.txt` / `VLESS_mobile.txt` — полные и мобильные списки
- `ALL_protocols.txt` — все протоколы

### Whitelists (`/whitelists`)
Белые списки для разрешённых соединений:
- `CIDR_full.txt` / `CIDR_mobile_*.txt` — CIDR диапазоны
- `SNI_full.txt` — SNI имена
- `CIDR_checked.txt` — проверенные диапазоны

### Tor Bridges (`/tor_bridges`)
Мосты для подключения к Tor:
- `bridges_webtunnel.txt` — WebTunnel мосты
- `bridges_obfs4.txt` — Obfs4 мосты
- `bridges_top100.txt` — Топ-100 мостов
- `bridges_all.txt` — Все доступные мосты

### Clients (`/clients`)
Инструкции по настройке популярных клиентов:
- `v2rayN.md` — для Windows
- `v2rayNG.md` — для Android
- `Streisand.md` — для iOS
- `Throne.md` — для macOS
- `Karing.md` — кроссплатформенный

## ⚠️ Важная информация

- Все конфиги собираются автоматически из открытых источников
- Работоспособность не гарантируется на 100%
- Используйте на свой страх и риск
- Рекомендуется регулярно обновлять список конфигов

## 📝 Лицензия

MIT License
