# Helper script for merging/uploading/downloading metadata files
#
# Contributors:
#    Andrei Sura <sura.andrei@gmail.com>
#    Ruchi Vivek Desai <ruchivdesai@gmail.com>

# Define variable defaults
MAKE_CONFIG_FILE := Makefile.ini

# To properly define the variables please create a Makefile.ini (see Makefile.ini.example)
ifneq ("$(wildcard $(MAKE_CONFIG_FILE))", "")
	include $(MAKE_CONFIG_FILE)
   REDCAP_URL := $(shell cat ${MAKE_CONFIG_FILE} | sed -e 's/ //g' | grep -v '^\#' | grep 'redcap_url=' | cut -d '=' -f2)
   REDCAP_VERSION := $(shell cat ${MAKE_CONFIG_FILE} | sed -e 's/ //g' | grep -v '^\#' | grep 'redcap_version=' | cut -d '=' -f2)
   PROJECT_ID := $(shell cat ${MAKE_CONFIG_FILE} | sed -e 's/ //g' | grep -v '^\#' | grep 'project_id=' | cut -d '=' -f2)
   API_TOKEN := $(shell cat ${MAKE_CONFIG_FILE} | sed -e 's/ //g' | grep -v '^\#' | grep 'api_token=' | cut -d '=' -f2)
endif

# Use variables
API_CALL             := curl -s -X POST $(REDCAP_URL)/api/ -d token=$(API_TOKEN) -d content=metadata -d format=csv
REDCAP_PROJECT_URL   := $(REDCAP_URL)/redcap_v$(REDCAP_VERSION)/ProjectSetup/index.php?pid=$(PROJECT_ID)
UPLOAD_CALL          := python ../scripts/upload-data-dictionary.py --url $(REDCAP_PROJECT_URL) --data_dictionary

help:
	@echo "Available tasks :"
	@echo "\t upload_one <form_name>   - Add a single dictionary to a project"
	@echo "\t upload_all               - Add every dictionary to a project"
	@echo "\t merge_all                - make the merged dictionary file"
	@echo "\t get_one                  - export one dictionary"

upload_one:
	@# Note: provide the form name as: ae_coding, adverse_events...
	$(eval FORM_FILE := $(filter-out $@,$(MAKECMDGOALS)).csv)
	@test -f $(FORM_FILE) || (echo 'The specified file "$(FORM_FILE)" does not exist' && exit 1)
	@echo "Uploading file: $(FORM_FILE)"
	$(UPLOAD_CALL) $(FORM_FILE)

upload_all:
	make merge_all
	$(UPLOAD_CALL) data-dictionary.csv

merge_all:
	rm -f data-dictionary.csv
	cat form_z1*.csv > data-dictionary.csv
	awk 'FNR>2' form_adverse_events.csv >> data-dictionary.csv
	awk 'FNR>2' form_ae_coding.csv >> data-dictionary.csv
	awk 'FNR>2' form_cm_coding.csv >> data-dictionary.csv
	awk 'FNR>2' form_conmeds.csv >> data-dictionary.csv

get_one:
	@# Note: provide the form name as: ae_coding, adverse_events...
	@$(eval FORM := $(filter-out $@,$(MAKECMDGOALS)))
	@$(API_CALL) -d forms[]=$(FORM)
