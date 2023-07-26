import numpy as np
import PyMoosh as pm
import matplotlib.pyplot as plt
from matplotlib import cbook
from matplotlib import cm
from matplotlib.colors import LightSource

# on veut tracer R = f(h) pour une structure à 6 couches (dont on ne connait pas les épaisseurs)

incidence = 0
wavelength = 600
mat_1 = 1.5
mat_2 = 2
th_1 = wavelength / (4 * mat_1)
th_2 = wavelength / (4 * mat_2)

materials = [1, mat_1**2, mat_2**2]

lay_pairs = 3 #7 couches 

stack = [0] + [1, 2] * lay_pairs + [1, 0]

reference_thicknesses = [0] + [th_1, th_2] * lay_pairs + [th_1, 0]
reference_structure = pm.Structure(materials, stack, reference_thicknesses)
rref, tref, Rref, Tref = pm.coefficient(reference_structure, wavelength, incidence, 0)


Rs = []
number_points = 100
ep_list = np.linspace(30, 200, number_points)


#i pour la liste des couches
#j pour la list des épaisseurs

# ep_ij = [epija epijb epijb epijd epije epijf epijk] avec i = 1 à 100 et j = 1 à 100
# epij1 = epij1a epij1b epij1c ... avec a = 1, b=2, c=3, etc


for epaisseur1 in ep_list:
    for epaisseur2 in ep_list:
        thicknesses = [0] + [epaisseur1, epaisseur2] * lay_pairs + [epaisseur1, 0]
        structure = pm.Structure(materials, stack, thicknesses)
        r, t, R, T = pm.coefficient(structure, wavelength, incidence, 0)
        Rs.append(R)
    

Rs = np.array(Rs)
maxRs = max(Rs)

Rs2 = Rs.reshape(number_points,number_points)
maxRs2 = np.max(Rs2)


z = Rs2
nrows , ncol = z.shape
x = ep_list
y = ep_list
x, y = np.meshgrid(x, y)

fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
ls = LightSource(270, 45)
rgb = ls.shade(z, cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')
surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=rgb, linewidth=0, antialiased=False, shade=False)
plt.show(block=False)

indices = np.where(Rs2 == Rs2.max())
val_max = Rs2[indices]
ep1_found = ep_list[indices[0]]
ep2_found = ep_list[indices[1]]

print("La réflectivité maximale vaut", val_max)
print("L'épaisseur du premier matériau est", ep1_found)
print("L'épaisseur du second matériau est", ep2_found)