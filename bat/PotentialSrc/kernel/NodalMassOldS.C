/****************************************************************/
/* MOOSE - Multiphysics Object Oriented Simulation Environment  */
/*                                                              */
/*          All contents are licensed under LGPL V2.1           */
/*             See LICENSE for full restrictions                */
/****************************************************************/

#include "NodalMassOldS.h"

// MOOSE includes
#include "MooseVariable.h"
#include "Kernel.h"
// C++ includes
#include <iostream>

template <>
InputParameters
validParams<NodalMassOldS>()
{
  InputParameters params = validParams<TimeKernel>();
  params.addRequiredParam<UserObjectName>(
      "fluid_density",
      "A RichardsDensity UserObject that defines the fluid density as a function of pressure.");

  params.addClassDescription("fluid_mass");
  return params;
}

NodalMassOldS::NodalMassOldS(const InputParameters & parameters)
  : TimeKernel(parameters),
    _density(getUserObject<RichardsDensity>("fluid_density")),
    _porosity_old(getMaterialProperty<Real>("porosity_old")),
    _u_old(valueOld())
{
}

Real
NodalMassOldS::computeQpResidual()
{
  Real density_old;
  Real mass_old;
  density_old = _density.density(_u_old[_qp]);
  mass_old = _porosity_old[_qp] * density_old *(_u_old[_qp]);

  return -_test[_i][_qp] * (mass_old) / _dt;
}
