#include <iostream>
#include <string>
#include <vector>
#include <stack>
using namespace std;

//scoring scheme

const int o = -2;
const int e = -1;
const int d = -2;
const int match = +2;
const int transition = -1;
const int transversion = -1;

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

int s(const string &x, const string &y, int i, int j){
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
pair<int, int> Ix(const string &x, const string &y, int i, int j, int**** &grid){
    if(i == 0 and j == 0){
        return make_pair(3,0);
    }
    if(i == 0){
        return make_pair(3,-99999);
    }
    pair<int, int> p = max(grid[i-1][j][0][1] + o, grid[i-1][j][1][1] + e, grid[i-1][j][2][1] + o);
    return p;
}
pair<int, int> Iy(const string &x, const string &y, int i, int j, int**** &grid){
    if(i == 0 and j == 0){
        return make_pair(3,0);
    }
    if(j == 0){
        return make_pair(3,-99999);
    }
    pair<int, int> p = max(grid[i][j-1][0][1] + o, grid[i][j-1][1][1] + o, grid[i][j-1][2][1] + e);
    return p;

}
pair<int, int> M(const string &x, const string &y, int i, int j, int**** &grid){
    if(i == 0 and j == 0){
        return make_pair(3,0);
    }
    if(i == 0 or j ==0){
        return make_pair(3,-99999);
    }
    pair<int, int> p = max(grid[i-1][j-1][0][1] + s(x, y, i, j), grid[i-1][j-1][1][1] + s(x,y,i,j), grid[i-1][j-1][2][1] + s(x, y, i, j));
    return p;

}
int main(){
    const string x = "GAATTCCGTTA";
    const string y = "GGATCGA";
    int ****grid;
    grid = new int***[x.length()+1];
    for(int i = 0; i < x.length() + 1; i++){
        grid[i] = new int**[y.length()+1];
        for(int j = 0; j< y.length() +1; j++){
            grid[i][j] = new int*[3];
            for(int h = 0; h < 3; h++){
                grid[i][j][h] = new int[2];
            }
        }
    }
    for(int i=0; i<= x.length(); i++){
        for(int j=0; j<= y.length(); j++){
            pair<int, int> m = M(x, y, i, j, grid);
            pair<int, int> ix = Ix(x, y, i, j, grid);
            pair<int, int> iy = Iy(x, y, i, j, grid);
            grid[i][j][0][0] = m.first;
            grid[i][j][0][1] = m.second;
            grid[i][j][1][0] = ix.first;
            grid[i][j][1][1] = ix.second;
            grid[i][j][2][0] = iy.first;
            grid[i][j][2][1] = iy.second;
        }
    }

    int i = x.length();
    int j = y.length();
    pair<int, int> f = max(grid[i][j][0][1], grid[i][j][1][1], grid[i][j][2][1]);
    int index = f.first;
    int value = f.second;
    cout << value << endl;
    cout << index << endl;
    stack<int> arrows;
    while(i > 0 or j > 0){
        arrows.push(index);
        int new_index = grid[i][j][index][0];
        if(index == 0){
            i--;
            j--;
        }else if(index == 1){
            i--;
        }else if(index == 2){
            j--;
        }
        index = new_index;
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
            for(int h = 0; h< 3; h++){
                delete[] grid[i][j][h];
            }
            delete[] grid[i][j];
        }
        delete [] grid[i];
    }
    
    return 0;
}
