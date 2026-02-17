include Python.mk
PROJECT	= gdrive
ifdef SLOW
	COV_FAIL_UNDER = 65
else
	COV_FAIL_UNDER = 60
endif
lint :: mypy
doc :: README.md
