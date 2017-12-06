#ifndef PorosityRand_H
#define PorosityRand_H

// MOOSE Includes
#include "InitialCondition.h"
#include <vector>

// Forward Declarations
class PorosityRand;
template<>
InputParameters validParams<PorosityRand>();


class PorosityRand : public InitialCondition
{
public:
    PorosityRand(const InputParameters & parameters);

    virtual Real value(const Point & p);
private:
    Real _porosity_val;

};

#endif //PorosityRand_H
