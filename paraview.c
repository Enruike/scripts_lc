#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include "mkl.h"


int Nx, Ny, Nz;

double trqq(double* Q){
	return Q[0] * Q[0] + Q[3] * Q[3] + Q[5] * Q[5] + 2 * (Q[1] * Q[1] + Q[2] * Q[2] + Q[4] * Q[4]); 
}
bool norm_v(float* vec){
	double mod = 0;
	mod = sqrt(vec[0] * vec[0] + vec[1] * vec[1] + vec[2] * vec[2]); 
	if (mod == 0){
		printf("Zero vector!\n");
		return false;
	}
	else{
		vec[0] = vec[0] / mod;
		vec[1] = vec[1] / mod;
		vec[2] = vec[2] / mod;
		return true;
	}
}

float dotProduct(float* n1, float* n2){
	return n1[0] * n2[0] + n1[1] * n2[1] + n1[2] * n2[2];
}

int peri(int node, int dir){
	if(dir == 0){
		if(node >= 0 && node < Nx)	
			return node;
		else if(node >= Nx)
			return node - Nx;
		else
			return node + Nx;
	}
	else if(dir == 1){
		if(node >= 0 && node < Ny)	
			return node;
		else if(node >= Ny)
			return node - Ny;
		else 
			return node + Ny;
	}
	else if(dir == 2){
		if(node >= 0 && node < Nz)	
			return node;
		else if(node >= Nz)
			return node - Nz;
		else 
			return node + Nz;
	}
	else{
		printf("Wrong input for function periodic.\n");
	}
	return 0;
}

int main(int argc, char *argv[]){
	float a[9] = {0};
	float v[3] = {0};
	int flag;
	int l = 0;
	int info;
	float S;
	float vector[3] = {0};
	int points;
	int points_red;
	int i_red;
	
	int Nx2, Ny2, Nz2;
	int x, y, z;
	char showcolor, showssb, showen;
	float vcolor[3] = {0};
	float nu[3] = {0};
	int geo;

	int dim = 2;
	if(argc == 2){
		dim = atoi(argv[1]);
	}
	else if(argc == 5){
		dim = atoi(argv[4]);
		printf("Input should be like ./iso nx ny nz ReducedDimension.\n");
	}	
/*
	printf("Show splay bend order parameter? Type y or n.\n");
	scanf("%c%*c", &showssb);
	printf("Show color? Type y or n.\n");
	scanf("%c%*c", &showcolor);
	if(showssb != 'y' && showssb != 'n'){
		printf("Please Enter valid value.\n");
		return 1;
	}
	if(showcolor != 'y' && showcolor != 'n'){
		printf("Please Enter valid value.\n");
		return 1;
	}
*/
	showssb = 'y';
	showcolor = 'y';
	FILE* file;
	file = fopen("view.vtk", "w");
	if(file == (FILE*)NULL)
		return 1;
	fprintf(file, "# vtk DataFile Version 3.0\n");
	fprintf(file, "vtk output\n");
	fprintf(file, "ASCII\n");
	fprintf(file, "DATASET STRUCTURED_GRID\n");

	FILE* param;
	param = fopen("param.in", "r");
	fscanf(param, "Nx %d\n", &Nx);
	fscanf(param, "Ny %d\n", &Ny);
	fscanf(param, "Nz %d\n", &Nz);	
	fclose(param);

	int count = 1;
	int lineNumber = 15;
	char line[100];

	param = fopen("param.in", "r");
	while(fgets(line, sizeof(line), param) != NULL){

		if(count == lineNumber){
			//printf("%s", line);
			sscanf(line, "geo %d", &geo);
			break;
		}
		else{
			count++;
		}

	}
	fclose(param);
	//printf("Geo vale: %d\n", geo);

	points = Nx * Ny * Nz;
	Nx2 = lrint((Nx - 1) / dim) + 1;
	Ny2 = lrint((Ny - 1) / dim) + 1;
	Nz2 = lrint((Nz - 1) / dim) + 1;
	points_red = Nx2 * Ny2 * Nz2;
	int rx = lrint((Nx - 1) / 2);
	int ry = lrint((Ny - 1) / 2);
	int rz = lrint((Nz - 1) / 2);

	float* S_array;
	S_array = (float*)malloc(points_red * sizeof(float));

	int* indx;
	indx = (int*)malloc(points * sizeof(int));
	double* q;
	q = (double*)malloc(points * 6 * sizeof(double));
	for(int i = 0; i < 6*points; i++){
		q[i] = 0;
	}

	float* color;
	float* radial;
	color = (float*)malloc(points_red * sizeof(float));
	radial = (float*)malloc(points_red * sizeof(float));
	for(int i = 0; i < points_red; i++){
		color[i] = 0;
		radial[i] = 0;
	}
	vcolor[0] = vcolor[1] = 0;
	vcolor[2] = 1;
	if(showcolor == 'y'){
		if(argc == 4 || argc == 5){
			vcolor[0] = atof(argv[1]); 
			vcolor[1] = atof(argv[2]); 
			vcolor[2] = atof(argv[3]); 
			double norm;
			norm = sqrt(vcolor[0] * vcolor[0] + vcolor[1] * vcolor[1] + vcolor[2] * vcolor[2]);
			vcolor[0] /= norm;
			vcolor[1] /= norm;
			vcolor[2] /= norm;
		}
	}

	printf("There are %d points.\n", points_red);
	fprintf(file, "DIMENSIONS\t %d\t %d\t %d\t\n", Nx2, Ny2, Nz2);
	fprintf(file, "POINTS\t %d\t float\n", points_red);

	FILE* grid;
	grid = fopen("grid.bin", "rb");
	if(grid == (FILE*)NULL){
		printf("File grid.bin not found.\n");
		return 1;
	}
	for(int i = 0; i < points; i++){
		fread(&indx[i], sizeof(int), 1, grid);
	}
	fclose(grid);

	FILE* qtensor;
	qtensor = fopen("Qtensor.bin", "rb");
	if(qtensor == (FILE*)NULL){
		printf("File Qtensor.bin not found.\n");
		return 1;
	}
	for(int i = 0; i < points; i++){
		if(indx[i] == 0 || indx[i] == 1){
			for(int n = 0; n < 6; n ++){
				fread(&q[i * 6 + n], sizeof(double), 1, qtensor);
			}	
		}
	}
	fclose(qtensor);

	i_red = 0;
	l = 0;
	for (int k = 0; k < Nz; k ++) {
		for (int j = 0; j < Ny; j++){
			for (int i = 0; i < Nx; i++){
				if((i % dim == 0) && (j % dim == 0) && (k % dim == 0)){
					fprintf(file, "\t%d\t%d\t%d\n", i, j, k);
					i_red ++;
				}
				else{
					indx[l] = -2;
				} 
				l ++;
			}
		}
	}

	if(i_red != points_red){
		printf("Error. i_red %d not equal to points_red %d\n", i_red, points_red);
	}

	fprintf(file, "\n");
	fprintf(file, "POINT_DATA\t%d\n", points_red);
	fprintf(file, "VECTORS directors float\n");
	i_red = 0;

	for (int k = 0; k < Nz; k ++) {
		for (int j = 0; j < Ny; j++){
			for (int i = 0; i < Nx; i++){
				l = i + j * Nx + k * Nx * Ny;
				if(indx[l] > -2){
					vector[0] = 0;
					vector[1] = 0;
					vector[2] = 0;
					S = 0.76;
					if(indx[l] == 0 || indx[l] == 1){
						a[0] = q[l * 6 + 0];
						a[3] = q[l * 6 + 1];
						a[6] = q[l * 6 + 2];
						a[4] = q[l * 6 + 3];
						a[7] = q[l * 6 + 4];
						a[8] = q[l * 6 + 5];
						info = LAPACKE_ssyev(LAPACK_COL_MAJOR, 'v', 'u', 3, a, 3, v);
						if (info != 0) {
							printf("Error in eigenvalue routine!\n");
							return 1;
						}
						vector[0] = a[6];
						vector[1] = a[7];
						vector[2] = a[8];
						S = 0.5 * 3 * v[2];
					}

					fprintf(file, "\t%f\t%f\t%f\n", vector[0], vector[1], vector[2]);
					S_array[i_red] = S;

					if(geo == 2){
						if(showcolor == 'y'){
							color[i_red] = fabs(dotProduct(vector, vcolor));
							nu[0] = i - rx;
							nu[1] = j - ry;
							nu[2] = 0;
							
							if(nu[0] != 0 || nu[1] != 0){
								norm_v(nu);
							}
							
							radial[i_red] = fabs(dotProduct(vector, nu));
						}
					}
					else if(geo == -2){
						if(showcolor == 'y'){
							color[i_red] = fabs(dotProduct(vector, vcolor));
							nu[0] = i - rx;
							nu[1] = j - 2;
							nu[2] = 0;
							
							if(nu[0] != 0 || nu[1] != 0){
								norm_v(nu);
							}
							
							radial[i_red] = fabs(dotProduct(vector, nu));
						}
					}
					else if(geo == -22){
						if(showcolor == 'y'){
							color[i_red] = fabs(dotProduct(vector, vcolor));
							nu[0] = i - 2;
							nu[1] = j - 2;
							nu[2] = 0;
							
							if(nu[0] != 0 || nu[1] != 0){
								norm_v(nu);
							}
							
							radial[i_red] = fabs(dotProduct(vector, nu));
						}
					}
					else if(geo == -3){
						if(showcolor == 'y'){
							color[i_red] = fabs(dotProduct(vector, vcolor));
							nu[0] = i - rx;
							nu[1] = j - 2;
							nu[2] = k - rz;
							
							if(nu[0] != 0 || nu[1] != 0 || nu[2] != 0){
								norm_v(nu);
							}
							
							radial[i_red] = fabs(dotProduct(vector, nu));
						}
					}
					else if (geo == -33)
					{
						if(showcolor == 'y'){
							color[i_red] = fabs(dotProduct(vector, vcolor));
							nu[0] = i - 2;
							nu[1] = j - 2;
							nu[2] = k - rz;
							
							if(nu[0] != 0 || nu[1] != 0 || nu[2] != 0){
								norm_v(nu);
							}
							
							radial[i_red] = fabs(dotProduct(vector, nu));
						}
					}
					
					else{
						if(showcolor == 'y'){
							color[i_red] = fabs(dotProduct(vector, vcolor));
							nu[0] = i - rx;
							nu[1] = j - ry;
							nu[2] = k - rz;
							
							if(nu[0] != 0 || nu[1] != 0 || nu[2] != 0){
								norm_v(nu);
							}
							
							radial[i_red] = fabs(dotProduct(vector, nu));
						}
					}
					i_red ++;
				}
			}
		}
	}

	//print out scalar order parameters 
	fprintf(file, "\n");
	fprintf(file, "SCALARS scalars float 1\n");
	fprintf(file, "LOOKUP_TABLE default\n");
	for(int i = 0; i < points_red; i++){
		fprintf(file, "\t%f\n", S_array[i]);
	}
	
	if(showcolor == 'y'){	
		fprintf(file, "\n");
		fprintf(file, "SCALARS colors float 1\n");
		fprintf(file, "LOOKUP_TABLE default\n");
		for(int i = 0; i < points_red; i++){
			fprintf(file, "\t%f\n", color[i]);
		}

		fprintf(file, "\n");
		fprintf(file, "SCALARS radialprojection float 1\n");
		fprintf(file, "LOOKUP_TABLE default\n");
		for(int i = 0; i < points_red; i++){
			fprintf(file, "\t%f\n", radial[i]);
		}
	}

	if(showssb == 'y'){	
		//splay bend order parameter
		fprintf(file, "\n");
		fprintf(file, "SCALARS splaybend float 1\n");
		fprintf(file, "LOOKUP_TABLE default\n");
		int xm, xp, ym, yp, zm, zp;
		int xpyp, xmym, xpym, xmyp;
		int xpzp, xmzm, xpzm, xmzp;
		int ypzp, ymzm, ypzm, ymzp;
		float ddQmn;
		float ddQ[6][6];
		
		if(geo == 2 || geo == -2 || geo == -22){

			for (int k = 0; k < Nz; k ++) {
				for (int j = 0; j < Ny; j++){
					for (int i = 0; i < Nx; i++){
						
						l = i + j * Nx + k * Nx * Ny;
					
						if(indx[l] > -2){
							ddQmn = -1;
							if(indx[l] == 0){

								xm = i - 1 + j * Nx + k * Nx * Ny;
								xp = i + 1 + j * Nx + k * Nx * Ny;
								ym = i + (j - 1) * Nx + k * Nx * Ny;
								yp = i + (j + 1) * Nx + k * Nx * Ny;
								zm = i + j * Nx + peri(k - 1, 2) * Nx * Ny;
								zp = i + j * Nx + peri(k + 1, 2) * Nx * Ny;
								xmym = i - 1 + (j - 1) * Nx + k * Nx * Ny;
								xmyp = i - 1 + (j + 1) * Nx + k * Nx * Ny;
								xpym = i + 1 + (j - 1) * Nx + k * Nx * Ny;
								xpyp = i + 1 + (j + 1) * Nx + k * Nx * Ny;
								xmzm = i - 1 + j * Nx + peri(k - 1, 2) * Nx * Ny;
								xmzp = i - 1 + j * Nx + peri(k + 1, 2) * Nx * Ny;
								xpzm = i + 1 + j * Nx + peri(k - 1, 2) * Nx * Ny;
								xpzp = i + 1 + j * Nx + peri(k + 1, 2) * Nx * Ny;
								ymzm = i + (j - 1) * Nx + peri(k - 1, 2) * Nx * Ny;
								ymzp = i + (j - 1) * Nx + peri(k + 1, 2) * Nx * Ny;
								ypzm = i + (j + 1) * Nx + peri(k - 1, 2) * Nx * Ny;
								ypzp = i + (j + 1) * Nx + peri(k + 1, 2) * Nx * Ny;
				
								for (int n = 0; n < 6; n++) {
									ddQ[0][n] = (q[xp * 6 + n]+q[xm * 6 + n] - 2 * q[l * 6 + n]);
									ddQ[3][n] = (q[yp * 6 + n]+q[ym * 6 + n] - 2 * q[l * 6 + n]);
									ddQ[5][n] = (q[zp * 6 + n]+q[zm * 6 + n] - 2 * q[l * 6 + n]);
									ddQ[1][n] = (q[xpyp * 6 + n] + q[xmym * 6 + n] - q[xpym * 6 + n] - q[xmyp * 6 + n]) * 0.25;
									ddQ[2][n] = (q[xpzp * 6 + n] + q[xmzm * 6 + n] - q[xpzm * 6 + n] - q[xmzp * 6 + n]) * 0.25;
									ddQ[4][n] = (q[ypzp * 6 + n] + q[ymzm * 6 + n] - q[ypzm * 6 + n] - q[ymzp * 6 + n]) * 0.25;
								}
			
								ddQmn = ddQ[0][0] + ddQ[3][3] + ddQ[5][5] + 2 * (ddQ[4][4] + ddQ[1][1] + ddQ[2][2]);
							}
							fprintf(file, "\t%f\n", ddQmn);
						}
					}
				}
			}			
		}

		else{
			for (int k = 0; k < Nz; k ++) {
				for (int j = 0; j < Ny; j++){
					for (int i = 0; i < Nx; i++){
						l = i + j * Nx + k * Nx * Ny;
						if(indx[l] > -2){
							ddQmn = -1;
							
							if(indx[l] == 0){
								xm = i - 1 + j * Nx + k * Nx * Ny;
								xp = i + 1 + j * Nx + k * Nx * Ny;
								ym = i + (j - 1) * Nx + k * Nx * Ny;
								yp = i + (j + 1) * Nx + k * Nx * Ny;
								zm = i + j * Nx + (k - 1) * Nx * Ny;
								zp = i + j * Nx + (k + 1) * Nx * Ny;
								xmym = i - 1 + (j - 1) * Nx + k * Nx * Ny;
								xmyp = i - 1 + (j + 1) * Nx + k * Nx * Ny;
								xpym = i + 1 + (j - 1) * Nx + k * Nx * Ny;
								xpyp = i + 1 + (j + 1) * Nx + k * Nx * Ny;
								xmzm = i - 1 + j * Nx + (k - 1) * Nx * Ny;
								xmzp = i - 1 + j * Nx + (k + 1) * Nx * Ny;
								xpzm = i + 1 + j * Nx + (k - 1) * Nx * Ny;
								xpzp = i + 1 + j * Nx + (k + 1) * Nx * Ny;
								ymzm = i + (j - 1) * Nx + (k - 1) * Nx * Ny;
								ymzp = i + (j - 1) * Nx + (k + 1) * Nx * Ny;
								ypzm = i + (j + 1) * Nx + (k - 1) * Nx * Ny;
								ypzp = i + (j + 1) * Nx + (k + 1) * Nx * Ny;
			
								for (int n = 0; n < 6; n++) {
									ddQ[0][n] = (q[xp * 6 + n]+q[xm * 6 + n] - 2 * q[l * 6 + n]);
									ddQ[3][n] = (q[yp * 6 + n]+q[ym * 6 + n] - 2 * q[l * 6 + n]);
									ddQ[5][n] = (q[zp * 6 + n]+q[zm * 6 + n] - 2 * q[l * 6 + n]);
									ddQ[1][n] = (q[xpyp * 6 + n] + q[xmym * 6 + n] - q[xpym * 6 + n] - q[xmyp * 6 + n]) * 0.25;
									ddQ[2][n] = (q[xpzp * 6 + n] + q[xmzm * 6 + n] - q[xpzm * 6 + n] - q[xmzp * 6 + n]) * 0.25;
									ddQ[4][n] = (q[ypzp * 6 + n] + q[ymzm * 6 + n] - q[ypzm * 6 + n] - q[ymzp * 6 + n]) * 0.25;
								}
						
								ddQmn = ddQ[0][0] + ddQ[3][3] + ddQ[5][5] + 2 * (ddQ[4][4] + ddQ[1][1] + ddQ[2][2]);
							}
							
							fprintf(file, "\t%f\n", ddQmn);
						}
					}
				}
			}	
		}
	}

	free(q);
	free(indx);
	free(color);
	free(radial);
	free(S_array);
	fclose(file);
	return 0;
}

