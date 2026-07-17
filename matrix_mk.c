#include <stdio.h>
#include <math.h>
int main()
{
    int refmatrix[3][3] = {{3,4,5}, {4,5,6}, {5,6,7}};
    int tempmatrix[3][3] = {{3,4,5}, {4,5,6}, {5,6,7}};
    int finalmatrix[3][3] = {{3,4,5}, {4,5,6}, {5,6,7}};
    int length=3;
    int sum=0;
    for (int k=0; k<length; k++)
    {
        for (int j=0; j<length; j++)
        {
            for (int i=0; i<length;i++)
            {
                sum += tempmatrix[k][i] * refmatrix[i][j];
            }
            finalmatrix[k][j] = sum;
            sum = 0;
        }
    }
    for (int i = 0; i < length; i++) {
        for (int j = 0; j < length; j++) {
            printf("%d ", finalmatrix[i][j]); // Print the element and a space
        }
        printf("\n"); // Move to the next line after finishing a row
    }


    
}
