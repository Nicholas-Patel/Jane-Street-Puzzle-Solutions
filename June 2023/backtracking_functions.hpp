//
//  backtracking_functions.hpp
//  NP_Cpp_Code
//
//  Created by Nicholas Patel on 4/06/23.
//

#ifndef backtracking_functions_hpp
#define backtracking_functions_hpp

#include <vector>
#include <unordered_set>
#include <iostream>
#include <sstream>
#include <string>
#include <numeric>
#include <stack>
#include <set>
using namespace std;

// 'Test' functions
int test_func(int a, int b);
void test_pass_by_value(vector < vector <int> > A);
void test_pass_by_reference(vector < vector <int> > &A);

// Code functions
void print_solution(vector <vector<int>> solution);
bool check_GCD_square(int N, int r, int c, vector<int> row_GCD, vector<int> col_GCD, vector<vector<int>> solution);
bool valid(int N, int num_digits, vector<vector<int>> solution);
bool check_for_2by2(int N, vector<vector<int>> solution);
bool check_blocked_nums(int N, vector<vector<int>> solution, vector<int> row_GCD, vector<int> col_GCD, int r1, int r2, int c1, int c2, int dr1, int dr2, int dc1, int dc2);
bool check_hard_code_values(int N, vector<vector<int>> solution);
vector <vector <tuple<int,int>>> dfs(vector<tuple<int,int>> nums, int nums_index, int length);
bool backtrack(int N, int num_digits, int num_added, set<int> nums_used, int layers, vector<int> nums, vector<int> row_GCD, vector<int> col_GCD, int r1, int r2, int c1, int c2, vector<vector<int>> &solution);
bool refined_backtrack(int N, int num_digits, int layers, vector<int> nums, vector<int> row_GCD, vector<int> col_GCD, int step, vector<int> corners, vector<tuple<int,int>> corner_vertices, vector<vector<int>> &solution);

#endif /* backtracking_functions_hpp */
