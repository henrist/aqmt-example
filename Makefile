define build_install_module
	@echo '----------------------------------------------'
	@echo 'Processing module: $(1)'
	@echo '----------------------------------------------'
	cd $(1) && CPATH="$(shell pwd)/aqmt/common" make
	cd $(1) && sudo make unload >/dev/null 2>&1
	cd $(1) && sudo make load
endef

all: get_repos sch_fq_codel sch_pfifo sch_pie aqmt

start_docker:
	cd aqmt/docker && TEST_PATH="$(shell pwd)" docker-compose up

ssh_aqm:
	cd aqmt/docker && ./ssh.sh aqm

aqmt_docker:
	cd aqmt/docker && make

aqmt:
	cd aqmt/aqmt && make
	cd aqmt/aqmt/ta && make

sch_fq_codel:
	$(call build_install_module, aqmt-fq-codel-scheduler)

sch_pfifo:
	$(call build_install_module, aqmt-pfifo-scheduler)
	cp aqmt-pfifo-scheduler/iproute2.patch aqmt/docker/container/iproute2-patches/pfifo-aqmt.patch

sch_pie:
	$(call build_install_module, aqmt-pie-scheduler)

get_repos:
	test -d aqmt || git clone https://github.com/henrist/aqmt.git
	test -d aqmt-fq-codel-scheduler || git clone https://github.com/henrist/aqmt-fq-codel-scheduler.git
	test -d aqmt-pfifo-scheduler || git clone https://github.com/henrist/aqmt-pfifo-scheduler.git
	test -d aqmt-pie-scheduler || git clone https://github.com/henrist/aqmt-pie-scheduler.git

.PHONY: aqmt
