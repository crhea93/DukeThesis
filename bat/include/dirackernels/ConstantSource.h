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

#ifndef CONSTANTSOURCE_H
#define CONSTANTSOURCE_H

// Moose Includes
#include "DiracKernel.h"

// Forward Declarations
class ConstantSource;

template <>
InputParameters validParams<ConstantSource>();

/**
 * TOOD
 */
class ConstantSource : public DiracKernel
{
public:
  ConstantSource(const InputParameters & parameters);

  virtual void addPoints() override;

protected:
  virtual Real computeQpResidual() override;

  const Real & _value;
  std::vector<Real> _centers_tips;
  std::vector<std::string> _shapes;
  Point _p;
};

#endif // CONSTANTSOURCE_H
