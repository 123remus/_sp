#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

#define N 5
#define THINKING 0
#define HUNGRY   1
#define EATING  2

pthread_mutex_t chopsticks[N];
pthread_t philosophers[N];
int ids[N];

void think(int id) {
    printf("Philosopher %d is thinking...\n", id);
    usleep(100000);
}

void eat(int id) {
    printf("Philosopher %d is eating...\n", id);
    usleep(100000);
}

void *philosopher(void *arg) {
    int id = *(int *)arg;
    int left = id;
    int right = (id + 1) % N;

    for (int i = 0; i < 5; i++) {
        think(id);

        if (id < (id + 1) % N) {  // pick lower-numbered chopstick first
            pthread_mutex_lock(&chopsticks[left]);
            pthread_mutex_lock(&chopsticks[right]);
        } else {
            pthread_mutex_lock(&chopsticks[right]);
            pthread_mutex_lock(&chopsticks[left]);
        }

        eat(id);

        pthread_mutex_unlock(&chopsticks[left]);
        pthread_mutex_unlock(&chopsticks[right]);
    }
    return NULL;
}

int main() {
    for (int i = 0; i < N; i++) {
        pthread_mutex_init(&chopsticks[i], NULL);
        ids[i] = i;
    }

    for (int i = 0; i < N; i++)
        pthread_create(&philosophers[i], NULL, philosopher, &ids[i]);

    for (int i = 0; i < N; i++)
        pthread_join(philosophers[i], NULL);

    printf("\nAll philosophers have finished dining.\n");

    for (int i = 0; i < N; i++)
        pthread_mutex_destroy(&chopsticks[i]);

    return 0;
}
