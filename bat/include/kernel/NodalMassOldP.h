/****************************************************************/
/* MOOSE - Multiphysics Object Oriented Simulation Environment  */
/*                                                              */
/*          All contents are licensed under LGPL V2.1           */
/*             See LICENSE for full restrictions                */
/****************************************************************/

#ifndef NODALMASSOLDP
#define NODALMASSOLDP

#include "TimeKernel.h"
#include "Material.h"
#include "RichardsDensity.h"



// Forward Declarations
class NodalMassOldP;

template <>
InputParameters validParams<NodalMassOldP>();

/**
 * -fluid_mass_old/dt with the fluid mass
 * being lumped to the nodes.
 */
class NodalMassOldP : public TimeKernel
{
public:
  NodalMassOldP(const InputParameters & parameters);

protected:
  virtual Real computeQpResidual();

  const RichardsDensity & _density;


  /// value of the porosity at the start of the timestep
  const MaterialProperty<Real> & _porosity_old;

  const VariableValue & _u_old;
  const VariableValue & _saturation_variable_old;
};

#endif // Q2PNEGATIVENODALMASSOLD
