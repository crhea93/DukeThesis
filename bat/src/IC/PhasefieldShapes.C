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

//--------------------------------------------------------------//
// This IC Module is meant to initiate the saturation of water
// even though we are solving for the saturation of gas
// Thus we must invert the values
//--------------------------------------------------------------//
#include "PhasefieldShapes.h"

template<>
InputParameters validParams<PhasefieldShapes>()
{
  InputParameters params = validParams<InitialCondition>();
  params.addRequiredParam<Real>("epsilon", "Phasefield transition parameter");
  params.addParam<std::vector<std::string> >("shapes", "array of shape types: crack, circle");
  params.addParam<std::vector<Real> >("centers_tips", "coordinates");
  //for gradients  (gradient_values = bottom_left_values br_vals top_left_values tr_vals)




  return params;
}

PhasefieldShapes::PhasefieldShapes(const InputParameters & parameters) :
    InitialCondition(parameters),
    _epsilon(getParam<Real>("epsilon")),
    _centers_tips(getParam<std::vector<Real> >("centers_tips")),
    _shapes(getParam<std::vector<std::string> >("shapes"))
{
}

Real
PhasefieldShapes::value(const Point & p)
{

//for shapes
double max_sat = 1.0-1e-5;
double aux_distance = 0.0;
double current_value = 0.0;
double _center_x, _center_y, _radius_a;
    _center_x = _centers_tips[0];
    _center_y = _centers_tips[1];
    _radius_a = _centers_tips[2];


    aux_distance=sqrt((p(0)-(_center_x))*(p(0)-(_center_x))+(p(1)-(_center_y))*(p(1)-(_center_y)));//distance to center
    if (aux_distance<_radius_a){
      current_value = max_sat*(aux_distance/_radius_a);
    }
    else{
      current_value = max_sat;
    }

  return current_value;
}
