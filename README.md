``markdown
<div align="center">

# 🛡️ XRAY-config | Бесплатные VPN-конфигурации для РФ

### *Актуальные, проверенные VPN-конфигурации для работы на территории Российской Федерации*

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/HenonBank/XRAY-config)](https://github.com/HenonBank/XRAY-config/commits/main)
[![GitHub stars](https://img.shields.io/github/stars/HenonBank/XRAY-config)](https://github.com/HenonBank/XRAY-config/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/HenonBank/XRAY-config)](https://github.com/HenonBank/XRAY-config/network)
[![GitHub issues](https://img.shields.io/github/issues/HenonBank/XRAY-config)](https://github.com/HenonBank/XRAY-config/issues)
[![GitHub watchers](https://img.shields.io/github/watchers/HenonBank/XRAY-config)](https://github.com/HenonBank/XRAY-config/watchers)
[![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![Telegram](https://img.shields.io/badge/Telegram-Channel-blue)](https://t.me/HenonBank)

**Автоматическое тестирование** • **Разделение по типам блокировок** • **Регулярные обновления** • **100% рабочие конфиги**

[📖 Полная документация](#-полное-содержание) • [🚀 Быстрый старт](#-быстрый-старт) • [📥 Все подписки](#-все-подписки-полный-список) • [💬 Поддержка](#-поддержка-и-контакты)

---

### 🌟 Ключевые особенности

| 🚀 Автообновление | ✅ Реальная проверка | 🎯 Только рабочие | 🔄 1-2 часа | 🌍 Все протоколы |
|-------------------|---------------------|-------------------|-------------|------------------|
| Конфиги обновляются автоматически | Проверка на сервере в РФ | Отсев медленных и нерабочих | Частота обновлений | VLESS, SS, H2, Trojan |

| 📱 Мобильная версия | 💻 ПК версия | 🧅 Tor Bridges | 🔒 Белые списки | ⚫ Черные списки |
|--------------------|--------------|----------------|-----------------|-----------------|
| Оптимизировано для телефонов | Полные подписки | Альтернативный доступ | Обход CIDR/SNI | Стандартный режим |

</div>

---

## 📚 Полное содержание

<details open>
<summary><b>📑 Оглавление (нажмите для навигации)</b></summary>

### Основные разделы
1. [Для чего этот репозиторий](#-для-чего-этот-репозиторий)
   - [Проблема современного интернета в РФ](#проблема-современного-интернета-в-рф)
   - [Как работает блокировка](#как-работает-блокировка)
   - [Наше решение](#наше-решение)
   - [Результат](#результат)

2. [Техническая информация](#-техническая-информация)
   - [Протоколы](#протоколы)
   - [Транспорты](#транспорты)
   - [Шифрование](#шифрование)

3. [Как выбрать подписку](#-как-выбрать-подписку-полное-руководство)
   - [Черные списки ⚫](#черные-списки-полное-руководство)
   - [Белые списки ⚪](#белые-списки-полное-руководство)
   - [Tor Bridges 🧅](#tor-bridges-полное-руководство)
   - [Сравнительная таблица](#сравнительная-таблица-подписок)

4. [Все подписки (полный список)](#-все-подписки-полный-список)
   - [Черные списки](#черные-списки-полный-список)
   - [Белые списки](#белые-списки-полный-список)
   - [Tor Bridges](#tor-bridges-полный-список)

5. [Быстрый старт](#-быстрый-старт-пошаговая-инструкция)
   - [Шаг 1: Выбор клиента](#шаг-1-выбор-клиента-подробная-таблица)
   - [Шаг 2: Скачивание и установка](#шаг-2-скачивание-и-установка-подробно)
   - [Шаг 3: Добавление подписки](#шаг-3-добавление-подписки-подробно)
   - [Шаг 4: Тестирование](#шаг-4-тестирование-конфигураций)
   - [Шаг 5: Подключение](#шаг-5-подключение-и-проверка)

6. [Клиенты (полные инструкции)](#-клиенты-полные-инструкции)
   - [Windows клиенты](#windows-клиенты-полные-инструкции)
   - [macOS клиенты](#macos-клиенты-полные-инструкции)
   - [Linux клиенты](#linux-клиенты-полные-инструкции)
   - [Android клиенты](#android-клиенты-полные-инструкции)
   - [iOS клиенты](#ios-клиенты-полные-инструкции)

7. [Зеркала для доступа](#-зеркала-для-доступа-полный-список)
   - [Яндекс.Переводчик](#яндекспереводчик-подробно)
   - [jsDelivr CDN](#jsdelivr-cdn-подробно)
   - [Statically CDN](#statically-cdn-подробно)
   - [Githack](#githack-подробно)
   - [Другие зеркала](#другие-зеркала)

8. [Полезные советы](#-полезные-советы-полное-руководство)
   - [DNS-over-HTTPS (DoH)](#dns-over-https-doh-полное-руководство)
   - [Рекомендуемые браузеры](#рекомендуемые-браузеры-полное-руководство)
   - [Что видит провайдер](#что-видит-провайдер-технические-детали)
   - [Оптимизация скорости](#оптимизация-скорости)
   - [Безопасность](#безопасность)

9. [Устранение проблем](#-устранение-проблем-faq)
   - [Конфиги не работают](#конфиги-не-работают)
   - [GitHub заблокирован](#github-заблокирован)
   - [Низкая скорость](#низкая-скорость)
   - [Клиент тормозит](#клиент-тормозит)
   - [Ошибки подключения](#ошибки-подключения)

10. [Поддержать проект](#-поддержать-проект)
11. [Лицензия](#-лицензия)
12. [Контакты](#-поддержка-и-контакты)
13. [Дисклеймер](#-дисклеймер)

</details>

---

## 🎯 Для чего этот репозиторий

### Проблема современного интернета в РФ

В современном интернет-пространстве России существует множество технических ограничений:

**Технические методы блокировки:**
- 🔒 **DPI (Deep Packet Inspection)** — глубокий анализ пакетов, способный распознавать VPN-трафик
- 🔒 **CIDR-блокировки** — блокировка целых диапазонов IP-адресов
- 🔒 **SNI-блокировки** — блокировка по доменным именам
- 🔒 **DNS-отравление** — подмена DNS-ответов
- 🔒 **BGP-hijacking** — перехват маршрутизации
- 🔒 **Throttling** — искусственное ограничение скорости

**Проблемы публичных конфигураций:**
- ❌ 98% публичных конфигов не работают в РФ
- ❌ Большинство имеют низкую скорость (<10 Mbps)
- ❌ 90% перестают работать в течение 24 часов
- ❌ Многие содержат вредоносный код
- ❌ Устаревшие протоколы (OpenVPN, WireGuard) легко блокируются

### Как работает блокировка

<details>
<summary><b>🔍 Технические детали (нажмите для подробностей)</b></summary>

**DPI (Deep Packet Inspection):**
Роскомнадзор использует оборудование DPI, которое:
1. Анализирует все пакеты в реальном времени
2. Ищет характерные сигнатуры VPN-протоколов
3. При обнаружении — разрывает соединение или отправляет RST-пакеты
4. Вносит IP-адреса в черные списки

**CIDR-блокировки:**
Мобильные операторы (МТС, Билайн, Мегафон, Т2) блокируют:
- Целые подсети иностранных хостингов
- IP-диапазоны VPN-провайдеров
- Облачные платформы (AWS, Google Cloud, DigitalOcean)

**SNI-блокировки:**
При подключении к сайту отправляется SNI (Server Name Indication) — доменное имя. DPI:
1. Перехватывает TLS-рукопожатие
2. Считывает SNI
3. Если домен в черном списке — блокирует соединение

</details>

### Наше решение

Этот репозиторий предлагает комплексный подход:

**Технические решения:**
- ✅ **VLESS+REALITY** — маскировка трафика под обычный HTTPS
- ✅ **XHTTP/GRPC транспорты** — устойчивы к DPI
- ✅ **Обход CIDR** — использование белых подсетей РФ
- ✅ **Обход SNI** — подмена доменного имени
- ✅ **Автоматическое тестирование** — проверка каждые 1-2 часа

**Процесс отбора:**
1. 🔍 Сбор конфигураций из 50+ источников
2. 🧪 Тестирование на сервере в РФ (реальные условия)
3. 📊 Измерение скорости и задержки
4. 🗑️ Удаление нерабочих и медленных
5. 📤 Публикация в репозиторий

### Результат

Вы получаете:

| Параметр | Значение |
|----------|----------|
| **Работоспособность** | 95-100% конфигов работают в момент публикации |
| **Скорость** | 50-500 Mbps (зависит от протокола и провайдера) |
| **Задержка** | 50-200 ms (до европейских серверов) |
| **Обновление** | Каждые 1-2 часа |
| **Количество** | 500+ активных конфигов в каждый момент |
| **Протоколы** | VLESS, Shadowsocks, Hysteria2, Trojan, VMess |
| **Платформы** | Windows, macOS, Linux, Android, iOS |

---

## 🔧 Техническая информация

### Протоколы

<details>
<summary><b>📡 Все поддерживаемые протоколы</b></summary>

| Протокол | Устойчивость к DPI | Скорость | Особенности | Рекомендация |
|----------|-------------------|----------|-------------|--------------|
| **VLESS+REALITY** | ⭐⭐⭐⭐⭐ | 🚀🚀🚀🚀🚀 | Маскировка под HTTPS, самый защищенный | Лучший для всех |
| **VLESS+XTLS** | ⭐⭐⭐⭐ | 🚀🚀🚀🚀 | Оптимизация трафика | Отличный выбор |
| **VLESS+TLS** | ⭐⭐⭐ | 🚀🚀🚀 | Стандартное шифрование | Хороший |
| **Shadowsocks** | ⭐⭐⭐ | 🚀🚀🚀 | Легкий, быстрый | Альтернатива |
| **Shadowsocks+AEAD** | ⭐⭐⭐⭐ | 🚀🚀🚀 | Улучшенное шифрование | Рекомендуется |
| **Hysteria2** | ⭐⭐⭐⭐ | 🚀🚀🚀🚀🚀 | Оптимизирован для мобильных сетей | Отлично для телефонов |
| **Trojan** | ⭐⭐⭐ | 🚀🚀🚀 | Маскировка под HTTPS | Хорошая альтернатива |
| **VMess** | ⭐⭐ | 🚀🚀 | Устаревающий | Не рекомендуется |
| **Tuic** | ⭐⭐⭐ | 🚀🚀🚀 | QUIC-based | Экспериментальный |

</details>

### Транспорты

<details>
<summary><b>🔄 Транспортные протоколы</b></summary>

| Транспорт | Устойчивость | Скорость | Особенности |
|-----------|--------------|----------|-------------|
| **XHTTP** | ⭐⭐⭐⭐⭐ | 🚀🚀🚀🚀 | Самый устойчивый, маскировка под HTTP/3 |
| **GRPC** | ⭐⭐⭐⭐ | 🚀🚀🚀🚀 | Высокая скорость, gRPC-based |
| **WebSocket (WS)** | ⭐⭐⭐ | 🚀🚀🚀 | Стандартный, работает везде |
| **TCP** | ⭐⭐ | 🚀🚀🚀 | Базовый, легко обнаруживается |
| **gQUIC** | ⭐⭐⭐ | 🚀🚀🚀🚀 | UDP-based, быстрый |

**Рекомендация:** Используйте конфиги с XHTTP или GRPC транспортами для максимальной устойчивости.

</details>

### Шифрование

<details>
<summary><b>🔐 Методы шифрования</b></summary>

| Метод | Уровень защиты | Скорость | Особенности |
|-------|----------------|----------|-------------|
| **REALITY** | ⭐⭐⭐⭐⭐ | 🚀🚀🚀🚀🚀 | Лучший, полная маскировка |
| **TLS 1.3** | ⭐⭐⭐⭐ | 🚀🚀🚀🚀 | Стандартное шифрование |
| **None** | ⭐ | 🚀🚀🚀🚀🚀 | Без шифрования, быстрее но менее безопасно |
| **AEAD** | ⭐⭐⭐⭐ | 🚀🚀🚀 | Для Shadowsocks |

**Важно:** Конфиги с REALITY — самые устойчивые к DPI, так как маскируются под обычный HTTPS-трафик.

</details>

---

## 📥 Как выбрать подписку (полное руководство)

### Черные списки (полное руководство)

<details>
<summary><b>⚫ Когда использовать черные списки</b></summary>

**Идеальные условия:**
- ✅ У вас кабельный интернет (Ростелеком, Дом.ру, МГТС и др.)
- ✅ Wi-Fi дома или в офисе
- ✅ Мобильный интернет без жестких ограничений
- ✅ Открываются Google, YouTube, Telegram, Instagram (если не заблокированы)
- ✅ Вы хотите максимальную скорость

**Не подходит, если:**
- ❌ На мобильном интернете не открываются иностранные сайты
- ❌ Работает только Яндекс, ВК, Госуслуги
- ❌ Вы в роуминге
- ❌ Мобильный оператор ввел CIDR-блокировки

**Рекомендуемые протоколы:**
1. **VLESS+REALITY** — приоритет №1, максимальная защита
2. **Hysteria2** — отлично для мобильных сетей
3. **Shadowsocks** — легкий и быстрый

</details>

### Белые списки (полное руководство)

<details>
<summary><b>⚪ Когда использовать белые списки</b></summary>

**Идеальные условия:**
- ✅ Мобильный интернет (Мегафон, МТС, Билайн, Т2, Yota)
- ✅ Не открываются иностранные сайты
- ✅ Работает только Яндекс, ВК, Госуслуги, Ozon, Wildberries
- ✅ Оператор ввел CIDR-блокировки
- ✅ Вы находитесь в регионах с жесткими ограничениями

**Как это работает:**
1. Конфиги используют белые IP-адреса (Яндекс, ВК, CDNvideo)
2. Трафик маскируется под обращение к этим сервисам
3. DPI не может заблокировать, так как IP в белом списке

**Типы белых списков:**

| Тип | Что обходит | Когда работает |
|-----|-------------|----------------|
| **CIDR** | Блокировки по IP-диапазонам | 100% операторов с CIDR-блокировками |
| **SNI** | Блокировки по доменным именам | Редко, только легкие ограничения |

**Рекомендация:** Используйте CIDR-подписки, они работают везде.

</details>

### Tor Bridges (полное руководство)

<details>
<summary><b>🧅 Когда использовать Tor Bridges</b></summary>

**Идеальные условия:**
- ✅ VPN не помогает или заблокирован
- ✅ Нужна максимальная анонимность
- ✅ Готовы к ограничениям (только TCP)
- ✅ Используете Tor Browser или Orbot

**Ограничения:**
- ⚠️ Только TCP-трафик (UDP не работает)
- ⚠️ Не работают:
  - Голосовые и видеозвонки (Telegram, WhatsApp, Discord)
  - Онлайн-игры (требуют UDP)
  - Стриминг в реальном времени
- ✅ Работает:
  - Браузинг (HTTP/HTTPS)
  - Текстовые сообщения
  - Email
  - SSH, FTP, другие TCP-приложения

**Как использовать:**
1. Скачайте Tor Browser (Windows/macOS/Linux) или Orbot (Android), Invizible Pro (Android/iOS)
2. Добавьте мосты из нашего репозитория
3. Подключитесь к сети Tor

</details>

### Сравнительная таблица подписок

| Параметр | Черные списки ⚫ | Белые списки ⚪ | Tor Bridges 🧅 |
|----------|-----------------|-----------------|---------------|
| **Скорость** | ⚡⚡⚡⚡⚡ | ⚡⚡⚡ | ⚡⚡ |
| **Задержка** | 50-150 ms | 100-300 ms | 200-500 ms |
| **Устойчивость** | 🛡️🛡️🛡️ | 🛡️🛡️🛡️🛡️ | 🛡️🛡️🛡️🛡️🛡️ |
| **UDP поддержка** | ✅ | ✅ | ❌ |
| **Игры** | ✅ Отлично | ⚠️ Средне | ❌ Не работает |
| **YouTube 4K** | ✅ | ⚠️ 1080p | ❌ 480p |
| **Звонки** | ✅ | ⚠️ | ❌ |
| **Анонимность** | 🟡 Средняя | 🟡 Средняя | 🟢 Высокая |
| **Где работает** | Кабель, Wi-Fi | Мобильные сети | Везде (с ограничениями) |

---

## 📥 Все подписки (полный список)

### Черные списки (полный список)

<details>
<summary><b>⚫ VLESS для телефона (150 конфигов)</b></summary>

**📄 Файл:** [`blacklists/VLESS_mobile.txt`](blacklists/VLESS_mobile.txt)

**🔗 RAW ссылка:** `https://raw.githubusercontent.com/HenonBank/XRAY-config/main/blacklists/VLESS_mobile.txt`

**📱 QR-код:** [Скачать PNG](blacklists/qr/VLESS_mobile.png)

**📊 Характеристики:**
- Количество: ~150 конфигов
- Протокол: VLESS+REALITY
- Транспорт: XHTTP, GRPC, WS
- Размер: ~50 KB
- Оптимально для: Android, iOS

**✨ Особенности:**
- 🚀 Только самые быстрые конфиги
- 📱 Оптимизировано для телефонов
- 🔄 Автообновление
- 💾 Легкий вес

**⚙️ Технические детали:**
- Отбор по скорости (>50 Mbps)
- Отбор по задержке (<150 ms)
- REALITY fingerprint: Chrome
- SNI: Общие домены (www.google.com, www.cloudflare.com)

</details>

<details>
<summary><b>⚫ VLESS полная (все конфиги)</b></summary>

**📄 Файл:** [`blacklists/VLESS_full.txt`](blacklists/VLESS_full.txt)

**🔗 RAW ссылка:** `https://raw.githubusercontent.com/HenonBank/XRAY-config/main/blacklists/VLESS_full.txt`

**📱 QR-код:** [Скачать PNG](blacklists/qr/VLESS_full.png)

**📊 Характеристики:**
- Количество: до 2000 конфигов
- Протокол: VLESS+REALITY, VLESS+XTLS
- Транспорт: XHTTP, GRPC, WS, TCP
- Размер: ~500 KB
- Оптимально для: Windows, macOS, Linux

**✨ Особенности:**
- 🌍 Максимальный выбор
- 💻 Для мощных устройств
- 🎯 Все доступные сервера
- ⚠️ Не рекомендуется для телефонов

</details>

<details>
<summary><b>⚫ ALL protocols (Shadowsocks, Hysteria2, Trojan, VMess)</b></summary>

**📄 Файл:** [`blacklists/ALL_protocols.txt`](blacklists/ALL_protocols.txt)

**🔗 RAW ссылка:** `https://raw.githubusercontent.com/HenonBank/XRAY-config/main/blacklists/ALL_protocols.txt`

**📱 QR-код:** [Скачать PNG](blacklists/qr/ALL_protocols.png)

**📊 Характеристики:**
- Количество: 500+ конфигов
- Протоколы: Shadowsocks, Hysteria2, Trojan, VMess
- Шифрование: AEAD, TLS, None
- Размер: ~200 KB

**✨ Особенности:**
- 🔄 Альтернатива VLESS
- 🚀 Hysteria2 для мобильных сетей
- 🔒 Shadowsocks для легкого трафика
- 🎯 Разные варианты обхода

**📋 Содержимое:**
```

· Shadowsocks 2022-blake3-aes-128-gcm (100+)
· Hysteria2 с маскировкой (100+)
· Trojan с REALITY (150+)
· VMess с WebSocket (150+)

```

</details>

---

### Белые списки (полный список)

<details>
<summary><b>⚪ CIDR для телефона №1 (150 конфигов)</b></summary>

**📄 Файл:** [`whitelists/CIDR_mobile_1.txt`](whitelists/CIDR_mobile_1.txt)

**🔗 RAW ссылка:** `https://raw.githubusercontent.com/HenonBank/XRAY-config/main/whitelists/CIDR_mobile_1.txt`

**📱 QR-код:** [Скачать PNG](whitelists/qr/CIDR_mobile_1.png)

**📊 Характеристики:**
- Количество: 150 конфигов
- Протокол: VLESS+REALITY
- CIDR подсети: Яндекс, VK, Mail.ru
- Размер: ~40 KB

**✨ Особенности:**
- 📱 Первые 150 CIDR-конфигов
- 🛡️ Обход CIDR-блокировок
- 🇷🇺 Белые подсети РФ
- 🚀 Оптимизирован для телефонов

**📋 Белые подсети:**
- Yandex: 77.88.0.0/18, 5.255.0.0/16, 87.250.0.0/16
- VK: 87.240.128.0/18, 95.213.0.0/16
- Mail.ru: 94.100.0.0/15

</details>

<details>
<summary><b>⚪ CIDR для телефона №2 (150 конфигов)</b></summary>

**📄 Файл:** [`whitelists/CIDR_mobile_2.txt`](whitelists/CIDR_mobile_2.txt)

**🔗 RAW ссылка:** `https://raw.githubusercontent.com/HenonBank/XRAY-config/main/whitelists/CIDR_mobile_2.txt`

**📱 QR-код:** [Скачать PNG](whitelists/qr/CIDR_mobile_2.png)

**📊 Характеристики:**
- Количество: 150 конфигов
- Протокол: VLESS+REALITY
- CIDR подсети: CDNvideo, Beeline, Rambler
- Размер: ~40 KB

**📋 Белые подсети:**
- CDNvideo: 80.82.64.0/20, 185.158.248.0/22
- Beeline: 85.21.0.0/16, 194.186.0.0/16
- Rambler: 81.19.64.0/19

</details>

<details>
<summary><b>⚪ CIDR полная (все конфиги)</b></summary>

**📄 Файл:** [`whitelists/CIDR_full.txt`](whitelists/CIDR_full.txt)

**🔗 RAW ссылка:** `https://raw.githubusercontent.com/HenonBank/XRAY-config/main/whitelists/CIDR_full.txt`

**📱 QR-код:** [Скачать PNG](whitelists/qr/CIDR_full.png)

**📊 Характеристики:**
- Количество: 1000+ конфигов
- Протокол: VLESS+REALITY, VLESS+TLS
- CIDR подсети: Все российские хостинги
- Размер: ~300 KB

**✨ Особенности:**
- 🌍 Полный охват белых подсетей
- 💻 Для ПК и мощных устройств
- 🛡️ Максимальная защита

</details>

<details>
<summary><b>⚪ CIDR проверенные (VK, Yandex, CDNvideo, Beeline)</b></summary>

**📄 Файл:** [`whitelists/CIDR_checked.txt`](whitelists/CIDR_checked.txt)

**🔗 RAW ссылка:** `https://raw.githubusercontent.com/HenonBank/XRAY-config/main/whitelists/CIDR_checked.txt`

**📊 Характеристики:**
- Количество: 300+ конфигов
- Протокол: VLESS+REALITY
- CIDR подсети: Только проверенные хостеры
- Размер: ~100 KB

**✨ Особенности:**
- 🎯 Только стабильные подсети
- 🔒 Минимальный риск блокировки
- 🚀 Высокая скорость

</details>

<details>
<summary><b>⚪ SNI полная (обход по доменам)</b></summary>

**📄 Файл:** [`whitelists/SNI_full.txt`](whitelists/SNI_full.txt)

**🔗 RAW ссылка:** `https://raw.githubusercontent.com/HenonBank/XRAY-config/main/whitelists/SNI_full.txt`

**📊 Характеристики:**
- Количество: 200+ конфигов
- Протокол: VLESS+REALITY
- SNI домены: yandex.ru, vk.com, mail.ru, ok.ru
- Размер: ~60 KB

**✨ Особенности:**
- 🔒 Обход SNI-блокировок
- 🌐 Легкий и быстрый
- 📡 Альтернатива CIDR

**📋 SNI домены:**
- yandex.ru, yandex.ua, yandex.by
- vk.com, vk.ru
- mail.ru, ok.ru
- rambler.ru, lenta.ru

</details>

---

### Tor Bridges (полный список)

<details>
<summary><b>🧅 Tor Bridges TOP-100</b></summary>

**📄 Файл:** [`tor_bridges/bridges_top100.txt`](tor_bridges/bridges_top100.txt)

**🔗 RAW ссылка:** `https://raw.githubusercontent.com/HenonBank/XRAY-config/main/tor_bridges/bridges_top100.txt`

**📊 Характеристики:**
- Количество: 100 мостов
- Типы: obfs4, webtunnel
- Размер: ~10 KB

**✨ Особенности:**
- 🏆 100 лучших мостов
- 🚀 Высокая скорость для Tor
- 🔄 Автоматическое обновление

</details>

<details>
<summary><b>🧅 Tor Bridges полная (все мосты)</b></summary>

**📄 Файл:** [`tor_bridges/bridges_all.txt`](tor_bridges/bridges_all.txt)

**🔗 RAW ссылка:** `https://raw.githubusercontent.com/HenonBank/XRAY-config/main/tor_bridges/bridges_all.txt`

**📊 Характеристики:**
- Количество: 500+ мостов
- Типы: obfs4, webtunnel, vanilla
- Размер: ~50 KB

</details>

<details>
<summary><b>🧅 Tor Bridges obfs4</b></summary>

**📄 Файл:** [`tor_bridges/bridges_obfs4.txt`](tor_bridges/bridges_obfs4.txt)

**🔗 RAW ссылка:** `https://raw.githubusercontent.com/HenonBank/XRAY-config/main/tor_bridges/bridges_obfs4.txt`

**📊 Характеристики:**
- Количество: 200+ мостов
- Тип: obfs4 (обфускация)
- Размер: ~20 KB

</details>

<details>
<summary><b>🧅 Tor Bridges webtunnel</b></summary>

**📄 Файл:** [`tor_bridges/bridges_webtunnel.txt`](tor_bridges/bridges_webtunnel.txt)

**🔗 RAW ссылка:** `https://raw.githubusercontent.com/HenonBank/XRAY-config/main/tor_bridges/bridges_webtunnel.txt`

**📊 Характеристики:**
- Количество: 200+ мостов
- Тип: webtunnel (WebSocket)
- Размер: ~20 KB

</details>

---

## 🚀 Быстрый старт (пошаговая инструкция)

### Шаг 1: Выбор клиента (подробная таблица)

<details>
<summary><b>💻 Клиенты для Windows</b></summary>

| Клиент | Ссылка | Версия | Особенности | Сложность |
|--------|--------|--------|-------------|-----------|
| **v2rayN** | [GitHub](https://github.com/2dust/v2rayN/releases) | 6.33+ | Универсальный, все протоколы, TUN режим | ⭐⭐ |
| **Karing** | [GitHub](https://github.com/KaringX/karing/releases) | 1.2.10+ | Простой, красивый, работает на всех платформах | ⭐ |
| **Throne** | [GitHub](https://github.com/throneproj/Throne/releases) | 1.0.8+ | Легкий, быстрый, преемник Nekoray | ⭐⭐ |
| **Nekoray** | [GitHub](https://github.com/MatsuriDayo/nekoray/releases) | 3.26+ | Устаревший, не рекомендуется | ⭐⭐ |

**Рекомендация:** Начните с Karing (проще всего), затем переходите на v2rayN (больше возможностей).

</details>

<details>
<summary><b>🍎 Клиенты для macOS</b></summary>

| Клиент | Ссылка | Версия | Особенности | Сложность |
|--------|--------|--------|-------------|-----------|
| **Karing** | [GitHub](https://github.com/KaringX/karing/releases) | 1.2.10+ | Универсальный, работает на Apple Silicon | ⭐ |
| **Throne** | [GitHub](https://github.com/throneproj/Throne/releases) | 1.0.8+ | Легкий, быстрый | ⭐⭐ |
| **v2rayN** | [GitHub](https://github.com/2dust/v2rayN/releases) | 6.33+ | Полная версия для macOS | ⭐⭐ |

**Для Apple Silicon (M1/M2/M3):** Используйте Karing — отлично работает.

</details>

<details>
<summary><b>🐧 Клиенты для Linux</b></summary>

| Клиент | Ссылка | Установка | Особенности |
|--------|--------|-----------|-------------|
| **Karing** | [GitHub](https://github.com/KaringX/karing/releases) | .deb, AppImage | Простой, работает на всех дистрибутивах |
| **Throne** | [GitHub](https://github.com/throneproj/Throne/releases) | .deb, AppImage | Легкий, быстрый |
| **v2rayA** | [GitHub](https://github.com/v2rayA/v2rayA) | Snap, Docker | Web-интерфейс, удобно |

**Для Ubuntu/Debian:** Karing (.deb) — лучший выбор.

</details>

<details>
<summary><b>📱 Клиенты для Android</b></summary>

| Клиент | Ссылка | Версия | Особенности | Сложность |
|--------|--------|--------|-------------|-----------|
| **v2rayNG** | [GitHub](https://github.com/2dust/v2rayNG/releases) | 1.8.20+ | Лучший для Android, все функции | ⭐⭐ |
| **NekoBox** | [GitHub](https://github.com/MatsuriDayo/NekoBoxForAndroid/releases) | 1.2.0+ | Красивый интерфейс | ⭐⭐ |
| **Karing** | [GitHub](https://github.com/KaringX/karing/releases) | 1.2.10+ | Универсальный | ⭐ |

**Рекомендация:** v2rayNG — самый функциональный.

</details>

<details>
<summary><b>📱 Клиенты для iOS</b></summary>

| Клиент | Ссылка | Цена | Особенности |
|--------|--------|------|-------------|
| **Streisand** | [App Store](https://apps.apple.com/app/streisand/id6450534064) | Бесплатно | Без сбора данных, все функции |
| **Karing** | [App Store](https://apps.apple.com/app/karing/id6472431552) | Бесплатно | Универсальный |
| **Shadowrocket** | [App Store](https://apps.apple.com/app/shadowrocket/id932747118) | Платно ($2.99) | Самый стабильный |
| **V2Box** | [App Store](https://apps.apple.com/app/v2box-v2ray-client/id6446814690) | Бесплатно | Альтернатива |

**Рекомендация:** Streisand (бесплатно, без рекламы).

</details>

### Шаг 2: Скачивание и установка (подробно)

<details>
<summary><b>📥 Пошаговая инструкция для v2rayN (Windows)</b></summary>

1. **Скачивание:**
   - Перейдите на [страницу релизов](https://github.com/2dust/v2rayN/releases)
   - Скачайте `v2rayN-windows-64.zip` (для 64-битной Windows)
   - Или `v2rayN-windows-32.zip` (для 32-битной)

2. **Установка:**
   - Распакуйте архив в папку (например, `C:\v2rayN`)
   - Запустите `v2rayN.exe` (от имени администратора рекомендуется)

3. **Первая настройка:**
   - При первом запуске выберите язык (Русский)
   - В настройках выберите **«Режим TUN»** для системного прокси

</details>

<details>
<summary><b>📥 Пошаговая инструкция для v2rayNG (Android)</b></summary>

1. **Скачивание:**
   - Перейдите на [страницу релизов](https://github.com/2dust/v2rayNG/releases)
   - Скачайте `v2rayNG_1.8.20.apk`

2. **Установка:**
   - Откройте скачанный APK-файл
   - Разрешите установку из неизвестных источников
   - Нажмите **«Установить»**

3. **Разрешения:**
   - При первом запуске разрешите приложению создавать VPN-подключения

</details>

<details>
<summary><b>📥 Пошаговая инструкция для Streisand (iOS)</b></summary>

1. **Скачивание:**
   - Откройте App Store
   - Найдите **«Streisand»**
   - Нажмите **«Получить»** → **«Установить»**

2. **Настройка:**
   - При первом запуске разрешите уведомления (опционально)
   - При добавлении подписки разрешите доступ к VPN

</details>

### Шаг 3: Добавление подписки (подробно)

<details>
<summary><b>➕ v2rayN: как добавить подписку</b></summary>

**Способ 1: Через интерфейс**
1. Нажмите **«Группа подписки»** → **«Добавить группу подписки»**
2. В поле **«Адрес»** вставьте RAW-ссылку:
```

https://raw.githubusercontent.com/HenonBank/XRAY-config/main/blacklists/VLESS_mobile.txt

```
3. В поле **«Имя»** введите название (например, "XRAY Blacklists")
4. Нажмите **«Добавить»**
5. Нажмите правой кнопкой на группу → **«Обновить текущую подписку»**

**Способ 2: Импорт из буфера**
1. Скопируйте RAW-ссылку
2. Нажмите **«Группа подписки»** → **«Импортировать подписку из буфера обмена»**

**Способ 3: Импорт из файла**
1. Скачайте файл конфигурации
2. Нажмите **«Группа подписки»** → **«Импортировать подписку из файла»**

</details>

<details>
<summary><b>➕ v2rayNG: как добавить подписку</b></summary>

1. Откройте приложение
2. Нажмите на иконку **«+»** в правом верхнем углу
3. Выберите **«Добавить подписку»**
4. Вставьте RAW-ссылку
5. Нажмите **«ОК»**
6. Нажмите на иконку обновления (круговая стрелка) для загрузки конфигов

</details>

<details>
<summary><b>➕ Streisand: как добавить подписку</b></summary>

1. Откройте приложение
2. Нажмите на иконку **«+»** в правом верхнем углу
3. Выберите **«Подписка»**
4. Вставьте RAW-ссылку
5. Нажмите **«Готово»**
6. Потяните вниз для обновления

</details>

<details>
<summary><b>➕ Karing: как добавить подписку</b></summary>

1. Откройте Karing
2. Нажмите **«Профили»** → **«Новый профиль»**
3. Выберите **«Подписка»**
4. Вставьте RAW-ссылку
5. Нажмите **«Сохранить»**
6. Нажмите на иконку обновления

</details>

### Шаг 4: Тестирование конфигураций

<details>
<summary><b>🔍 Как правильно тестировать</b></summary>

**Важно:** Используйте **«Реальную задержку»** (Real ping), а не TCP/ICMP ping!

**Почему это важно:**
- **TCP ping** — проверяет только TCP-соединение, не показывает реальную скорость
- **ICMP ping** — проверяет только ICMP, может быть разрешен даже если VPN не работает
- **Real ping** — проверяет реальное VPN-соединение с установлением шифрования

**Как тестировать в разных клиентах:**

| Клиент | Действие |
|--------|----------|
| **v2rayN** | Выделить все → иконка молнии → «Проверить реальную задержку» |
| **v2rayNG** | Три точки → «Проверить реальную задержку» |
| **Streisand** | Выбрать подписку → иконка «Тест задержки» |
| **Karing** | Выбрать подписку → иконка молнии |

**Интерпретация результатов:**
- 🟢 **Зеленый (50-150 ms)** — отлично, можно использовать
- 🟡 **Желтый (150-300 ms)** — хорошо, но возможны задержки
- 🔴 **Красный (>300 ms или ошибка)** — не использовать

</details>

### Шаг 5: Подключение и проверка

<details>
<summary><b>🔌 Как подключиться</b></summary>

**v2rayN:**
1. Выберите конфиг с наименьшей задержкой
2. Нажмите **Enter**
3. В системном трее нажмите правой кнопкой на иконку v2rayN
4. Выберите **«Режим VPN»** → **«Режим TUN»**

**v2rayNG:**
1. Выберите конфиг с наименьшей задержкой
2. Нажмите на иконку **«Стрелка»** рядом с конфигом
3. Нажмите на кнопку **«VPN»** внизу экрана
4. Разрешите создание VPN-подключения

**Streisand:**
1. Выберите конфиг с наименьшей задержкой
2. Нажмите на переключатель рядом с конфигом
3. Разрешите создание VPN-подключения

**Проверка подключения:**
1. Откройте [2ip.ru](https://2ip.ru) — IP должен измениться
2. Откройте [youtube.com](https://youtube.com) — должен открываться
3. Проверьте скорость на [speedtest.net](https://speedtest.net)

</details>

---

## 🧩 Клиенты (полные инструкции)

### Windows клиенты (полные инструкции)

<details>
<summary><b>📌 v2rayN — полная инструкция</b></summary>

**Установка:**
1. Скачайте последнюю версию с [GitHub](https://github.com/2dust/v2rayN/releases)
2. Распакуйте архив в `C:\v2rayN`
3. Запустите `v2rayN.exe` от имени администратора

**Настройка режима TUN (рекомендуется):**
1. Нажмите **«Настройки»** → **«Настройки параметров»**
2. В разделе **«Ядро»** выберите **«Режим TUN»**
3. В разделе **«TUN»** выберите **«Разрешить всем приложениям»**
4. Нажмите **«Сохранить»**

**Добавление подписки:**
1. Нажмите **«Группа подписки»** → **«Добавить группу подписки»**
2. Введите:
   - **Адрес:** `https://raw.githubusercontent.com/HenonBank/XRAY-config/main/blacklists/VLESS_mobile.txt`
   - **Имя:** `XRAY Blacklists`
3. Нажмите **«Добавить»**
4. Правой кнопкой на группу → **«Обновить текущую подписку»**

**Тестирование:**
1. Выделите все конфиги (Ctrl+A)
2. Нажмите на иконку молнии (⚡)
3. Выберите **«Проверить реальную задержку»**
4. Дождитесь окончания (1-2 минуты)
5. Отсортируйте по столбцу **«Задержка»**

**Подключение:**
1. Выберите конфиг с наименьшей задержкой
2. Нажмите **Enter**
3. В системном трее нажмите на иконку v2rayN
4. Выберите **«Режим VPN»** → **«Режим TUN»**

**Настройка автообновления:**
1. Правой кнопкой на группу подписки
2. Выберите **«Настройки группы подписки»**
3. Включите **«Автообновление»**
4. Установите интервал (рекомендуется 6 часов)

**Полезные горячие клавиши:**
- `Ctrl+A` — выделить все
- `Enter` — активировать выбранный конфиг
- `F5` — обновить подписку
- `F2` — переименовать
- `Delete` — удалить

</details>

<details>
<summary><b>📌 Karing — полная инструкция</b></summary>

**Установка:**
1. Скачайте последнюю версию с [GitHub](https://github.com/KaringX/karing/releases)
2. Запустите установщик и следуйте инструкциям
3. После установки запустите Karing

**Добавление подписки:**
1. Нажмите **«Профили»** в левом меню
2. Нажмите **«Новый профиль»** (или + в правом нижнем углу)
3. Выберите **«Подписка»**
4. В поле URL вставьте RAW-ссылку
5. Нажмите **«Сохранить»**
6. Нажмите на иконку обновления (круговая стрелка)

**Тестирование:**
1. Выберите добавленную подписку
2. Нажмите на иконку молнии (⚡)
3. Дождитесь окончания проверки
4. Выберите конфиг с наименьшим пингом

**Подключение:**
1. Выберите конфиг
2. Нажмите **«Подключиться»**
3. При первом подключении разрешите создание VPN-туннеля

**Настройка автообновления:**
1. Нажмите на шестеренку (настройки)
2. Выберите **«Подписки»**
3. Включите **«Автоматическое обновление»**
4. Установите интервал (рекомендуется 6 часов)

</details>

---

### Android клиенты (полные инструкции)

<details>
<summary><b>📌 v2rayNG — полная инструкция</b></summary>

**Установка:**
1. Скачайте последний APK с [GitHub](https://github.com/2dust/v2rayNG/releases)
2. Откройте скачанный файл
3. Разрешите установку из неизвестных источников
4. Нажмите **«Установить»**

**Добавление подписки:**
1. Откройте v2rayNG
2. Нажмите на иконку **«+»** в правом верхнем углу
3. Выберите **«Добавить подписку»**
4. Вставьте RAW-ссылку в поле
5. Нажмите **«ОК»**
6. Нажмите на иконку обновления (круговая стрелка) в правом верхнем углу

**Тестирование:**
1. Нажмите на три точки (⋮) в правом верхнем углу
2. Выберите **«Проверка реальной задержки»**
3. Дождитесь окончания проверки (1-2 минуты)
4. Конфиги с наименьшим пингом будут отображаться сверху

**Подключение:**
1. Выберите конфиг с наименьшей задержкой
2. Нажмите на иконку **«Стрелка»** (▶) рядом с конфигом
3. Нажмите на кнопку **«VPN»** внизу экрана
4. В диалоговом окне нажмите **«ОК»** для создания VPN-подключения

**Настройка автообновления:**
1. Нажмите на три точки (⋮)
2. Выберите **«Настройки»**
3. Найдите **«Автообновление подписок»**
4. Включите и установите интервал (рекомендуется 6 часов)

**Дополнительные настройки:**
- **Режим разделения трафика:** Настройки → «Маршрут» → «Проксировать все»
- **DNS:** Настройки → «DNS» → выберите «Cloudflare (1.1.1.1)»
- **Уведомления:** Настройки → «Уведомления» → включите для контроля статуса

</details>

<details>
<summary><b>📌 NekoBox — полная инструкция</b></summary>

**Установка:**
1. Скачайте APK с [GitHub](https://github.com/MatsuriDayo/NekoBoxForAndroid/releases)
2. Установите как обычное приложение

**Добавление подписки:**
1. Нажмите на иконку **«+»** внизу
2. Выберите **«Подписка»**
3. Вставьте RAW-ссылку
4. Нажмите **«Сохранить»**
5. Нажмите на иконку обновления

**Тестирование:**
1. Выберите подписку
2. Нажмите на иконку **«Молния»**
3. Дождитесь результатов

**Подключение:**
1. Выберите конфиг
2. Нажмите на переключатель в правом верхнем углу

</details>

---

### iOS клиенты (полные инструкции)

<details>
<summary><b>📌 Streisand — полная инструкция</b></summary>

**Установка:**
1. Откройте App Store
2. Найдите **«Streisand»**
3. Нажмите **«Получить»** → **«Установить»**
4. После установки откройте приложение

**Добавление подписки:**
1. Нажмите на иконку **«+»** в правом верхнем углу
2. Выберите **«Подписка»**
3. Вставьте RAW-ссылку
4. Нажмите **«Готово»**
5. Потяните вниз для обновления

**Тестирование:**
1. Выберите добавленную подписку
2. Нажмите на иконку **«Тест задержки»** (молния)
3. Дождитесь окончания проверки
4. Конфиги с наименьшим пингом будут отображаться сверху

**Подключение:**
1. Выберите конфиг с наименьшей задержкой
2. Нажмите на переключатель рядом с конфигом
3. При первом подключении нажмите **«Разрешить»** для создания VPN

**Настройки:**
- **DNS:** Настройки → «DNS» → выберите «Cloudflare (1.1.1.1)»
- **Автообновление:** Настройки → «Автообновление» → включите
- **Уведомления:** Настройки → «Уведомления» → включите

**Особенности:**
- Streisand не собирает данные о пользователях
- Поддерживает все основные протоколы
- Есть встроенный тест скорости

</details>

<details>
<summary><b>📌 Karing (iOS) — полная инструкция</b></summary>

**Установка:**
1. Откройте App Store
2. Найдите **«Karing»**
3. Установите приложение

**Добавление подписки:**
1. Откройте Karing
2. Нажмите **«Профили»** внизу
3. Нажмите **«Новый профиль»**
4. Выберите **«Подписка»**
5. Вставьте RAW-ссылку
6. Нажмите **«Сохранить»**

**Тестирование:**
1. Выберите подписку
2. Нажмите на иконку молнии
3. Дождитесь результатов

**Подключение:**
1. Выберите конфиг с наименьшим пингом
2. Нажмите **«Подключиться»**
3. Разрешите создание VPN

</details>

---

## 🪞 Зеркала для доступа (полный список)

### Яндекс.Переводчик (подробно)

<details>
<summary><b>🌐 Как использовать Яндекс.Переводчик</b></summary>

**Важно:** Этот способ работает **только для ручного копирования** через браузер! Автообновление в клиентах не работает, так как Яндекс изменяет параметры конфигов.

**Формат ссылки:**
```

https://translate.yandex.ru/translate?url=ССЫЛКА_НА_ПОДПИСКУ&lang=de-de

```

**Готовые ссылки для всех подписок:**

**Черные списки:**
- VLESS mobile: `https://translate.yandex.ru/translate?url=https://raw.githubusercontent.com/HenonBank/XRAY-config/main/blacklists/VLESS_mobile.txt&lang=de-de`
- VLESS full: `https://translate.yandex.ru/translate?url=https://raw.githubusercontent.com/HenonBank/XRAY-config/main/blacklists/VLESS_full.txt&lang=de-de`
- ALL protocols: `https://translate.yandex.ru/translate?url=https://raw.githubusercontent.com/HenonBank/XRAY-config/main/blacklists/ALL_protocols.txt&lang=de-de`

**Белые списки:**
- CIDR mobile 1: `https://translate.yandex.ru/translate?url=https://raw.githubusercontent.com/HenonBank/XRAY-config/main/whitelists/CIDR_mobile_1.txt&lang=de-de`
- CIDR mobile 2: `https://translate.yandex.ru/translate?url=https://raw.githubusercontent.com/HenonBank/XRAY-config/main/whitelists/CIDR_mobile_2.txt&lang=de-de`
- CIDR full: `https://translate.yandex.ru/translate?url=https://raw.githubusercontent.com/HenonBank/XRAY-config/main/whitelists/CIDR_full.txt&lang=de-de`
- CIDR checked: `https://translate.yandex.ru/translate?url=https://raw.githubusercontent.com/HenonBank/XRAY-config/main/whitelists/CIDR_checked.txt&lang=de-de`
- SNI full: `https://translate.yandex.ru/translate?url=https://raw.githubusercontent.com/HenonBank/XRAY-config/main/whitelists/SNI_full.txt&lang=de-de`

**Tor Bridges:**
- Top 100: `https://translate.yandex.ru/translate?url=https://raw.githubusercontent.com/HenonBank/XRAY-config/main/tor_bridges/bridges_top100.txt&lang=de-de`
- All bridges: `https://translate.yandex.ru/translate?url=https://raw.githubusercontent.com/HenonBank/XRAY-config/main/tor_bridges/bridges_all.txt&lang=de-de`
- Obfs4: `https://translate.yandex.ru/translate?url=https://raw.githubusercontent.com/HenonBank/XRAY-config/main/tor_bridges/bridges_obfs4.txt&lang=de-de`
- Webtunnel: `https://translate.yandex.ru/translate?url=https://raw.githubusercontent.com/HenonBank/XRAY-config/main/tor_bridges/bridges_webtunnel.txt&lang=de-de`

**Инструкция:**
1. Откройте ссылку в браузере
2. Дождитесь загрузки страницы перевода
3. Скопируйте содержимое (Ctrl+A → Ctrl+C)
4. В клиенте добавьте конфиги из буфера обмена

</details>

### jsDelivr CDN (подробно)

<details>
<summary><b>🌐 Как использовать jsDelivr CDN</b></summary>

**Формат ссылки:**
```

https://cdn.jsdelivr.net/gh/HenonBank/XRAY-config@main/ПУТЬ_К_ФАЙЛУ

```

**Готовые ссылки:**

**Черные списки:**
- VLESS mobile: `https://cdn.jsdelivr.net/gh/HenonBank/XRAY-config@main/blacklists/VLESS_mobile.txt`
- VLESS full: `https://cdn.jsdelivr.net/gh/HenonBank/XRAY-config@main/blacklists/VLESS_full.txt`
- ALL protocols: `https://cdn.jsdelivr.net/gh/HenonBank/XRAY-config@main/blacklists/ALL_protocols.txt`

**Белые списки:**
- CIDR mobile 1: `https://cdn.jsdelivr.net/gh/HenonBank/XRAY-config@main/whitelists/CIDR_mobile_1.txt`
- CIDR mobile 2: `https://cdn.jsdelivr.net/gh/HenonBank/XRAY-config@main/whitelists/CIDR_mobile_2.txt`
- CIDR full: `https://cdn.jsdelivr.net/gh/HenonBank/XRAY-config@main/whitelists/CIDR_full.txt`

**Tor Bridges:**
- Top 100: `https://cdn.jsdelivr.net/gh/HenonBank/XRAY-config@main/tor_bridges/bridges_top100.txt`

**Особенности:**
- ✅ Поддерживает автообновление в клиентах
- ✅ Быстрая доставка через CDN
- ✅ Работает при блокировке GitHub

</details>

### Statically CDN (подробно)

<details>
<summary><b>🌐 Как использовать Statically CDN</b></summary>

**Формат ссылки:**
```

https://cdn.statically.io/gh/HenonBank/XRAY-config@main/ПУТЬ_К_ФАЙЛУ

```

**Готовые ссылки:**

**Черные списки:**
- VLESS mobile: `https://cdn.statically.io/gh/HenonBank/XRAY-config@main/blacklists/VLESS_mobile.txt`
- VLESS full: `https://cdn.statically.io/gh/HenonBank/XRAY-config@main/blacklists/VLESS_full.txt`

**Белые списки:**
- CIDR mobile 1: `https://cdn.statically.io/gh/HenonBank/XRAY-config@main/whitelists/CIDR_mobile_1.txt`

**Особенности:**
- ✅ Альтернатива jsDelivr
- ✅ Поддерживает автообновление
- ✅ Работает в РФ

</details>

### Githack (подробно)

<details>
<summary><b>🌐 Как использовать Githack</b></summary>

**Формат ссылки (Rawcdn — через Cloudflare):**
```

https://rawcdn.githack.com/HenonBank/XRAY-config/main/ПУТЬ_К_ФАЙЛУ

```

**Формат ссылки (Raw — напрямую):**
```

https://raw.githack.com/HenonBank/XRAY-config/main/ПУТЬ_К_ФАЙЛУ

```

**Готовые ссылки:**
- VLESS mobile (Rawcdn): `https://rawcdn.githack.com/HenonBank/XRAY-config/main/blacklists/VLESS_mobile.txt`
- VLESS mobile (Raw): `https://raw.githack.com/HenonBank/XRAY-config/main/blacklists/VLESS_mobile.txt`

**Особенности:**
- ✅ Работает через Cloudflare
- ✅ Поддерживает автообновление
- ✅ Хорошо работает при блокировках

</details>

### Другие зеркала

<details>
<summary><b>🌐 Дополнительные способы доступа</b></summary>

**GitHub Proxy:**
```

https://ghproxy.com/https://raw.githubusercontent.com/HenonBank/XRAY-config/main/blacklists/VLESS_mobile.txt

```

**GitMirror:**
```

https://raw.gitmirror.com/HenonBank/XRAY-config/main/blacklists/VLESS_mobile.txt

```

**Archive.org (архив):**
```

https://web.archive.org/web/https://raw.githubusercontent.com/HenonBank/XRAY-config/main/blacklists/VLESS_mobile.txt

```

**Telegram Bot (создайте свой):**
Можно создать Telegram бота, который будет выдавать актуальные ссылки.

</details>

---

## 🔧 Полезные советы (полное руководство)

### DNS-over-HTTPS (DoH) (полное руководство)

<details>
<summary><b>🔒 Что такое DoH и зачем он нужен</b></summary>

**Что такое DNS-over-HTTPS:**
DNS-over-HTTPS — это технология шифрования DNS-запросов. Вместо обычных незашифрованных DNS-запросов (которые видит провайдер), DoH отправляет запросы через HTTPS, как обычный веб-трафик.

**Преимущества DoH:**
- 🔒 Провайдер не видит, какие сайты вы открываете
- 🛡️ Защита от DNS-подмены и DNS-спуфинга
- 🚀 Иногда быстрее обычного DNS
- 🌍 Можно использовать публичные DNS (Cloudflare, Quad9)

**Недостатки DoH:**
- ⚠️ DNS-провайдер (Cloudflare, Google) видит ваши запросы
- ⚠️ Не скрывает IP-адреса сайтов
- ⚠️ Не заменяет VPN

**Как DoH помогает при блокировках:**
- Обходит DNS-блокировки (провайдер не видит запросы)
- Защищает от DNS-отравления
- Не помогает при IP-блокировках (нужен VPN)

</details>

<details>
<summary><b>📱 Настройка DoH на Android</b></summary>

**Способ 1: Через настройки системы (Android 9+)**
1. Перейдите в **Настройки** → **Сеть и интернет**
2. Нажмите **«Расширенные настройки»** → **«Персональный DNS»**
3. Выберите **«Имя хоста личного DNS-провайдера»**
4. Введите адрес:
   - **Cloudflare:** `cloudflare-dns.com`
   - **Quad9:** `dns.quad9.net`
   - **AdGuard:** `dns.adguard.com`
5. Нажмите **«Сохранить»**

**Способ 2: Через приложение**
1. Скачайте **«1.1.1.1 + WARP»** из Google Play
2. Установите и откройте
3. Нажмите на переключатель для включения
4. Выберите **«DNS-only»** (только DNS) или **«WARP»** (VPN)

</details>

<details>
<summary><b>💻 Настройка DoH на Windows</b></summary>

**Способ 1: Через настройки сети (Windows 11)**
1. Перейдите в **Параметры** → **Сеть и интернет**
2. Выберите ваше подключение (Wi-Fi или Ethernet)
3. Нажмите **«DNS-сервер»** → **«Редактировать»**
4. Выберите **«Вручную»**
5. Включите **«IPv4»**
6. Введите:
   - **Предпочитаемый DNS:** `1.1.1.1`
   - **Альтернативный DNS:** `1.0.0.1`
7. Включите **«Шифрование DNS»**
8. Выберите **«Только шифрованный»**

**Способ 2: Через командную строку**
```cmd
netsh dns add encryption server=1.1.1.1 dohtemplate=https://cloudflare-dns.com/dns-query
netsh dns add encryption server=1.0.0.1 dohtemplate=https://cloudflare-dns.com/dns-query
```

Способ 3: Через приложение

1. Скачайте «1.1.1.1» для Windows
2. Установите и запустите
3. Нажмите на переключатель для включения

</details>

<details>
<summary><b>🍎 Настройка DoH на macOS</b></summary>

1. Перейдите в Системные настройки → Сеть
2. Выберите ваше подключение (Wi-Fi или Ethernet)
3. Нажмите «Дополнительно»
4. Перейдите на вкладку «DNS»
5. Нажмите «+» и добавьте:
   · 1.1.1.1
   · 1.0.0.1
6. Нажмите «ОК» → «Применить»

Для шифрованного DNS:

1. Скачайте «1.1.1.1» из App Store
2. Установите и включите

</details>

<details>
<summary><b>📱 Настройка DoH на iOS</b></summary>

Способ 1: Через профиль конфигурации

1. Откройте Safari и перейдите на 1.1.1.1/ru/
2. Нажмите «Загрузить приложение»
3. Установите приложение «1.1.1.1: Faster Internet»
4. Откройте приложение и включите

Способ 2: Через приложение

1. Скачайте «1.1.1.1: Faster Internet» из App Store
2. Откройте приложение
3. Нажмите на переключатель для включения
4. Разрешите создание VPN-профиля

</details>

---

Рекомендуемые браузеры (полное руководство)

<details>
<summary><b>🔥 Mozilla Firefox — полная настройка</b></summary>

Почему Firefox:

· 🦊 Лучший среди массовых браузеров
· 🔒 Хорошая политика конфиденциальности
· 🚀 Быстрый и стабильный
· 🛡️ Встроенная защита от трекеров
· 🔧 Множество настроек приватности

Установка:

1. Перейдите на firefox.com
2. Скачайте и установите

Настройка приватности:

1. Откройте Настройки (три полоски → Настройки)
2. Перейдите в раздел «Приватность и защита»
3. В разделе «Усиленная защита от отслеживания» выберите «Строгий»
4. Включите «DNS-over-HTTPS»:
   · Поставьте галочку «Включить DNS-over-HTTPS»
   · Выберите провайдера (рекомендуется Cloudflare)
5. В разделе «Разрешения» отключите ненужные
6. В разделе «Данные сайтов» настройте очистку cookies при закрытии

Установка расширений:

1. uBlock Origin — блокировщик рекламы и трекеров
   · Перейдите в addons.mozilla.org
   · Найдите «uBlock Origin» и установите
2. Privacy Badger — дополнительная защита от трекеров
3. HTTPS Everywhere — принудительное HTTPS

</details>

<details>
<summary><b>🦊 LibreWolf — полная настройка</b></summary>

Почему LibreWolf:

· 🔒 Форк Firefox с акцентом на приватность
· 🛡️ Вырезана телеметрия Mozilla
· ⚙️ Оптимальные настройки из коробки
· 🔄 Автоматическое обновление
· 🚫 Без сбора данных

Установка:

1. Перейдите на librewolf.net
2. Скачайте версию для вашей ОС
3. Установите как обычное приложение

Особенности (из коробки):

· ✅ Встроенный uBlock Origin
· ✅ Отключена телеметрия
· ✅ Автоматическая очистка cookies при закрытии
· ✅ Защита от fingerprinting
· ✅ DoH включен по умолчанию
· ✅ Блокировка трекеров

Дополнительная настройка:

1. Откройте Настройки → Приватность и защита
2. Проверьте, что выбран «Строгий» режим защиты
3. При необходимости настройте исключения для отдельных сайтов

</details>

<details>
<summary><b>🔰 Ungoogled Chromium — полная настройка</b></summary>

Почему Ungoogled Chromium:

· 🔒 Chromium без телеметрии Google
· 🚀 Такая же скорость как у Chrome
· 🛡️ Полная приватность
· ⚙️ Открытый исходный код
· 📦 Можно использовать расширения из Chrome Web Store

Установка:

1. Перейдите на GitHub
2. Скачайте версию для вашей ОС
3. Распакуйте и запустите

Настройка:

1. Включите DoH:
   · Перейдите в Настройки → Конфиденциальность и безопасность
   · В разделе «Безопасность» включите «Использовать безопасный DNS»
   · Выберите провайдера (Cloudflare)
2. Установите расширения:
   · uBlock Origin (из Chrome Web Store)
   · Privacy Badger

</details>

---

Что видит провайдер (технические детали)

<details>
<summary><b>🔍 Полный анализ: без VPN</b></summary>

Что видит провайдер при обычном интернете:

Что видит Как видит Можно ли скрыть
IP-адрес сайта Всегда виден, это основа TCP/IP ❌ Только через VPN
SNI (домен) Виден в TLS-рукопожатии ⚠️ DoH не скрывает, VPN скрывает
DNS-запросы Видны в открытом виде ✅ DoH скрывает
Объем трафика Виден всегда ❌
Время подключения Видно всегда ❌
Протокол Виден (TCP/UDP) ⚠️ VPN маскирует
Содержимое Зашифровано HTTPS ❌ Не видит

Что НЕ видит провайдер:

· ❌ Содержимое веб-страниц
· ❌ Пароли и логины
· ❌ Сообщения в мессенджерах
· ❌ Что вы ищете в Google
· ❌ Видео, которое смотрите на YouTube

Технические детали:

```
Пользователь → [DNS запрос] → Провайдер (видит запрос)
Пользователь → [HTTPS запрос] → Провайдер (видит IP, SNI)
Пользователь → [Сайт] → Провайдер (видит зашифрованные пакеты)
```

</details>

<details>
<summary><b>🔒 Полный анализ: с VPN</b></summary>

Что видит провайдер при использовании VPN:

Что видит Детали
IP-адрес Только IP VPN-сервера
SNI Не видит (весь трафик зашифрован)
DNS-запросы Не видит (идут через VPN)
Объем трафика Видит, но не знает, что внутри
Время Видит время подключения
Протокол Видит VPN-протокол (может распознать)

Что НЕ видит провайдер:

· ❌ Какие сайты вы посещаете
· ❌ IP-адреса сайтов
· ❌ SNI
· ❌ Содержимое трафика
· ❌ DNS-запросы

Технические детали:

```
Пользователь → [Зашифрованный VPN трафик] → Провайдер (видит только VPN-сервер)
Провайдер → [Зашифрованный трафик] → VPN-сервер
VPN-сервер → [Открытый трафик] → Сайт
```

</details>

<details>
<summary><b>🛡️ Полный анализ: с DoH + VPN</b></summary>

Максимальная приватность:

Что видит провайдер Статус
IP-адрес Только IP VPN-сервера
SNI ❌ Не видит
DNS-запросы ❌ Не видит (зашифрованы DoH)
Объем трафика Видит, но не знает содержимое
Протокол Видит VPN-протокол

Дополнительная защита:

· DNS-запросы идут через DoH к Cloudflare/Quad9
· Провайдер не знает, какие сайты вы открываете
· Даже если VPN заблокируют, DoH продолжает работать

Технические детали:

```
Пользователь → [DoH запрос] → Провайдер (видит только IP DoH-сервера)
Пользователь → [VPN трафик] → Провайдер (видит только IP VPN-сервера)
Провайдер не может связать DNS-запросы и трафик
```

</details>

---

Оптимизация скорости

<details>
<summary><b>🚀 Как увеличить скорость VPN</b></summary>

1. Выбор ближайшего сервера:

· Тестируйте конфиги с наименьшей задержкой (Real ping)
· Выбирайте конфиги с указанием страны (RU, NL, DE)

2. Настройка MTU:

· В v2rayN: Настройки → «MTU» → установите 1400
· Это уменьшает фрагментацию пакетов

3. Отключение IPv6:

· В Windows: Свойства сети → отключить IPv6
· Некоторые VPN-серверы медленно работают через IPv6

4. Выбор протокола:

· Hysteria2 — самый быстрый для мобильных сетей
· VLESS+REALITY — оптимальный баланс скорости и защиты

5. DNS-сервер:

· Используйте Cloudflare (1.1.1.1) для максимальной скорости
· Избегайте медленных DNS-провайдеров

6. Закрытие фоновых приложений:

· Закройте торренты, обновления Windows
· Они потребляют трафик и снижают скорость

</details>

---

Безопасность

<details>
<summary><b>🛡️ Рекомендации по безопасности</b></summary>

1. Используйте проверенные клиенты:

· ✅ v2rayN, Karing, Streisand (официальные GitHub/App Store)
· ❌ Не скачивайте клиенты с подозрительных сайтов

2. Проверяйте подписи:

· На GitHub проверяйте, что репозиторий официальный
· Проверяйте цифровые подписи, если доступны

3. Не используйте публичные конфиги для чувствительных данных:

· Конфиги из этого репозитория — публичные
· Не вводите пароли от банков, пока не проверите скорость и надежность

4. Включайте DoH:

· Это дополнительный уровень защиты DNS-запросов

5. Обновляйте клиенты:

· Своевременно обновляйте v2rayN, v2rayNG, Streisand
· В новых версиях исправляют уязвимости

6. Используйте HTTPS везде:

· Даже с VPN используйте HTTPS для дополнительной защиты

7. Не отключайте антивирус:

· Некоторые антивирусы могут ложно срабатывать на VPN-клиенты
· Добавьте клиент в исключения, но не отключайте защиту

</details>

---

❓ Устранение проблем (FAQ)

Конфиги не работают

<details>
<summary><b>❓ Что делать, если конфиги не работают</b></summary>

Шаг 1: Проверьте интернет

· Откройте yandex.ru, vk.com, google.com
· Если не открываются — проблема с интернетом, а не с конфигами

Шаг 2: Обновите подписку

· В клиенте нажмите «Обновить подписку»
· Дождитесь окончания загрузки

Шаг 3: Проверьте Real ping

· Используйте «Реальную задержку», а не TCP/ICMP
· Конфиги с красным пингом — нерабочие

Шаг 4: Попробуйте другой протокол

· Если не работают VLESS, попробуйте Shadowsocks
· Переключитесь с черных списков на белые

Шаг 5: Перезапустите клиент

· Закройте клиент полностью
· Запустите заново

Шаг 6: Смените клиент

· Если не работает в v2rayN, попробуйте Karing
· Разные клиенты по-разному обрабатывают конфиги

Шаг 7: Проверьте системное время

· Некорректное время может вызывать ошибки TLS
· Синхронизируйте время через настройки

</details>

GitHub заблокирован

<details>
<summary><b>❓ Что делать, если GitHub заблокирован</b></summary>

Вариант 1: Используйте зеркала

· jsDelivr: https://cdn.jsdelivr.net/gh/HenonBank/XRAY-config@main/...
· Statically: https://cdn.statically.io/gh/HenonBank/XRAY-config@main/...
· Githack: https://rawcdn.githack.com/HenonBank/XRAY-config/main/...

Вариант 2: Яндекс.Переводчик (ручное копирование)

· Откройте ссылку через Яндекс.Переводчик
· Скопируйте конфиги вручную

Вариант 3: Используйте VPN для доступа к GitHub

· Иронично, но если GitHub заблокирован — используйте VPN
· Подключитесь через работающий конфиг

Вариант 4: Используйте Tor Browser

· Скачайте Tor Browser заранее
· Через Tor можно открыть GitHub

</details>

Низкая скорость

<details>
<summary><b>❓ Почему низкая скорость и как исправить</b></summary>

Причины низкой скорости:

Причина Решение
Далеко сервер Выберите конфиг с меньшей задержкой
Медленный протокол Используйте Hysteria2 или VLESS+REALITY
Загруженный сервер Смените конфиг
Проблемы с MTU Установите MTU=1400 в настройках
IPv6 включен Отключите IPv6
Фоновые приложения Закройте торренты, обновления
Wi-Fi помехи Переключитесь на кабель или 5GHz Wi-Fi

Оптимальные настройки для скорости:

1. Используйте Hysteria2 или VLESS+REALITY
2. Выбирайте сервера с задержкой <100 ms
3. Включите DoH (Cloudflare)
4. Установите MTU=1400
5. Отключите IPv6

</details>

Клиент тормозит

<details>
<summary><b>❓ Почему клиент тормозит на телефоне</b></summary>

Причина: Слишком много конфигов в подписке.

Решение:

· Используйте *_mobile.txt версии подписок
· В них не более 150 конфигов
· Это оптимально для телефонов

Рекомендуемые мобильные подписки:

· blacklists/VLESS_mobile.txt (150 конфигов)
· whitelists/CIDR_mobile_1.txt (150 конфигов)
· whitelists/CIDR_mobile_2.txt (150 конфигов)

Если все равно тормозит:

· Удалите неиспользуемые подписки
· Обновите клиент до последней версии
· Перезагрузите телефон

</details>

Ошибки подключения

<details>
<summary><b>❓ Распространенные ошибки и их решение</b></summary>

Ошибка: "All outbound proxies are failed" (v2rayN)

· Причина: конфиг не работает
· Решение: обновите подписку, выберите другой конфиг

Ошибка: "Failed to start tun2socks"

· Причина: проблемы с правами администратора
· Решение: запустите v2rayN от имени администратора

Ошибка: "TLS handshake failed"

· Причина: неверное системное время
· Решение: синхронизируйте время в настройках

Ошибка: "Context deadline exceeded"

· Причина: таймаут подключения
· Решение: выберите конфиг с меньшей задержкой

Ошибка: "Permission denied" (Android)

· Причина: не хватает прав для VPN
· Решение: в настройках разрешите приложению создавать VPN

Ошибка: "No such file or directory"

· Причина: повреждена установка клиента
· Решение: переустановите клиент

</details>