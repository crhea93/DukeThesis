//
//  main.cpp
//  Packing_Fraction
//
//  Created by Carter Rhea on 4/8/2017.
//  Copyright © 2017 Carter Rhea. All rights reserved.
//
/*
 Program Function: This program was created to read in data from .txt file which contains the x and y positions of particles along with their radius and calculates the packing fraction of the particles for a given radius. The packing fraction is the sum of all the particles areas (whether completely or partially intersecting the annulus) divided by that of the annulus. Finally the program follows the nodes given by Christian which it then steps through the Packing Fraction calculator in order to find the packing fraction as a function of annulus radius and grid location to give a schema of Packing Fractions. This is outputted into a .csv file which contains the X and Y coordinates of the annulus along with the Packing Fraction for an annulus centered at that location.
 Formulas:
 d - Basic distance formula
 A_in_calc - Calculates the area of the particles which are completely contained within the annulus
 A_mid_calc - Calculates the area of the particles whose centers lie between the inner and mid radii (defined later). It determines whether the particle is completely contianed within the circle or if it overlaps with it (using the lens equation).
 A_out_calc - Calculates the area of thep particles who centers lie between the mid and outer radii (defined later). It determines whether or not the particle ovelaps the annulus. If so, then it calculates the area of the overlap. It uses the lens equation for this.
 Max_val - Calculates the maximum radius of a particle using the data from the .txt file.
 Min_val - Calculates the minimum radius of a particle using the data from the .txt file.
 Packing_Fraction - This function opens the .txt file and calculates the packing fraction (which is returns).

 */

//#include "additional.h"
//#include "NN.hpp"
//#include "PF.hpp"

#include <iomanip>
#include <array>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <stdio.h>
#include <math.h>
#include <vector>
#include <map>
#include <tuple>
#define _USE_MATH_DEFINES
using namespace std;
//user defined headers
double distances(double x_pos1, double y_pos1, double x_pos2, double y_pos2){
    float power = 2.0;
    double x_diff = pow(x_pos2 - x_pos1,power);
    double y_diff = pow(y_pos2 - y_pos1,power);
    double dist = x_diff+y_diff;
    double true_dist = sqrt(dist);
    return true_dist;
}

//max value from vector
double max_val_vec(vector<double> vec){
    double max_val = 0.0; //need better value here
    double* pmax_val = &max_val;
    for (int i=0;i<vec.size();i++){
        if (vec[i]>*pmax_val){
            *pmax_val = vec[i];
        }
    }
    return max_val;
}


//calculates the max val iterator of the dist vector and correspondes it with the value of the index at that same iterator
int index_of_max(vector<double> dist,vector<int> index){
    double max_val = 0;
    double* pmax_val = &max_val;
    int max_val_it = 0;
    int* pmax_val_it = &max_val_it;
    for (int i=0;i<dist.size();i++){
        if (dist[i]>*pmax_val){
            *pmax_val_it = index[i];
        }
    }
    return max_val_it;
}
//calculate the index of the max val of the inputted vector
int index_of_max_dist(vector<double> vec){
    double max_val = 0.0;
    double* pmax_val = &max_val;
    int max_val_it = 0;
    int* pmax_val_it = &max_val_it;
    for (int i=0;i<vec.size();i++){
        if (vec[i]>*pmax_val){
            *pmax_val_it = i;
        }
    }
    return max_val_it;
}


int index_of_min(vector<double> dist,vector<int> index){
    double min_val = 10000;//arbitrary for now
    double* pmin_val = &min_val;
    int min_val_it = 0;
    int* pmin_val_it = &min_val_it;
    for (int i=0;i<dist.size();i++){
        if (dist[i]<*pmin_val){
            *pmin_val_it = index[i];
            *pmin_val = dist[i];
        }
    }
    return min_val_it;
}
//calculate the index of the max val of the inputted vector
int index_of_min_vec(vector<double> vec){
    double min_val = 10000;
    double* pmin_val = &min_val;
    int min_val_it = 0;
    int* pmin_val_it = &min_val_it;
    for (int i=0;i<vec.size();i++){
        if (vec[i]<*pmin_val){
            *pmin_val_it = i;
            *pmin_val = vec[i];
        }
    }
    return min_val_it;
}
//calculate the min val of the inputted vector
double min_val_vec(vector<double> vec){
    double min_val = 10000; //need better value here
    double* pmin_val = &min_val;
    for (int i=0;i<vec.size();i++){
        if (vec[i]<*pmin_val){
            *pmin_val = vec[i];
        }
    }
    return min_val;
}

//calculate what part of the annulus is in the domain
double ann_area_calc(double annulus_x,double annulus_y,float annulus_radius,float domain_radius){
    double A = 0.0;
    double A_1 = 0.0;
    double A_2 = 0.0;
    double A_3 = 0.0;
    double r_1 = domain_radius;
    double r_2 = annulus_radius;
    double distance_ann = distances(annulus_x,annulus_y,0.0,0.0);
    double power = 2.0;
    if (distance_ann <= domain_radius-annulus_radius){
        A = M_PI*pow(annulus_radius,power);
        return A;
    }
    else {
        A_1 = pow(r_1,power)*acos((pow(distance_ann,power)+pow(r_1,power)-pow(r_2,power))/(2*distance_ann*r_1));
        A_2 = pow(r_2,power)*acos((pow(distance_ann,power)+pow(r_2,power)-pow(r_1,power))/(2*distance_ann*r_2));
        A_3 = (1./2.)*sqrt((-distance_ann+r_1+r_2)*(distance_ann+r_1-r_2)*(distance_ann-r_1+r_2)*(distance_ann+r_1+r_2));
        A =  A_1+A_2-A_3 ;
        return A;
    }

}
//calculate particles' areas totally inside the annulus
double A_in_calc(double rad, float annulus_radius){
    double A = 0.0;
    if (rad<annulus_radius){
        A = M_PI*pow(rad,2.0);
    }
    else{
        A = M_PI*pow(annulus_radius, 2.0);
    }
    return A;
}
//calculate particles' areas whose centers are in the annulus but aren't contained completely
double A_mid_calc(double x_pos, double y_pos, double rad, float annulus_radius, double annulus_x, double annulus_y){
    double A=0.0;
    double distance_ann = distances(x_pos,y_pos, annulus_x, annulus_y);
    double r_1 = annulus_radius;
    double r_2 = rad;
    float power = 2.0;
    // Now to decide whether or not the partcile lies completely or partially within the annulus.
    if (distance_ann + r_2 <= r_1){
        A = M_PI*pow(r_2,power);
        return A;
    }
        // If not we must use the lens equation.
    else {
        double A_1 = pow(r_1,power)*acos((pow(distance_ann,power)+pow(r_1,power)-pow(r_2,power))/(2*distance_ann*r_1));
        double A_2 = pow(r_2,power)*acos((pow(distance_ann,power)+pow(r_2,power)-pow(r_1,power))/(2*distance_ann*r_2));
        double A_3 = (1./2.)*sqrt((-distance_ann+r_1+r_2)*(distance_ann+r_1-r_2)*(distance_ann-r_1+r_2)*(distance_ann+r_1+r_2));
        A = A_1+A_2-A_3;
        return A;
    }
}
//calculates particles' areas whose centers are outside the annulus but overlap with it

double A_out_calc(double x_pos, double y_pos, double rad, float annulus_radius, double annulus_x, double annulus_y){
    double A=0.0;
    double distance_ann = distances(x_pos,y_pos,annulus_x,annulus_y);
    double r_1 = annulus_radius;
    double r_2 = rad;
    float power = 2.0;
    if (distance_ann <= r_1+r_2){
        double A_1 = pow(r_1,power)*acos((pow(distance_ann,power)+pow(r_1,power)-pow(r_2,power))/(2*distance_ann*r_1));
        double A_2 = pow(r_2,power)*acos((pow(distance_ann,power)+pow(r_2,power)-pow(r_1,power))/(2*distance_ann*r_2));
        double A_3 = (1./2.)*sqrt((-distance_ann+r_1+r_2)*(distance_ann+r_1-r_2)*(distance_ann-r_1+r_2)*(distance_ann+r_1+r_2));
        A =  A_1+A_2-A_3 ;
        //return A;
    }
    else{
        //std::cout<<"Particle values not calculated"<<std::endl;
    }
    return A;
}


double max_val(double vect[], int* nval){
    double temp = 0;
    for(int i = 0; i < *nval; i++){
        if(vect[i]>temp){
            temp = vect[i];
        }
    }
    return temp;
}

double min_val(double vect[], int* nval){
    double temp = max_val(vect,nval);
    for(int i = 0; i < *nval; i++){
        if(vect[i]<temp){
            temp = vect[i];
        }
    }
    return temp;
}
//create class for each node to store packing fraction data
class node{
public:
    double x;
    double y;
    double packing_fraction=0.0;

    void Packing_Fraction_Calculation(double domain_radius, double annulus_radius, double annulus_x,
                                      double annulus_y, double max_rad, vector<double> x_pos,vector<double> y_pos,
                                      vector<double> rad, vector<double> dist);
};

tuple<map<int,vector<int>>,map<int,vector<int>>,map<int,int>,map<int,int>> Nearest_neightbors_both(const int* pnparticles,int* pmesh,vector<double> x_pos,vector<double> y_pos,vector<double> x_mesh,vector<double> y_mesh, double max_x_val, int num_of_NN){
    //size of mesh for nearest neighbor search
    int grid_size_mesh = 101;//number of nodes per row/column
    int jump = 100;//value that makes sure we are on the right cell number! number of cells per row/column
    struct cell{
        vector <int> indices; //must use stack and not heap here since size of indices will change constantly
        vector <int> mesh_ind; //easier to allow it to be in dynamically allocated by std::vector with .push_back() .

    };
    vector<vector<cell>> cells(100,vector<cell>(100));//jump^2 . Make an array of cell type

    //cout<<"built cells"<<endl;
    double x_grid_mesh[grid_size_mesh] ;
    double y_grid_mesh[grid_size_mesh] ;
    //dependent on the size of the annulus! This could definately change depending on what we are looking at
    double h_x = (2*max_x_val+0.25)/(grid_size_mesh-1.0);
    double h_y = (2*max_x_val+0.35)/(grid_size_mesh-1.0);
    //double h_x = (1510)/(grid_size_mesh-1.0);
    //double h_y = (1510)/(grid_size_mesh-1.0);
    for(int i = 0; i < grid_size_mesh; i++){
        x_grid_mesh[i] =-(max_x_val+.1)+i*h_x;
        //cout<<x_grid_mesh[i]<<endl;
    }
    for(int i = 0; i < grid_size_mesh; i++){
        y_grid_mesh[i] =-(max_x_val+.1)+i*h_y;
    }

    //Now our bounding box should be a bit bigger than our domain!
    //cout<<"set up grid"<<endl;

    //cout<<x_mesh_res[0]<<" "<<x_mesh[21]<<endl;
    // Populate cells with nodes and particles
    int in_count = 0;
    int in1 = 0;
    int in2 = 0;
  #pragma omp sections
  {
    #pragma omp section
    {
    //int in_count=0;
    for (int i=0;i<*pmesh;i++){ //all mesh
        for (int j=0;j<grid_size_mesh-1;j++){ // x positions of grid
            for (int k=0;k<grid_size_mesh-1;k++){ // y positions of grid
                //now check where the particle is...

                if (((x_mesh[i]>=x_grid_mesh[j])&&(x_mesh[i]<x_grid_mesh[j+1]))&&((y_mesh[i]>=y_grid_mesh[k])&&(y_mesh[i]<y_grid_mesh[k+1]))){ //push back index
                    cells[j][k].mesh_ind.push_back(i); //ex) i=1,j=2 ==> cell (22) look at diagram. That is also second row and third column
                    in1++;
                }//end if

          }//end k
        }//end j
    }//end i
  }//end section
    #pragma omp section
    {
      //in2 = 0;
    for (int i=0;i<*pnparticles;i++){ //all particles
        for (int j=0;j<grid_size_mesh-1;j++){ // x positions of grid
            for (int k=0;k<grid_size_mesh-1;k++){ // y positions of grid
                //now check where the particle is...
                if (((x_pos[i]>x_grid_mesh[j])&&(x_pos[i]<=x_grid_mesh[j+1]))&&((y_pos[i]>y_grid_mesh[k])&&(y_pos[i]<=y_grid_mesh[k+1]))){ //push back index
                    cells[j][k].indices.push_back(i); //ex) i=1,j=2 ==> cell (22) look at diagram. That is also second row and third column
                    //cout << "IN!"<<endl;
                    in2++;
                }//end if
            }//end k
        }//end j
    }//end i
  }//end section
}//end sections
  in_count = in1+in2;
    vector<int> ind;
    map<int, vector<int>> NN_part;
    map<int,int> Cell_part; //Map between particle and cell number

    //I am going to store all the nodes in a map that maps the particle to its list of nearest neighbors (particles)!

    vector<int> part_ind;
    map <int, vector<int>> NN_mesh;
    map <int,int> Cell_mesh;
    #pragma omp parallel
    {
    int mesh_nodes_number = 0;
    int number_in = 0;
    #pragma omp for private(part_ind) schedule(dynamic,10)
    for (int i=0;i<grid_size_mesh-1;i++){
        for(int j=0; j<grid_size_mesh-1;j++){
            if (cells[i][j].mesh_ind.size() >0){
                for(int k=0; k<cells[i][j].mesh_ind.size();k++){//stepping through each node in each cell
                    part_ind.clear();
                    int add=0;
                    int mesh_ind = cells[i][j].mesh_ind[k];
                    //cout<<"I am mesh node number "<<mesh_nodes_number<<endl;
                    //cout<<"We are finding "<<part_ind.size()<<" many particles"<<endl;
                    while (part_ind.size()<num_of_NN){//search until we find enough particles
                        part_ind.clear();
                        for (int m=-add;m<add+1;m++){//left right  search
                            for (int n=-add;n<add+1;n++){//up down search
                                if ((i+m>=0&&i+m<jump)&&(j+n>=0&&j+n<jump)){ // make sure we stay within cell
                                    for (int part_in_cell=0;part_in_cell<cells[i+m][j+n].indices.size();part_in_cell++){
                                        int particle = cells[i+m][j+n].indices[part_in_cell];
                                        part_ind.push_back(particle);
                                        number_in++;
                                    }
                                }
                                else{
                                    //cout<<"Cell doesnt exist. Moving to next cell"<<endl;
                                }//not a cell. do nothing
                            }
                        }
                        add++;//check further around
                        //cout<<"We have found this many particles in the cell for node number "<<mesh_ind<<": "<<part_ind.size()<<endl;

                    }//end while loop so found enough particles



                    mesh_nodes_number ++;
                    //still at mesh point "k"; now lets get a list of distances between mesh point k and the surrounding particles from part_ind
                    vector<double> mesh_part_distances;
                    for (int part=0;part<part_ind.size();part++){
                        int current_particles_index = part_ind[part];
                        double dist = distances(x_mesh[mesh_ind], y_mesh[mesh_ind], x_pos[current_particles_index], y_pos[current_particles_index]);
                        mesh_part_distances.push_back(dist);//just added the distance between the mesh point and the particle
                    }//done filling distance vector!
                    //now to get the 10 particles nearest to the mesh point using mesh_part_distances
                    vector<int> NN_mesh_part_rel ;//list of NN for this particular mesh_ind
                    for (int nn=0;nn<part_ind.size();nn++){//just 1!
                        //int index_of_nearest_particle = index_of_min(mesh_part_distances,part_ind);
                        int index_of_min = index_of_min_vec(mesh_part_distances);
                        NN_mesh_part_rel.push_back(part_ind[index_of_min]); //now we have added the nearest particle to the NN list
                        part_ind.erase(part_ind.begin()+index_of_min);
                        mesh_part_distances.erase(mesh_part_distances.begin()+index_of_min); // effectively ignore the (erase) the previous min dist.

                    }//end of nearest neighbor calculations
                    //now that we have finished filling the NN list for the mesh point "k" lets add it to our map
                    NN_mesh.insert(pair<int,vector<int>>(mesh_ind,NN_mesh_part_rel));//now we added the mesh index and its NN particles to my map!!
                }//end of k

            }//end of if there are any nodes in cell 20*i+j

        }//end of j
    }//end of i and nearest neighbor search
  }//end parallel


    return make_tuple(NN_part,NN_mesh,Cell_part,Cell_mesh);
}




void node::Packing_Fraction_Calculation(double domain_radius, double annulus_radius, double annulus_x, double annulus_y,
                                        double max_rad, vector<double> x_pos, vector<double> y_pos, vector<double> rad,
                                        vector<double> dist) {
    //set annulus parts of interest which are used in determining overlap candidates
    double inner, mid, outer;
    inner = annulus_radius - max_rad;
    mid = annulus_radius;
    outer = annulus_radius + max_rad;
    //find area of particles totally inside the circle and those that overlap
    //Some initialization
    double A_in_total = 0.0;
    double A_mid_total = 0.0;
    double A_out_total = 0.0;
    double A_total = 0.0;
    double A_annulus = 0.0;
    A_annulus = ann_area_calc(annulus_x,annulus_y,annulus_radius, domain_radius);
    //Now to calculate our different areas.
    int i;
    #pragma omp for private(i)
    for (i=0;i<dist.size();i++){
        //if (distances(x_pos[i],y_pos[i],0.0,0.0)>domain_radius){//particle not totally in domain
        //    cout<<"particle not in annulus"<<endl;
        //    A_total += 0.0; //for now set to zero. Soon we need to do 3 circle intersection!
        //}
        //else{//particle totally in domain
            if(dist[i] <= inner){
                A_in_total += A_in_calc(rad[i],annulus_radius);
            }
            if((dist[i] > inner) and (dist[i] <= mid)){
                A_mid_total += A_mid_calc(x_pos[i],y_pos[i],rad[i],annulus_radius,annulus_x,annulus_y);
            }
            if((dist[i] > mid) and (dist[i] <= outer)){
                A_out_total += A_out_calc(x_pos[i],y_pos[i],rad[i],annulus_radius,annulus_x,annulus_y);
            }
            else{
                //cout<<"Particle not in the annulus"<<endl;
            }
        //}//end else
    }//end of iteration
    // now for calculating the Packing Fraction
    A_total = A_in_total+A_mid_total+A_out_total;
    /*if (A_total==0){
        cout<<"I am positioned at : "<<annulus_x<<" " <<annulus_y<<endl;
        cout<<"The number of particles near this annulus are: "<<dist.size()<<endl;
        cout<<"The distance between the first particle and the annulus' center is: "<<dist[0]<<endl;*/
//  cout<<"A_total is :"<<A_total<<endl;
        //cout<<"A_annulus is:"<<A_annulus<<endl;
        //cout<<" "<<endl;
    //}
    packing_fraction = A_total/A_annulus+1e-2;
    //std::cout<<packing_fraction<<std::endl;
    //return PF;
}


// Here we will actually set the annulus radius and grid size and then create our .csv file
int create(string input_path_initial_data, string output_path, string mesh_to_read, string mesh_connectivity, string file_name, string outputname, float domain_radius, float annulus_radius, const int* pnparticles, int* pnnodes, int* number_cell_elements, int num_of_NN, double particle_rad){
    //now we determine the x,y coordinate pairs corresponding to nodes given by Christian
    string line1;
    vector<vector<double>> Values(*pnnodes,vector<double>(2));
    //string filename;
    ifstream fileIN1;

    fileIN1.open(mesh_to_read+".txt");

    //
    //read data file
    while(fileIN1){

        for(int i=0;i<*pnnodes;i++){
            for (int j=0;j<2;j++){
                fileIN1 >> Values[i][j];
            }
        }

    }
    cout<<"We have finished reading in all of the mesh nodes!"<<endl;
    fileIN1.close();
    vector<double> x_grid(*pnnodes);
    vector<double> y_grid(*pnnodes);


    for(int i = 0; i < *pnnodes; i++){
        x_grid[i] = Values[i][0];
    }

    for(int i = 0; i < *pnnodes; i++){
        y_grid[i] = Values[i][1];
    }

    fileIN1.close();
    //done reading in mesh

    // Simply some housekeeping so that we can properly read in the file as an array

    vector<vector<double>> Values_part(*pnparticles,vector<double>(2));//number depends on mesh file read in
    //string filename;
    ifstream fileIN2;
    //Reading in particles from LAMMPSFILES
    std::cout<<"Reading in LAMMPS Data"<<std::endl;
    fileIN2.open(input_path_initial_data+file_name+".txt");
    std::cout<<input_path_initial_data+file_name+".txt"<<std::endl;
    while(fileIN2){
        for(int i=0;i<*pnparticles;i++){
            for (int j=0;j<2;j++){
                fileIN2 >> Values_part[i][j];
              //  std::cout<<Values_part[i][j]<<" ";

          }//end if
        //  std::cout<<" "<<std::endl;
        }

        //std::cout<<" "<<std::endl;

    }
    fileIN2.close();
    //cout<<"Starting to set up particle informational vectors"<<endl;
    //Lets create the parameters of interest! I dont care about the velocities so Ill ignore those columns.
    vector<double> x_pos(*pnparticles);
    vector<double> y_pos(*pnparticles);
    vector<double> rad(*pnparticles);
    //must divide by 100 to normalize particles given by yingjie into cm
    for(int i = 0; i < *pnparticles; i++){
        x_pos[i] = (Values_part[i][0]);
        y_pos[i] =  (Values_part[i][1]);
        rad[i] = particle_rad;

    }

    //cout<<"We have finished reading in all of the particles!"<<endl;



    //read in the mesh connectivity...
    ifstream fileIN3;
    //values from matlab must have 1 subtracted

    vector<vector<double>>Values_mesh(*number_cell_elements,vector<double>(4));

    fileIN3.open(mesh_connectivity+".txt");
    std::cout<<"Reading in connectivity"<<std::endl;
    //
    //read data file
    while(fileIN3){

        for(int i=0;i<*number_cell_elements;i++){
            for (int j=0;j<4;j++){
                fileIN3 >> Values_mesh[i][j];

            }
        }
    }
    //cout<<"We have finished reading in all of the mesh connectivity elements!"<<endl;

    fileIN3.close();




    //lets calculate the max radius value first since we need it to calculate the minimum radius.
    double max_rad;
    max_rad = max_val_vec(rad);
    //Now we can get the minimum radius
    double min_rad;
    min_rad = min_val_vec(rad);
    //and the medium now!
    double med_rad;
    med_rad = (max_rad+min_rad)/2.0;
    //end reading in data from particles files

    //calculate max x-val to pass into nearest neighborbor search if not dealing with circular geometry
    double max_x_val;
    max_x_val = max_val_vec(x_pos);

    //list of nearest neighbors for the particles
    //NN_particles = Nearest_neightbors(pnparticles, x_pos, y_pos, 10)
    //list of nearest neighbors for the mesh points
    //cout<<"We are starting the Nearest Neighbor Algorithm!"<<endl;
    tuple<map<int,vector<int>>,map<int,vector<int>>,map<int,int>,map<int,int>> NNs = Nearest_neightbors_both(pnparticles, pnnodes, x_pos, y_pos, x_grid, y_grid,max_x_val,num_of_NN);
    //cout<<"We just finished the Nearest Neighbor Algorithm!"<<endl;
    map<int,vector<int>> NN_parts = get<0>(NNs);
    map<int,vector<int>> NN_meshes = get<1>(NNs);
    map<int,int> Cell_parts = get<2>(NNs);
    map<int,int> Cell_meshes = get<3>(NNs);
    string ann_rad = to_string(annulus_radius);
    // Create array of x,y,and corrresponding z values
    ofstream out;
    out.open("/Users/crhea/Desktop/total.txt");

    //vector<vector<double>> PF(*pnnodes,vector<double>(3));
    //node nodes[*pnnodes];
    node* nodes;
    nodes = new node[*pnnodes]; //create array of class of nodes
    //cout<<"We are beginning to calculate the packing fractions!"<<endl;
    for(int count=0;count<*pnnodes;count++){
        //PF[count][0] = x_grid[count]/100.;
        //PF[count][1] = y_grid[count]/100.;
        //PF[count][2] = 0.0;
        nodes[count].x = x_grid[count];
        nodes[count].y = y_grid[count];

        //cout<<nodes[count].x<<endl;

        //check if annulus is in domain (though it should be for this!)
        double dist_ann_dom = distances(x_grid[count],y_grid[count],0.0,0.0);
        if (dist_ann_dom <= domain_radius+max_rad){//only bother running through calculations if annulus is in the domain!
            //now lets figure out which particles to pass into PF based on NN...
            vector<int> particles_in_annulus; //index of particle near mesh point
            vector<double> x_in_annulus;
            vector<double> y_in_annulus;
            vector<double> dist_in_annulus; //distances of node to coordinates of particles near mesh point
            vector<double> rad_in_annulus;
            particles_in_annulus = NN_meshes[count];
            int in =0;
            for (int part=0;part<particles_in_annulus.size();part++){
                x_in_annulus.push_back(x_pos[particles_in_annulus[part]]); //x-coordinate of particle in annulus
                y_in_annulus.push_back(y_pos[particles_in_annulus[part]]); //y-coordinate of particle in annulus
                dist_in_annulus.push_back(distances(x_in_annulus[part],y_in_annulus[part],x_grid[count],y_grid[count]));
                rad_in_annulus.push_back(rad[particles_in_annulus[part]]);
                in++;
            } // get info for each particle
            //if (in==0){

            //}
            nodes[count].Packing_Fraction_Calculation(domain_radius, annulus_radius, x_grid[count], y_grid[count], max_rad, x_in_annulus, y_in_annulus, rad_in_annulus, dist_in_annulus);
        }//end if annulus in domain
//string file_name = "lammps_pos_out_simple";
      //      cout<<"outside"<<endl;
        }
    //}//end count
    //out.close();
    /*ofstream outputfile;
    outputfile.open(output_path+outputname+".vtk");


    outputfile<< "# vtk DataFile Version 2.0" <<'\n';
    outputfile<<"Packing Fraction Fields"<<'\n';
    outputfile<< "ASCII"<<'\n';
    outputfile<<"DATASET UNSTRUCTURED_GRID"<<'\n';
    outputfile<<"POINT_DATA "<< *pnnodes<<'\n';
    outputfile<<"SCALARS PackingFraction double"<<'\n';
    outputfile<<"LOOKUP_TABLE default"<<'\n';
    for (int count=0;count<*pnnodes;count++) {
        outputfile << nodes[count].packing_fraction << '\n';
    }
    outputfile.close();
    */

    ofstream outputfile2;
    outputfile2.open(output_path+outputname+".txt");

    for(int i=0;i<*pnnodes;i++){
        outputfile2<<double(nodes[i].x)<<" "<<double(nodes[i].y)<<" "<<double(nodes[i].packing_fraction)<<" "<<endl;
    }
    outputfile2.close();
    delete [] nodes;//be good!
    return 0;
}







int main(){
string input_path = "/home/crhea/Documents/DukeThesis/Mesh/";
string input_path_lammps_Data = "/home/crhea/Dropbox/Thesis/PrimaryFiles/SweepSimulations/Test/LAMMPSFILES/";
string output_path = "/home/crhea/Documents/DukeThesis/";
string mesh_to_read = "/home/crhea/Documents/DukeThesis/Mesh/Central_Square_nodes";
string mesh_connectivity = "/home/crhea/Documents/DukeThesis/Mesh/Central_Square_connectivity";
string file_name = "lammps_pos_out_simple";
string outputname = "porosity_openmp";
double domain_radius = 1.8;
double annulus_radius = 0.02;
int nparticles = 9960;
      const  int* pnparticles = &nparticles;
int nnodes =5123;
      int* pnnodes =&nnodes;
int number_cell_elements = 9944;
      int* pnumber_cell_elements = &number_cell_elements;
int num_of_NN = 100;
double particle_rad = 0.005;
    //create(input_path, input_path_lammps_Data,output_path,mesh_to_read,mesh_connectivity, file_name,outputname, domain_radius, annulus_radius, pnparticles, pnnodes,pnumber_cell_elements,num_of_NN,particle_rad);
    create(input_path_lammps_Data,output_path,mesh_to_read,mesh_connectivity, file_name,outputname, domain_radius, annulus_radius, pnparticles, pnnodes,pnumber_cell_elements,num_of_NN,particle_rad);

    return 0;
}
