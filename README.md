<div align="center">

# 🛡️ XRAY-config | Бесплатные VPN-конфигурации для РФ

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/HenonBank/XRAY-config)](https://github.com/HenonBank/XRAY-config/commits/main)
[![GitHub stars](https://img.shields.io/github/stars/HenonBank/XRAY-config)](https://github.com/HenonBank/XRAY-config/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/HenonBank/XRAY-config)](https://github.com/HenonBank/XRAY-config/network)
[![GitHub issues](https://img.shields.io/github/issues/HenonBank/XRAY-config)](https://github.com/HenonBank/XRAY-config/issues)
[![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

**Актуальные, проверенные VPN-конфигурации для работы на территории Российской Федерации**  
Автоматическое тестирование • Разделение по типам блокировок • Регулярные обновления • 100% рабочие конфиги

[📖 Документация](#-содержание) • [🚀 Быстрый старт](#-быстрый-старт) • [📥 Подписки](#-подписки) • [💬 Поддержка](#-поддержать-проект)

</div>

---

## 📋 Содержание

1. [Для чего этот репозиторий](#-для-чего-этот-репозиторий)
2. [Как выбрать подписку](#-как-выбрать-подписку)
   - [Черные списки ⚫](#-черные-списки)
   - [Белые списки ⚪](#-белые-списки)
   - [Tor Bridges 🧅](#-tor-bridges)
3. [Подписки](#-подписки)
   - [Черные списки](#черные-списки-подробно)
   - [Белые списки](#белые-списки-подробно)
   - [Tor Bridges](#tor-bridges-подробно)
4. [Быстрый старт](#-быстрый-старт)
5. [Клиенты](#-клиенты)
6. [Зеркала](#-зеркала-для-доступа)
7. [Полезные советы](#-полезные-советы)
8. [FAQ](#-faq)
9. [Поддержать проект](#-поддержать-проект)

---

## 🎯 Для чего этот репозиторий

Здесь собраны **только рабочие конфигурации**, прошедшие проверку на сервере в России. Обновление происходит автоматически каждые 1-2 часа. Медленные и нерабочие конфиги удаляются.

| Тип | Для каких условий | Протоколы |
|-----|------------------|-----------|
| **Черные списки** ⚫ | Обычный интернет (кабель, Wi-Fi, мобильный без жестких ограничений) | VLESS, Shadowsocks, Hysteria2, Trojan, VMess |
| **Белые списки** ⚪ | Мобильный интернет с CIDR/SNI-блокировками (Мегафон, МТС, Билайн, Т2, Yota) | VLESS (CIDR/SNI) |
| **Tor Bridges** 🧅 | Альтернатива через сеть Tor (только TCP-трафик) | Bridges (obfs4, webtunnel) |

---

## 📥 Как выбрать подписку

### ⚫ Черные списки

**Когда использовать:** Если у вас обычный интернет (кабель, Wi-Fi, мобильный без жестких ограничений). Открываются Google, YouTube, Telegram, но некоторые сайты заблокированы.

**Особенности:**
- 🚀 Максимальная скорость (до 500 Mbps)
- 🌍 Работает везде
- 📡 Подходит для всех типов подключения
- 🎮 Идеально для игр и стриминга
- 📱 Работает на всех устройствах

**Рекомендуемые протоколы:**
1. **VLESS+REALITY** — приоритет №1, максимальная защита от DPI
2. **Hysteria2** — отлично для мобильных сетей, высокая скорость
3. **Shadowsocks** — легкий и быстрый, работает везде
4. **Trojan** — хорошая альтернатива

### ⚪ Белые списки

**Когда использовать:** Если у вас мобильный интернет и **не работают** иностранные сайты (кроме Яндекса, ВК, Госуслуг). Актуально для Мегафон, МТС, Билайн, Т2, Yota.

**Особенности:**
- 🛡️ Обходит CIDR-блокировки по IP
- 🔒 Обходит SNI-блокировки по доменам
- 📱 Оптимизирован для мобильных сетей
- 🇷🇺 Использует белые подсети РФ
- 🔄 Автоматическое обновление

**Типы белых списков:**
- **CIDR** — обход блокировок по IP-диапазонам (работает у 100% операторов)
- **SNI** — обход по доменным именам (работает редко, но быстрее)

### 🧅 Tor Bridges

**Когда использовать:** Если VPN не помогает или нужна максимальная анонимность. Подходит для обхода самых жестких блокировок.

**Особенности:**
- 🧅 Анонимность через сеть Tor
- 🔄 Работает через мосты (obfs4, webtunnel)
- 📡 Альтернативный способ доступа
- 🛡️ Максимальная защита от DPI

**Ограничения:**
- ⚠️ Только TCP-трафик (UDP не работает)
- ⚠️ Не работают: голосовые/видеозвонки, онлайн-игры, стриминг
- ✅ Работает: браузинг, текстовые сообщения, email, SSH, FTP

---

## 📥 Подписки

### Черные списки (подробно)

<details>
<summary><b>⚫ VLESS для телефона (150 конфигов)</b></summary>

**📄 Файл:** [`blacklists/VLESS_mobile.txt`](blacklists/VLESS_mobile.txt)

**🔗 RAW ссылка:** `https://raw.githubusercontent.com/HenonBank/XRAY-config/main/blacklists/VLESS_mobile.txt`

**📊 Характеристики:**
- Количество: ~150 конфигов
- Протокол: VLESS+REALITY, VLESS+XTLS
- Транспорт: XHTTP, GRPC, WS
- Размер: ~50 KB
- Оптимально для: Android, iOS

**✨ Особенности:**
- 🚀 Только самые быстрые конфиги (скорость >50 Mbps)
- 📱 Оптимизировано для телефонов
- 🔄 Автообновление каждые 1-2 часа
- 💾 Легкий вес, быстро загружается

</details>

<details>
<summary><b>⚫ VLESS полная (все конфиги)</b></summary>

**📄 Файл:** [`blacklists/VLESS_full.txt`](blacklists/VLESS_full.txt)

**🔗 RAW ссылка:** `https://raw.githubusercontent.com/HenonBank/XRAY-config/main/blacklists/VLESS_full.txt`

**📊 Характеристики:**
- Количество: до 2000 конфигов
- Протокол: VLESS+REALITY, VLESS+XTLS, VLESS+TLS
- Транспорт: XHTTP, GRPC, WS, TCP
- Размер: ~500 KB
- Оптимально для: Windows, macOS, Linux

**✨ Особенности:**
- 🌍 Максимальный выбор серверов
- 💻 Для мощных устройств
- 🎯 Все доступные конфигурации
- ⚠️ Не рекомендуется для телефонов

</details>

<details>
<summary><b>⚫ ALL protocols (Shadowsocks, Hysteria2, Trojan, VMess)</b></summary>

**📄 Файл:** [`blacklists/ALL_protocols.txt`](blacklists/ALL_protocols.txt)

**🔗 RAW ссылка:** `https://raw.githubusercontent.com/HenonBank/XRAY-config/main/blacklists/ALL_protocols.txt`

**📊 Характеристики:**
- Количество: 500+ конфигов
- Протоколы: Shadowsocks, Hysteria2, Trojan, VMess
- Шифрование: AEAD, TLS, None
- Размер: ~200 KB

**✨ Особенности:**
- 🔄 Альтернатива VLESS
- 🚀 Hysteria2 оптимизирован для мобильных сетей
- 🔒 Shadowsocks для легкого трафика
- 🎯 Разные варианты обхода DPI

</details>

---

### Белые списки (подробно)

<details>
<summary><b>⚪ CIDR для телефона №1 (150 конфигов)</b></summary>

**📄 Файл:** [`whitelists/CIDR_mobile_1.txt`](whitelists/CIDR_mobile_1.txt)

**🔗 RAW ссылка:** `https://raw.githubusercontent.com/HenonBank/XRAY-config/main/whitelists/CIDR_mobile_1.txt`

**📊 Характеристики:**
- Количество: 150 конфигов
- Протокол: VLESS+REALITY
- CIDR подсети: Яндекс, VK, Mail.ru
- Размер: ~40 KB

**📋 Белые подсети:**
- Yandex: 77.88.0.0/18, 5.255.0.0/16, 87.250.0.0/16
- VK: 87.240.128.0/18, 95.213.0.0/16
- Mail.ru: 94.100.0.0/15

</details>

<details>
<summary><b>⚪ CIDR для телефона №2 (150 конфигов)</b></summary>

**📄 Файл:** [`whitelists/CIDR_mobile_2.txt`](whitelists/CIDR_mobile_2.txt)

**🔗 RAW ссылка:** `https://raw.githubusercontent.com/HenonBank/XRAY-config/main/whitelists/CIDR_mobile_2.txt`

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

**📊 Характеристики:**
- Количество: 1000+ конфигов
- Протокол: VLESS+REALITY, VLESS+TLS
- CIDR подсети: Все российские хостинги
- Размер: ~300 KB

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

</details>

---

### Tor Bridges (подробно)

<details>
<summary><b>🧅 Tor Bridges TOP-100</b></summary>

**📄 Файл:** [`tor_bridges/bridges_top100.txt`](tor_bridges/bridges_top100.txt)

**🔗 RAW ссылка:** `https://raw.githubusercontent.com/HenonBank/XRAY-config/main/tor_bridges/bridges_top100.txt`

**📊 Характеристики:**
- Количество: 100 мостов
- Типы: obfs4, webtunnel
- Размер: ~10 KB

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
- Тип: obfs4 (обфускация трафика)
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

## 🚀 Быстрый старт

### Шаг 1: Выбор клиента

| Платформа | Рекомендуемые клиенты | Ссылка |
|-----------|----------------------|--------|
| **Windows** | v2rayN, Karing | [v2rayN](https://github.com/2dust/v2rayN/releases) / [Karing](https://github.com/KaringX/karing/releases) |
| **macOS** | Karing, Throne | [Karing](https://github.com/KaringX/karing/releases) / [Throne](https://github.com/throneproj/Throne/releases) |
| **Linux** | Karing, Throne | [Karing](https://github.com/KaringX/karing/releases) / [Throne](https://github.com/throneproj/Throne/releases) |
| **Android** | v2rayNG, NekoBox | [v2rayNG](https://github.com/2dust/v2rayNG/releases) / [NekoBox](https://github.com/MatsuriDayo/NekoBoxForAndroid/releases) |
| **iOS** | Streisand, Karing | [Streisand](https://apps.apple.com/app/streisand/id6450534064) / [Karing](https://apps.apple.com/app/karing/id6472431552) |

### Шаг 2: Добавление подписки

**RAW ссылки для копирования:**
