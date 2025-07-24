#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <regex>
#include <filesystem>
#include <map>

namespace fs = std::filesystem;

// Supported file extensions to analyze
const std::vector<std::string> supportedExtensions = {".cpp", ".h", ".hpp", ".py", ".java"};

struct CodeMetrics {
    int cyclomaticComplexity = 1; // Starts at 1 per McCabe's metric
    int linesOfCode = 0;
    int maxNestingDepth = 0;
};

// Check if the file extension matches supported source code types
bool isSourceFile(const fs::path& path) {
    std::string ext = path.extension().string();
    for (const auto& supportedExt : supportedExtensions) {
        if (ext == supportedExt) return true;
    }
    return false;
}

// Calculate cyclomatic complexity for C++-style code (basic regex catch)
int calculateCyclomaticComplexity(const std::string& code) {
    std::regex decisionRegex(R"(\b(if|else if|for|while|case|catch|&&|\|\|)\b)");
    auto words_begin = std::sregex_iterator(code.begin(), code.end(), decisionRegex);
    auto words_end = std::sregex_iterator();
    return 1 + std::distance(words_begin, words_end);
}

// Calculate maximum nesting depth by tracking curly braces `{}` (C++/Java style)
int calculateMaxNestingDepth(const std::string& code) {
    int maxDepth = 0;
    int currentDepth = 0;
    for (char ch : code) {
        if (ch == '{') currentDepth++;
        else if (ch == '}') currentDepth--;
        if (currentDepth > maxDepth) maxDepth = currentDepth;
    }
    return maxDepth;
}

// Count lines of code excluding empty lines and whitespace-only lines
int countLinesOfCode(const std::string& code) {
    int count = 0;
    size_t pos = 0;
    while (pos < code.size()) {
        size_t end = code.find('\n', pos);
        if (end == std::string::npos) end = code.size();
        std::string line = code.substr(pos, end - pos);
        // Trim whitespace
        line.erase(0, line.find_first_not_of(" \t\r\n"));
        line.erase(line.find_last_not_of(" \t\r\n") + 1);
        if (!line.empty()) count++;
        pos = end + 1;
    }
    return count;
}

// Analyze a single file and return metrics
CodeMetrics analyzeFile(const fs::path& filepath) {
    CodeMetrics metrics;
    std::ifstream file(filepath);
    if (!file) {
        std::cerr << "ERROR: Could not open file " << filepath << std::endl;
        return metrics;
    }
    std::string content((std::istreambuf_iterator<char>(file)),
                         std::istreambuf_iterator<char>());

    metrics.cyclomaticComplexity = calculateCyclomaticComplexity(content);
    metrics.linesOfCode = countLinesOfCode(content);
    metrics.maxNestingDepth = calculateMaxNestingDepth(content);
    return metrics;
}

// Recursively scan directory and analyze all source code files found
std::map<fs::path, CodeMetrics> analyzeDirectory(const fs::path& directory) {
    std::map<fs::path, CodeMetrics> results;
    if (!fs::exists(directory) || !fs::is_directory(directory)) {
        std::cerr << "ERROR: Directory does not exist: " << directory << std::endl;
        return results;
    }

    for (auto const& dirEntry : fs::recursive_directory_iterator(directory)) {
        if (!dirEntry.is_regular_file()) continue;
        auto path = dirEntry.path();
        if (!isSourceFile(path)) continue;

        CodeMetrics metrics = analyzeFile(path);
        results.emplace(path, metrics);
    }
    return results;
}

// Print a summary report
void printReport(const std::map<fs::path, CodeMetrics>& analysisResults) {
    std::cout << "Code Review Summary:\n";
    std::cout << "-------------------------------------------------\n";
    for (const auto& [filepath, metrics] : analysisResults) {
        std::cout << "File: " << filepath.string() << "\n"
                  << "  Lines of Code: " << metrics.linesOfCode << "\n"
                  << "  Cyclomatic Complexity: " << metrics.cyclomaticComplexity << "\n"
                  << "  Max Nesting Depth: " << metrics.maxNestingDepth << "\n";
        if (metrics.maxNestingDepth > 5) {
            std::cout << "  [Warning] Deep nesting (>5) detected. Consider refactoring.\n";
        }
        if (metrics.cyclomaticComplexity > 10) {
            std::cout << "  [Warning] High cyclomatic complexity (>10). Refactor recommended.\n";
        }
        std::cout << "-------------------------------------------------\n";
    }
}

int main(int argc, char* argv[]) {
    std::cout << "=== CodeReviewer++ CLI - Basic Static Code Analyzer ===\n";
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <directory-to-analyze>\n";
        return 1;
    }
    fs::path directoryToAnalyze = argv[1];
    auto results = analyzeDirectory(directoryToAnalyze);
    if (results.empty()) {
        std::cout << "No supported source files found in directory.\n";
    } else {
        printReport(results);
    }
    return 0;
}
