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

#include "ConstantCoupled.h"

/**
 * This function defines the valid parameters for
 * this Kernel and their default values
 */
template<>
InputParameters validParams<ConstantCoupled>()
{
  InputParameters params = validParams<Kernel>();
  params.addRequiredParam<Real>("epsilon", "Phasefield transition parameter");
  params.addParam<std::vector<std::string> >("shapes", "array of shape types: crack, circle");
  params.addParam<std::vector<Real> >("centers_tips", "coordinates");
  params.addParam<Real>("press_init_val","Initial Pressure Value");

  //coupled variables
  return params;
}

ConstantCoupled::ConstantCoupled(const InputParameters & parameters) :
  // You must call the constructor of the base class first
  Kernel(parameters),
  _epsilon(getParam<Real>("epsilon")),
  _centers_tips(getParam<std::vector<Real> >("centers_tips")),
  _shapes(getParam<std::vector<std::string> >("shapes")),
  _press_val(getParam<Real>("press_init_val"))

{}

Real ConstantCoupled::computeQpResidual()
{
  double p0,p1;
  double aux_distance = 0.0;
  double current_value = 0.0;
  double current_value_aux = 0.0;
  if (_shapes[0]=="circle"){
      double _center_x, _center_y, _radius_a;
          _center_x = _centers_tips[0];
          _center_y = _centers_tips[1];
          _radius_a = _centers_tips[2];

          p0 = _q_point[_qp](0);
          p1 = _q_point[_qp](1);

          aux_distance=sqrt((p0-(_center_x))*(p0-(_center_x))+(p1-(_center_y))*(p1-(_center_y)));//distance to center
          if (aux_distance<_radius_a){
            current_value_aux = _press_val;//-_press_val*(aux_distance/_radius_a);
            //std::cout<<current_value_aux<<std::endl;
            current_value = -_test[_i][_qp] * current_value_aux;
          }
          else{
            // if not in circle then simply set to zero!
            current_value = 0.0;
          }
    }

else{
    double x_min,x_max,y_min,y_max;
    x_min = _centers_tips[0];
    x_max = _centers_tips[1];
    y_min = _centers_tips[2];
    y_max = _centers_tips[3];
    p0 = _q_point[_qp](0);
    p1 = _q_point[_qp](1);

    if (((x_min<=p0)&&(p0<=x_max))&&((y_min<=p1)&&(p1<=y_max))){
        //aux_distance=sqrt((p0-(x_max))*(p0-(x_min))+(p1-(_y_min))*(p1-(y_max)))
        //current_value_aux = _press_val-_press_val*(aux_distance/_radius_a);
        //std::cout<<current_value_aux<<std::endl;
        current_value_aux = _press_val;
        current_value = -_test[_i][_qp] * current_value_aux;
    }
    else{
      current_value = 0.0;
    }

  }

  return current_value;
}
Real ConstantCoupled::computeQpJacobian()
{
  // the partial derivative of _grad_u is just _grad_phi[_j]
  return 0;
  //return _test[_i][_qp]*_phi[_j][_qp];
}
