#include <stdio.h>
#include <math.h>
#include <stdbool.h>
#include <string.h>

int main() {
    FILE *fileout;
    double xstep = 0.1;
    double ystep = 0.1;
    int xlength = 3;
    int ylength = 2;
    int Nits = 1000;
    double V0 = 8.0;

    // 1. Define dimensions
    int i = (double)xlength / xstep;
    int j = (double)ylength / ystep;

    fileout = fopen("laplace.txt", "w");
    if (fileout == NULL) {
        printf("Error opening file.\n");
        return 1;
    }

    // 2. Declare the matrices
    float matrix[i][j];
    float new_matrix[i][j];

    // Initialize both matrices with 0.0
    for (int r = 0; r < i; r++) {
        for (int c = 0; c < j; c++) {
            matrix[r][c] = 0.0f;
            new_matrix[r][c] = 0.0f;
        }
    }

    // 3. Set the first row (index 0) to V0
    for (int col = 0; col < j; col++) {
        matrix[0][col] = (float)V0;
        new_matrix[0][col] = (float)V0;
    }

    // 4. Iteration Loop
    for (int x = 1; x <= Nits; x++) {
        for (int r = 1; r < i - 1; r++) {
            for (int c = 1; c < j - 1; c++) {
                new_matrix[r][c] = 0.25f * (matrix[r - 1][c] + matrix[r + 1][c] + matrix[r][c - 1] + matrix[r][c + 1]);
            }
        }

        // Copy new_matrix to matrix using memcpy
        memcpy(matrix, new_matrix, sizeof(matrix));

        // Save progress at iteration 1, and then every 10 iterations thereafter
        if (x == 1 || x % 10 == 0) {
            fprintf(fileout, "--- Iteration %d ---\n", x);
            
            // Loop through every row and column
            for (int r = 0; r < i; r++) {
                for (int c = 0; c < j; c++) {
                    double x_val = r * xstep;
                    double y_val = c * ystep;
                    fprintf(fileout, "x: %.2f  y: %.2f  Potential: %.4f\n", x_val, y_val, matrix[r][c]);
                }
            }
            fprintf(fileout, "\n"); // Blank line for readability between matrices
        }
    }

    fclose(fileout);
    printf("High-resolution progress saved to laplace.txt (101 frames total)\n");
    return 0;
}
