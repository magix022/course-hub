cmake_minimum_required(VERSION 3.21)
project(core_ui)

set(CMAKE_CXX_STANDARD 14)
find_package(Qt5 COMPONENTS
        Core
        Gui
        Widgets
        REQUIRED)



# see https://cmake.org/cmake/help/latest/module/FindPython3.html#module:FindPython3
set(Python3_EXECUTABLE "/Users/theofabilous/opt/anaconda3/envs/Py3-10/bin/python")
set(Python3_LIBRARY_DIRS "/Users/theofabilous/opt/anaconda3/envs/Py3-10/lib")
set(Python3_INCLUDE_DIR "/Users/theofabilous/opt/anaconda3/envs/Py3-10/include/python3.10")
find_package(Python3 3.10 COMPONENTS Interpreter Development NumPy)
if(Python3_NumPy_FOUND)
    message(STATUS " - - - - - - - Python3 NumPy found! - - - - - - -")
    message(SATUS "Python3_NumPy_INCLUDE_DIRS=${Python3_NumPy_INCLUDE_DIRS}")
    message(SATUS "Python3_NumPy_VERSION=${Python3_NumPy_VERSION}")
    message(STATUS "test")
endif()

macro(print_all_variables)
    message(STATUS "print_all_variables------------------------------------------{")
    get_cmake_property(_variableNames VARIABLES)
    foreach (_variableName ${_variableNames})
        message(STATUS "${_variableName}=${${_variableName}}")
    endforeach()
    message(STATUS "print_all_variables------------------------------------------}")
endmacro()

print_all_variables()


add_executable(core_ui main.cpp MainWidget.cpp MainWidget.h MainTabs.cpp
        MainTabs.h Schedule.cpp Schedule.h CalendarTab.cpp CalendarTab.h
        CalendarEntryDialog.cpp CalendarEntryDialog.h CalendarEntry.cpp
        pyhelper.h pythoncomm.cpp)
target_link_libraries(core_ui
        Qt5::Core
        Qt5::Gui
        Qt5::Widgets
        Python3::Python
        Python3::NumPy
        )

