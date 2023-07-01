//
//  main.cpp
//  NP_Cpp_Code
//
//  Created by Nicholas Patel on 3/06/23.
//  Solution to Jane Street June 2023 Puzzle
//

#include "backtracking_functions.hpp"

int main(void) {
    
    // Set boundary conditions
    bool real_problem = true;
    int N; vector<int> row_GCD; vector<int> col_GCD; vector <int> nums;
    vector<int> corners; vector<tuple<int,int>> corner_vertices;
    
    if (!real_problem) {
        N = 5;
        row_GCD = {0, 5, 3, 123, 1};
        col_GCD = {0,  1, 1, 5, 4};
        nums = {4,5,3,2,1};
        corners = {1,1};
        corner_vertices = {{0,4}, {1,3}};
    }
    else {
        N = 9;
        row_GCD = {55, 1, 6, 1, 24, 3, 6, 7, 2};
        col_GCD = {5,  1, 6, 1, 8, 1, 22, 7, 8};
        nums = {5,8,7,9,6,4,3,2,1};
        corners = {0, 2, 2, 0};
        corner_vertices = {{0,0}, {8,8}, {7,7}, {1,1}};
    }
    
    int num_digits = ((N * (N+1))/2);
    
    // Initialise solution parameters
    vector < vector<int> > solution; solution.clear();
    for (int i = 0; i < N; i++){
        vector<int> row;
        for (int j = 0; j < N; j++) {
            row.push_back(0);
        }
        solution.push_back(row);
    }
            
    // Initialise backtracking variables
    set<int> nums_used; nums_used.empty();
    // int r1 = 0; int c1 = 0; int r2 = N-1; int c2 = N-1; int num_added = 0;
    bool found; int layers = 0; int step = 0; bool check_legit;
    
    // Perform the backtrack
    // Old (without frame): found = backtrack(N, num_digits, num_added, nums_used, layers, nums, row_GCD, col_GCD, r1, r2, c1, c2, solution);
    found = refined_backtrack(N, num_digits, layers, nums, row_GCD, col_GCD, step, corners, corner_vertices, solution);
    cout << found << endl;
    
    check_legit = valid(N, num_digits, solution);
    cout << check_legit << endl;
    
    return 0;
}
