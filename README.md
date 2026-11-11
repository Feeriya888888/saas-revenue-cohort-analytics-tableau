 SaaS Revenue & Cohort Retention Analytics in Tableau

Продвинутый BI-проект по **Tableau Desktop / Tableau Server**, посвящённый продуктовой и финансовой аналитике B2B SaaS-платформы (*Subscription Revenue, Net Dollar Retention & Churn Analysis*).

## 1. Архитектура решения и бизнес-задача
Проект решает задачу сквозного мониторинга ключевых метрик подписочного бизнеса для CEO, CFO и Product-менеджеров:
* **Контроль выручки:** динамика MRR (Monthly Recurring Revenue), ARR (Annual Recurring Revenue) и среднего чека на клиента (ARPU).
* **Когортный анализ удержания:** оценка выживаемости платящих клиентов и удержания выручки (**Net Dollar Retention — NDR**) с помощью продвинутых LOD-выражений (`FIXED`, `INCLUDE`, `EXCLUDE`).
* **Декомпозиция изменений MRR (MRR Waterfall / Bridge):** расчёт New MRR, Expansion MRR (апсейлы), Contraction MRR (даунгрейды) и Churned MRR (отток) с использованием табличных вычислений (`LOOKUP`, `WINDOW_SUM`).

## 2. Стек технологий
* **BI & Визуализация:** Tableau Desktop 2024.x+ (LOD Expressions, Table Calculations, Dynamic Zone Visibility, Parameter Actions).
* **Подготовка данных:** Python (генерация реалистичного B2B SaaS датасета с когортным поведением) / PostgreSQL (витрина данных).

## 3. Структура репозитория
* `README.md` — документация проекта, описание логики вычислений и инструкция по сборке дашборда.
* `generate_saas_data.py` — скрипт генерации исторических данных по подпискам, платежам и апгрейдам тарифов за 24 месяца (готов к подключению в Tableau как `.csv` или загрузке в БД).
* `tableau_calculated_fields.md` — справочник всех продвинутых вычисляемых полей Tableau (LOD-выражения, табличные расчёты, динамические параметры).
* `saas_executive_dashboard.twb` — готовый XML-шаблон рабочей книги Tableau, подключённый к локальному файлу данных `saas_subscriptions_mart.csv`.

## 4. Пошаговая инструкция запуска
1. Сгенерируйте датасет для дашборда:
   ```bash
   python generate_saas_data.py
   ```
   В текущей директории появится файл `saas_subscriptions_mart.csv` (~15 000 записей).
2. Откройте файл `saas_executive_dashboard.twb` в **Tableau Desktop** (или загрузите в **Tableau Public**).
3. При запросе источника данных укажите сгенерированный файл `saas_subscriptions_mart.csv`.

## 5. Ключевые визуализации в дашборде
1. **Executive KPI Cards (BANs + Sparklines):** MRR, ARR, Net Dollar Retention (NDR %), Logo Churn Rate (%) со сравнением MoM (`▲ +4.2%`).
2. **MRR Movement Waterfall Chart:** каскадная диаграмма, показывающая вклад новых продаж, расширений (Expansion) и оттока (Churn) в итоговый прирост выручки.
3. **Cohort Retention Heatmap:** треугольная тепловая карта удержания клиентов и выручки по месяцам жизни когорты (`Month 0` — `Month 12`).
4. **Pareto Revenue Concentration (80/20 Curve):** кривая Лоренца для оценки зависимости бизнеса от крупных Enterprise-клиентов.
