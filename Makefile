CONTIKI_PROJECT = naiveflooding
APPS+=powertrace
all: $(CONTIKI_PROJECT)
CONTIKI=../..
DEFINES = NETSTACK_CONF_RDC=nullrdc_driver,NETSTACK_CONF_MAC=csma_driver
CONTIKI_WITH_RIME = 1
include $(CONTIKI)/Makefile.include
