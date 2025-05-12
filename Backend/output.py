import numpy as np

# MCMC simulation to generate samples
SAMPLES = MCMC(A, a, B, b, num_iter=int(1e6), thinning=int(1e4))

def summarize_samples(SAMPLES):
    """
    Computes summary statistics (mean and standard deviation) for sampled ingredients.

    Args:
        samples (np.ndarray): MCMC samples (thinned).
    """

mean_sample = np.mean(SAMPLES, axis=0)
std_sample = np.std(SAMPLES, axis=0)


def print_results(Zutaten, SAMPLES, mean_sample, std_sample):
   """
    Prints a summary of MCMC prediction results.

    Args:
        Zutaten (List[str]): List of ingredient names.
        SAMPLES (np.ndarray): Original MCMC samples for count display.
        mean_sample (np.ndarray): Mean values per ingredient.
        std_sample (np.ndarray): Standard deviations per ingredient.
    """
    print(f"MCMC predictions from {SAMPLES.shape[0]:d} (thinned) samples:")
    print("=" * 56)
    for i, zutat in enumerate(Zutaten):
      print(
         "{:>38}".format(zutat)
         + f": {mean_sample[i] * 100:5.2g}% +/- {2*std_sample[i] * 100:4.2f}%"
      )
    print("=" * 56)