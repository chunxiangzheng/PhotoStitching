import AminoAcidMass

N_term = 16.01
WATER = 18.01056
CHO = 29.00274
C_term = 17.00274
H = 1.0078
NH2 = 16.01
CO = 27.99491
# The mass of the photostitching modification
# TODO (chunxiangzheng): this should be an input variable
# when we move this to command line tools
MOD = 68.06260

# Capitalized M indicates the modified peptide
# Star indicates the position of the mod
# TODO (chunxiangzheng): move this to input variable
seq_M = "CAQK*"

# Small m indicates the unmodified peptide
# TODO (chunxiangzheng): move this to input variable
seq_m = "LLSPGH"

def findModPosition(seq):
	# Assuming there's only one mod
	for i in range(0, len(seq) - 1):
		if (seq[i + 1] == "*"):
			return i
		i = i + 1
	return len(seq)

mod_pos = findModPosition(seq_M)
seq_M_clean = seq_M.replace("*", "")

def pepMassNeutral(seq, x_mass):
	mass = 0
	for i in range(0, len(seq)):
		if (seq[i] != "X"):
			mass = mass + AminoAcidMass.MASS[seq[i]]
		else:
			mass = mass + x_mass
	return mass

# When calculate fragment, one peptide is treated as static mod
# The other is normal peptide
# when stitching sequence is static mod, appendix is M
# otherwise, appendix is m

# TODO (chunxiangzheng): change the design to using decorators

def calc_a_ion(seq, x_mass):
	return N_term + pepMassNeutral(seq, x_mass) - CHO

def calc_b_ion(seq, x_mass):
	return N_term + pepMassNeutral(seq, x_mass) - H

def calc_c_ion(seq, x_mass):
	return N_term + pepMassNeutral(seq, x_mass) + NH2

def calc_x_ion(seq, x_mass):
	return C_term + pepMassNeutral(seq, x_mass) + CO - H

def calc_y_ion(seq, x_mass):
	return C_term + pepMassNeutral(seq, x_mass) + H

def calc_z_ion(seq, x_mass):
	return C_term + pepMassNeutral(seq, x_mass) - NH2



def fragment(seq, x_mass, appendix):
	fragments = {}
    for i in range(1, len(seq)):
    	left_seq = seq[0 : i]
    	right_seq = seq[i : ]
    	fragments["a" + str(i)] = calc_a_ion(seq, x_mass)
    	fragments["b" + str(i)] = calc_b_ion(seq, x_mass)
    	fragments["c" + str(i)] = calc_c_ion(seq, x_mass)
    	fragments["x" + str(i)] = calc_x_ion(seq, x_mass)
    	fragments["y" + str(i)] = calc_y_ion(seq, x_mass)
    	fragments["z" + str(i)] = calc_z_ion(seq, x_mass)

	return fragments


    


