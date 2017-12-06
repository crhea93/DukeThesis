/****************************************************************/
/*               DO NOT MODIFY THIS HEADER                      */
/* MOOSE - Multiphysics Object Oriented Simulation Environment  */
/*                                                              */
/*           (c) 2010 Battelle Energy Alliance, LLC             */
/*                   ALL RIGHTS RESERVED                        */
/*                                                              */
/*          Prepared by Battelle Energy Alliance, LLC           */
/*            Under Contract No. DE-AC07-05ID14517              */
/*            With the U. S. Department of Energy               */
/*                                                              */
/*            See COPYRIGHT for full restrictions               */
/****************************************************************/

#ifndef TIMEDERIVATIVEP_H
#define TIMEDERIVATIVEP_H

#include "TimeKernel.h"
#include "Material.h"
#include "RichardsDensity.h"

// Forward Declaration
class TimeDerivativeP;

template <>
InputParameters validParams<TimeDerivativeP>();

class TimeDerivativeP : public TimeKernel
{
public:
  TimeDerivativeP(const InputParameters & parameters);

  virtual void computeJacobian() override;

protected:
  virtual Real computeQpResidual() override;
  virtual Real computeQpJacobian() override;
  bool _lumping;

  const RichardsDensity & _density;
  /// current value of the porosity
  const MaterialProperty<Real> & _porosity;

};

#endif // TIMEDERIVATIVE_H
