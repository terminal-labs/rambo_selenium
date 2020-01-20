/home/{{ grains['user'] }}/selenium_work/sample.py:
  file.managed:
    - source: salt://code/sample.py
    - user: {{ grains['user'] }}
    - group: {{ grains['user'] }}
    - mode: 744

/home/{{ grains['user'] }}/selenium_work/build_bot.py:
  file.managed:
    - source: salt://code/build_bot.py
    - user: {{ grains['user'] }}
    - group: {{ grains['user'] }}
    - mode: 744
