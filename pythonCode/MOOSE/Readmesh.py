'''
Simply read the finite element mesh and return the number of nodes and elements
'''
import netCDF4
def count_FEMesh(Mesh):
    nc = netCDF4.Dataset(Mesh+".e")
    x = nc.variables['coord'][0]
    connect = nc.variables['connect1']
    num_nodes = len(x)
    conn_num = len(connect)
    return num_nodes,conn_num
