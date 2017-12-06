
/* -*- c++ -*- ----------------------------------------------------------
   LAMMPS - Large-scale Atomic/Molecular Massively Parallel Simulator
   http://lammps.sandia.gov, Sandia National Laboratories
   Steve Plimpton, sjplimp@sandia.gov

   Copyright (2003) Sandia Corporation.  Under the terms of Contract
   DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government retains
   certain rights in this software.  This software is distributed under
   the GNU General Public License.

   See the README file in the top-level LAMMPS directory.
------------------------------------------------------------------------- */

#ifdef FIX_CLASS
FixStyle(viscous/field,FixViscousField)
#else

#ifndef LMP_FIX_VISCOUS_Field_H
#define LMP_FIX_VISCOUS_Field_H

#include "fix.h"
#include <vector>
#include <string>
namespace LAMMPS_NS {

class FixViscousField : public Fix {
 public:
  FixViscousField(class LAMMPS *, int, char **);
  virtual ~FixViscousField();
  int setmask();
  void init();
  void setup(int);
  void min_setup(int);
  void post_force(int);
  void post_force_respa(int, int, int);
  void min_post_force(int);

 protected:
  double *gamma;
  int ilevel_respa;
 //------Viscosity Forces--------//
    std::string fluidViscosityFile; //file to be read in for viscosity information
    std::vector<double> fluidViscosity;//n x 1 vector
    std::string VelFieldFileX;
    std::string VelFieldFileY;
    std::vector<double> VelFieldX;
    std::vector<double> VelFieldY;
};

}

#endif
#endif

/* ERROR/WARNING messages:

E: Illegal ... command

Self-explanatory.  Check the input script syntax and compare to the
documentation for the command.  You can use -echo screen as a
command-line option when running LAMMPS to see the offending line.

*/
