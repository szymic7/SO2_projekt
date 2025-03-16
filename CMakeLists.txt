cmake_minimum_required(VERSION 3.27)
project(SO2_projekt)

set(CMAKE_CXX_STANDARD 20)

set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(SO2_projekt main.cpp
        DiningPhilosophers.cpp
        DiningPhilosophers.h)
