# 🛡️ XRAY-config | Бесплатные VPN-конфигурации для РФ

<div align="center">

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/HenonBank/XRAY-config)](https://github.com/HenonBank/XRAY-config/commits/main)
[![GitHub stars](https://img.shields.io/github/stars/HenonBank/XRAY-config)](https://github.com/HenonBank/XRAY-config/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/HenonBank/XRAY-config)](https://github.com/HenonBank/XRAY-config/issues)

**Актуальные, проверенные VPN-конфигурации для работы на территории Российской Федерации**  
Автоматическое тестирование • Разделение по типам блокировок • Регулярные обновления

[📖 Документация](#-содержание) • [🚀 Быстрый старт](#-быстрый-старт) • [💬 Поддержка](#-поддержка)

</div>

---

## 📋 Содержание

- [Для чего этот репозиторий](#-для-чего-этот-репозиторий)
- [Как выбрать подписку](#-как-выбрать-подписку)
  - [Черные списки ⚫](#-черные-списки-)
  - [Белые списки ⚪](#-белые-списки-)
  - [Tor Bridges 🧅](#-tor-bridges-)
- [Быстрый старт](#-быстрый-старт)
- [Клиенты](#-клиенты)
- [Зеркала для доступа](#-зеркала-для-доступа)
- [Полезные советы](#-полезные-советы)
- [Поддержать проект](#-поддержать-проект)
- [Лицензия](#-лицензия)

---

## 🎯 Для чего этот репозиторий

Здесь собраны **только рабочие конфигурации**, прошедшие проверку на сервере в России.  
Обновление происходит автоматически каждые 1-2 часа. Медленные и нерабочие конфиги удаляются.

| Тип | Для каких условий | Протоколы |
|-----|------------------|-----------|
| **Черные списки** ⚫ | Обычный интернет (кабель, Wi-Fi, мобильный без жестких ограничений) | VLESS, Shadowsocks, Hysteria2, Trojan, VMess |
| **Белые списки** ⚪ | Мобильный интернет с CIDR/SNI-блокировками (Мегафон, МТС, Билайн, Т2, Yota) | VLESS (CIDR/SNI) |
| **Tor Bridges** 🧅 | Альтернатива через сеть Tor (только TCP-трафик) | Bridges (obfs4, webtunnel) |

---

## 📥 Как выбрать подписку

### ⚫ Черные списки

Используйте, если открываются Google, YouTube, Telegram, но некоторые сайты заблокированы.

| Файл | Описание | Размер |
|------|----------|--------|
| [`blacklists/VLESS_mobile.txt`](blacklists/VLESS_mobile.txt) | 150 быстрых VLESS-конфигов для телефона | ~150 конфигов |
| [`blacklists/VLESS_full.txt`](blacklists/VLESS_full.txt) | Все VLESS-конфиги — для ПК | до 2000 конфигов |
| [`blacklists/ALL_protocols.txt`](blacklists/ALL_protocols.txt) | Shadowsocks, Hysteria2, Trojan, VMess | все доступные |

<details>
<summary><b>📱 QR-коды для быстрого импорта</b></summary>

| Подписка | QR-код |
|----------|--------|
| VLESS mobile | ![QR](blacklists/qr/VLESS_mobile.png) |
| VLESS full | ![QR](blacklists/qr/VLESS_full.png) |
| ALL protocols | ![QR](blacklists/qr/ALL_protocols.png) |

</details>

---

### ⚪ Белые списки

Если на мобильном интернете **не работают** иностранные сайты (кроме Яндекса, ВК, Госуслуг).

| Файл | Описание |
|------|----------|
| [`whitelists/CIDR_mobile_1.txt`](whitelists/CIDR_mobile_1.txt) | Первые 150 CIDR-конфигов для телефона |
| [`whitelists/CIDR_mobile_2.txt`](whitelists/CIDR_mobile_2.txt) | Вторые 150 CIDR-конфигов |
| [`whitelists/CIDR_full.txt`](whitelists/CIDR_full.txt) | Все CIDR-конфиги (обход по IP-диапазонам) |
| [`whitelists/CIDR_checked.txt`](whitelists/CIDR_checked.txt) | Только подсети VK, Yandex, CDNvideo, Beeline |
| [`whitelists/SNI_full.txt`](whitelists/SNI_full.txt) | Обход по SNI (доменным именам) |

<details>
<summary><b>📱 QR-коды для быстрого импорта</b></summary>

| Подписка | QR-код |
|----------|--------|
| CIDR mobile 1 | ![QR](whitelists/qr/CIDR_mobile_1.png) |
| CIDR mobile 2 | ![QR](whitelists/qr/CIDR_mobile_2.png) |
| CIDR full | ![QR](whitelists/qr/CIDR_full.png) |

</details>

---

### 🧅 Tor Bridges

Если VPN не помогает или нужна максимальная анонимность.

| Файл | Описание |
|------|----------|
| [`tor_bridges/bridges_top100.txt`](tor_bridges/bridges_top100.txt) | 100 лучших мостов |
| [`tor_bridges/bridges_all.txt`](tor_bridges/bridges_all.txt) | Полный список мостов |
| [`tor_bridges/bridges_obfs4.txt`](tor_bridges/bridges_obfs4.txt) | Мосты типа obfs4 |
| [`tor_bridges/bridges_webtunnel.txt`](tor_bridges/bridges_webtunnel.txt) | Мосты типа webtunnel |

<details>
<summary><b>📱 QR-коды для быстрого импорта</b></summary>

| Подписка | QR-код |
|----------|--------|
| Top 100 | ![QR](tor_bridges/qr/top100.png) |
| All bridges | ![QR](tor_bridges/qr/all.png) |

</details>

---

## 🚀 Быстрый старт

### 1️⃣ Скачайте клиент

| Платформа | Рекомендуемые клиенты |
|-----------|----------------------|
| **Windows** | [v2rayN](https://github.com/2dust/v2rayN), [Karing](https://github.com/KaringX/karing) |
| **macOS** | [Karing](https://github.com/KaringX/karing), [Throne](https://github.com/throneproj/Throne) |
| **Linux** | [Karing](https://github.com/KaringX/karing), [Throne](https://github.com/throneproj/Throne) |
| **Android** | [v2rayNG](https://github.com/2dust/v2rayNG), [NekoBox](https://github.com/MatsuriDayo/NekoBoxForAndroid) |
| **iOS** | [Streisand](https://apps.apple.com/app/streisand/id6450534064), [Karing](https://apps.apple.com/app/karing/id6472431552) |

### 2️⃣ Добавьте подписку

```bash
# Скопируйте RAW-ссылку на нужный файл
https://raw.githubusercontent.com/HenonBank/XRAY-config/main/blacklists/VLESS_mobile.txt
