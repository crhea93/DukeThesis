/* ----------------------------------------------------------------------
   LAMMPS - Large-scale Atomic/Molecular Massively Parallel Simulator
   http://lammps.sandia.gov, Sandia National Laboratories
   Steve Plimpton, sjplimp@sandia.gov

   Copyright (2003) Sandia Corporation.  Under the terms of Contract
   DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government retains
   certain rights in this software.  This software is distributed under
   the GNU General Public License.

   See the README file in the top-level LAMMPS directory.
------------------------------------------------------------------------- */

#include <math.h>
#include <stdlib.h>
#include <string.h>
#include "fix_viscous_field.h"
#include "atom.h"
#include "update.h"
#include "respa.h"
#include "error.h"
#include "force.h"
#include <iostream>
#include <fstream>
#include <sstream>

using namespace LAMMPS_NS;
using namespace FixConst;

/* ---------------------------------------------------------------------- */

FixViscousField::FixViscousField(LAMMPS *lmp, int narg, char **arg) :
  Fix(lmp, narg, arg),
  gamma(NULL)
{
  dynamic_group_allow = 1;

  if (narg < 4) error->all(FLERR,"Illegal fix viscous command");

  double gamma_one = force->numeric(FLERR,arg[3]);
  gamma = new double[atom->ntypes+1];
  for (int i = 1; i <= atom->ntypes; i++) gamma[i] = gamma_one;

  // optional args
  /*
  int iarg = 4;
  while (iarg < narg) {
    if (strcmp(arg[iarg],"scale") == 0) {
      if (iarg+3 > narg) error->all(FLERR,"Illegal fix viscous command");
      int itype = force->inumeric(FLERR,arg[iarg+1]);
      double scale = force->numeric(FLERR,arg[iarg+2]);
      if (itype <= 0 || itype > atom->ntypes)
        error->all(FLERR,"Illegal fix viscous command");
      gamma[itype] = gamma_one * scale;
      iarg += 3;
    } else error->all(FLERR,"Illegal fix viscous command");
  }*/

  //fluidViscosityFile = arg[3];
  //And the field of velocity

  VelFieldFileX = arg[4];

  VelFieldFileY = arg[5];

  fluidViscosityFile = arg[6];

  respa_level_support = 1;
  ilevel_respa = 0;




}

/* ---------------------------------------------------------------------- */

FixViscousField::~FixViscousField()
{
//  std::cout<<"Nothing Set"<<std::endl;

  delete [] gamma;
}

/* ---------------------------------------------------------------------- */

int FixViscousField::setmask()
{
  //std::cout<<"Mask Set"<<std::endl;
  int mask = 0;
  mask |= POST_FORCE;
  mask |= POST_FORCE_RESPA;
  mask |= MIN_POST_FORCE;
  return mask;
}

/* ---------------------------------------------------------------------- */

void FixViscousField::init()
{
  //std::cout<<"init Set"<<std::endl;
/*
  int max_respa = 0;
  //std::cout<<"Init done"<<std::endl;
  if (strstr(update->integrate_style,"respa")) {
    ilevel_respa = max_respa = ((Respa *) update->integrate)->nlevels-1;
    if (respa_level >= 0) ilevel_respa = MIN(respa_level,max_respa);
  }*/


  //Read in Velocity field X
  std::ifstream fileIN;
  fileIN.open(VelFieldFileX);
  std::string lineA;
  int lines=0;
  while(fileIN.good()){
      while(getline(fileIN,lineA)){
          std::istringstream streamA(lineA);
          lines++;
      }
  }
  fileIN.close();
  //string filename;
  std::ifstream fileIN1;
  fileIN1.open(VelFieldFileX);

  //
  //read data file
  std::vector<std::vector<double>> ValuesVel(lines,std::vector<double>(3));
  while(fileIN1.good()){

      for(int i=0;i<lines;i++){
          for (int j=0;j<3;j++){
              fileIN1 >> ValuesVel[i][j];
          }
      }

  }
  fileIN1.close();
  for(int i = 0; i < lines; i++){
      VelFieldX.push_back(ValuesVel[i][2]);
      //VelFieldY.push_back(ValuesVel[i][3]);
      //VelFieldZ.push_back(ValuesVel[i][4]);
      //std::cout<<VelFieldX[i]<<std::endl;
  }

  //Read in Velocity field Y
  std::ifstream fileINy1;
  fileINy1.open(VelFieldFileY);
  std::string lineAy;
  int linesy=0;
  while(fileINy1.good()){
      while(getline(fileINy1,lineAy)){
          std::istringstream streamAy(lineAy);
          linesy++;
      }
  }
  fileINy1.close();
  //string filename;
  std::ifstream fileIN1y;
  fileIN1y.open(VelFieldFileY);

  //
  //read data file
  std::vector<std::vector<double>> ValuesVely(linesy,std::vector<double>(3));
  while(fileIN1y.good()){

      for(int i=0;i<linesy;i++){
          for (int j=0;j<3;j++){
              fileIN1y >> ValuesVely[i][j];
          }
      }

  }
  fileIN1y.close();
  for(int i = 0; i < linesy; i++){
      //VelFieldX.push_back(ValuesVel[i][2]);
      VelFieldY.push_back(ValuesVely[i][2]);
      //VelFieldZ.push_back(ValuesVel[i][4]);
      //std::cout<<VelFieldY[i]<<std::endl;
  }
//std::cout<<"Done reading in"<<std::endl;

//Read in Viscosity File
std::ifstream fileINf;
fileINf.open(fluidViscosityFile);
std::string lineAf;
int linesf=0;
while(fileINf.good()){
    while(getline(fileINf,lineAf)){
        std::istringstream streamAf(lineAf);
        linesf++;
    }
}
fileINf.close();
//string filename;
std::ifstream fileIN1f;
fileIN1f.open(fluidViscosityFile);

//
//read data file
std::vector<std::vector<double>> ValuesVisc(lines,std::vector<double>(3));
while(fileIN1f.good()){

    for(int i=0;i<linesf;i++){
        for (int j=0;j<3;j++){
            fileIN1f >> ValuesVisc[i][j];
        }
    }

}
fileIN1f.close();
for(int i = 0; i < lines; i++){
    fluidViscosity.push_back(ValuesVisc[i][2]);
    //VelFieldY.push_back(ValuesVel[i][3]);
    //VelFieldZ.push_back(ValuesVel[i][4]);
    //std::cout<<VelFieldX[i]<<std::endl;
}


}

/* ---------------------------------------------------------------------- */

void FixViscousField::setup(int vflag)
{
  //std::cout<<"setup Set"<<std::endl;

/*  if (strstr(update->integrate_style,"verlet"))
    post_force(vflag);
  else {
    ((Respa *) update->integrate)->copy_flevel_f(ilevel_respa);
    post_force_respa(vflag,ilevel_respa,0);
    ((Respa *) update->integrate)->copy_f_flevel(ilevel_respa);
  }*/
}

/* ---------------------------------------------------------------------- */

void FixViscousField::min_setup(int vflag)
{
  //std::cout<<"min_setup Set"<<std::endl;

  post_force(vflag);
}

/* ---------------------------------------------------------------------- */

void FixViscousField::post_force(int vflag)
{
  // apply drag force to atoms in group
  // direction is opposed to velocity vector
  // magnitude depends on atom type
  //std::cout<<"Post Forces"<<std::endl;
  double **v = atom->v;
  double **f = atom->f;
  int *mask = atom->mask;
  int *type = atom->type;
  int nlocal = atom->nlocal;

  double drag;
  //std::cout<<"Calculating Forces"<<std::endl;
  for (int i = 0; i < nlocal; i++)
    if (mask[i] & groupbit) {
      drag = gamma[type[i]]*fluidViscosity[i];
      //drag = gamma;
      f[i][0] -= drag*(v[i][0]-VelFieldX[i]);
      f[i][1] -= drag*(v[i][1]-VelFieldY[i]);
      f[i][2] -= drag*v[i][2];
      //std::cout<<"Particle "<<i<<" with x-vel of "<<VelFieldX[i]<<std::endl;
    }
}

/* ---------------------------------------------------------------------- */

void FixViscousField::post_force_respa(int vflag, int ilevel, int iloop)
{
  //if (ilevel == ilevel_respa) post_force(vflag);
}

/* ---------------------------------------------------------------------- */

void FixViscousField::min_post_force(int vflag)
{
  post_force(vflag);
}
