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
MAX_PING_MS = 2700  # МАКСИМАЛЬНЫЙ ПИНГ В МИЛЛИСЕКУНДАХ (2 секунд)

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

# ========= ПОЛНЫЙ СПИСОК ДОМЕНОВ =========
DOMAIN_NAMES = {
    # X5 Retail Group (Пятёрочка, Перекрёсток)
    'x5.ru': 'Пятёрочка',
    '5ka.ru': 'Пятёрочка',
    '5ka-cdn.ru': 'Пятёрочка',
    '5ka.static.ru': 'Пятёрочка',
    'ads.x5.ru': 'Пятёрочка',
    'perekrestok.ru': 'Перекрёсток',
    'vprok.ru': 'Перекрёсток',
    'dixy.ru': 'Дикси',
    
    # Fasssst и его поддомены
    'fasssst.ru': 'Fasssst',
    'rontgen.fasssst.ru': 'Fasssst',
    'res.fasssst.ru': 'Fasssst',
    'yt.fasssst.ru': 'Fasssst',
    'fast.strelkavpn.ru': 'StrelkaVPN',
    'strelkavpn.ru': 'StrelkaVPN',
    
    # Maviks - торговая компания
    'maviks.ru': 'Maviks',
    'ru.maviks.ru': 'Maviks',
    'a.ru.maviks.ru': 'Maviks',
    
    # Tree-top
    'tree-top.cc': 'TreeTop',
    'a.ru.tree-top.cc': 'TreeTop',
    
    # Connect-Iskra
    'connect-iskra.ru': 'Iskra',
    '212-wl.connect-iskra.ru': 'Iskra',
    
    # VK и связанные сервисы
    'vk.com': 'VK',
    'vk.ru': 'VK',
    'vkontakte.ru': 'VK',
    'userapi.com': 'VK',
    'cdn.vk.com': 'VK',
    'cdn.vk.ru': 'VK',
    'id.vk.com': 'VK',
    'id.vk.ru': 'VK',
    'login.vk.com': 'VK',
    'login.vk.ru': 'VK',
    'api.vk.com': 'VK',
    'api.vk.ru': 'VK',
    'im.vk.com': 'VK',
    'm.vk.com': 'VK',
    'm.vk.ru': 'VK',
    'sun6-22.userapi.com': 'VK',
    'sun6-21.userapi.com': 'VK',
    'sun6-20.userapi.com': 'VK',
    'sun9-38.userapi.com': 'VK',
    'sun9-101.userapi.com': 'VK',
    'pptest.userapi.com': 'VK',
    'vk-portal.net': 'VK',
    'stats.vk-portal.net': 'VK',
    'akashi.vk-portal.net': 'VK',
    'vkvideo.ru': 'VK Видео',
    'm.vkvideo.ru': 'VK Видео',
    'queuev4.vk.com': 'VK',
    'eh.vk.com': 'VK',
    'cloud.vk.com': 'VK',
    'cloud.vk.ru': 'VK',
    'admin.cs7777.vk.ru': 'VK',
    'admin.tau.vk.ru': 'VK',
    'analytics.vk.ru': 'VK',
    'api.cs7777.vk.ru': 'VK',
    'api.tau.vk.ru': 'VK',
    'away.cs7777.vk.ru': 'VK',
    'away.tau.vk.ru': 'VK',
    'business.vk.ru': 'VK',
    'connect.cs7777.vk.ru': 'VK',
    'cs7777.vk.ru': 'VK',
    'dev.cs7777.vk.ru': 'VK',
    'dev.tau.vk.ru': 'VK',
    'expert.vk.ru': 'VK',
    'id.cs7777.vk.ru': 'VK',
    'id.tau.vk.ru': 'VK',
    'login.cs7777.vk.ru': 'VK',
    'login.tau.vk.ru': 'VK',
    'm.cs7777.vk.ru': 'VK',
    'm.tau.vk.ru': 'VK',
    'm.vkvideo.cs7777.vk.ru': 'VK Видео',
    'me.cs7777.vk.ru': 'VK',
    'ms.cs7777.vk.ru': 'VK',
    'music.vk.ru': 'VK Музыка',
    'oauth.cs7777.vk.ru': 'VK',
    'oauth.tau.vk.ru': 'VK',
    'oauth2.cs7777.vk.ru': 'VK',
    'ord.vk.ru': 'VK',
    'push.vk.ru': 'VK',
    'r.vk.ru': 'VK',
    'target.vk.ru': 'VK',
    'tech.vk.ru': 'VK',
    'ui.cs7777.vk.ru': 'VK',
    'ui.tau.vk.ru': 'VK',
    'vkvideo.cs7777.vk.ru': 'VK Видео',
    
    # Speedload
    'speedload.ru': 'Speedload',
    'api.speedload.ru': 'Speedload',
    'chat.speedload.ru': 'Speedload',
    
    # Serverstats
    'serverstats.ru': 'ServerStats',
    'cdnfive.serverstats.ru': 'ServerStats',
    'cdncloudtwo.serverstats.ru': 'ServerStats',
    
    # Furypay
    'furypay.ru': 'FuryPay',
    'api.furypay.ru': 'FuryPay',
    
    # JoJack
    'jojack.ru': 'JoJack',
    'spb.jojack.ru': 'JoJack',
    'at.jojack.ru': 'JoJack',
    
    # Tcp-reset-club
    'tcp-reset-club.net': 'TCP Reset',
    'est01-ss01.tcp-reset-club.net': 'TCP Reset',
    'nl01-ss01.tcp-reset-club.net': 'TCP Reset',
    'ru01-blh01.tcp-reset-club.net': 'TCP Reset',
    
    # Государственные
    'gov.ru': 'Госуслуги',
    'kremlin.ru': 'Кремль',
    'government.ru': 'Правительство',
    'duma.gov.ru': 'Госдума',
    'genproc.gov.ru': 'Генпрокуратура',
    'epp.genproc.gov.ru': 'Генпрокуратура',
    'cikrf.ru': 'ЦИК',
    'izbirkom.ru': 'Избирком',
    'gosuslugi.ru': 'Госуслуги',
    'sfd.gosuslugi.ru': 'Госуслуги',
    'esia.gosuslugi.ru': 'Госуслуги',
    'bot.gosuslugi.ru': 'Госуслуги',
    'contract.gosuslugi.ru': 'Госуслуги',
    'novorossiya.gosuslugi.ru': 'Госуслуги',
    'pos.gosuslugi.ru': 'Госуслуги',
    'lk.gosuslugi.ru': 'Госуслуги',
    'map.gosuslugi.ru': 'Госуслуги',
    'partners.gosuslugi.ru': 'Госуслуги',
    'gosweb.gosuslugi.ru': 'Госуслуги',
    'voter.gosuslugi.ru': 'Госуслуги',
    'gu-st.ru': 'Госуслуги',
    'nalog.ru': 'ФНС',
    'pfr.gov.ru': 'ПФР',
    'digital.gov.ru': 'Минцифры',
    'adm.digital.gov.ru': 'Минцифры',
    'xn--80ajghhoc2aj1c8b.xn--p1ai': 'Минцифры',
    
    # NSDI ресурсы
    'a.res-nsdi.ru': 'NSDI',
    'b.res-nsdi.ru': 'NSDI',
    'a.auth-nsdi.ru': 'NSDI',
    'b.auth-nsdi.ru': 'NSDI',
    
    # Одноклассники
    'ok.ru': 'Одноклассники',
    'odnoklassniki.ru': 'Одноклассники',
    'cdn.ok.ru': 'Одноклассники',
    'st.okcdn.ru': 'Одноклассники',
    'st.ok.ru': 'Одноклассники',
    'apiok.ru': 'Одноклассники',
    'jira.apiok.ru': 'Одноклассники',
    'api.ok.ru': 'Одноклассники',
    'm.ok.ru': 'Одноклассники',
    'live.ok.ru': 'Одноклассники',
    'multitest.ok.ru': 'Одноклассники',
    'dating.ok.ru': 'Одноклассники',
    'tamtam.ok.ru': 'Одноклассники',
    '742231.ms.ok.ru': 'Одноклассники',
    
    # Ozon
    'ozon.ru': 'Ozon',
    'www.ozon.ru': 'Ozon',
    'seller.ozon.ru': 'Ozon',
    'bank.ozon.ru': 'Ozon',
    'pay.ozon.ru': 'Ozon',
    'securepay.ozon.ru': 'Ozon',
    'adv.ozon.ru': 'Ozon',
    'invest.ozon.ru': 'Ozon',
    'ord.ozon.ru': 'Ozon',
    'autodiscover.ord.ozon.ru': 'Ozon',
    'st.ozone.ru': 'Ozon',
    'ir.ozone.ru': 'Ozon',
    'vt-1.ozone.ru': 'Ozon',
    'ir-2.ozone.ru': 'Ozon',
    'xapi.ozon.ru': 'Ozon',
    'owa.ozon.ru': 'Ozon',
    'learning.ozon.ru': 'Ozon',
    'mapi.learning.ozon.ru': 'Ozon',
    'ws.seller.ozon.ru': 'Ozon',
    
    # Wildberries
    'wildberries.ru': 'Wildberries',
    'wb.ru': 'Wildberries',
    'static.wb.ru': 'Wildberries',
    'seller.wildberries.ru': 'Wildberries',
    'banners.wildberries.ru': 'Wildberries',
    'fw.wb.ru': 'Wildberries',
    'finance.wb.ru': 'Wildberries',
    'jitsi.wb.ru': 'Wildberries',
    'dnd.wb.ru': 'Wildberries',
    'user-geo-data.wildberries.ru': 'Wildberries',
    'banners-website.wildberries.ru': 'Wildberries',
    'chat-prod.wildberries.ru': 'Wildberries',
    'a.wb.ru': 'Wildberries',
    
    # Avito
    'avito.ru': 'Avito',
    'm.avito.ru': 'Avito',
    'api.avito.ru': 'Avito',
    'avito.st': 'Avito',
    'img.avito.st': 'Avito',
    'sntr.avito.ru': 'Avito',
    'stats.avito.ru': 'Avito',
    'cs.avito.ru': 'Avito',
    'www.avito.st': 'Avito',
    'st.avito.ru': 'Avito',
    'www.avito.ru': 'Avito',
    
    # Avito.st изображения (все 00-99)
    **{f'{i:02d}.img.avito.st': 'Avito' for i in range(100)},
    
    # Банки
    'sberbank.ru': 'Сбербанк',
    'online.sberbank.ru': 'Сбербанк',
    'sber.ru': 'Сбербанк',
    'id.sber.ru': 'Сбербанк',
    'bfds.sberbank.ru': 'Сбербанк',
    'cms-res-web.online.sberbank.ru': 'Сбербанк',
    'esa-res.online.sberbank.ru': 'Сбербанк',
    'pl-res.online.sberbank.ru': 'Сбербанк',
    'www.sberbank.ru': 'Сбербанк',
    'vtb.ru': 'ВТБ',
    'www.vtb.ru': 'ВТБ',
    'online.vtb.ru': 'ВТБ',
    'chat3.vtb.ru': 'ВТБ',
    's.vtb.ru': 'ВТБ',
    'sso-app4.vtb.ru': 'ВТБ',
    'sso-app5.vtb.ru': 'ВТБ',
    'gazprombank.ru': 'Газпромбанк',
    'alfabank.ru': 'Альфа-Банк',
    'metrics.alfabank.ru': 'Альфа-Банк',
    'tinkoff.ru': 'Тинькофф',
    'tbank.ru': 'Тинькофф',
    'cdn.tbank.ru': 'Тинькофф',
    'hrc.tbank.ru': 'Тинькофф',
    'cobrowsing.tbank.ru': 'Тинькофф',
    'le.tbank.ru': 'Тинькофф',
    'id.tbank.ru': 'Тинькофф',
    'imgproxy.cdn-tinkoff.ru': 'Тинькофф',
    'banki.ru': 'Банки.ру',
    
    # Яндекс
    'yandex.ru': 'Яндекс',
    'ya.ru': 'Яндекс',
    'dzen.ru': 'Дзен',
    'kinopoisk.ru': 'Кинопоиск',
    'yastatic.net': 'Яндекс',
    'yandex.net': 'Яндекс',
    'mail.yandex.ru': 'Яндекс Почта',
    'disk.yandex.ru': 'Яндекс Диск',
    'maps.yandex.ru': 'Яндекс Карты',
    'api-maps.yandex.ru': 'Яндекс Карты',
    'enterprise.api-maps.yandex.ru': 'Яндекс Карты',
    'music.yandex.ru': 'Яндекс Музыка',
    'yandex.by': 'Яндекс',
    'yandex.com': 'Яндекс',
    'travel.yandex.ru': 'Яндекс Путешествия',
    'informer.yandex.ru': 'Яндекс',
    'mediafeeds.yandex.ru': 'Яндекс',
    'mediafeeds.yandex.com': 'Яндекс',
    'uslugi.yandex.ru': 'Яндекс Услуги',
    'kiks.yandex.ru': 'Яндекс',
    'kiks.yandex.com': 'Яндекс',
    'frontend.vh.yandex.ru': 'Яндекс',
    'favicon.yandex.ru': 'Яндекс',
    'favicon.yandex.com': 'Яндекс',
    'favicon.yandex.net': 'Яндекс',
    'browser.yandex.ru': 'Яндекс Браузер',
    'browser.yandex.com': 'Яндекс Браузер',
    'api.browser.yandex.ru': 'Яндекс Браузер',
    'api.browser.yandex.com': 'Яндекс Браузер',
    'wap.yandex.ru': 'Яндекс',
    'wap.yandex.com': 'Яндекс',
    '300.ya.ru': 'Яндекс',
    'brontp-pre.yandex.ru': 'Яндекс',
    'suggest.dzen.ru': 'Дзен',
    'suggest.sso.dzen.ru': 'Дзен',
    'sso.dzen.ru': 'Дзен',
    'mail.yandex.com': 'Яндекс Почта',
    'yabs.yandex.ru': 'Яндекс',
    'neuro.translate.yandex.ru': 'Яндекс Перевод',
    'cdn.yandex.ru': 'Яндекс',
    'zen.yandex.ru': 'Дзен',
    'zen.yandex.com': 'Дзен',
    'zen.yandex.net': 'Дзен',
    'collections.yandex.ru': 'Яндекс Коллекции',
    'collections.yandex.com': 'Яндекс Коллекции',
    'an.yandex.ru': 'Яндекс',
    'sba.yandex.ru': 'Яндекс',
    'sba.yandex.com': 'Яндекс',
    'sba.yandex.net': 'Яндекс',
    'surveys.yandex.ru': 'Яндекс Опросы',
    'yabro-wbplugin.edadeal.yandex.ru': 'Яндекс',
    'api.events.plus.yandex.net': 'Яндекс Плюс',
    'speller.yandex.net': 'Яндекс Спеллер',
    'avatars.mds.yandex.net': 'Яндекс',
    'avatars.mds.yandex.com': 'Яндекс',
    'mc.yandex.ru': 'Яндекс',
    'mc.yandex.com': 'Яндекс',
    '3475482542.mc.yandex.ru': 'Яндекс',
    'zen-yabro-morda.mediascope.mc.yandex.ru': 'Яндекс',
    
    # Яндекс CDN и сервисы
    'travel.yastatic.net': 'Яндекс',
    'api.uxfeedback.yandex.net': 'Яндекс',
    'api.s3.yandex.net': 'Яндекс',
    'cdn.s3.yandex.net': 'Яндекс',
    'uxfeedback-cdn.s3.yandex.net': 'Яндекс',
    'uxfeedback.yandex.ru': 'Яндекс',
    'cloudcdn-m9-15.cdn.yandex.net': 'Яндекс',
    'cloudcdn-m9-14.cdn.yandex.net': 'Яндекс',
    'cloudcdn-m9-13.cdn.yandex.net': 'Яндекс',
    'cloudcdn-m9-12.cdn.yandex.net': 'Яндекс',
    'cloudcdn-m9-10.cdn.yandex.net': 'Яндекс',
    'cloudcdn-m9-9.cdn.yandex.net': 'Яндекс',
    'cloudcdn-m9-7.cdn.yandex.net': 'Яндекс',
    'cloudcdn-m9-6.cdn.yandex.net': 'Яндекс',
    'cloudcdn-m9-5.cdn.yandex.net': 'Яндекс',
    'cloudcdn-m9-4.cdn.yandex.net': 'Яндекс',
    'cloudcdn-m9-3.cdn.yandex.net': 'Яндекс',
    'cloudcdn-m9-2.cdn.yandex.net': 'Яндекс',
    'cloudcdn-ams19.cdn.yandex.net': 'Яндекс',
    'http-check-headers.yandex.ru': 'Яндекс',
    'cloud.cdn.yandex.net': 'Яндекс',
    'cloud.cdn.yandex.com': 'Яндекс',
    'cloud.cdn.yandex.ru': 'Яндекс',
    'dr2.yandex.net': 'Яндекс',
    'dr.yandex.net': 'Яндекс',
    's3.yandex.net': 'Яндекс',
    'static-mon.yandex.net': 'Яндекс',
    'sync.browser.yandex.net': 'Яндекс',
    'storage.ape.yandex.net': 'Яндекс',
    'strm-rad-23.strm.yandex.net': 'Яндекс',
    'strm.yandex.net': 'Яндекс',
    'strm.yandex.ru': 'Яндекс',
    'log.strm.yandex.ru': 'Яндекс',
    'egress.yandex.net': 'Яндекс',
    'cdnrhkgfkkpupuotntfj.svc.cdn.yandex.net': 'Яндекс',
    'csp.yandex.net': 'Яндекс',
    
    # Mail.ru Group (полный список)
    'mail.ru': 'Mail.ru',
    'e.mail.ru': 'Mail.ru',
    'my.mail.ru': 'Mail.ru',
    'cloud.mail.ru': 'Mail.ru',
    'inbox.ru': 'Mail.ru',
    'list.ru': 'Mail.ru',
    'bk.ru': 'Mail.ru',
    'myteam.mail.ru': 'Mail.ru',
    'trk.mail.ru': 'Mail.ru',
    '1l-api.mail.ru': 'Mail.ru',
    '1l.mail.ru': 'Mail.ru',
    '1l-s2s.mail.ru': 'Mail.ru',
    '1l-view.mail.ru': 'Mail.ru',
    '1link.mail.ru': 'Mail.ru',
    '1l-hit.mail.ru': 'Mail.ru',
    '2021.mail.ru': 'Mail.ru',
    '2018.mail.ru': 'Mail.ru',
    '23feb.mail.ru': 'Mail.ru',
    '2019.mail.ru': 'Mail.ru',
    '2020.mail.ru': 'Mail.ru',
    '1l-go.mail.ru': 'Mail.ru',
    '8mar.mail.ru': 'Mail.ru',
    '9may.mail.ru': 'Mail.ru',
    'aa.mail.ru': 'Mail.ru',
    '8march.mail.ru': 'Mail.ru',
    'afisha.mail.ru': 'Mail.ru',
    'agent.mail.ru': 'Mail.ru',
    'amigo.mail.ru': 'Mail.ru',
    'analytics.predict.mail.ru': 'Mail.ru',
    'alpha4.minigames.mail.ru': 'Mail.ru',
    'alpha3.minigames.mail.ru': 'Mail.ru',
    'answer.mail.ru': 'Mail.ru',
    'api.predict.mail.ru': 'Mail.ru',
    'answers.mail.ru': 'Mail.ru',
    'authdl.mail.ru': 'Mail.ru',
    'av.mail.ru': 'Mail.ru',
    'apps.research.mail.ru': 'Mail.ru',
    'auto.mail.ru': 'Mail.ru',
    'bb.mail.ru': 'Mail.ru',
    'bender.mail.ru': 'Mail.ru',
    'beko.dom.mail.ru': 'Mail.ru',
    'azt.mail.ru': 'Mail.ru',
    'bd.mail.ru': 'Mail.ru',
    'autodiscover.corp.mail.ru': 'Mail.ru',
    'aw.mail.ru': 'Mail.ru',
    'beta.mail.ru': 'Mail.ru',
    'biz.mail.ru': 'Mail.ru',
    'blackfriday.mail.ru': 'Mail.ru',
    'bitva.mail.ru': 'Mail.ru',
    'blog.mail.ru': 'Mail.ru',
    'bratva-mr.mail.ru': 'Mail.ru',
    'browser.mail.ru': 'Mail.ru',
    'calendar.mail.ru': 'Mail.ru',
    'capsula.mail.ru': 'Mail.ru',
    'cdn.newyear.mail.ru': 'Mail.ru',
    'cars.mail.ru': 'Mail.ru',
    'code.mail.ru': 'Mail.ru',
    'cobmo.mail.ru': 'Mail.ru',
    'cobma.mail.ru': 'Mail.ru',
    'cog.mail.ru': 'Mail.ru',
    'cdn.connect.mail.ru': 'Mail.ru',
    'cf.mail.ru': 'Mail.ru',
    'comba.mail.ru': 'Mail.ru',
    'compute.mail.ru': 'Mail.ru',
    'codefest.mail.ru': 'Mail.ru',
    'combu.mail.ru': 'Mail.ru',
    'corp.mail.ru': 'Mail.ru',
    'commba.mail.ru': 'Mail.ru',
    'crazypanda.mail.ru': 'Mail.ru',
    'ctlog.mail.ru': 'Mail.ru',
    'cpg.money.mail.ru': 'Mail.ru',
    'ctlog2023.mail.ru': 'Mail.ru',
    'ctlog2024.mail.ru': 'Mail.ru',
    'cto.mail.ru': 'Mail.ru',
    'cups.mail.ru': 'Mail.ru',
    'da.biz.mail.ru': 'Mail.ru',
    'da-preprod.biz.mail.ru': 'Mail.ru',
    'data.amigo.mail.ru': 'Mail.ru',
    'dk.mail.ru': 'Mail.ru',
    'dev1.mail.ru': 'Mail.ru',
    'dev3.mail.ru': 'Mail.ru',
    'dl.mail.ru': 'Mail.ru',
    'deti.mail.ru': 'Mail.ru',
    'dn.mail.ru': 'Mail.ru',
    'dl.marusia.mail.ru': 'Mail.ru',
    'doc.mail.ru': 'Mail.ru',
    'dragonpals.mail.ru': 'Mail.ru',
    'dom.mail.ru': 'Mail.ru',
    'duck.mail.ru': 'Mail.ru',
    'dev2.mail.ru': 'Mail.ru',
    'ds.mail.ru': 'Mail.ru',
    'education.mail.ru': 'Mail.ru',
    'dobro.mail.ru': 'Mail.ru',
    'esc.predict.mail.ru': 'Mail.ru',
    'et.mail.ru': 'Mail.ru',
    'fe.mail.ru': 'Mail.ru',
    'finance.mail.ru': 'Mail.ru',
    'five.predict.mail.ru': 'Mail.ru',
    'foto.mail.ru': 'Mail.ru',
    'games-bamboo.mail.ru': 'Mail.ru',
    'games-fisheye.mail.ru': 'Mail.ru',
    'games.mail.ru': 'Mail.ru',
    'genesis.mail.ru': 'Mail.ru',
    'geo-apart.predict.mail.ru': 'Mail.ru',
    'golos.mail.ru': 'Mail.ru',
    'go.mail.ru': 'Mail.ru',
    'gpb.finance.mail.ru': 'Mail.ru',
    'gibdd.mail.ru': 'Mail.ru',
    'health.mail.ru': 'Mail.ru',
    'guns.mail.ru': 'Mail.ru',
    'horo.mail.ru': 'Mail.ru',
    'hs.mail.ru': 'Mail.ru',
    'help.mcs.mail.ru': 'Mail.ru',
    'imperia.mail.ru': 'Mail.ru',
    'it.mail.ru': 'Mail.ru',
    'internet.mail.ru': 'Mail.ru',
    'infra.mail.ru': 'Mail.ru',
    'hi-tech.mail.ru': 'Mail.ru',
    'jd.mail.ru': 'Mail.ru',
    'journey.mail.ru': 'Mail.ru',
    'junior.mail.ru': 'Mail.ru',
    'juggermobile.mail.ru': 'Mail.ru',
    'kicker.mail.ru': 'Mail.ru',
    'knights.mail.ru': 'Mail.ru',
    'kino.mail.ru': 'Mail.ru',
    'kingdomrift.mail.ru': 'Mail.ru',
    'kobmo.mail.ru': 'Mail.ru',
    'komba.mail.ru': 'Mail.ru',
    'kobma.mail.ru': 'Mail.ru',
    'kommba.mail.ru': 'Mail.ru',
    'kombo.mail.ru': 'Mail.ru',
    'kz.mcs.mail.ru': 'Mail.ru',
    'konflikt.mail.ru': 'Mail.ru',
    'kombu.mail.ru': 'Mail.ru',
    'lady.mail.ru': 'Mail.ru',
    'landing.mail.ru': 'Mail.ru',
    'la.mail.ru': 'Mail.ru',
    'legendofheroes.mail.ru': 'Mail.ru',
    'legenda.mail.ru': 'Mail.ru',
    'loa.mail.ru': 'Mail.ru',
    'love.mail.ru': 'Mail.ru',
    'lotro.mail.ru': 'Mail.ru',
    'mailer.mail.ru': 'Mail.ru',
    'mailexpress.mail.ru': 'Mail.ru',
    'man.mail.ru': 'Mail.ru',
    'maps.mail.ru': 'Mail.ru',
    'marusia.mail.ru': 'Mail.ru',
    'mcs.mail.ru': 'Mail.ru',
    'media-golos.mail.ru': 'Mail.ru',
    'mediapro.mail.ru': 'Mail.ru',
    'merch-cpg.money.mail.ru': 'Mail.ru',
    'miniapp.internal.myteam.mail.ru': 'Mail.ru',
    'media.mail.ru': 'Mail.ru',
    'mobfarm.mail.ru': 'Mail.ru',
    'mowar.mail.ru': 'Mail.ru',
    'mozilla.mail.ru': 'Mail.ru',
    'mosqa.mail.ru': 'Mail.ru',
    'mking.mail.ru': 'Mail.ru',
    'minigames.mail.ru': 'Mail.ru',
    'nebogame.mail.ru': 'Mail.ru',
    'money.mail.ru': 'Mail.ru',
    'net.mail.ru': 'Mail.ru',
    'new.mail.ru': 'Mail.ru',
    'newyear2018.mail.ru': 'Mail.ru',
    'news.mail.ru': 'Mail.ru',
    'newyear.mail.ru': 'Mail.ru',
    'nonstandard.sales.mail.ru': 'Mail.ru',
    'notes.mail.ru': 'Mail.ru',
    'octavius.mail.ru': 'Mail.ru',
    'operator.mail.ru': 'Mail.ru',
    'otvety.mail.ru': 'Mail.ru',
    'otvet.mail.ru': 'Mail.ru',
    'otveti.mail.ru': 'Mail.ru',
    'panzar.mail.ru': 'Mail.ru',
    'park.mail.ru': 'Mail.ru',
    'pernatsk.mail.ru': 'Mail.ru',
    'pets.mail.ru': 'Mail.ru',
    'pms.mail.ru': 'Mail.ru',
    'pochtabank.mail.ru': 'Mail.ru',
    'pokerist.mail.ru': 'Mail.ru',
    'pogoda.mail.ru': 'Mail.ru',
    'polis.mail.ru': 'Mail.ru',
    'primeworld.mail.ru': 'Mail.ru',
    'pp.mail.ru': 'Mail.ru',
    'ptd.predict.mail.ru': 'Mail.ru',
    'public.infra.mail.ru': 'Mail.ru',
    'pulse.mail.ru': 'Mail.ru',
    'pubg.mail.ru': 'Mail.ru',
    'quantum.mail.ru': 'Mail.ru',
    'rate.mail.ru': 'Mail.ru',
    'pw.mail.ru': 'Mail.ru',
    'rebus.calls.mail.ru': 'Mail.ru',
    'rebus.octavius.mail.ru': 'Mail.ru',
    'rev.mail.ru': 'Mail.ru',
    'rl.mail.ru': 'Mail.ru',
    'rm.mail.ru': 'Mail.ru',
    'riot.mail.ru': 'Mail.ru',
    'reseach.mail.ru': 'Mail.ru',
    's3.babel.mail.ru': 'Mail.ru',
    'rt.api.operator.mail.ru': 'Mail.ru',
    's3.mail.ru': 'Mail.ru',
    's3.media-mobs.mail.ru': 'Mail.ru',
    'sales.mail.ru': 'Mail.ru',
    'sangels.mail.ru': 'Mail.ru',
    'sdk.money.mail.ru': 'Mail.ru',
    'service.amigo.mail.ru': 'Mail.ru',
    'security.mail.ru': 'Mail.ru',
    'shadowbound.mail.ru': 'Mail.ru',
    'socdwar.mail.ru': 'Mail.ru',
    'sochi-park.predict.mail.ru': 'Mail.ru',
    'souz.mail.ru': 'Mail.ru',
    'sphere.mail.ru': 'Mail.ru',
    'staging-analytics.predict.mail.ru': 'Mail.ru',
    'staging-sochi-park.predict.mail.ru': 'Mail.ru',
    'staging-esc.predict.mail.ru': 'Mail.ru',
    'stand.bb.mail.ru': 'Mail.ru',
    'sport.mail.ru': 'Mail.ru',
    'stand.aoc.mail.ru': 'Mail.ru',
    'stand.cb.mail.ru': 'Mail.ru',
    'startrek.mail.ru': 'Mail.ru',
    'static.dl.mail.ru': 'Mail.ru',
    'stand.pw.mail.ru': 'Mail.ru',
    'stand.la.mail.ru': 'Mail.ru',
    'stormriders.mail.ru': 'Mail.ru',
    'static.operator.mail.ru': 'Mail.ru',
    'stream.mail.ru': 'Mail.ru',
    'status.mcs.mail.ru': 'Mail.ru',
    'street-combats.mail.ru': 'Mail.ru',
    'support.biz.mail.ru': 'Mail.ru',
    'support.mcs.mail.ru': 'Mail.ru',
    'team.mail.ru': 'Mail.ru',
    'support.tech.mail.ru': 'Mail.ru',
    'tech.mail.ru': 'Mail.ru',
    'tera.mail.ru': 'Mail.ru',
    'tiles.maps.mail.ru': 'Mail.ru',
    'todo.mail.ru': 'Mail.ru',
    'tidaltrek.mail.ru': 'Mail.ru',
    'tmgame.mail.ru': 'Mail.ru',
    'townwars.mail.ru': 'Mail.ru',
    'tv.mail.ru': 'Mail.ru',
    'ttbh.mail.ru': 'Mail.ru',
    'typewriter.mail.ru': 'Mail.ru',
    'u.corp.mail.ru': 'Mail.ru',
    'ufo.mail.ru': 'Mail.ru',
    'vkdoc.mail.ru': 'Mail.ru',
    'vk.mail.ru': 'Mail.ru',
    'voina.mail.ru': 'Mail.ru',
    'warface.mail.ru': 'Mail.ru',
    'wartune.mail.ru': 'Mail.ru',
    'weblink.predict.mail.ru': 'Mail.ru',
    'warheaven.mail.ru': 'Mail.ru',
    'welcome.mail.ru': 'Mail.ru',
    'webstore.mail.ru': 'Mail.ru',
    'webagent.mail.ru': 'Mail.ru',
    'wf.mail.ru': 'Mail.ru',
    'whatsnew.mail.ru': 'Mail.ru',
    'wh-cpg.money.mail.ru': 'Mail.ru',
    'wok.mail.ru': 'Mail.ru',
    'www.biz.mail.ru': 'Mail.ru',
    'wos.mail.ru': 'Mail.ru',
    'www.mail.ru': 'Mail.ru',
    'www.pubg.mail.ru': 'Mail.ru',
    'www.wf.mail.ru': 'Mail.ru',
    'www.mcs.mail.ru': 'Mail.ru',
    'rs.mail.ru': 'Mail.ru',
    'top-fwz1.mail.ru': 'Mail.ru',
    'privacy-cs.mail.ru': 'Mail.ru',
    'r0.mradx.net': 'Mail.ru',
    
    # Медиа и новости
    'rutube.ru': 'Rutube',
    'static.rutube.ru': 'Rutube',
    'rutubelist.ru': 'Rutube',
    'pic.rutubelist.ru': 'Rutube',
    'ssp.rutube.ru': 'Rutube',
    'preview.rutube.ru': 'Rutube',
    'goya.rutube.ru': 'Rutube',
    'smotrim.ru': 'Смотрим',
    'ivi.ru': 'Ivi',
    'cdn.ivi.ru': 'Ivi',
    'okko.tv': 'Okko',
    'start.ru': 'Start',
    'wink.ru': 'Wink',
    'kion.ru': 'Kion',
    'premier.one': 'Premier',
    'more.tv': 'More.tv',
    'm.47news.ru': '47 News',
    'lenta.ru': 'Лента.ру',
    'gazeta.ru': 'Газета.ру',
    'kp.ru': 'Комсомольская Правда',
    'rambler.ru': 'Рамблер',
    'ria.ru': 'РИА Новости',
    'tass.ru': 'ТАСС',
    'interfax.ru': 'Интерфакс',
    'kommersant.ru': 'Коммерсант',
    'vedomosti.ru': 'Ведомости',
    'rbc.ru': 'РБК',
    'russian.rt.com': 'RT',
    'iz.ru': 'Известия',
    'mk.ru': 'Московский Комсомолец',
    'rg.ru': 'Российская Газета',
    
    # Кинопоиск
    'www.kinopoisk.ru': 'Кинопоиск',
    'widgets.kinopoisk.ru': 'Кинопоиск',
    'payment-widget.plus.kinopoisk.ru': 'Кинопоиск',
    'external-api.mediabilling.kinopoisk.ru': 'Кинопоиск',
    'external-api.plus.kinopoisk.ru': 'Кинопоиск',
    'graphql-web.kinopoisk.ru': 'Кинопоиск',
    'graphql.kinopoisk.ru': 'Кинопоиск',
    'tickets.widget.kinopoisk.ru': 'Кинопоиск',
    'st.kinopoisk.ru': 'Кинопоиск',
    'quiz.kinopoisk.ru': 'Кинопоиск',
    'payment-widget.kinopoisk.ru': 'Кинопоиск',
    'payment-widget-smarttv.plus.kinopoisk.ru': 'Кинопоиск',
    'oneclick-payment.kinopoisk.ru': 'Кинопоиск',
    'microapps.kinopoisk.ru': 'Кинопоиск',
    'ma.kinopoisk.ru': 'Кинопоиск',
    'hd.kinopoisk.ru': 'Кинопоиск',
    'crowdtest.payment-widget-smarttv.plus.tst.kinopoisk.ru': 'Кинопоиск',
    'crowdtest.payment-widget.plus.tst.kinopoisk.ru': 'Кинопоиск',
    'api.plus.kinopoisk.ru': 'Кинопоиск',
    'st-im.kinopoisk.ru': 'Кинопоиск',
    'sso.kinopoisk.ru': 'Кинопоиск',
    'touch.kinopoisk.ru': 'Кинопоиск',
    
    # Карты и транспорт
    '2gis.ru': '2ГИС',
    '2gis.com': '2ГИС',
    'api.2gis.ru': '2ГИС',
    'keys.api.2gis.com': '2ГИС',
    'favorites.api.2gis.com': '2ГИС',
    'styles.api.2gis.com': '2ГИС',
    'tile0.maps.2gis.com': '2ГИС',
    'tile1.maps.2gis.com': '2ГИС',
    'tile2.maps.2gis.com': '2ГИС',
    'tile3.maps.2gis.com': '2ГИС',
    'tile4.maps.2gis.com': '2ГИС',
    'api.photo.2gis.com': '2ГИС',
    'filekeeper-vod.2gis.com': '2ГИС',
    'i0.photo.2gis.com': '2ГИС',
    'i1.photo.2gis.com': '2ГИС',
    'i2.photo.2gis.com': '2ГИС',
    'i3.photo.2gis.com': '2ГИС',
    'i4.photo.2gis.com': '2ГИС',
    'i5.photo.2gis.com': '2ГИС',
    'i6.photo.2gis.com': '2ГИС',
    'i7.photo.2gis.com': '2ГИС',
    'i8.photo.2gis.com': '2ГИС',
    'i9.photo.2gis.com': '2ГИС',
    'jam.api.2gis.com': '2ГИС',
    'catalog.api.2gis.com': '2ГИС',
    'api.reviews.2gis.com': '2ГИС',
    'public-api.reviews.2gis.com': '2ГИС',
    'mapgl.2gis.com': '2ГИС',
    'd-assets.2gis.ru': '2ГИС',
    'disk.2gis.com': '2ГИС',
    's0.bss.2gis.com': '2ГИС',
    's1.bss.2gis.com': '2ГИС',
    'ams2-cdn.2gis.com': '2ГИС',
    'tutu.ru': 'Туту.ру',
    'img.tutu.ru': 'Туту.ру',
    'rzd.ru': 'РЖД',
    'ticket.rzd.ru': 'РЖД',
    'pass.rzd.ru': 'РЖД',
    'cargo.rzd.ru': 'РЖД',
    'company.rzd.ru': 'РЖД',
    'contacts.rzd.ru': 'РЖД',
    'team.rzd.ru': 'РЖД',
    'my.rzd.ru': 'РЖД',
    'prodvizhenie.rzd.ru': 'РЖД',
    'disk.rzd.ru': 'РЖД',
    'market.rzd.ru': 'РЖД',
    'secure.rzd.ru': 'РЖД',
    'secure-cloud.rzd.ru': 'РЖД',
    'travel.rzd.ru': 'РЖД',
    'welcome.rzd.ru': 'РЖД',
    'adm.mp.rzd.ru': 'РЖД',
    'link.mp.rzd.ru': 'РЖД',
    'pulse.mp.rzd.ru': 'РЖД',
    'mp.rzd.ru': 'РЖД',
    'ekmp-a-51.rzd.ru': 'РЖД',
    'cdek.ru': 'СДЭК',
    'cdek.market': 'СДЭК',
    'calc.cdek.ru': 'СДЭК',
    'pochta.ru': 'Почта России',
    'ws-api.oneme.ru': 'Oneme',
    
    # Телеком
    'rostelecom.ru': 'Ростелеком',
    'rt.ru': 'Ростелеком',
    'mts.ru': 'МТС',
    'megafon.ru': 'Мегафон',
    'beeline.ru': 'Билайн',
    'tele2.ru': 'Tele2',
    't2.ru': 'Tele2',
    'www.t2.ru': 'Tele2',
    'msk.t2.ru': 'Tele2',
    's3.t2.ru': 'Tele2',
    'yota.ru': 'Yota',
    'domru.ru': 'Дом.ру',
    'ertelecom.ru': 'ЭР-Телеком',
    'selectel.ru': 'Selectel',
    'timeweb.ru': 'Timeweb',
    
    # Погода
    'gismeteo.ru': 'Гисметео',
    'meteoinfo.ru': 'Метео',
    'rp5.ru': 'RП5',
    
    # Работа
    'hh.ru': 'HeadHunter',
    'superjob.ru': 'SuperJob',
    'rabota.ru': 'Работа.ру',
    
    # Авто
    'auto.ru': 'Auto.ru',
    'sso.auto.ru': 'Auto.ru',
    'drom.ru': 'Drom',
    'avto.ru': 'Avto.ru',
    
    # Еда
    'eda.ru': 'Eda.ru',
    'food.ru': 'Food.ru',
    'edadeal.ru': 'Edadeal',
    'delivery-club.ru': 'Delivery Club',
    
    # Дом и стройка
    'leroymerlin.ru': 'Леруа Мерлен',
    'lemanapro.ru': 'Лемана Про',
    'cdn.lemanapro.ru': 'Лемана Про',
    'static.lemanapro.ru': 'Лемана Про',
    'dmp.dmpkit.lemanapro.ru': 'Лемана Про',
    'receive-sentry.lmru.tech': 'Лемана Про',
    'partners.lemanapro.ru': 'Лемана Про',
    'petrovich.ru': 'Петрович',
    'maxidom.ru': 'Максидом',
    'vseinstrumenti.ru': 'ВсеИнструменты',
    '220-volt.ru': '220 Вольт',
    
    # Max
    'max.ru': 'Max',
    'dev.max.ru': 'Max',
    'web.max.ru': 'Max',
    'api.max.ru': 'Max',
    'legal.max.ru': 'Max',
    'st.max.ru': 'Max',
    'botapi.max.ru': 'Max',
    'link.max.ru': 'Max',
    'download.max.ru': 'Max',
    'i.max.ru': 'Max',
    'help.max.ru': 'Max',
    
    # Прочее
    'mos.ru': 'Мос.ру',
    'taximaxim.ru': 'Такси Максим',
    'moskva.taximaxim.ru': 'Такси Максим',
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
        'AT': 'Австрия', 'CH': 'Швейцария', 'BE': 'Бельгия', 'IT': 'Италия',
        'ES': 'Испания', 'PT': 'Португалия', 'AU': 'Австралия', 'NZ': 'Новая Зеландия',
        'BR': 'Бразилия', 'ZA': 'ЮАР', 'IN': 'Индия', 'KR': 'Корея', 'CN': 'Китай',
        'TW': 'Тайвань', 'UA': 'Украина', 'KZ': 'Казахстан', 'BY': 'Беларусь',
        'LV': 'Латвия', 'LT': 'Литва', 'EE': 'Эстония', 'RO': 'Румыния', 'BG': 'Болгария',
        'HU': 'Венгрия', 'SK': 'Словакия', 'SI': 'Словения', 'HR': 'Хорватия',
        'RS': 'Сербия', 'TR': 'Турция', 'IL': 'Израиль', 'AE': 'ОАЭ', 'SA': 'Саудовская Аравия',
        'EG': 'Египет',
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
        try:
            url = f"https://ipwhois.io/json/{target_ip}"
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode())
                if data.get('country_code'):
                    country_info['country'] = data.get('country_code')
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
        if os.path.exists(LOG_FILE):
            mtime = datetime.fromtimestamp(os.path.getmtime(LOG_FILE))
            if now - mtime > timedelta(seconds=LOG_CLEAN_INTERVAL):
                open(LOG_FILE, "w").close()
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
                    if not d:
                        continue
                    domains.add(d)
                    suffixes.append("." + d)
            print(f"📋 Загружено {len(domains)} доменов из whitelist.txt")
        except:
            print("⚠️ Ошибка загрузки whitelist.txt")
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
                    elif k.lower() == 'path':
                        path_parts = re.findall(r'[a-zA-Z0-9][a-zA-Z0-9\-\.]+[a-zA-Z0-9]\.[a-zA-Z]{2,}', v_decoded)
                        for d in path_parts:
                            domains.add(d.lower())
        if '#' in after_at:
            fragment = after_at.split('#', 1)[1]
            try:
                fragment_decoded = urllib.parse.unquote(fragment)
                domain_in_frag = re.findall(r'[a-zA-Z0-9][a-zA-Z0-9\-\.]+[a-zA-Z0-9]\.[a-zA-Z]{2,}', fragment_decoded)
                for d in domain_in_frag:
                    domains.add(d.lower())
            except:
                pass
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
    for key in DOMAIN_NAMES:
        if d.endswith("." + key):
            return DOMAIN_NAMES[key]
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
            parts = domain.split('.')
            for i in range(len(parts) - 1):
                sub = ".".join(parts[i:])
                if sub in DOMAIN_NAMES:
                    return True
            if len(parts) >= 2:
                base = ".".join(parts[-2:])
                if base in DOMAIN_NAMES:
                    return True
            for key in DOMAIN_NAMES:
                if domain.endswith("." + key):
                    return True
    return False

# ========= СКАЧИВАНИЕ =========
async def fetch(session, url, sem):
    async with sem:
        try:
            print(f"Скачиваю: {url}")
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
    print(f"Обработано: {stats['processed']} | Найдено VLESS: {stats['found']}", end="\r")

# ========= ОЧИСТКА =========
async def clean_vless():
    print("\nОчищаю дубликаты и проверяю валидность...")
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
    print(f"Очистка завершена. Итоговых конфигов: {len(valid)}")

# ========= ФИЛЬТРАЦИЯ =========
async def filter_vless():
    print("\n=== Фильтрация по whitelist ===")
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
    print(f"\nФильтрация завершена. Итог: {passed} конфигов.")

# ========= ПЕРЕИМЕНОВАНИЕ =========
async def rename_configs():
    print("\n=== Переименование конфигов по протоколу и SNI ===")
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
    print(f"\nПереименование завершено. Итог: {processed} конфигов.")

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
        params = {}
        if params_part:
            for param in params_part.split('&'):
                if '=' in param:
                    k, v = param.split('=', 1)
                    params[k] = v
        encoded_params = []
        for k, v in params.items():
            if k in ['security', 'type', 'fp', 'pbk', 'sid', 'flow']:
                encoded_params.append(f"{k}={v}")
            else:
                try:
                    encoded_params.append(f"{k}={urllib.parse.quote(v, safe='')}")
                except:
                    encoded_params.append(f"{k}={v}")
        new_params = "&".join(encoded_params) if encoded_params else ""
        if fragment:
            try:
                if any(ord(c) > 127 for c in fragment):
                    encoded_fragment = urllib.parse.quote(fragment, safe='')
                else:
                    encoded_fragment = fragment
            except:
                encoded_fragment = fragment
        else:
            encoded_fragment = ""
        base = f"vless://{uuid}@{host_only}"
        if new_params:
            base += f"?{new_params}"
        if encoded_fragment:
            base += f"#{encoded_fragment}"
        return base
    except Exception as e:
        return url

async def encode_all_configs():
    print("\n=== Кодирование конфигов для Xray ===")
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
    print(f"\nКодирование завершено. Всего: {total}, изменено: {changed}")

# ========= XRAY-ТЕСТЕР С ФИЛЬТРАЦИЕЙ ПО ПИНГУ =========
class SimpleProgress:
    def __init__(self, total):
        self.total = total
        self.current = 0
        self.start_time = time.time()
        self.lock = threading.Lock()
        self.working_count = 0
        self.retry_count = 0
        self.rejected_count = 0  # Добавлен счетчик отклоненных по пингу
    
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
        print(f"\r✅ Готово! {self.current} конфигов за {elapsed:.1f}с ({self.current/elapsed:.1f} к/с), рабочих: {self.working_count}, отклонено по пингу: {self.rejected_count}, повторов: {self.retry_count}")

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
        self.max_ping_ms = max_ping_ms  # Максимальный допустимый пинг
        self.test_url = XRAY_TEST_URL
        self.timeout = XRAY_TIMEOUT
        self.max_retries = MAX_RETRIES
        self.retry_delay = RETRY_DELAY
        
        if platform.system() == 'Windows':
            self.xray_path = Path('./xray_bin/xray.exe')
        else:
            possible_paths = ['/usr/bin/xray', '/usr/local/bin/xray', './xray_bin/xray', '/opt/xray/xray']
            self.xray_path = None
            for path in possible_paths:
                if Path(path).exists():
                    self.xray_path = Path(path)
                    break
            if not self.xray_path:
                self.xray_path = Path('/usr/bin/xray')
        
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
                print(f"📋 Загружено {len(self.saved_urls)} уже сохраненных конфигов из {output_file}")
            except:
                pass
        
        print(f"🔍 XrayTester инициализирован")
        print(f"   📁 Входной файл: {self.input_file}")
        print(f"   📁 Выходной файл: {self.output_file}")
        print(f"   📁 Xray путь: {self.xray_path}")
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
                query = after_at[q_pos+1:]
            else:
                host_part = after_at
                query = ""
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
            params = {}
            if query:
                for param in query.split('&'):
                    if '=' in param:
                        k, v = param.split('=', 1)
                        try:
                            v = urllib.parse.unquote(v)
                        except:
                            pass
                        params[k] = v
            return {
                'uuid': uuid,
                'host': host,
                'port': port,
                'params': params,
                'url': url
            }
        except Exception as e:
            return None

    def create_xray_config(self, parsed, port):
        try:
            params = parsed['params']
            flow = params.get('flow', '')
            security = params.get('security', '')
            
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
                                "encryption": "none",
                                "flow": flow
                            }]
                        }]
                    },
                    "streamSettings": {
                        "network": params.get('type', 'tcp'),
                        "security": security
                    },
                    "tag": "proxy"
                }]
            }
            
            if security == 'reality':
                config["outbounds"][0]["streamSettings"]["realitySettings"] = {
                    "serverName": params.get('sni', parsed['host']),
                    "fingerprint": params.get('fp', 'chrome'),
                    "publicKey": params.get('pbk', ''),
                    "shortId": params.get('sid', ''),
                    "spiderX": params.get('spx', '/')
                }
            elif security == 'tls':
                config["outbounds"][0]["streamSettings"]["tlsSettings"] = {
                    "serverName": params.get('sni', parsed['host']),
                    "allowInsecure": True
                }
            
            if params.get('type') in ('ws', 'websocket'):
                config["outbounds"][0]["streamSettings"]["wsSettings"] = {
                    "path": params.get('path', '/'),
                    "headers": {"Host": params.get('host', params.get('sni', parsed['host']))}
                }
            
            if params.get('type') in ('grpc', 'gun'):
                config["outbounds"][0]["streamSettings"]["grpcSettings"] = {
                    "serviceName": params.get('servicename', params.get('service', '')),
                    "multiMode": True
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
                existing_fragment = re.sub(r'^[🇷🇺🇺🇸🇩🇪🇳🇱🇬🇧🇫🇷🇨🇦🇯🇵🇸🇬🇭🇰🇫🇮🇸🇪🇳🇴🇩🇰🇵🇱🇨🇿🇦🇹🇨🇭🇧🇪🇮🇹🇪🇸🇵🇹🇦🇺🇧🇷🇮🇳🇰🇷🇨🇳🇹🇼🇺🇦🇰🇿🇧🇾🇹🇷🇮🇱🇦🇪🇸🇦🇪🇬]+\s*', '', existing_fragment)
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
        # Проверяем пинг
        if ping > self.max_ping_ms:
            print(f"\n⏱️ ПРЕВЫШЕН ПИНГ: {ping:.0f}ms > {self.max_ping_ms}ms - конфиг НЕ добавлен")
            return False
        
        final_url = self.add_country_flag_to_url(url, country_code, protocol, ping, service_name)
        
        if final_url in self.saved_urls:
            return False
        
        try:
            with open(self.output_file, 'a', encoding='utf-8') as f:
                f.write(final_url + '\n')
            self.saved_urls.add(final_url)
            print(f"\n💾 СОХРАНЕНО: {final_url[:100]}...")
            return True
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
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

    def check_alternative_methods(self, parsed, url):
        host = parsed['host']
        port = parsed['port']
        params = parsed['params']
        security = params.get('security', '')
        sni = params.get('sni', host)
        
        tcp_ok = check_tcp_connection(host, port, timeout=2)
        if not tcp_ok:
            return None
        
        if security in ['reality', 'tls']:
            try:
                start = time.time()
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((host, port))
                ssl_sock = context.wrap_socket(sock, server_hostname=sni or host)
                ssl_sock.do_handshake()
                version = ssl_sock.version()
                ping = (time.time() - start) * 1000
                ssl_sock.close()
                sock.close()
                if version:
                    return {'working': True, 'ping': ping, 'method': 'tls_check'}
            except:
                pass
        
        return None

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
                        print(f"\n✅ РАБОТАЕТ: {parsed['host']} | Пинг: {ping:.0f}ms")
                        
                        if ping > self.max_ping_ms:
                            print(f"   ⏱️ Пинг {ping:.0f}ms превышает лимит {self.max_ping_ms}ms - пропускаем")
                            if progress:
                                progress.update('⏱️ пинг', working=False, rejected=True)
                            self.port_manager.release_port(port)
                            return None
                        
                        country_code = self.get_country_for_host(parsed['host'], parsed['port'])
                        if country_code:
                            print(f"   🌍 Страна: {get_country_name(country_code)} ({country_code})")
                        else:
                            print(f"   🌍 Страна: не определена")
                        
                        saved = self.save_working_config(url, ping, country_code, protocol, service_name)
                        if saved:
                            print(f"   💾 Конфиг сохранен в {self.output_file}")
                        else:
                            if ping <= self.max_ping_ms:
                                print(f"   ⚠️ Конфиг уже существует в {self.output_file}")
                        
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
        
        # Альтернативная проверка
        alt_result = self.check_alternative_methods(parsed, url)
        if alt_result and alt_result.get('working'):
            ping = alt_result.get('ping', 100)
            print(f"\n✅ РАБОТАЕТ (TLS): {parsed['host']} | Пинг: {ping:.0f}ms")
            
            if ping > self.max_ping_ms:
                print(f"   ⏱️ Пинг {ping:.0f}ms превышает лимит {self.max_ping_ms}ms - пропускаем")
                if progress:
                    progress.update('⏱️ пинг', working=False, rejected=True)
                return None
            
            country_code = self.get_country_for_host(parsed['host'], parsed['port'])
            if country_code:
                print(f"   🌍 Страна: {get_country_name(country_code)} ({country_code})")
            
            saved = self.save_working_config(url, ping, country_code, protocol, service_name)
            if saved:
                print(f"   💾 Конфиг сохранен в {self.output_file}")
            else:
                if ping <= self.max_ping_ms:
                    print(f"   ⚠️ Конфиг уже существует в {self.output_file}")
            
            if progress:
                progress.update('✅', working=True)
            return {'url': url, 'ping': ping, 'method': 'tls_check', 'country': country_code}
        
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
        print(f"⏱️ Таймаут: {self.timeout}с")
        print(f"📏 Максимальный пинг: {self.max_ping_ms}ms")
        print(f"📁 Результаты сохраняются в: {self.output_file}")
        print('='*60)
        
        if os.path.exists(self.debug_file):
            os.remove(self.debug_file)
        
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
        
        # Сортировка по пингу
        working.sort(key=lambda x: x['ping'])
        
        print(f"\n📊 Результаты:")
        print(f"   ✅ Работает и добавлено: {len(working)}")
        print(f"   📁 Всего сохранено в {self.output_file}: {len(self.saved_urls)} уникальных конфигов")
        print(f"   📏 Максимальный пинг: {self.max_ping_ms}ms")
        
        if working:
            print(f"\n📈 Топ-5 по пингу:")
            for i, w in enumerate(working[:5], 1):
                print(f"   {i}. {w['ping']:.0f}ms - {w.get('method', 'unknown')}")
        
        print('='*60 + '\n')
        
        return working

    def run(self):
        self.test_all()

# ========= ОСНОВНОЙ ЦИКЛ =========
async def main_cycle():
    global cycle_counter
    cycle_counter += 1
    print(f"\n{'='*60}")
    print(f"=== НОВЫЙ ЦИКЛ #{cycle_counter} ===")
    print(f"{'='*60}")
    
    if cycle_counter % CYCLES_BEFORE_DEBUG_CLEAN == 0:
        if os.path.exists(DEBUG_FILE):
            os.remove(DEBUG_FILE)
            print(f"🧹 Очищен {DEBUG_FILE} после {cycle_counter} циклов")
    
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
    
    if not os.path.exists(SOURCES_FILE):
        print(f"❌ Нет файла {SOURCES_FILE}")
        return
    
    try:
        with open(SOURCES_FILE, "r", encoding="utf-8", errors="ignore") as f:
            urls = [line.strip() for line in f if line.strip()]
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
        print(f"✅ Рабочие конфиги с пингом до {MAX_PING_MS}ms будут сохраняться в {WORK_FILE}")
        
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
            print(f"\n📊 ИТОГО РАБОЧИХ КОНФИГОВ В {WORK_FILE}: {total_working}")
    else:
        print("⏭️ Нет новых конфигов для обработки")

async def run_forever():
    print("\n🔄 Запуск бесконечного цикла...")
    print(f"⏱️ Каждый час будет выполняться проверка и добавление новых конфигов")
    print(f"📏 Максимальный пинг: {MAX_PING_MS}ms (конфиги с большим пингом НЕ сохраняются)")
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
            print(f"⏳ Ожидание 60 секунд перед перезапуском...")
            await asyncio.sleep(60)

if __name__ == "__main__":
    try:
        asyncio.run(run_forever())
    except KeyboardInterrupt:
        print("\n👋 Программа остановлена")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
