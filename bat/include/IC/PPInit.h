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

#ifndef PPINIT_H
#define PPINIT_H

// MOOSE Includes
#include "InitialCondition.h"

// Forward Declarations
class PPInit;

template<>
InputParameters validParams<PPInit>();

/**
 * PhasefieldShapes just returns a constant value.
 */
class PPInit : public InitialCondition
{
public:

  /**
   * Constructor: Same as the rest of the MOOSE Objects
   */
  PPInit(const InputParameters & parameters);

  /**
   * The value of the variable at a point.
   *
   * This must be overriden by derived classes.
   */
  virtual Real value(const Point & p);

private:


  Real _epsilon;
  std::vector<Real> _centers_tips;
  std::vector<std::string> _shapes;
  Real _press_val;


};

#endif //PPINIT_H
