.check-uncommitted: $(addprefix .ensure-pushed-,$(subst ./,,$(shell mkdir -p packages; cd packages; find . -maxdepth 1 -mindepth 1 -type d)))

.check-dependency-compatibility:
	.venv/bin/pipdeptree --warn=fail

.check-for-updates: $(addprefix .check-newer-,$(subst ./,,$(shell cd packages; find . -maxdepth 1 -mindepth 1 -type d)))

install-dependencies:
	make -j .venv/bin/python .check-uncommitted
	.venv/bin/pip install --requirement=requirements.txt.freeze --src=./packages --upgrade
	make -j install-frontend

upgrade-dependencies:
	make -j .check-uncommitted .venv/bin/python
	PYTHONWARNINGS="ignore" .venv/bin/pip install --requirement=requirements.txt --src=./packages --upgrade --process-dependency-links
	make -j .check-dependency-compatibility
	# write freeze file
	# pkg-ressources is automatically added on ubuntu, but breaks the install.
	# https://stackoverflow.com/a/40167445/1380673
	.venv/bin/pip freeze | grep -v "pkg-resources" > requirements.txt.freeze
	make .check-for-updates
	@echo -e "\033[32msucceeded, please check output above for warnings\033[0m"

run-flask:
	. .venv/bin/activate; flask run --with-threads --reload --eager-loading 2>&1

install-frontend:
	/usr/bin/env yarn install # --modules-folder ./resources
