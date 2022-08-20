COMPONENT?=authix
VERSION:=src/${COMPONENT}/version.py

include make/common.mk

include make/install.mk
include make/test.mk
include make/run.mk
include make/lint.mk
include make/ci.mk

.DEFAULT:help
