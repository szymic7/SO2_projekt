CXX = g++
CXXFLAGS = -std=c++20 -pthread -Wall -Wextra -O2

SRC = main.cpp DiningPhilosophers.cpp
OUT = SO2_projekt1

all: $(OUT)

$(OUT): $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) -o $(OUT)

clean:
	rm -f $(OUT)