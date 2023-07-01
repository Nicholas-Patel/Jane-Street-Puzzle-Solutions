//
//  backtracking_functions.cpp
//  NP_Cpp_Code
//
//  Created by Nicholas Patel on 4/06/23.
//

#include "backtracking_functions.hpp"


// #################################################################
// 'Test' functions
// #################################################################

int test_func(int a, int b) {
  return (a + b);
}

void test_pass_by_value(vector <vector<int> > A) {
    A[0][0] = -999;
    cout << A[0][0] << endl;
    return;
}

void test_pass_by_reference(vector <vector<int> > &A) {
    A[0][0] = -999;
    cout << A[0][0] << endl;
    return;
}


// #################################################################
// Code functions
// #################################################################

void print_solution(vector <vector<int>> solution) {
    for (unsigned int i = 0; i < solution.size(); i++)
    {
        for (unsigned int j = 0; j < solution[i].size(); j++)
        {
            cout << solution[i][j] << " ";
        }
        cout << endl;
    }
    cout << " " << endl;
    return;
}

bool check_GCD_square(int N, int r, int c, vector<int> row_GCD, vector<int>  col_GCD, vector<vector<int>> solution) {
    
    // Check GCD of row numbers
    if (row_GCD[r] > 0) {
        string row = "";
        for (int i = 0; i < N; i++){
            row += to_string(solution[r][i]);
        }
        row += "0";
        vector <int> row_nums;
        string str_piece;
        stringstream obj_ss(row);
        while (!obj_ss.eof()) {
            getline(obj_ss, str_piece, '0');
            if (str_piece.size()>0) {row_nums.push_back(stoi(str_piece));}
        }
        if (row_nums.size() == 0) {
            return false;
        }
        int x = row_nums[0];
        for (int i = 0; i < row_nums.size(); i++) {
            x = gcd(x, row_nums[i]);
        }
        if (x != row_GCD[r]) {
            return false;
        }
    }
    
    // Check GCD of column numbers
    if (col_GCD[c] > 0) {
        string col = "";
        for (int i = 0; i < N; i++){
            col += to_string(solution[i][c]);
        }
        col += "0";
        vector <int> col_nums;
        string str_piece;
        stringstream obj_ss(col);
        while (!obj_ss.eof()) {
            getline(obj_ss, str_piece, '0');
            if (str_piece.size() > 0) {col_nums.push_back(stoi(str_piece));}
        }
        if (col_nums.size() == 0) {
            return false;
        }
        int x = col_nums[0];
        for (int i = 0; i < col_nums.size(); i++) {
            x = gcd(x, col_nums[i]);
        }
        if (x != col_GCD[c]) {
            return false;
        }
    }
    
    // Else it passes both GCD checks!
    return true;
}

bool valid(int N, int num_digits, vector<vector<int>> solution){
    
    // Check entries form a single connected component
    int x0 = 0; int y0 = 0;
    int i; int j; int k;
    bool found = false;
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            if (solution[i][j] != 0){
                x0 = i; y0 = j;
                found = true;
            }
            if (found) {
                break;
            }
        }
        if (found) {
            break;
        }
    }
        
    int directions[4][2] = {{-1,0}, {0,-1}, {1,0}, {0,1}};
    tuple <int,int> t0 = make_tuple(x0, y0);
    stack < tuple<int,int> > stack; stack.push(t0);
    set < tuple <int,int> > visited; visited.insert(t0);
    int dx = 0; int dy = 0; int new_i; int new_j; bool is_in_set = false;
    while (stack.size() > 0) {
        t0 = stack.top(); stack.pop();
        tie(i,j) = t0;
        for (k = 0; k < 4; k++) {
            dx = directions[k][0]; dy = directions[k][1];
            new_i = i + dx; new_j = j + dy;
            if ((((new_i>=0) && (new_i < N)) && ((new_j >=0) && (new_j < N)))) {
                t0 = make_tuple(new_i, new_j);
                is_in_set = visited.count(t0);
                if ((solution[new_i][new_j] != 0) && (!is_in_set)) {
                    visited.insert(t0);
                    stack.push(t0);
                }
            }
        }
    }
    if (visited.size() < num_digits) {
        return false;
    }
    
    // Check that every 2x2 square contains an unfilled cell
    for (i = 0; i < N-1; i++) {
        for (j = 0; j < N-1; j++) {
            if ((solution[i][j] != 0) && (solution[i+1][j] != 0) && (solution[i][j+1] != 0) && (solution[i+1][j+1] != 0)) {
                return false;
            }
        }
    }
    
    // Else all conditions passed so return True!
    return true;
}

bool check_for_2by2(int N, vector<vector<int>> solution) {
    for (int i = 0; i < N-1; i++) {
        for (int j = 0; j < N-1; j++) {
            if (solution[i][j]!=0 && solution[i+1][j]!=0 && solution[i][j+1]!=0 && solution[i+1][j+1]!=0) {
                return false;
            }
        }
    }
    return true;
}

bool check_blocked_nums(int N, vector<vector<int>> solution, vector<int> row_GCD, vector<int> col_GCD, int r1, int r2, int c1, int c2, int dr1, int dr2, int dc1, int dc2) {
        
    int i; int j; int k; string row; string col; string str_piece; stringstream obj_ss; vector <int> row_nums; vector <int> col_nums; int x;
    
    // Check partial row factors
    if (dc1 > 0) {
        for (i = r1+dr1; i < r2+dr2+1; i++) {
            if ((row_GCD[i] > 0) && (solution[i][c1] == 0)) {
                row = ""; row_nums.clear();
                for (j = 0; j < c1; j++){
                    row += to_string(solution[i][j]);
                }
                row += "0";
                stringstream obj_ss(row);
                while (!obj_ss.eof()) {
                    getline(obj_ss, str_piece, '0');
                    if (str_piece.size()>0) {row_nums.push_back(stoi(str_piece));}
                }
                for (k = 0; k < row_nums.size(); k++) {
                    x = row_nums[k];
                    if (x % row_GCD[i] != 0) {
                        return false;
                    }
                }
            }
        }
    }
    
    if (dc2 < 0) {
        for (i = r1+dr1; i < r2+dr2+1; i++) {
            if ((row_GCD[i] > 0) && (solution[i][c2] == 0)) {
                row = ""; row_nums.clear();
                for (j = c2+1; j < N; j++){
                    row += to_string(solution[i][j]);
                }
                row += "0";
                stringstream obj_ss(row);
                while (!obj_ss.eof()) {
                    getline(obj_ss, str_piece, '0');
                    if (str_piece.size()>0) {row_nums.push_back(stoi(str_piece));}
                }
                for (k = 0; k < row_nums.size(); k++) {
                    x = row_nums[k];
                    if (x % row_GCD[i] != 0) {
                        return false;
                    }
                }
            }
        }
    }

    // Check partial column factors
    if (dr1 > 0) {
        for (i = c1+dc1; i < c2+dc2+1; i++) {
            if ((col_GCD[i] > 0) && (solution[r1][i] == 0)) {
                col = ""; col_nums.clear();
                for (j = 0; j < r1; j++){
                    col += to_string(solution[j][i]);
                }
                col += "0";
                stringstream obj_ss(col);
                while (!obj_ss.eof()) {
                    getline(obj_ss, str_piece, '0');
                    if (str_piece.size()>0) {col_nums.push_back(stoi(str_piece));}
                }
                for (k = 0; k < col_nums.size(); k++) {
                    x = col_nums[k];
                    if (x % col_GCD[i] != 0) {
                        return false;
                    }
                }
            }
        }
    }
    
    if (dr2 < 0) {
        for (i = c1+dc1; i < c2+dc2+1; i++) {
            if ((col_GCD[i] > 0) && (solution[r2][i] == 0)) {
                col = ""; col_nums.clear();
                for (j = r2+1; j < N; j++){
                    col += to_string(solution[j][i]);
                }
                col += "0";
                stringstream obj_ss(col);
                while (!obj_ss.eof()) {
                    getline(obj_ss, str_piece, '0');
                    if (str_piece.size()>0) {col_nums.push_back(stoi(str_piece));}
                }
                for (k = 0; k < col_nums.size(); k++) {
                    x = col_nums[k];
                    if (x % col_GCD[i] != 0) {
                        return false;
                    }
                }
            }
        }
    }
    
    return true;

}

bool check_hard_code_values(int N, vector<vector<int>> solution) {
    
    // Hard-code values which cannot be used
    vector<tuple<int,int>> fives = {{0, 6}, {0, 7},{0, 8}};
    int x; int y;
    for (int i = 0; i<fives.size(); i++) {
        tie(x,y) = fives[i];
        if (solution[x][y] == 5) {
            return false;
        }
    }
    return true;
}

vector <vector <tuple<int,int>>> dfs(vector<tuple<int,int>> nums, int nums_index, int length) {
    
    vector <vector <tuple<int,int>>> res;
    vector <vector <tuple<int,int>>> subproblem;
    vector<tuple<int,int>> combination;
    
    // Check terminating cases
    if (length == 0 || (nums.size() - nums_index < length)) {
        return res;
    }
    
    // If we don't include current element, nums[nums_index]
    subproblem = dfs(nums, nums_index + 1, length);
    for (int i = 0; i < subproblem.size(); i++) {
        res.push_back(subproblem[i]);
    }
    
    // If we do include the current element
    combination.push_back(nums[nums_index]);
    subproblem = dfs(nums, nums_index + 1, length - 1);
    if (length == 1 && subproblem.size() == 0) {
        res.push_back(combination);
        return res;
    }
    for (int j = 0; j < subproblem.size(); j++) {
        combination = subproblem[j];
        combination.push_back(nums[nums_index]);
        res.push_back(combination);
    }

    return res;
}

bool backtrack(int N, int num_digits, int num_added, set<int> nums_used, int layers, vector<int> nums, vector<int> row_GCD, vector<int> col_GCD, int r1, int r2, int c1, int c2, vector<vector<int>> &solution){

    // Terminating case
    if (layers == N) {
        bool valid_sol = valid(N, num_digits, solution);
        if (valid_sol) {
            print_solution(solution);
            return true;
        }
        return false;
    }
    
    // Check if square left is physically big enough
    int area = ((r2-r1+1) * (c2-c1+1));
    if ((area < num_digits - num_added) || (r1>r2) || (c1>c2)) {
        return false;
    }
    
    // Else backtrack
    vector<vector<int>> reductions = {{1, 0, 1, 0}, {0, -1, 1, 0}, {0, -1, 0, -1}, {1, 0, 0, -1}};
    vector<vector<int>> need_to_check = {{r1, c1}, {r2, c1}, {r2, c2}, {r1, c2}};
    vector < vector <tuple<int,int>> > all_indices;
    int i; tuple <int, int> t; vector <tuple<int, int>> indices;
    
    for (i = c1; i < c2+1; i++) {t = make_tuple(r1, i); indices.push_back(t);}
    for (i = r1+1; i < r2+1; i++) {t = make_tuple(i, c1); indices.push_back(t);}
    all_indices.push_back(indices); indices.clear();

    for (i = r1; i < r2+1; i++) {t = make_tuple(i, c1); indices.push_back(t);}
    for (i = c1+1; i < c2+1; i++) {t = make_tuple(r2, i); indices.push_back(t);}
    all_indices.push_back(indices); indices.clear();
    
    for (i = c1; i < c2+1; i++) {t = make_tuple(r2, i); indices.push_back(t);}
    for (i = r1; i < r2; i++) {t = make_tuple(i, c2); indices.push_back(t);}
    all_indices.push_back(indices); indices.clear();

    for (i = c1; i < c2+1; i++) {t = make_tuple(r1, i); indices.push_back(t);}
    for (i = r1+1; i < r2+1; i++) {t = make_tuple(i, c2); indices.push_back(t);}
    all_indices.push_back(indices); indices.clear();

    vector<vector<tuple<int,int>>> combs;
    vector<tuple<int,int>> enter;
    vector<int> bound_changes;
    vector<int> check;
    int x; int a; int b; bool GCD_ok; bool subproblem_ok; bool square_subset_ok; bool blocked_ok;
    for (int j = 0; j < 4; j++) {
        indices = all_indices[j];
        bound_changes = reductions[j];
        check = need_to_check[j];
        for (int k = 0; k < nums.size(); k++) {
            x = nums[k];
            if (!nums_used.count(x)) {
                combs = dfs(indices, 0, x);
                nums_used.insert(x);
                for (int l = 0; l < combs.size(); l++) {
                    
                    enter = combs[l];
                    for (int m = 0; m < enter.size(); m++) {
                        tie(a,b) = enter[m];
                        solution[a][b] = x;
                    }
                                        
                    GCD_ok = (check_GCD_square(N, check[0], check[1], row_GCD, col_GCD, solution));
                    if (GCD_ok) {
                        blocked_ok = (check_blocked_nums(N, solution, row_GCD, col_GCD, r1, r2, c1, c2, bound_changes[0], bound_changes[1], bound_changes[2], bound_changes[3]));
                        if (blocked_ok) {
                            square_subset_ok = check_for_2by2(N, solution);
                            if (square_subset_ok) {
                                subproblem_ok = backtrack(N, num_digits, num_added+x, nums_used, layers+1, nums, row_GCD, col_GCD, r1+bound_changes[0], r2+bound_changes[1], c1+bound_changes[2], c2+bound_changes[3], solution);
                                if (subproblem_ok) {
                                    return true;
                                }
                            }
                        }
                    }
                    
                    for (int m = 0; m < enter.size(); m++) {
                        tie(a,b) = enter[m];
                        solution[a][b] = 0;
                    }
                }
                nums_used.erase(x);
            }
        }
    }
        
    return false;
}

bool refined_backtrack(int N, int num_digits, int layers, vector<int> nums, vector<int> row_GCD, vector<int> col_GCD, int step, vector<int> corners, vector<tuple<int,int>> corner_vertices, vector<vector<int>> &solution) {
    
    // Terminating case
    if (layers == N) {
        bool valid_sol = valid(N, num_digits, solution);
        if (valid_sol) {
            print_solution(solution);
            return true;
        }
        return false;
    }
    
    // Else backtrack
    
    if (step < corners.size()) {
        // Setup search
        int corner = corners[step];
        int x = nums[step];
        int a, b;
        int r1, r2, c1, c2;
        int i;
        tuple<int,int> t;
        tie(a,b) = corner_vertices[step];
        vector <tuple<int, int>> indices;
        vector<vector<tuple<int,int>>> combs;
        vector<tuple<int,int>> enter;
        bool GCD_ok; bool subproblem_ok; bool square_subset_ok; bool blocked_ok;
        int check_r, check_c;
        int dr1 = 0, dr2 = 0, dc1 = 0, dc2 = 0;
        
        if (corner == 0) {
            // Top left
            r1 = a; c1 = b; r2 = a+N-step-1; c2 = b+N-step-1;
            for (i = c1; i < c2+1; i++) {t = make_tuple(r1, i); indices.push_back(t);}
            for (i = r1+1; i < r2+1; i++) {t = make_tuple(i, c1); indices.push_back(t);}
            check_r = r1; check_c = c1;
            dr1 = 1; dc1 = 1;

        } else if (corner == 1) {
            // Top right
            r1 = a; c2 = b; r2 = a+N-step-1; c1 = b-N+step+1;
            for (i = c1; i < c2+1; i++) {t = make_tuple(r1, i); indices.push_back(t);}
            for (i = r1+1; i < r2+1; i++) {t = make_tuple(i, c2); indices.push_back(t);}
            check_r = r1; check_c = c2;
            dr1 = 1; dc2 = -1;
                    
        } else if (corner == 2) {
            // Bottom right
            r2 = a; c2 = b; r1 = a-N+step+1; c1 = b-N+step+1;
            for (i = c1; i < c2+1; i++) {t = make_tuple(r2, i); indices.push_back(t);}
            for (i = r1; i < r2; i++) {t = make_tuple(i, c2); indices.push_back(t);}
            check_r = r2; check_c = c2;
            dr2 = -1; dc2 = -1;
            
        } else {
            // Bottom left
            r2 = a; c1 = b; r1 = a-N+step+1; c2 = b+N-step-1;
            for (i = r1; i < r2+1; i++) {t = make_tuple(i, c1); indices.push_back(t);}
            for (i = c1+1; i < c2+1; i++) {t = make_tuple(r2, i); indices.push_back(t);}
            check_r = r2; check_c = c1;
            dr2 = -1; dc1 = 1;
        }
        
        // Perform search
        combs = dfs(indices, 0, x);
        for (int l = 0; l < combs.size(); l++) {
            enter = combs[l];
            for (int m = 0; m < enter.size(); m++) {
                tie(a,b) = enter[m];
                solution[a][b] = x;
            }
            GCD_ok = check_GCD_square(N, check_r, check_c, row_GCD, col_GCD, solution);
            if (GCD_ok) {
                blocked_ok = check_blocked_nums(N, solution, row_GCD, col_GCD, r1, r2, c1, c2, dr1, dr2, dc1, dc2);
                if (blocked_ok) {
                    square_subset_ok = check_for_2by2(N, solution);
                    if (square_subset_ok) {
                        subproblem_ok = refined_backtrack(N, num_digits, layers+1, nums, row_GCD, col_GCD, step+1, corners, corner_vertices, solution);
                        if (subproblem_ok) {
                            return true;
                        }
                    }
                }
            }
            for (int m = 0; m < enter.size(); m++) {
                tie(a,b) = enter[m];
                solution[a][b] = 0;
            }
        }
        
    } else {
        
        // Complete enumeration of remaining numbers
        
        set<int> nums_used; nums_used.empty();
        int r1 = 0; int r2 = N-1; int c1 = 0; int c2 = N-1;
        int num_added = 0;
        int a,b;
        
        for (int i = 0; i<N; i++) {
            for (int j=0; j<N;j++) {
                if (solution[i][j] != 0) {
                    num_added = num_added + 1;
                    nums_used.insert(solution[i][j]);
                }
            }
        }
        
        for (int i = 0; i < corners.size(); i++) {
            tie(a,b) = corner_vertices[i];
            if (corners[i] == 0) {
                r1 = max(r1, a+1);
                c1 = max(c1, b+1);
            } else if (corners[i] == 1) {
                r1 = max(r1, a+1);
                c2 = min(c2, b-1);
            } else if (corners[i]==2) {
                r2 = min(r2, a-1);
                c2 = min(c2, b-1);
            } else {
                r2 = min(r2, a-1);
                c1 = max(c1, b+1);
            }
            
        }
        
        bool reached;
        reached = backtrack(N, num_digits, num_added, nums_used, layers, nums, row_GCD, col_GCD, r1, r2, c1, c2, solution);
        if (reached) {
            return true;
        }
    }
    
    return false;
}

