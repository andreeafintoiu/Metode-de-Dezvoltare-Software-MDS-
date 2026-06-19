// ex5.cpp
#include <iostream>
#include <map>
#include <vector>
#include <string>
#include <algorithm>

int main() {
    std::map<std::string, std::vector<int>> gradebook = {
        {"alice",   {90, 85, 92}},
        {"bob",     {78, 88}},
        {"charlie", {95, 70, 80}},
    };

    std::map<std::string, int> averages;
    for (auto& [name, scores] : gradebook) {
        int sum = 0;
        for (int s : scores) sum += s;
        averages[name] = sum / scores.size();
    }

    std::vector<std::pair<std::string, int>> sorted_rankings(averages.begin(), averages.end());
    
    std::sort(sorted_rankings.begin(), sorted_rankings.end(), [](const auto& a, const auto& b) {
        return a.second > b.second;
    });

    std::cout << "Rankings:" << std::endl;
    for (auto& [name, avg] : sorted_rankings) {
        std::cout << "  " << name << ": " << avg << std::endl;
    }

    return 0;
}
