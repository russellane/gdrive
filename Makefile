include Python.mk
PROJECT	= gdrive
ifdef SLOW
	COV_FAIL_UNDER = 66
else
	COV_FAIL_UNDER = 61
endif
doc :: README.md
