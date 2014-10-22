#include <iostream>
#include <string>
#include <vector>
#include <stack>
using namespace std;

//scoring scheme
const int d = -2;
const int match = +1;
const int transition = -1;
const int transversion = -2;

int ***grid;

int scoring_matrix[4][4] = 
    {
        {match, transition, transversion, transversion},//C 
        {transition, match, transversion, transversion},//T
        {transversion, transversion, match, transition},//A
        {transversion, transversion, transition, match} //G
    };

int char_to_int(char base){
    if(base == 'C'){
        return 0;
    }
    if(base == 'T'){
        return 1;
    }
    if(base == 'A'){
        return 2;
    }
    else{
        return 3;
    }
}

int s(string x, string y, int i, int j){
    return scoring_matrix[char_to_int(x[i-1])][char_to_int(y[j-1])];
}
pair<int, int> max(int x, int y, int z){
    int max = x;
    int i = 0;
    if (y > max){
        max = y;
        i = 1;
    }
    if(z > max){
        max = z;
        i = 2;
    }
    return make_pair(i, max);
}
pair<int, int> F(string x, string y, int i, int j){
    if(i == 0 and j == 0){
        return make_pair(3,0);
    }
    if(i > 0 and j > 0){
        pair<int, int> p = max(grid[i-1][j-1][1] + s(x, y, i, j), grid[i-1][j][1] + d, grid[i][j-1][1] + d);
        return p;
    }
    if(i > 0){
        int value = grid[i-1][j][1] + d;
        return make_pair(1, value);
    }else{
        int value = grid[i][j-1][1] + d;
        return make_pair(2,value);
    }
}

int main(){
    const string x = "GAATTCCGTTA";
    const string y = "GGATCGA";
//    int grid[x.length()][y.length()][2];
    grid = new int**[x.length()+1];
    for(int i = 0; i < x.length() + 1; i++){
        grid[i] = new int*[y.length()+1];
        for(int j = 0; j< y.length() +1; j++){
            grid[i][j] = new int[2];
        }
    }

    for(int i=0; i<= x.length(); i++){
        for(int j=0; j<= y.length(); j++){
            pair<int, int> p = F(x, y, i, j);
            grid[i][j][0] = p.first;
            grid[i][j][1] = p.second;
        }
    }
     
    int i = x.length();
    int j = y.length();
    stack<int> arrows;
    while(i > 0 or j > 0){
        int index = grid[i][j][0];
        arrows.push(index);
        if(index == 0){
            i--;
            j--;
        }else if(index == 1){
            i--;
        }else if(index == 2){
            j--;
        }
    }

    while(arrows.size() > 0){
        int a = arrows.top();
        arrows.pop();
        if(a == 0){
            cout << x[i] << " " << y[j] << endl;
            i++;
            j++;
        }else if(a == 1){
            cout << x[i] << " " << "-" << endl;
            i++;
        }else if(a == 2){
            cout << "-" << " " << y[j] << endl;
            j++;
        }
    }
    for(int i = 0; i < x.length() + 1; i++){
        for(int j = 0; j< y.length() +1; j++){
            delete[] grid[i][j];
        }
        delete [] grid[i];
    }
    
    return 0;
}
