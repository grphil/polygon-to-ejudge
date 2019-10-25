# polygon-to-ejudge
polygon-to-ejduпу это скрипт, который импортиирует задачи и контесты из полигона в ejudge, поддерживая более расширенную функциональнось, по сравнению с обычным встроенным в ejudge скриптом импорта.

На данный момент поддерживается импорт, обновление и удаление задач и контестов в ejudge. 

Если в polygon были включенны баллы, то для задачи создаётся valuer.cfg и если контест имеет олимпиалный тип (не acm), то соответствующие valuer настройки сразу переносятся в serve.cfg.

Так же скрипт импортирует условие и переводит все теховские формулы в формат mathjax. При этом условие на обязательно должно компилироваться в html в polygon и, например, таблицы тоже переносятся. При это никакие картинки и дополнительные к условию файлы пока не поддерживаются.

## Требования

* Python3
* [polygon-cli](https://github.com/kunyavskiy/polygon-cli)

Если нужен импорт условий, то дополниительно нужно:

* [pandoc](https://pandoc.org/)
* В папке установки ejudge (EJUDGE_PREFIX) надо в файл `share/ejudge/csp/contests/unpriv_header.csp` добавить импорт скрипта mathjax, чтобы формулы корректно отображались. Проверенно, что если добавить строки

```
<script type="text/x-mathjax-config">
MathJax.Hub.Config({
    CommonHTML: {
        scale: 80
    },
    showMathMenu: false
});
</script>
<script type="text/javascript" async src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-MML-AM_CHTML"></script>
```
Внутрь `<head>` тега, то всё работает корректно.

## Настройка

В `polygon_to_ejudge/config.py` надо установиить
* `JUDGES_DIR` равным путю к папке `judges`
* `GVALUER_LOCATION` равным путю к скомпилированной программе gvaluer. Это не обязательно делать если задачи с баллами ипортироваться не будут.
* `CREATE_STATEMENTS` равным False, если не надо создавать условия для задач

## Использование

Для запуска надо использовать `run.py`. 

При этом чтобы сменить аккаунт на polygon надо использовать `./run.py logout`.