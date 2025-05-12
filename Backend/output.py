# MCMC simulation to generate samples
SAMPLES = MCMC(A, a, B, b, num_iter=int(1e6), thinning=int(1e4))


mean_sample = np.mean(SAMPLES, axis=0)
std_sample = np.std(SAMPLES, axis=0)

print(f"MCMC predictions from {SAMPLES.shape[0]:d} (thinned) samples:")
print("=" * 56)
for i, zutat in enumerate(Zutaten):
    print(
     "{:>38}".format(zutat)
     + f": {mean_sample[i] * 100:5.2g}% +/- {2*std_sample[i] * 100:4.2f}%"
    )
print("=" * 56)