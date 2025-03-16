#ifndef SO2_PROJEKT_DININGPHILOSOPHERS_H
#define SO2_PROJEKT_DININGPHILOSOPHERS_H

#include <iostream>
#include <thread>
#include <vector>
#include <mutex>
#include <semaphore>
#include <random>

using namespace std;

class DiningPhilosophers {

    enum class State
    {
        THINKING = 0,
        HUNGRY = 1,
        EATING = 2
    };

    int n_philosophers; // number of philosophers

    vector<thread> philosophers; // philosophers' threads
    State *state; // array to keep track of philosophers' states

    std::mutex critical_region_mtx; // mutex for the access to the forks
    std::mutex output_mtx; // mutex for console output

    // vector of semaphores for philosophers' threads
    std::vector<std::unique_ptr<std::binary_semaphore>> both_forks_available;

    int min_time = 1000; // minimum time of thinking/eating
    int max_time = 2000; // maximum time of thinking/eating
    std::mt19937 gen;

    void philosopher(int id);
    int my_rand(int min, int max);
    void test(int id);
    void think(int id);
    void takeForks(int id);
    void eat(int id);
    void putDownForks(int id);

public:

    DiningPhilosophers(int n);
    void setMinTime(int time);
    void setMaxTime(int time);
    void startDining();
};


#endif //SO2_PROJEKT_DININGPHILOSOPHERS_H
