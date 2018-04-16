[Mesh]
  type = FileMesh
file = /home/clr56/Documents/DukeThesis/Mesh/Disk.e
[]


[UserObjects]
  [./DensityWater]
    type = RichardsDensityConstBulk
    dens0 = 1
    bulk_mod = 0.5 # notice small quantity, so the PETSc constant state works
  [../]
  [./DensityGas]
    type = RichardsDensityConstBulk
    dens0 = 0.5
    bulk_mod = 0.3 # notice small quantity, so the PETSc constant state works
  [../]
  [./RelPermWater]
    type = RichardsRelPermPower
    simm = 0.2
    n = 2
  [../]
  [./RelPermGas]
    type = Q2PRelPermPowerGas
    simm = 0.1
    n = 3
  [../]
  [./borehole_total_outflow_mass]
    type = RichardsSumQuantity
  [../]
[]

[Variables]
  [./pp]
     #scaling = 1e-8
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


[Q2P]
  porepressure = pp
  saturation = sat
  water_density = DensityWater
  water_relperm = RelPermWater
water_viscosity = 100.0
  gas_density = DensityGas
  gas_relperm = RelPermGas
  gas_viscosity = 0.5
  diffusivity = 0.0
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
[Kernels]
#[./central_drop]
#  type = ConstantCoupled
#  variable = pp
#  epsilon = 0.01
#  shapes = 'circle'
#  centers_tips = '0.0 0.0 0.01'
#  press_init_val = -0.7994
#[../]
[./central_drop_sat]
  type = ConstantCoupled
  variable = sat
  epsilon = 0.01
  shapes = 'circle'
  centers_tips = '0.0 0.0 0.05'
  press_init_val = 0.99
[../]
[]
[DiracKernels]
  [./bh_water]
    type = Q2PBorehole
    bottom_pressure = -0.7994
    point_file = jn30.bh
    SumQuantityUO = borehole_total_outflow_mass
    variable = sat
    unit_weight = '0 0 0'
    character = -1
    fluid_density = DensityWater
    fluid_relperm = RelPermWater
    other_var = pp
    var_is_porepressure = false
    fluid_viscosity = 100.0
  [../]
 
[]


[ICs]
[./porosity_init]
  type = readinic
  variable = porosity
dataFile = /home/clr56/Desktop/Results/Thesis/SweepSimulations/Viscosity_100.0/Porosity.txt
[../]
[./porosity_init_old]
  type = readinic
  variable = porosity_old
dataFile = /home/clr56/Desktop/Results/Thesis/SweepSimulations/Viscosity_100.0/Porosity_old.txt
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
  dt = 0.001
  end_time = 0.01
[]

[Outputs]
file_base = MOOSEFILES/MOOSEOutput
exodus = true
  [./CSV]
    type = CSV
  [../]
[]
