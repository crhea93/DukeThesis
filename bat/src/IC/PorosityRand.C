#include "PorosityRand.h"

#include <algorithm>
template<>
InputParameters validParams<PorosityRand>()
{
    InputParameters params = validParams<InitialCondition>();
    params.addRequiredParam<Real>("PorosityVal", "Average youngs modulus to be used");
    params.addParam<Real>("val","Values of Youngs Modulus");
    return params;
}

PorosityRand::PorosityRand(const InputParameters & parameters) :
InitialCondition(parameters),
_porosity_val(getParam<Real>("PorosityVal"))
{}


Real
PorosityRand::value(const Point & p)
{

  // Apply random value to youngs modulus in inner ring
  double M = _porosity_val-.4;
  double N = _porosity_val+.4;
  double _val;
  _val = M + rand() / (RAND_MAX / (N - M ));
  std::cout<<_val<<std::endl;
  return  _val;


}
