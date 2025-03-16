#include <iostream>
#include <cstdlib>
#include "DiningPhilosophers.h"

using namespace std;

//---------------------------------------------------------------------------------------------------------------------

int main(int argc, char* argv[]) {

    int n; // number of philosophers

    try {
        n = stoi(argv[1]);
    } catch (const std::invalid_argument& e) {
        cerr << "Error: Invalid argument. Please provide a valid integer." << endl;
        return 1;
    } catch (const std::out_of_range& e) {
        cerr << "Error: Number out of range. Please provide a smaller integer." << endl;
        return 1;
    } catch (...) {
        cerr << "Unknown error occurred." << endl;
        return 1;
    }

    cout << "Integer typed: " << n << endl;


    DiningPhilosophers dining_philosophers(n);
    dining_philosophers.setMinTime(2000);
    dining_philosophers.setMaxTime(3000);
    dining_philosophers.startDining();


    return 0;

}

//---------------------------------------------------------------------------------------------------------------------
