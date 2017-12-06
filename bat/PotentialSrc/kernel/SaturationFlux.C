/****************************************************************/
/* MOOSE - Multiphysics Object Oriented Simulation Environment  */
/*                                                              */
/*          All contents are licensed under LGPL V2.1           */
/*             See LICENSE for full restrictions                */
/****************************************************************/

#include "SaturationFlux.h"

// MOOSE includes
#include "Assembly.h"
#include "MooseVariable.h"
#include "SystemBase.h"

// libMesh includes
#include "libmesh/quadrature.h"

// C++ includes
#include <iostream>

template <>
InputParameters
validParams<SaturationFlux>()
{
  InputParameters params = validParams<Kernel>();
  params.addRequiredParam<UserObjectName>(
      "fluid_density",
      "A RichardsDensity UserObject that defines the fluid density as a function of pressure.");
  params.addRequiredCoupledVar("porepressure_variable",
                               "The variable representing the porepressure");
  params.addRequiredParam<UserObjectName>(
      "fluid_relperm",
      "A RichardsRelPerm UserObject (eg RichardsRelPermPowerGas) that defines the "
      "fluid relative permeability as a function of the saturation Variable.");
  params.addRequiredParam<Real>("fluid_viscosity", "The fluid dynamic viscosity");
  params.addClassDescription(
      "Flux according to Darcy-Richards flow.  The Variable of this Kernel must be the saturation");
  return params;
}

SaturationFlux::SaturationFlux(const InputParameters & parameters)
  : Kernel(parameters),
    _density(getUserObject<RichardsDensity>("fluid_density")),
    _pp(coupledValue("porepressure_variable")),
    _grad_pp(coupledGradient("porepressure_variable")),
    _relperm(getUserObject<RichardsRelPerm>("fluid_relperm")),
    _viscosity(getParam<Real>("fluid_viscosity")),
    _gravity(getMaterialProperty<RealVectorValue>("gravity")),
    _permeability(getMaterialProperty<RealTensorValue>("permeability"))
{
}



Real
SaturationFlux::computeQpResidual()
{
    Real coeff = _relperm.relperm(_u[_qp]) * _density.density(_u[_qp]) / _viscosity;
  return -_grad_test[_i][_qp] *
         (coeff * _permeability[_qp] * (_grad_pp[_qp] - _density.density(_u[_qp]) * _gravity[_qp]));
}

Real
SaturationFlux::computeQpJacobian()
{
    return 0;
}

Real
SaturationFlux::computeQpOffDiagJacobian()
{
  return 0.0;

}
