/****************************************************************/
/* MOOSE - Multiphysics Object Oriented Simulation Environment  */
/*                                                              */
/*          All contents are licensed under LGPL V2.1           */
/*             See LICENSE for full restrictions                */
/****************************************************************/

#include "NodalMassOldP.h"

// MOOSE includes
#include "Kernel.h"
// C++ includes
#include <iostream>
// MOOSE includes
#include "Assembly.h"
#include "MooseVariable.h"
#include "MooseVariableScalar.h"
#include "Problem.h"
 #include "SubProblem.h"
 #include "SystemBase.h"
template <>
InputParameters
validParams<NodalMassOldP>()
{
  InputParameters params = validParams<TimeKernel>();
  params.addRequiredParam<UserObjectName>(
      "fluid_density",
      "A RichardsDensity UserObject that defines the fluid density as a function of pressure.");
      params.addCoupledVar("saturation_variable", "");

  params.addClassDescription(" fluid_mass");
  return params;
}

NodalMassOldP::NodalMassOldP(const InputParameters & parameters)
  : TimeKernel(parameters),
    _density(getUserObject<RichardsDensity>("fluid_density")),
    _porosity_old(getMaterialProperty<Real>("porosity_old")),

    _u_old(valueOld()),
    _saturation_variable_old(coupledValueOld("saturation_variable"))
{
}

Real
NodalMassOldP::computeQpResidual()
{
  Real density_old;
  Real mass_old;

  density_old = _density.density(_u_old[_qp]);
  mass_old = _porosity_old[_qp] * density_old *(1-(_saturation_variable_old[_qp]));


  return -_test[_i][_qp] * (mass_old) / _dt;
}
