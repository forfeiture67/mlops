# ДЗ 5. MLflow

Запускать из корня репозитория последовательно:

```powershell
$env:MLFLOW_DISABLE_TELEMETRY = "true"
python -m hw05.train_mlflow
python -m hw05.train_artifacts
python -m hw05.train_autolog --epochs 5
python -m hw05.search_runs
mlflow ui --backend-store-uri sqlite:///hw05/mlflow.db --host 127.0.0.1 --port 5000 --workers 1
```

Открыть http://127.0.0.1:5000. Остановить UI: Ctrl+C.
Первый запуск создаёт SQLite-базу: дождитесь его окончания перед следующим скриптом.
Отдельный запущенный сервер для записи не требуется — скрипты работают с SQLite напрямую.

| Скрипт | Результат |
|---|---|
| train_mlflow | Три запуска: lr, hidden, epochs, seed, train_loss по эпохам, test_accuracy |
| train_artifacts | Дополнительно: loss.png, predictions.png, model_summary.txt, metrics.json, модель с signature |
| train_autolog | Lightning; автоматические параметры, train/validation/test метрики и модель |
| search_runs | Сортировка запусков по test_accuracy и CSV в results/experiments.csv |

В ручных запусках сравниваются (lr=0.01, hidden=32), (0.001, 32), (0.01, 64),
по 10 эпох. Это демонстрация tracking; после выбора конфигурации по test_accuracy
эта же оценка уже не является независимой итоговой оценкой выбранной модели.
В Lightning используется дополнительное validation-разделение внутри train;
исходная test-часть проверяется только после fit.

Основной эксперимент: `digits-mlops`. Автоматическое логирование: `digits-autolog`.
База `mlflow.db` и каталог моделей `mlartifacts` локальные и игнорируются Git.
База содержит пути к артефактам конкретного компьютера, поэтому не включается в поставку.
`results` содержит выполненные здесь запуски; новые команды пересоздадут отчёты
с вашими run_id. Метрики могут немного отличаться между платформами и версиями.

Дополнительный тест `python -m pytest hw05/tests -v` проверяет настоящую запись
параметров/метрик/артефактов во временную SQLite и совпадение предсказаний
загруженной модели в native и pyfunc форматах.

Для загрузки native-модели используйте корень этого же репозитория: классы
модели определены в модуле hw04.
