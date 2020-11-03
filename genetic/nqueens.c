#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>

int BOARD_SIZE;

void genetic();
void brute_force();
int ** init_population(int pop_size);
int * init_board();
void print_board(int *board);
int num_queens_in_danger(int *board);
int is_in_danger(int *board, int row);
int min(int x, int y);
int * weighted_pick_parent(int **population, int pop_size);
int * reproduce(int *parent1, int *parent2);
void mutate_organism(int *board);
bool backtrack_solve(int *board, int row, bool* col_has_queen);
double get_time_elapsed(void (*fn)(void));


int queen_comp(const void *elem1, const void *elem2) {
    int *board1 = *((int **) elem1);
    int *board2 = *((int **) elem2);

    int res1 = num_queens_in_danger(board1);
    int res2 = num_queens_in_danger(board2);
    if (res1 > res2) return 1;
    if (res1 < res2) return -1;
    return 0;
}

int shuffle_comp(const void *elem1, const void *elem2) {
    return (rand() % 100 < 50) ? 1 : -1;
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        printf("Usage => ./nqueens {genetic|brute_force|compare} {board_size}\n");
        exit(1);
    }

    BOARD_SIZE = atoi(argv[2]);
    
    char *type = argv[1];
    printf("input %s\n", type);
    if (strcmp(type, "genetic") == 0) {
        printf("GENETIC      time taken: %f\n", get_time_elapsed(genetic));
    } 
    else if (strcmp(type, "brute_force") == 0) {
        printf("BRUTE FORCE  time taken: %f\n", get_time_elapsed(brute_force));
    }
    else if (strcmp(type, "compare") == 0) {
        double genetic_elapsed = get_time_elapsed(genetic);
        double brute_force_elapsed = get_time_elapsed(brute_force);
        
        printf("GENETIC      time taken: %f\n", genetic_elapsed);
        printf("BRUTE FORCE  time taken: %f\n", brute_force_elapsed);
    }
    else {
        printf("Usage => ./nqueens {genetic|brute_force|compare} {board_size}\n");
        exit(1);
    }
}

double get_time_elapsed(void (*fn)(void)) {
    clock_t t = clock();
    fn();
    t = clock() - t;
    return ((double)t)/CLOCKS_PER_SEC;
}

void genetic() {
    int pop_size = 30;
    int max_generations = 10000;

    srand(time(0));

    int **population = init_population(pop_size);
    qsort(population, pop_size, sizeof(int *), queen_comp);

    for(int gen = 0; gen < max_generations; gen++) {
        int fitness = num_queens_in_danger(population[0]);
        printf("gen %d, fitness: %d\n", gen, fitness);
        if(fitness == 0) break;

        for(int child_num = 0; child_num < pop_size; child_num++) {
            int *parent1 = weighted_pick_parent(population, pop_size);
            int *parent2 = weighted_pick_parent(population, pop_size);

            int *child = reproduce(parent1, parent2);
            population[pop_size + child_num] = child;
        }

        qsort(population, pop_size*2, sizeof(int *), queen_comp);
        
        // discard unfit organisms
        for(int i = pop_size; i < pop_size*2; i++) {
            free(population[i]);
        }
    }

    print_board(population[0]);
    printf("num queens in danger %d\n", num_queens_in_danger(population[0]));
}

void brute_force() {
    int *board = malloc(BOARD_SIZE * sizeof(int));
    for(int i = 0; i < BOARD_SIZE; i++) {
        board[i] = -1;
    }

    bool *col_has_queen = calloc(BOARD_SIZE, sizeof(bool));
    bool res = backtrack_solve(board, 0, col_has_queen);

    // print_board(board);
    printf(res ? "true\n" : "false\n");
}

bool backtrack_solve(int *board, int row, bool* col_has_queen) {
    if (row >= BOARD_SIZE) {
        return true;
    }


    for(int col = 0; col < BOARD_SIZE; col++) {
        if(col_has_queen[col]) continue;

        board[row] = col;
        col_has_queen[col] = true;

        if (!is_in_danger(board, row) && backtrack_solve(board, row+1, col_has_queen)) {
            return true;
        }

        // it didn't work, revert
        board[row] = -1;
        col_has_queen[col] = false;
    }

    return false;
}

int * weighted_pick_parent(int **population, int pop_size) {
    int *weights = malloc(pop_size * sizeof(int));
    int weight_sum = 0;
    for(int i = 0; i < pop_size; i++) {
        weights[i] = 1 + 2 * (BOARD_SIZE - num_queens_in_danger(population[i]));
        weight_sum += weights[i];
    }

    int rnd = rand() % weight_sum;
    int i;
    for(i = 0; i < pop_size; i++) {
        if(rnd < weights[i]) break;

        rnd -= weights[i];
    }

    free(weights);
    return population[i];
}

int * reproduce(int *parent1, int *parent2) {
    int partition = rand() % BOARD_SIZE;
    int *child = malloc(BOARD_SIZE * sizeof(int));
    int *child_seen = calloc(BOARD_SIZE, sizeof(int));

    // loop from 0 to partition-1 in parent1 and copy to child
    int i;
    for(i = 0; i < partition; i++) {
        int col = parent1[i];
        child[i] = col;
        child_seen[col] = 1;
    }

    // loop through all cols in parent2, and add the ones not existing in child, in order
    for(int pi = 0; pi < BOARD_SIZE; pi++) {
        int col = parent2[pi];
        if (child_seen[col] == 0) {
            child[i] = col;
            i++;
        }
    }

    // mutation
    float r = (float)rand()/RAND_MAX;
    if(r < 0.9) {
        mutate_organism(child);
    }

    return child;
}

void mutate_organism(int *board) {
    int src_row = rand() % BOARD_SIZE;
    int dst_row = rand() % BOARD_SIZE;

    int temp = board[src_row];
    board[src_row] = board[dst_row];
    board[dst_row] = temp;
}

int ** init_population(int pop_size) {
    int **population = malloc(2 * pop_size * sizeof(int *));
    for(int i = 0; i < pop_size; i++) {
        population[i] = init_board();
    }

    return population;
}

int * init_board() {
    int *board = malloc(BOARD_SIZE * sizeof(int));
    for(int i = 0; i < BOARD_SIZE; i++) {
        board[i] = i;
    }

    qsort(board, BOARD_SIZE, sizeof(int), shuffle_comp);
    return board;
}

void print_board(int *board) {
    int **expanded = malloc(BOARD_SIZE * sizeof(int *));
    for(int r = 0; r < BOARD_SIZE; r++) {
        expanded[r] = calloc(BOARD_SIZE, sizeof(int));
        expanded[r][board[r]] = 1;
    }

    for(int r = 0; r < BOARD_SIZE; r++) {
        for(int c = 0; c < BOARD_SIZE; c++) {
            printf("%d ", expanded[r][c]);
        }
        printf("\n");
    }
}

int num_queens_in_danger(int *board) {
    int num = 0;
    for(int r = 0; r < BOARD_SIZE; r++) {
        num += is_in_danger(board, r);
    }
    return num;
}

int is_in_danger(int *board, int row) {
    // check TL to BR diag
    int sum = 0;
    int m = min(row, board[row]);
    int r = row - m;
    int c = board[row] - m;

    while(r < BOARD_SIZE && c < BOARD_SIZE) {
        if (c == board[r]) sum++;
        if(sum > 1) return 1;
        r++;
        c++;
    }

    // check TR to BL diag
    sum = 0;
    m = min(row, BOARD_SIZE - board[row]);
    r = row-m;
    c = board[row] + m;
    while(r < BOARD_SIZE && c >= 0) {
        if (c == board[r]) sum++;
        if (sum > 1) return 1;
        r++;
        c--;
    }

    return 0;
}

int min(int x, int y) {
    return (x < y) ? x : y;
}
