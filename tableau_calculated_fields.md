# Справочник продвинутых вычисляемых полей (Tableau Calculated Fields)

Ниже приведены формулы уровня **Senior BI Analyst**, реализованные в проекте.

---

## 1. Уровни детализации (LOD Expressions)

### `Cohort Month (LOD)` — Фиксация месяца привлечения клиента
Гарантирует корректную привязку клиента к когорте независимо от фильтров на листе:
```tableau
{ FIXED [Customer Id] : MIN(DATETRUNC('month', [Billing Month])) }
```

### `Cohort Initial Customers` — Размер когорты на старте (Month 0)
Используется в знаменателе для расчёта процента удержания клиентов (Logo Retention %):
```tableau
{ FIXED [Cohort Month] : COUNTD(IF [Months Since Signup] = 0 THEN [Customer Id] END) }
```

### `Cohort Initial MRR` — Стартовая выручка когорты (Month 0)
Используется в знаменателе для расчёта **Net Dollar Retention (NDR %)**:
```tableau
{ FIXED [Cohort Month] : SUM(IF [Months Since Signup] = 0 THEN [Mrr Amount] END) }
```

### `Customer Lifetime Value (Actual LTV)` — Фактическая накопленная выручка с клиента
```tableau
{ FIXED [Customer Id] : SUM([Mrr Amount]) }
```

---

## 2. Когортные метрики (Retention & NDR)

### `Logo Retention %` — Процент удержания клиентов
```tableau
COUNTD(IF [Is Active] = 1 THEN [Customer Id] END) / MAX([Cohort Initial Customers])
```

### `Net Dollar Retention (NDR %)` — Чистое удержание выручки с учётом апсейлов
Значение > 100% означает, что апсейлы перекрывают отток внутри когорты:
```tableau
SUM([Mrr Amount]) / MAX([Cohort Initial MRR])
```

---

## 3. Табличные вычисления (Table Calculations)

### `MRR MoM Growth %` — Помесячный темп роста выручки
Настройка: *Compute Using -> Table (Across)* по оси `Billing Month`:
```tableau
(SUM([Mrr Amount]) - LOOKUP(SUM([Mrr Amount]), -1)) / ABS(LOOKUP(SUM([Mrr Amount]), -1))
```

### `Running Total % of Revenue` — Кривая Парето (80/20)
Настройка: *Compute Using -> Customer Id* (сортировка по убыванию `SUM([Mrr Amount])`):
```tableau
RUNNING_SUM(SUM([Mrr Amount])) / TOTAL(SUM([Mrr Amount]))
```

### `3-Month Moving Average MRR` — Сглаженный тренд выручки
```tableau
WINDOW_AVG(SUM([Mrr Amount]), -2, 0)
```

---

## 4. Динамическая интерактивность (Parameters & Dynamic Switch)

### Параметр `[p_Selected_Metric]`
* Тип данных: `String`
* Допустимые значения: `"MRR"`, `"ARR"`, `"Active Customers"`, `"ARPU"`

### Вычисляемое поле `[Dynamic KPI Measure]`
```tableau
CASE [p_Selected_Metric]
    WHEN "MRR" THEN SUM([Mrr Amount])
    WHEN "ARR" THEN SUM([Mrr Amount]) * 12
    WHEN "Active Customers" THEN COUNTD(IF [Is Active] = 1 THEN [Customer Id] END)
    WHEN "ARPU" THEN SUM([Mrr Amount]) / NULLIF(COUNTD(IF [Is Active] = 1 THEN [Customer Id] END), 0)
END
```
