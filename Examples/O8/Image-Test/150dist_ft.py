import diffractsim

diffractsim.set_backend("CPU") #Change the string to "CUDA" to use GPU acceleration

from diffractsim import MonochromaticField, mm, nm, cm

F = MonochromaticField(
    wavelength=632.8 * nm, extent_x=10 * mm, extent_y=10 * mm, Nx=500, Ny=500
)

import sys
droppedFile = sys.argv[1]

F.add_aperture_from_image(
    droppedFile
)

rgb = F.compute_colors_at(150*cm)
F.plot(rgb, xlim=[-7, 7], ylim=[-7, 7])