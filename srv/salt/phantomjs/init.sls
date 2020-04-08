phantomjs_dependencies:
  pkg.installed:
    - pkgs:
      - build-essential
      - chrpath
      - libssl-dev
      - libxft-dev
      - libfreetype6
      - libfreetype6-dev
      - libfontconfig1
      - libfontconfig1-dev

create_downloads_dir:
  cmd.run:
    - name: mkdir -p /tmp/downloads
    - user: {{ grains['user'] }}

download_phantomjs:
  cmd.run:
    - name: wget https://tl-phantomjs.s3-us-west-2.amazonaws.com/phantomjs-1.9.8-linux-x86_64.zip
    - cwd: /tmp/downloads
    - user: {{ grains['user'] }}

phantomjs_bin:
  archive.extracted:
    - name: /home/{{ grains['user'] }}/phantomjs
    - source: /tmp/downloads/phantomjs-1.9.8-linux-x86_64.zip
    - enforce_toplevel: False
    - archive_format: zip
    - source_hash: md5=8fc6efa7c7bda01f1cea1ee5098ada1a
    - user: {{ grains['user'] }}
    - group: {{ grains['user'] }}

/home/{{ grains['user'] }}/phantomjs:
  file.directory:
    - user: {{ grains['user'] }}
    - group: {{ grains['user'] }}
    - mode: 744
    - recurse:
      - user
      - group
      - mode

/usr/local/bin/phantomjs:
  file.symlink:
    - target: /home/{{ grains['user'] }}/phantomjs/phantomjs-1.9.8-linux-x86_64/bin/phantomjs
    - force: True
    - user: {{ grains['user'] }}
    - group: {{ grains['user'] }}
    - mode: 744
