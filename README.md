# **simple forum API**

порядок запуска API (поднимается вместе с базой):
* ставим docker (docker-compose) на машину
* смотрим в docker-compose в корне проекта на порты, чтобы не были в 
использовании на машине (default: postgresql: 5430, forum-api: 8080)
* создаем venv (python3 -m venv $(PATHTOENV)), включаем его 
(. activate в $(PATHTOENV)/bin), ставим проект 
(pip3 install .$(PATHTOPROJECTROOT))
* все готово - запускаем тесты pytest $(PATHTOPROJECTROOT)/tests/test_api_v1.py