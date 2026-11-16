# ДЗ 2–5: пошагово в одном репозитории

Все команды ниже — для **PowerShell** (в том числе терминала VS Code).
Итог: четыре папки в `main` репозитория https://github.com/forfeiture67/mlops.
Первое занятие остаётся в корне. Для каждого ДЗ будет свой коммит, а не новый репозиторий.
Выполняйте блоки по порядку; после ошибки сначала разберитесь с ней, затем продолжайте.

## 1. Скачать свой репозиторий

Если репозитория ещё нет на компьютере:

```powershell
New-Item -ItemType Directory -Force "$HOME\Projects" | Out-Null
Set-Location "$HOME\Projects"
git clone https://github.com/forfeiture67/mlops.git
Set-Location mlops
```

Если он уже есть, откройте **его существующую папку** в VS Code → Terminal → New Terminal.
Повторно клонировать в неё не нужно. Проверьте:

```powershell
git remote -v
git status
git branch --show-current
```

Адрес origin должен содержать `forfeiture67/mlops`. Если есть незакоммиченные свои
изменения, сначала сохраните их обычным коммитом — `pull`/переключение веток выполняйте
с чистым рабочим деревом. Далее:

```powershell
git switch main
git pull --ff-only origin main
```

Если Git впервые просит имя/email при коммите, задайте **свои** данные в этом репозитории:
`git config user.name "Ваше имя"` и `git config user.email "Ваш email GitHub"`.
Текст в кавычках здесь нужно заменить. Данные другого автора использовать не требуется.

## 2. Перенести подготовленные файлы

Распакуйте архив MLOps_HW2_HW5.zip. Откройте находящуюся внутри папку `mlops_homework`.
**Скопируйте её содержимое** в корень своего клонированного `mlops`:
папки `hw02`, `hw03`, `hw04`, `hw05`, файл `requirements-mlops.txt`,
`pytest.ini`, `.coveragerc`, `.gitignore`, `.gitattributes` и Markdown-инструкции.
Папку `mlops_homework` целиком внутрь `mlops` создавать не надо.

В архиве нет чужой папки `.git` и нет файлов ДЗ 1. Исходные `main.py`,
`pyproject.toml`, `uv.lock`, `.python-version`, `README.md` вашего ДЗ 1 сохраняются.
В `.gitignore` сохранены исходные правила и добавлены исключения для результатов новых ДЗ.
Если вы уже дописывали свои правила, объедините их с новыми.
В `.gitattributes` также сохраните собственные правила, если этот файл уже появился у вас.

Ожидаемая структура: `mlops/hw03/dvc.yaml`, `mlops/hw04/train.py`, `mlops/hw05/train_mlflow.py`.
Проверьте, что скопировались скрытые служебные файлы, особенно `hw03/.dvc/config`.

## 3. Подготовить Python и зависимости

Нужен установленный Python **3.12 x64**. Проверка и создание отдельного окружения:

```powershell
py -3.12 --version
py -3.12 -m venv .venv-mlops
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv-mlops\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install torch==2.15.0 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements-mlops.txt
```

CPU-версия PyTorch достаточна, видеокарта не нужна. Установка остальных зависимостей
может занять несколько минут. `Set-ExecutionPolicy` действует только в текущем окне.
Если политика компьютера запрещает активацию, вместо `python` используйте
`.\.venv-mlops\Scripts\python.exe`, вместо `dvc` — `.\.venv-mlops\Scripts\dvc.exe`,
вместо `mlflow` — `.\.venv-mlops\Scripts\mlflow.exe` **из корня репозитория**.
Для команд внутри hw03 путь к окружению начинается с `..\`.

При каждом новом открытии терминала из корня репозитория достаточно:

```powershell
.\.venv-mlops\Scripts\Activate.ps1
```

Проверка:

```powershell
python --version
python -c "import torch, mlflow; print(torch.__version__, mlflow.__version__)"
dvc version
```

Сначала закоммитьте общую инфраструктуру. Это позволит выполнять ДЗ 2 с чистым деревом:

```powershell
git add .gitignore .gitattributes .coveragerc pytest.ini requirements-mlops.txt HOMEWORKS.md GUIDE_WINDOWS.md VERIFICATION.md REFERENCES.md
git commit -m "chore: add shared MLOps homework setup"
```

Остальные папки пока будут untracked — это нормально: в коммиты добавляем явно указанные пути.

## 4. ДЗ 2 — Git, ветки, конфликт

Все команды — из корня `mlops`. Сначала создайте и закоммитьте начальные файлы:

```powershell
Set-Content -Path hw02/sample.txt -Value @('collect data', 'prepare data', 'train model') -Encoding ascii
Set-Content -Path hw02/conflict.txt -Value 'base' -Encoding ascii
git add hw02
git diff --cached
git commit -m "hw02: add initial Git practice files"
```

Покажем создание и удаление вспомогательного файла отдельными коммитами:

```powershell
Set-Content -Path hw02/temporary.txt -Value 'temporary experiment' -Encoding ascii
git add hw02/temporary.txt
git commit -m "hw02: add temporary file"
git rm hw02/temporary.txt
git commit -m "hw02: remove temporary file"
```

Создайте временную ветку и измените строку:

```powershell
git switch -c hw02-conflict
Set-Content -Path hw02/conflict.txt -Value 'feature' -Encoding ascii
git add hw02/conflict.txt
git commit -m "hw02: change conflict line in feature branch"
```

Перейдите в `main` и измените ту же строку иначе:

```powershell
git switch main
Set-Content -Path hw02/conflict.txt -Value 'main' -Encoding ascii
git add hw02/conflict.txt
git commit -m "hw02: change conflict line in main"
git merge hw02-conflict
```

**Здесь ожидается CONFLICT.** Это часть упражнения. Чтобы разрешить конфликт,
замените содержимое файла согласованным вариантом и завершите merge:

```powershell
Get-Content hw02/conflict.txt
Set-Content -Path hw02/conflict.txt -Value 'main + feature' -Encoding ascii
git add hw02/conflict.txt
git commit -m "hw02: resolve merge conflict"
git branch -d hw02-conflict
git log --graph --oneline --all -12
git push origin main
```

Временная ветка удалена, merge-коммит и оба изменения остались в истории `main`.
Новые репозитории не создавались. Повторно этот сценарий с теми же файлами не запускайте:
он рассчитан на первое выполнение. Ссылка для сдачи:
https://github.com/forfeiture67/mlops/tree/main/hw02

## 5. ДЗ 3 — DVC с локальным remote

Перейдите из корня в папку ДЗ:

```powershell
Set-Location hw03
```

Папка `.dvc` уже включена в архив. Поэтому `dvc init` повторно не нужен.
При самостоятельном создании проекта с нуля здесь использовалась бы команда
`dvc init --subdir`, потому что Git-репозиторий находится уровнем выше.

Создайте данные, настройте remote и запустите четыре стадии:

```powershell
python -m pipeline.make_data
dvc add data/raw.csv
New-Item -ItemType Directory -Force ../../mlops-dvc-storage | Out-Null
dvc remote add -f -d local ../../mlops-dvc-storage
dvc repro --force
dvc dag
dvc metrics show
dvc push
dvc status
```

`--force` нужен для первого локального воспроизведения: в архиве уже есть `dvc.lock`,
но ваш компьютер ещё не имеет кэша. Дальше используйте обычный `dvc repro`:
он пропускает неизменившиеся стадии. `dvc push` переносит данные и модель в
соседнюю папку `mlops-dvc-storage`; `git push` ниже отправляет код и метаданные в GitHub.
Это разные операции.

Ожидаемые значения по исходным параметрам: MAE ≈ 0.737621, RMSE ≈ 0.998612,
R² ≈ 0.994492. `dvc status` должен сообщить, что данные и пайплайн актуальны.
Повторный запуск:

```powershell
dvc repro
```

Теперь проверка восстановления **одного сгенерированного файла**:

```powershell
Remove-Item data/clean.csv
dvc pull
Test-Path data/clean.csv
```

Последняя команда должна вывести `True`. Эта проверка показывает восстановление
рабочего файла; полная проверка с пустым локальным кэшем уже выполнена при подготовке.

Чтобы показать изменение параметров, откройте `params.json` и измените
`"test_ratio": 0.2` на `0.25`, сохраните файл, выполните `dvc repro` и `dvc metrics show`.
Стадия prepare останется прежней, split/train/evaluate пересчитаются.
Затем верните `0.2`, снова выполните `dvc repro` и `dvc push`, чтобы получить
исходные контрольные суммы. Этот эксперимент опционален.

Вернитесь в корень, закоммитьте код и DVC-метаданные:

```powershell
Set-Location ..
git add hw03 .gitignore .gitattributes
git diff --cached --stat
git commit -m "hw03: add reproducible DVC pipeline and local remote"
git push origin main
```

CSV и модель не попадут в Git: DVC добавил для них правила `.gitignore`.
В Git должны быть `.dvc/config`, `.dvc/.gitignore`, `.dvcignore`, `raw.csv.dvc`,
`dvc.yaml`, `dvc.lock`, код, параметры и небольшой `metrics.json`.

Локальный remote **не доступен преподавателю автоматически**. По условию он разрешён.
README объясняет, как заново создать те же данные и пайплайн без доступа к вашему диску.
Если преподавателю нужен именно `dvc pull` со своего компьютера, потребуется
общедоступный/выданный ему доступ к удалённому хранилищу; локальная папка этого не обеспечивает.

Ссылка: https://github.com/forfeiture67/mlops/tree/main/hw03

## 6. ДЗ 3 — сравнить Git и Git LFS в том же репозитории

Основное описанное требование ДЗ 3 уже выполнено DVC-пайплайном.
Этот раздел воспроизводит дополнительный LFS-пример из присланных репозиториев.
Git LFS обычно входит в Git for Windows. Проверка из корня:

```powershell
git lfs version
git lfs install
```

Если команда `git lfs` не найдена, установите Git LFS и повторите проверку.
Далее обе версии файла будем коммитить в `main`. Каждый файл — всего 2 MiB:

```powershell
python hw03/make_lfs_files.py --version 1
git lfs track "hw03/lfs_demo/with-lfs.bin"
git add .gitattributes
git add -f hw03/lfs_demo/plain.bin hw03/lfs_demo/with-lfs.bin
git commit -m "hw03: compare regular Git and LFS binary version 1"
```

Генератор создаёт одинаковое содержимое двух файлов, поэтому сравнение корректно.
`-f` указан только для этих двух учебных файлов: общие правила игнорируют бинарные файлы.
Теперь посмотрите, что реально хранится в Git:

```powershell
git lfs ls-files
git show HEAD:hw03/lfs_demo/with-lfs.bin
git cat-file -s HEAD:hw03/lfs_demo/plain.bin
git cat-file -s HEAD:hw03/lfs_demo/with-lfs.bin
```

Для обычного файла размер Git-объекта — `2097152` байта. Для LFS — короткий текстовый
указатель (около 130 байт), содержащий `version`, `oid sha256:...`, `size 2097152`.
Рабочая копия LFS-файла при этом по-прежнему содержит полноценные 2 MiB.
Размеры сравнивают **Git-объекты**, а не суммарное занимаемое место с учётом LFS-хранилища.

Создайте вторую версию и повторите:

```powershell
python hw03/make_lfs_files.py --version 2
git add hw03/lfs_demo/plain.bin hw03/lfs_demo/with-lfs.bin
git commit -m "hw03: update regular Git and LFS binaries to version 2"
git show HEAD~1:hw03/lfs_demo/with-lfs.bin
git show HEAD:hw03/lfs_demo/with-lfs.bin
git push origin main
```

OID должен измениться. LFS-объекты передаются при `git push` установленным LFS-hook.
Не удаляйте `.gitattributes` после этого. При клонировании с установленным LFS
содержимое подтягивается автоматически; при необходимости — `git lfs pull`.
Если GitHub отказывает из-за лимитов LFS, основная часть ДЗ 3 с DVC остаётся выполненной,
а отправку LFS-объектов нужно завершить после решения вопроса с доступным хранилищем.

## 7. ДЗ 4 — код и тесты всего ML-пайплайна

Из корня репозитория:

```powershell
python -m hw04.train --epochs 10
python -m pytest hw04/tests -v --cov=hw04 --cov-report=term-missing
```

Ожидается **11 passed**. Тесты: блок, модель и backward, данные, батчи,
изменение весов, обучение на малой выборке, воспроизводимость, запуск CLI,
сохранение и повторная загрузка модели. Присутствуют unit → integration → E2E,
а также отдельные marks для data/training/property.

Можно показать преподавателю группы отдельно:

```powershell
python -m pytest hw04/tests -m unit -v
python -m pytest hw04/tests -m data -v
python -m pytest hw04/tests -m integration -v
python -m pytest hw04/tests -m training -v
python -m pytest hw04/tests -m property -v
python -m pytest hw04/tests -m e2e -v
```

Сохраните собственный короткий отчёт после запуска модели:

```powershell
New-Item -ItemType Directory -Force hw04/results | Out-Null
Copy-Item hw04/artifacts/metrics.json hw04/results/metrics.json
python -m pytest hw04/tests --junitxml=hw04/results/pytest.xml
```

Зафиксируйте именно ДЗ 4:

```powershell
git add hw04 pytest.ini .coveragerc
git diff --cached --stat
git commit -m "hw04: implement digits pipeline and unit-to-e2e tests"
git push origin main
```

Модель и временные каталоги не коммитятся. Результаты вашего запуска в results — коммитятся.
Ссылка: https://github.com/forfeiture67/mlops/tree/main/hw04

## 8. ДЗ 5 — MLflow

Из корня репозитория, **последовательно**, дождитесь завершения каждой команды:

```powershell
$env:MLFLOW_DISABLE_TELEMETRY = "true"
python -m hw05.train_mlflow
python -m hw05.train_artifacts
python -m hw05.train_autolog --epochs 5
python -m hw05.search_runs
python -m pytest hw05/tests -v
```

Первые два скрипта создают по три запуска с разными lr/hidden.
Первый логирует параметры и метрики, второй ещё и картинки, описание, JSON и модель.
Третий демонстрирует autolog для Lightning с отдельной validation-выборкой.
Четвёртый выводит сравнительную таблицу и записывает `hw05/results/experiments.csv`.
Последняя команда — **1 passed**: реальная запись в MLflow и загрузка модели.
Ваши новые run_id и отчёты заменят приложенные примеры результатов.

Откройте интерфейс MLflow:

```powershell
mlflow ui --backend-store-uri sqlite:///hw05/mlflow.db --host 127.0.0.1 --port 5000 --workers 1
```

В браузере: http://127.0.0.1:5000. Откройте `digits-mlops`, выделите несколько запусков,
нажмите Compare, посмотрите `test_accuracy`, кривую `train_loss`, параметры `lr`, `hidden`.
В запусках `artifacts-*` откройте Artifacts: loss.png, predictions.png, model_summary.txt,
metrics.json. Модели MLflow 3 также отображаются в Logged Models/Models.
В `digits-autolog` проверьте автоматические метрики `train_loss`, `val_loss`, `val_accuracy`,
`test_accuracy` и залогированную модель.
При желании сохраните скриншоты интерфейса в `hw05/results` для сдачи.
Остановите UI сочетанием Ctrl+C, затем:

```powershell
git add hw05
git diff --cached --stat
git commit -m "hw05: add MLflow tracking artifacts autolog and run comparison"
git push origin main
```

База `hw05/mlflow.db` и локальные модели `hw05/mlartifacts` игнорируются Git.
В репозитории остаются код и лёгкие отчёты; база с абсолютными локальными путями
не переносится на другой компьютер. Для воспроизведения запустите те же команды.
Ссылка: https://github.com/forfeiture67/mlops/tree/main/hw05

## 9. Итоговая проверка и дальнейшие домашки

```powershell
git branch --show-current
git status
python -m pytest -q
python -m ruff check hw03 hw04 hw05
git log --graph --oneline --all -20
git push origin main
```

Должна быть ветка `main`, **12 passed**, проверка ruff без ошибок.
Если Git сообщает `nothing to commit, working tree clean`, всё закоммичено.
На GitHub откройте https://github.com/forfeiture67/mlops и убедитесь, что видны четыре папки.
Для будущего ДЗ достаточно создать новую папку, например hw06, и выполнить
`git add hw06`, `git commit -m "hw06: ..."`, `git push origin main`.
Отдельная ветка или репозиторий для каждого ДЗ не обязательны.

Если `push` отклонён, потому что удалённая ветка обновилась, с чистым рабочим деревом
выполните `git pull --rebase origin main`, разрешите возможные конфликты и повторите
`git push origin main`. После такого rebase граф учебного merge может измениться;
для сохранения исходного merge-графа можно вместо rebase использовать обычное слияние
`git pull --no-rebase origin main`. `push --force` для этой работы не нужен.
