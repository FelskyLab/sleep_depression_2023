SHELL= /usr/bin/bash
VENV_PATH = environments/poetry
PYTHON = $(VENV_PATH)/bin/python3
PIP = $(VENV_PATH)/bin/pip
# Just update $PATH

.PHONY: init

init:
	@echo "Initializing mamba"
	@/external/rprshnas01/netdata_kcni/dflab/.opt/mambaforge/bin/mamba init
	@echo "\"Closing and re-opening current shell\""
	@source ~/.bashrc 


