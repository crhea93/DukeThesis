#ifndef READINICCOUPLED_H
#define READINICCOUPLED_H

// MOOSE Includes
#include "InitialCondition.h"
#include <vector>

// Forward Declarations
class readinicCoupled;
template<>
InputParameters validParams<readinicCoupled>();


class readinicCoupled : public InitialCondition
{
public:
    readinicCoupled(const InputParameters & parameters);
    
    virtual Real value(const Point & p) override;
    virtual void initialSetup() override;
private:

    std::vector<double> _init_val;
    const VariableValue & _sat_val;
    
};

#endif //READINICCOUPLED_H
