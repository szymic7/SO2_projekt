#include <iostream>
#include "DiningPhilosophers.h"

//---------------------------------------------------------------------------------------------------------------------

int main(int argc, char* argv[]) {
    int n;  // number of philosophers

    try {
        n = std::stoi(argv[1]);
    } catch (const std::invalid_argument& e) {
        std::cerr << "Error: Invalid argument. Please provide a valid integer.\n";
        return 1;
    } catch (...) {
        std::cerr << "Unknown error occurred.\n";
        return 1;
    }

    DiningPhilosophers dining_philosophers(n);
    dining_philosophers.setMinTime(5000);
    dining_philosophers.setMaxTime(6000);
    dining_philosophers.startDining();

    return 0;
}

//---------------------------------------------------------------------------------------------------------------------
