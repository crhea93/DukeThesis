[Mesh]
  type = FileMesh
file = /home/clr56/Documents/DukeThesis/Mesh/square_Ref1_extended.e
[]



[UserObjects]
  [./DensityWater]
    type = RichardsDensityConstBulk
    dens0 = 1
    bulk_mod = 1
  [../]
  [./DensityGas]
    type = RichardsDensityConstBulk
    dens0 = 0.5
    bulk_mod = 0.5
  [../]
  [./RelPermWater]
    type = RichardsRelPermPower
    simm = 0.0
    n = 2
  [../]
  [./RelPermGas]
    type = Q2PRelPermPowerGas
    simm = 0.0
    n = 3
  [../]
[]

[Variables]
  [./pp]
  [../]
  [./sat]
  [../]
[]
[AuxVariables]
[./porosity]
[../]
[./porosity_old]
[../]
  [./velocity_x]
    order = CONSTANT
    family = MONOMIAL
  [../]
  [./velocity_y]
    order = CONSTANT
    family = MONOMIAL
  [../]

[]
[BCs]
[./press_right]
type = DirichletBC
boundary = 1
variable = pp
value = 1.0
[../]
[./sat_left]
type = DirichletBC
boundary = 1
variable = sat
value = 1.0
[../]
[]


[Q2P]
  porepressure = pp
  saturation = sat
  water_density = DensityWater
  water_relperm = RelPermWater
water_viscosity = 1.0
  gas_density = DensityGas
  gas_relperm = RelPermGas
  gas_viscosity = 0.5
  diffusivity = 0.01
 # output_total_masses_to = 'CSV'
 # save_gas_flux_in_Q2PGasFluxResidual = true
 # save_water_flux_in_Q2PWaterFluxResidual = true
 # save_gas_Jacobian_in_Q2PGasJacobian = true
 # save_water_Jacobian_in_Q2PWaterJacobian = true
[]


[AuxKernels]
  [./velocity_x]
    type = DarcyVelocity
    variable = velocity_x
    component = x
    execute_on = timestep_end
    darcy_pressure = pp
  [../]
  [./velocity_y]
    type = DarcyVelocity
    variable = velocity_y
    component = y
    execute_on = timestep_end
    darcy_pressure = pp
  [../]

[]



[ICs]
[./saT_init]
  type = readinic
  variable = sat
dataFile = /media/clr56/Data/Results/FrontCapPor/FrontCapPor_1.0/MOOSEValues_sat_updated.txt
[../]
[./press_init]
  type = readinic
  variable = pp
dataFile = /media/clr56/Data/Results/FrontCapPor/FrontCapPor_1.0/MOOSEValues_press_updated.txt
[../]
[./porosity_init]
  type = readinic
  variable = porosity
dataFile = /media/clr56/Data/Results/FrontCapPor/FrontCapPor_1.0/Porosity.txt
[../]
[./porosity_init_old]
  type = readinic
  variable = porosity_old
dataFile = /media/clr56/Data/Results/FrontCapPor/FrontCapPor_1.0/Porosity_old.txt
[../]
[]
[Materials]
  [./rock]
    type = Q2PMaterialC
    block = 1
    por_var = porosity
   por_var_old = porosity_old
  mat_permeability = '1E-2 0 0  0 1E-2 0  0 0 1E-2'
    gravity = '0 0 0'
  [../]
[]
  
[Postprocessors]
  [./dofs]
    type = NumDOFs
  [../]
  [./veltyx]
    type = ElementalVelocity
    variable = velocity_x
    output =/media/clr56/Data/Results/FrontCapPor/FrontCapPor_1.0/velocitiesX
  [../]
  [./veltyy]
    type = ElementalVelocity
    variable = velocity_y
    output = /media/clr56/Data/Results/FrontCapPor/FrontCapPor_1.0/velocitiesY
  [../]
  [./sat_updated_out]
    type = NodalPrintOut
    variable = sat
     output = /media/clr56/Data/Results/FrontCapPor/FrontCapPor_1.0/MOOSEValues_sat_updated
  [../]
  [./press_updated_out]
    type = NodalPrintOut
    variable = pp
     output = /media/clr56/Data/Results/FrontCapPor/FrontCapPor_1.0/MOOSEValues_press_updated
  [../]
[]


[Preconditioning]
  active = 'andy'
  [./andy]
    type = SMP
    full = true
    petsc_options_iname = '-ksp_type -pc_type -snes_atol -snes_rtol -snes_max_it'
    petsc_options_value = 'bcgs bjacobi 1E-12 1E-10 10000'
  [../]
[]

[Executioner]
  type = Transient
  solve_type = Newton
  dt = 0.01
  end_time = 0.01
  l_tol = 1e-8
  nl_rel_tol = 1e-8
  nl_abs_tol = 1e-8
[]

[Outputs]
file_base = ../../../../../../media/clr56/Data/Results/FrontCapPor/FrontCapPor_1.0/MOOSEFILES/MOOSEOutput
  exodus = true
  #[./CSV]
  #  type = CSV
  #[../]
[]
