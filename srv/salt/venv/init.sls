/home/{{ grains['user'] }}/selenium_work:
  file.directory:
    - user: {{ grains['user'] }}
    - makedirs: True

install_venv:
  cmd.run:
    - name: virtualenv /home/{{ grains['user'] }}/selenium_work
    - cwd: /home/{{ grains['user'] }}/selenium_work
    - user: {{ grains['user'] }}
