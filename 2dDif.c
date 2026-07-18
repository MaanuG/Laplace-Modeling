#include <stdio.h>
#include <math.h>
#include <string.h>

int main()
{

    double dx = 0.1;
    double dy = 0.1;

    double xlength = 3.0;
    double ylength = 2.0;

    double D = 1.0;          
    double dt = 0.002;       
    double totalTime = 1.0;

    int nx = (int)(xlength / dx) + 1;
    int ny = (int)(ylength / dy) + 1;

    int Nt = (int)(totalTime / dt);



    double alpha = D * dt / (dx * dx);

    if (alpha > 0.25)
    {
        printf("WARNING: Explicit scheme is unstable!\n");
        printf("Current alpha = %f\n", alpha);
        return 1;
    }

    FILE *fileout = fopen("diffusion.txt", "w");

    if (fileout == NULL)
    {
        printf("Error opening file.\n");
        return 1;
    }


    double rho[nx][ny];
    double rho_new[nx][ny];


    for (int i = 0; i < nx; i++)
    {
        for (int j = 0; j < ny; j++)
        {
            rho[i][j] = 0.0;
            rho_new[i][j] = 0.0;
        }
    }


    int cx = nx / 2;
    int cy = ny / 2;

    rho[cx][cy] = 50.0;
    rho_new[cx][cy] = 50.0;


    for (int n = 0; n <= Nt; n++)
    {
        double time = n * dt;


        fprintf(fileout, "===== Time = %.5f =====\n", time);

        for (int i = 0; i < nx; i++)
        {
            for (int j = 0; j < ny; j++)
            {
                fprintf(fileout,
                        "x %.2f  y %.2f  rho %.6f\n",
                        i * dx,
                        j * dy,
                        rho[i][j]);
            }
        }

        fprintf(fileout, "\n");


        for (int i = 1; i < nx - 1; i++)
        {
            for (int j = 1; j < ny - 1; j++)
            {
                double laplacian =
                    rho[i+1][j]
                  + rho[i-1][j]
                  + rho[i][j+1]
                  + rho[i][j-1]
                  - 4.0 * rho[i][j];

                rho_new[i][j] =
                    rho[i][j]
                    + alpha * laplacian;
            }
        }


        for (int i = 0; i < nx; i++)
        {
            rho_new[i][0] = 0.0;
            rho_new[i][ny-1] = 0.0;
        }

        for (int j = 0; j < ny; j++)
        {
            rho_new[0][j] = 0.0;
            rho_new[nx-1][j] = 0.0;
        }


        memcpy(rho, rho_new, sizeof(rho));
    }

    fclose(fileout);

    printf("Simulation complete.\n");
    printf("Output written to diffusion.txt\n");

    return 0;
}
