help:
	@echo "usage: make [command]"

download_python_environment_manager:
	@if test ! -d ".tmp/python-environment-manager-master";then \
	        sudo apt install -y wget unzip; \
		sudo rm -rf maintenance; \
		sudo su -m $(SUDO_USER) -c "mkdir -p .tmp"; \
		sudo su -m $(SUDO_USER) -c "cd .tmp; wget https://github.com/terminal-labs/python-environment-manager/archive/master.zip"; \
		sudo su -m $(SUDO_USER) -c "cd .tmp; unzip -qq master.zip"; \
	fi

create: download_python_environment_manager
	@sudo bash .tmp/python-environment-manager-master/maintenance/vagrant_saltstates/build.sh $(SUDO_USER)
