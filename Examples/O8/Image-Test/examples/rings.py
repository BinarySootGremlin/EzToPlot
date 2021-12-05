import diffractsim
diffractsim.set_backend("CPU") #Change the string to "CUDA" to use GPU acceleration

from diffractsim import PolychromaticField, cf, mm, cm

F = PolychromaticField(
    spectrum=1.5 * cf.illuminant_d65,
    extent_x=12.0 * mm,
    extent_y=12.0 * mm,
    Nx=1200,
    Ny=1200,
    spectrum_size = 200, spectrum_divisions = 40  # increase these values to improve color resolution
)

F.add_aperture_from_image(
    "./apertures/rings.jpg", pad=(9 * mm, 9 * mm), Nx=1500, Ny=1500
)
rgb = F.compute_colors_at(150*cm)
F.plot(rgb, xlim=[-8, 8], ylim=[-8, 8])
