Docker-update
=========

Роль для обновления docker на Nomad worker.

Requirements
------------

Запускать обновление поочереди только на одном Nomad worker,
чтобы контейнеры смогли перехать на свободные воркеры.

Role Variables
--------------

vars/main.yml
templates/daemon.json.v.X.X.j2

Example Playbook
----------------

ansible-playbook -i hosts docker-update.yml

docker-update.yml:
    - hosts: nomad1
      roles:
         - docker-update
