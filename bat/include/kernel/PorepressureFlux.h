/****************************************************************/
/* MOOSE - Multiphysics Object Oriented Simulation Environment  */
/*                                                              */
/*          All contents are licensed under LGPL V2.1           */
/*             See LICENSE for full restrictions                */
/****************************************************************/

#ifndef POREPRESSUREFLUX
#define POREPRESSUREFLUX

#include "Kernel.h"
#include "RichardsDensity.h"
#include "RichardsRelPerm.h"
#include "Material.h"

// Forward Declarations
class PorepressureFlux;

template <>
InputParameters validParams<PorepressureFlux>();

/**
 * This is a fully upwinded flux Kernel
 * The Variable of this Kernel should be the porepressure
 *
 * The residual for the kernel is the darcy flux.
 * This is
 * R_i = int{mobility*flux_no_mob} = int{mobility*grad(pot)*permeability*grad(test_i)}
 * for node i.  where int is the integral over the element, and
 * pot = Porepressure - density*gravity.x
 *
 * However, in fully-upwind, the first step is to take the mobility outside the
 * integral.
 * R_i = mobility*int{flux_no_mob} = mobility*F_i
 * NOTE: R_i is exactly the mass flux flowing out of node i.
 * Similarly, F_i is a measure of fluid flowing out of node i.
 *
 * This leads to the definition of upwinding:
 *
 *   If F_i is positive then R_i = mobility_i * F_i
 *   That is, we use the upwind value of mobility.
 *
 * For the F_i<0 nodes we construct their R_i using mass conservation
 */
class PorepressureFlux : public Kernel
{
public:
  PorepressureFlux(const InputParameters & parameters);

protected:
  /**
   * Note that this is not the complete residual for the quadpoint
   * In computeResidual we sum over the quadpoints and then add
   * the upwind mobility parts
   */
  virtual Real computeQpResidual();

  virtual Real computeQpJacobian();
  virtual Real computeQpOffDiagJacobian();

  /// fluid density
  const RichardsDensity & _density;

  /// saturation at the nodes
  const VariableValue & _sat;

  /// variable number of the saturation variable
  unsigned int _sat_var;

  /// fluid relative permeability
  const RichardsRelPerm & _relperm;

  /// fluid viscosity
  Real _viscosity;

  /// gravity
  const MaterialProperty<RealVectorValue> & _gravity;

  /// permeability
  const MaterialProperty<RealTensorValue> & _permeability;

};

#endif // Q2PPOREPRESSUREFLUX
