#include <random>
#include "DiningPhilosophers.h"

//----------------------------------------------------------------------------------------------------------------------

/** @brief Constructor method for DiningPhilosophers class
 *
 * Initializes a pseudo-random number generator and sets the parameters of an object of DiningPhilosophers class
 *
 * @param n number of the philosophers in the problem
 */
DiningPhilosophers::DiningPhilosophers(int n) : gen(std::random_device{}()) {

    n_philosophers = n;
    state = new State[n];

    // creating semaphores for each philosopher thread
    for (int i = 0; i < n_philosophers; i++) {
        both_forks_available.emplace_back(std::make_unique<std::binary_semaphore>(0));
    }

}

//----------------------------------------------------------------------------------------------------------------------

void DiningPhilosophers::setMinTime(int time) {
    min_time = time;
}

//----------------------------------------------------------------------------------------------------------------------

void DiningPhilosophers::setMaxTime(int time) {
    max_time = time;
}

//----------------------------------------------------------------------------------------------------------------------

/**
 * @brief Method representing a behavior of a philosopher
 *
 * Runs an infinite loop, where the philosopher thinks, tries to take the forks, eats and puts the forks down
 *
 * @param id id of a philosopher
 */
void DiningPhilosophers::philosopher(int id)
{
    while (true)
    {
        think(id);
        takeForks(id);
        eat(id);
        putDownForks(id);
    }
}

//----------------------------------------------------------------------------------------------------------------------

/**
 * @brief Method testing if the philosopher may eat
 *
 * Calculates indexes of philosopher's neighbors, checking if tested philosopher is hungry and his neighbors
 * are not eating; if so, he's starting eating
 *
 * @param id id of the philosopher which is being tested
 */
void DiningPhilosophers::test(int id)
{
    int left = (id - 1 + n_philosophers) % n_philosophers;
    int right = (id + 1) % n_philosophers;

    if (state[id] == State::HUNGRY &&
        state[left] != State::EATING &&
        state[right] != State::EATING)
    {
        state[id] = State::EATING;
        both_forks_available[id]->release(); // release the semaphore - enable the philosopher to eat
    }
}

//----------------------------------------------------------------------------------------------------------------------

/** @brief Method representing a philosopher thinking
 *
 * Generates a random duration in range [400; 800], enters a critical section for uninterrupted print and
 * sleeps a current thread for the drawn amount of time
 *
 * @param id id of the philosopher's thread
 */
void DiningPhilosophers::think(int id)
{
    int time = std::uniform_int_distribution<>(min_time, max_time)(gen);
    {
        std::lock_guard<std::mutex> lck(output_mtx); // critical section for uninterrupted print
        cout << "\033[34mPhilosopher " << id << " is THINKING for " << time << "ms\033[0m" << endl;
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(time));
}

//----------------------------------------------------------------------------------------------------------------------

/** @brief Method representing a philosopher trying to take two forks to eat
 *
 * Entering a critical section for an access to the forks, entering second critical section to print a current
 * state of a philosopher and testing if he can eat; if not - the thread is being blocked by the semaphore
 *
 * @param id id of a philosopher trying to take forks
 */
void DiningPhilosophers::takeForks(int id)
{
    // scope 1 - protect access to the state array
    {
        std::lock_guard<std::mutex> lck{critical_region_mtx};
        state[id] = State::HUNGRY;

        // scope 2 - protect access to cout (console output)
        {
            std::lock_guard<std::mutex> lock(output_mtx);
            cout << "\033[31mPhilosopher " << id << " is HUNGRY\033[0m" << endl;
        }

        test(id); // check if a philosopher can eat
    }

    both_forks_available[id]->acquire(); // block the thread if forks were not acquired
}

//----------------------------------------------------------------------------------------------------------------------

/** @brief Method representing a philosopher eating
 *
 * Generates a random duration in range [400; 800], enters a critical section for uninterrupted print and
 * sleeps a current thread for the drawn amount of time
 *
 * @param id id of a philosopher eating
 */
void DiningPhilosophers::eat(int id)
{
    int time = std::uniform_int_distribution<>(min_time, max_time)(gen);
    {
        std::lock_guard<std::mutex> lk(output_mtx);
        cout << "\033[32mPhilosopher " << id << " is EATING for " << time << "ms\033[0m" << endl;
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(time));
}

//----------------------------------------------------------------------------------------------------------------------

/** @brief Method representing a philosopher freeing up the forks after finishing eating
 *
 * Calculates the indexes of a philosopher's neighbors, enters a critical region to share access to the forks,
 * setting a state of the philosopher to thinking and testing if his neighbors may eat
 *
 * @param id id of a philosopher putting down the forks
 */
void DiningPhilosophers::putDownForks(int id)
{
    // indexes of left and right neighbor
    int left_neighbor = (id - 1 + n_philosophers) % n_philosophers;
    int right_neighbor = (id + 1) % n_philosophers;

    std::lock_guard<std::mutex> lck{critical_region_mtx}; // enter critical region
    state[id] = State::THINKING;
    test(left_neighbor); // check if the left neighbor can eat
    test(right_neighbor); // check if the right neighbor can eat
}

//----------------------------------------------------------------------------------------------------------------------


void DiningPhilosophers::startDining() {

    // creating and starting philosopher threads
    for (int i = 0; i < n_philosophers; i++) {
        philosophers.emplace_back(&DiningPhilosophers::philosopher, this, i);
    }

    // waiting for all philosopher threads to finish
    for (auto& phil_thread : philosophers) {
        if (phil_thread.joinable()) {
            phil_thread.join();
        }
    }

}

//----------------------------------------------------------------------------------------------------------------------