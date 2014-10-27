#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <stack>
using namespace std;

//scoring scheme
// hard coded in global variables for scoring scheme (easier for testing)
// TODO: set values from command line arguements
const int o = -2;
const int e = -1;
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
//compare x and y at point (i, j) using scoring matrix
int s(const string &x, const string &y, int i, int j){
    return scoring_matrix[char_to_int(x[i-1])][char_to_int(y[j-1])];
}
//return which is a max and its value
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
/* return a std::pair of ints <index, value>.
 *  value refers to the max scoring sequence that comes to grid point (i, j) by the diagonal 
 *  value of -32767 is used as a form of N/A. It's a bit of a hack. it's the minimum value of a int (2^-15 + 1)
 *  index tells you which of {M, Ix, Iy} the max scoring sequence came from.
 *  index 0: M
 *  index 1: Ix
 *  index 2: Iy
 *  idnex 3: N/A, will be used to detect an error where -32767 is actually the max
*/
pair<int, int> M(const string &x, const string &y, int i, int j, int**** &grid){
    if(i == 0 and j == 0){
        return make_pair(3,0);
    }
    if(i == 0 or j ==0){
        return make_pair(3,-32767);
    }
    pair<int, int> p = max(grid[i-1][j-1][0][1] + s(x, y, i, j), 
            grid[i-1][j-1][1][1] + s(x,y,i,j), grid[i-1][j-1][2][1] + s(x, y, i, j));
    //I decided to allow Iy directly after Ix. I did the opposite in python. easy to change between the two as desired
    return p;
}
pair<int, int> Ix(const string &x, const string &y, int i, int j, int**** &grid){
    if(i == 0 and j == 0){
        return make_pair(3,0);
    }
    if(i == 0){
        return make_pair(3,-32767);
    }
    pair<int, int> p = max(grid[i-1][j][0][1] + o, grid[i-1][j][1][1] + e, grid[i-1][j][2][1] + o);
    //I noticed that because M, Ix and Iy are set to 0 for the origin (0,0). that means that a gap in the first base is treated as an extension.
    return p;
}
pair<int, int> Iy(const string &x, const string &y, int i, int j, int**** &grid){
    if(i == 0 and j == 0){
        return make_pair(3,0);
    }
    if(j == 0){
        return make_pair(3,-32767);
    }
    pair<int, int> p = max(grid[i][j-1][0][1] + o, grid[i][j-1][1][1] + o, grid[i][j-1][2][1] + e);
    return p;

}
int main(int argc, char *argv[]){
    //command line interface
    bool file_mode = false;
    string input_file;
    string output_file;
    if(argc > 1){
        if(strcmp(argv[1], "-f") == 0){
            if(argc != 4){
                cout << "Usage: " << argv[0] << " -f input_file output_file" << endl;
                return 1;
            }else{
                file_mode = true;
                input_file = argv[2];
                output_file = argv[3];
            }
        }else{
            cout << "Usage: " << argv[0] << " -f input_file output_file" << endl;
            return 1;
        }
    }
    //set value of x and y either with file or default values for testing
    string x;
    string y;
    if(file_mode){
        ifstream in(input_file);
        if(in.is_open()){
            getline(in,x);
            getline(in,y);
            in.close();
        }else{
            cout << "ERROR: failed to read file" << endl;
        }
    }else{
        x = "GAATTCCGTTA";
        y = "GGATCGA";
    }
    //dynamically allocate a grid. necessary because we don't know the length of x and y.
    //this is less efficient because it isn't a continous block in memory for loop ups but it's required
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
    //call M, Ix, Iy, moving down and across 
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
    //move in reverse and construct optimal path
    int i = x.length();
    int j = y.length();
    pair<int, int> f = max(grid[i][j][0][1], grid[i][j][1][1], grid[i][j][2][1]);
    int index = f.first;
    int value = f.second;
    cout << "score: " << value << endl;
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
    //print out aligned seqs
    vector<char> xout, yout;
    //allocate max possible lengths of vectors to avoid having to copy later on
    xout.reserve(x.length() + y.length());
    yout.reserve(x.length() + y.length());
    cout << "x y" << endl;
    while(arrows.size() > 0){
        int a = arrows.top();
        arrows.pop();
        if(a == 0){
            xout.push_back(x[i]);
            yout.push_back(y[j]);
            cout << x[i] << " " << y[j] << endl;
            i++;
            j++;
        }else if(a == 1){
            xout.push_back(x[i]);
            yout.push_back('-');
            cout << x[i] << " " << "-" << endl;
            i++;
        }else if(a == 2){
            xout.push_back('-');
            yout.push_back(y[j]);
            cout << "-" << " " << y[j] << endl;
            j++;
        }else if(a == 3){
            cout << "ERROR" << endl;
        }
    }
    //write to output
    if(file_mode){
        ofstream output;
        output.open(output_file);
        for(vector<char>::const_iterator i = xout.begin(); i != xout.end(); i++)
            output << *i;
        output << '\n';
        for(vector<char>::const_iterator i = yout.begin(); i != yout.end(); i++)
            output << *i;
        output << '\n';
        output.close();
    }
    // cleanup dynamicly allocated array
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
