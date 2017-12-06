/****************************************************************/
/* MOOSE - Multiphysics Object Oriented Simulation Environment  */
/*                                                              */
/*          All contents are licensed under LGPL V2.1           */
/*             See LICENSE for full restrictions                */
/****************************************************************/

#ifndef NODALMASSP
#define NODALMASSP

#include "TimeKernel.h"
#include "Material.h"
#include "RichardsDensity.h"

// Forward Declarations
class NodalMassP;

template <>
InputParameters validParams<NodalMassP>();

/**
 * fluid_mass/dt lumped to the nodes
 */
class NodalMassP : public TimeKernel
{
public:
  NodalMassP(const InputParameters & parameters);

protected:
  virtual Real computeQpResidual();

  virtual Real computeQpJacobian();

  virtual Real computeQpOffDiagJacobian(unsigned int jvar);

  const RichardsDensity & _density;
  /// current value of the porosity
  const MaterialProperty<Real> & _porosity;
  const VariableValue & _saturation_variable;
};

#endif // Q2PNODALMASS
