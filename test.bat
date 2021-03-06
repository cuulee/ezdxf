@ECHO OFF
ECHO ********************************************************
ECHO Running Python 3.6 tests
ECHO ********************************************************
CALL test36.bat

ECHO ********************************************************
ECHO Running Python 3.7 tests
ECHO ********************************************************
CALL test37.bat

ECHO ********************************************************
ECHO Running pypy2 tests
ECHO ********************************************************
CALL testpypy.bat

ECHO ********************************************************
ECHO Running Python 3.6 integration tests with pytest
ECHO ********************************************************
pytest integration_tests

ECHO ********************************************************
ECHO Running pypy2 integration tests with pytest
ECHO ********************************************************
CALL pypy.bat -m pytest integration_tests
