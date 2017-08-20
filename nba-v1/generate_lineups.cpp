#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
#include <algorithm>
#include <set>
#include <map>

using namespace std;

void parse_file(string file_name, vector < vector < string > > &out)
{
    fstream file;
    file.open(file_name.c_str());
    for (string line; getline(file,line);)
    {
        vector < string > row;
        stringstream curr_row(line);
        while (curr_row.good())
        {
            string sub;
            getline(curr_row, sub, ',');
            sub.erase(remove(sub.begin(), sub.end(), '"'), sub.end());
            row.push_back(sub);
        }
        out.push_back(row);
    }
}

void print_vector(vector < vector < string > > &player_list)
{
    for (int i = 0; i< player_list.size(); i++)
    {
        for (int j = 0; j < player_list[0].size(); j++)
            {
                cout << player_list[i][j];
            }
            cout<<endl;
    }
}

void get_positions(const vector < vector < string > > &player_list, map <string, vector <int> > &positions, int column)
{
    for (int i = 0; i < player_list.size(); i++)
    {
        positions[player_list[i][column]].push_back(i);
    }
}

void get_lineups( const vector < vector < string > > &player_list, const vector < string > &heading, set < set < string > > &lineups)
{
}

int main()
{
    vector < vector < string > > player_list;
    parse_file("D:/fd_nba.csv", player_list);
    vector < string > heading = player_list[0];
    player_list.erase(player_list.begin());
    set < set < string > > lineups;
    int max_intersection = 4;
    map <string, vector <int> > positions;
    cout<<"1"<<heading[1]<<"1"<<endl;

    print_vector(player_list);
    get_positions(player_list, positions, find(heading.begin(), heading.end(), "Position") - heading.begin());
    get_lineups(player_list, heading, lineups);

    return 0;
}
