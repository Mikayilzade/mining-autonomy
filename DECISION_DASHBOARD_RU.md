# Mining Autonomy — панель решений

**Обновлено:** 29.08.2026  
**Назначение:** понятная русская сводка по уже выполненному исследованию и текущей реализации. Это не новый discovery-проход и не разрешение на реальные денежные действия.

## Сводка за 30 секунд

- **Реальная прибыль пока не доказана.**
- **Discovery завершён: Runs 001–062.**
- Основной shortlist:
  1. PayanAgent
  2. OKX.AI A2A ASP
  3. agent2agent.market
  4. AgentGigs.io
  5. MCPize
  6. OKX.AI A2MCP
  7. API Mart
  8. Compute / inference suppliers
- **PayanAgent** остаётся кандидатом №1, но I002 не доказал реальный количественный поток оплачиваемых заявок.
- **OKX.AI A2A** — кандидат №2, но I003 не подтвердил анонимно доступный live-feed задач.
- **Не хватает реальной себестоимости работы на твоём ПК.** I181 ещё не выполнен на реальной машине.
- **Resource / Execution Router уже реализован и укреплён до I196.**
- Сейчас бутылочное горлышко — реальные данные, а не архитектура.

## Что делать сейчас

| Решение | Статус | Рекомендация |
|---|---|---|
| Снова открывать широкий поиск идей | **НЕТ** | Не надо |
| Запустить I181 на своём ПК | **ДА — локально, без затрат** | **Следующий шаг** |
| Покупать ваттметр / счётчик | **НЕТ** | Не покупать |
| Разрешить bounded read-only наблюдение реальных рынков | **РЕШЕНИЕ ПОЛЬЗОВАТЕЛЯ** | Полезно для следующего шага |
| Платить за API / VPS / GPU / аккаунты | **НЕТ** | Пока не тратить |
| Принимать/выполнять платную задачу или двигать деньги | **НЕТ** | Пока рано |

## Где мы находимся

```text
Большой список вариантов заработка
        ↓
Discovery Runs 001–062 — ЗАВЕРШЁН
        ↓
I001 — shortlist из 8 основных кандидатов
        ↓
#1 PayanAgent
#2 OKX.AI A2A
        ↓
I002 / I003 — реальный спрос пока не подтверждён
        ↓
Cross-market evaluator + Resource / Execution Router реализованы
        ↓
Реальная себестоимость выполнения: НЕТ ДАННЫХ
Реальные payout / acceptance / failures / fees: НЕТ ДАННЫХ
Read-only production authorization: FALSE
        ↓
Подтверждённый прибыльный маршрут: ПОКА НЕТ
        ↓
Первый реальный денежный тест: ЕЩЁ НЕ ГОТОВ
```

## Топ-кандидаты

### 1. PayanAgent

**Модель:** machine-to-machine рынок задач / запросов.

**Почему №1:** API-first модель request → bid → fulfil → settlement лучше всего соответствует исходной идее: бот наблюдает рынок, отбирает задачи, считает себестоимость и выполняет только выгодные.

**Что уже известно:**
- есть machine-readable механика;
- есть requests/bids/fulfil;
- есть публичные claims по offers / receipts;
- подходит под полностью автономный сценарий.

**Что не доказано:**
- реальный текущий поток оплачиваемых bespoke-задач;
- реальные суммы выплат;
- конкуренция и вероятность получения задачи;
- acceptance / rejection / dispute / non-payment;
- полные комиссии и маржа.

**Статус:** **главный кандидат, но прибыльность не доказана**.

### 2. OKX.AI A2A ASP

**Модель:** агент/провайдер может смотреть открытые задачи, договариваться о цене, выполнять заказ и получать оплату через escrow.

**Сильные стороны:**
- очень хорошее совпадение с исходной идеей;
- open-task / negotiation / escrow / approval workflow;
- технически подходит под автономную обработку задач.

**Блокеры:**
- анонимный live-feed задач не подтверждён;
- onboarding / geography / KYC не закрыты;
- реальный объём задач и цены неизвестны.

**Статус:** **кандидат №2, но экономика неизвестна**.

### 3. agent2agent.market

Архитектура хорошо подходит: register → browse → accept → submit → receive payment.

Проблема: в наблюдавшемся snapshot было **0 открытых задач / 0 активности** на Base Sepolia.

**Статус:** WATCHLIST.

### 4. AgentGigs.io

Есть REST API + webhooks/SSE + escrow/payout.

Проблема: в публичном jobs snapshot было **0 total/open jobs**. Плюс Stripe Connect / KYC / география выплат.

**Статус:** WATCHLIST / GEO-GATED.

### 5. MCPize

**Модель:** не искать задачи, а разместить собственный MCP/микросервис и получать деньги за вызовы.

Плюсы:
- build once;
- можно автоматизировать обслуживание;
- потенциально пассивнее task-market модели.

Минусы:
- buyer demand не доказан;
- platform fee;
- payout/KYC;
- hosting/model/API cost может съесть маржу.

**Статус:** сильный пассивный резервный вариант.

### 6. OKX.AI A2MCP

**Статус:** вторичный passive target.  
Спрос пока не измерен; есть wallet/review/x402 зависимости.

### 7. API Mart

Слабые доказательства спроса, upstream rights, wallet/geography, неизвестная маржа.

**Статус:** PARKED.

### 8. Compute / inference suppliers

Сюда входят GPU/CPU provider, inference provider, compute marketplace, storage/bandwidth provider.

Здесь критична реальная себестоимость:
- электричество;
- загрузка;
- maintenance;
- availability;
- opportunity cost;
- payout;
- job supply / utilization.

**Статус:** DEFERRED до I181 и реальной local-cost модели.

## Что ещё было исследовано

- Golem / Akash и другие compute providers;
- Vast / Nosana / Golem GPU / io.net / Salad и другие GPU/AI providers;
- AI incentive networks;
- transcoding;
- Storj / Sia / Filecoin и storage;
- bandwidth / VPN / relay nodes;
- blockchain validators / RPC / indexers;
- ZK/prover markets;
- keeper / solver infrastructure;
- machine-to-machine task markets;
- домашний CPU/GPU/bandwidth/storage;
- DePIN;
- доходность на капитал;
- automated trading families;
- micro-SaaS / API / цифровые продукты / лицензирование;
- слабые/сомнительные варианты вроде faucets, ad-clicking, human microtask botting и cloud-mining сайтов.

## Resource / Execution Router — что уже умеет система

| Backend | Решение |
|---|---|
| Python / deterministic local | **Использовать первым, если достаточно** |
| Собственный ПК CPU/GPU/local model | **Сначала измерить I181** |
| ChatGPT/Codex subscription | Использовать для проектной работы, не считать автономным unlimited API |
| Бесплатный CI/cloud tier | Использовать выборочно |
| Дешёвый внешний LLM/API | Пока не активировать |
| Более сильный дорогой API | Только если дешёвый backend не проходит |
| Будущий VPS/server | Не арендовать до подтверждения прибыли |

Главный принцип:

**дешёвый deterministic filter → local/deterministic execution → AI только если нужен → самый дешёвый backend, который даёт достаточную вероятность успеха и положительную консервативную маржу.**

## Два главных недостающих блока

### A. Реальная себестоимость исполнения

Нужно:

1. Запустить **I181 на реальном ПК**.
2. Проверить наличие встроенного cumulative energy counter.
3. Если его нет — I182 только с уже имеющимся надёжным внешним whole-system meter.
4. Добавить:
   - реальный тариф электричества;
   - availability;
   - opportunity cost;
   - ownership confirmation;
   - UTC observed_at.
5. После этого прогнать I178/I179.

Если надёжного измерения энергии нет — **не придумывать и не оценивать приблизительно**.

### B. Реальная рыночная выручка

Нужно измерить:

- сколько реально появляется задач;
- бюджеты / payout;
- насколько быстро они исчезают;
- конкуренцию;
- вероятность получить задачу;
- approval/rejection;
- retries / failures;
- platform fees;
- payment / withdrawal / gas / conversion;
- dispute / non-payment;
- watcher overhead;
- human maintenance time.

Пока разрешение на bounded read-only production observation = **false**.

## Когда можно будет тестировать реальный заработок

Только если реальные данные покажут:

```text
ожидаемая реально получаемая выручка
- platform/payment/withdrawal/conversion
- marginal execution cost
- retries/failures
- maintenance/human time
- watcher overhead
- allocated non-sunk fixed cost
- opportunity cost
- dispute/non-payment risk
> положительный безопасный порог прибыли
```

И даже после этого отдельное разрешение требуется для регистрации, credentials, KYC, кошельков, принятия задачи, публикации сервиса, расходов, settlement и движения денег.

## Что я бы сделал сейчас

1. **Не тратить деньги.**
2. **Закрыть I181 на твоём ПК.**
3. **Оставить PayanAgent №1, OKX.AI A2A №2.**
4. Для рыночной ветки отдельно разрешить только **bounded read-only public observation** без аккаунтов, KYC, credentials, принятия задач и денег.
5. Первый реальный платный тест делать только тогда, когда ключевые `UNKNOWN` заменены реальными измерениями и Router показывает положительную консервативную маржу.

## Итог

Проект уже не на стадии «ищем идеи».

Он на стадии:

**«система выбора и экономика готовы; теперь нужны реальные данные о себестоимости и реальном спросе, чтобы понять, где действительно есть деньги».**
