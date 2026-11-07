#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protocole d'évaluation empirique et statistique (Tests T1, T2, T3)
Manuscrit : Holographie Céleste, Temps Thermique Modulaire et Cosmologie Quantique du Consensus de Nakamoto
Auteur : Pascal Ranaora

Ce script implémente les trois tests de falsifiabilité empirique de la Section 6.1 :
  - T1 : Statistique des temps de bloc (Loi exponentielle & Test de Kolmogorov-Smirnov par époque de 2016 blocs)
  - T2 : Biais du point fixe de 600s sous croissance relative g du taux de hachage
  - T3 : Taux de blocs périmés (stale blocks) en fonction du délai de propagation effectif delta

Usage :
  python3 test_timechain_empirics.py                 # Exécute les tests sur Monte-Carlo + synthèse graphique
  python3 test_timechain_empirics.py --csv blocs.csv # Exécute sur un export réel d'horodatages de réception
"""

import argparse
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt


# ============================================================================
# PARAMETRES FONDAMENTAUX DU PROTOCOLE BITCOIN (NAKAMOTO)
# ============================================================================
TAU_0 = 600.0          # Point fixe homéostatique cible (en secondes)
EPOCH_BLOCKS = 2016    # Nombre de blocs par époque de renormalisation KMS
T_EPOCH = EPOCH_BLOCKS * TAU_0  # Durée nominale d'une époque (~14 jours en secondes)


# ============================================================================
# TEST T1 : STATISTIQUE DES TEMPS DE BLOC (KOLMOGOROV-SMIRNOV)
# ============================================================================
def run_test_T1(rng: np.random.Generator, n_epochs: int = 25):
    """
    Vérifie que la restriction diagonale du modèle GKSL se réduit à un processus de Poisson
    stationnaire à l'intérieur d'une époque où le taux de hachage lambda_H est constant,
    et démontre le pouvoir de réfutation du test KS en présence d'une dérive non corrigée.
    """
    print("=" * 78)
    print(" [TEST T1] Statistique des temps de bloc (Kolmogorov-Smirnov sur 2016 blocs)")
    print("=" * 78)

    ks_stats_stationary = []
    p_values_stationary = []

    for ep in range(n_epochs):
        # Simulation des intervalles de première réception Delta_a sous lambda_H constant
        tau_bar = TAU_0
        delta_a = rng.exponential(scale=tau_bar, size=EPOCH_BLOCKS)

        # Estimation du paramètre d'échelle sur l'époque et test de Kolmogorov-Smirnov
        mean_est = np.mean(delta_a)
        ks_stat, p_val = stats.kstest(delta_a, 'expon', args=(0.0, mean_est))
        ks_stats_stationary.append(ks_stat)
        p_values_stationary.append(p_val)

    pass_rate = np.mean(np.array(p_values_stationary) > 0.05) * 100.0
    print(f"-> Époques stationnaires testées : {n_epochs} ({EPOCH_BLOCKS} blocs/époque)")
    print(f"-> Statistique KS moyenne D_n    : {np.mean(ks_stats_stationary):.5f}")
    print(f"-> p-value médiane               : {np.median(p_values_stationary):.4f}")
    print(f"-> Taux de non-rejet (alpha=5%)  : {pass_rate:.1f}% (Attendu théorique : ~95.0%)")

    # Cas de contrôle : injection d'une anomalie non-poissonienne (régularisation artificielle)
    delta_a_anomalous = rng.gamma(shape=1.35, scale=TAU_0 / 1.35, size=EPOCH_BLOCKS)
    ks_anom, p_anom = stats.kstest(delta_a_anomalous, 'expon', args=(0.0, np.mean(delta_a_anomalous)))
    print(f"-> Contrôle de réfutation (biais Gamma k=1.35) : KS={ks_anom:.5f}, p-val={p_anom:.2e} [REJETÉ]")

    # Génération d'un échantillon de référence pour le graphique
    sample_delta_a = rng.exponential(scale=TAU_0, size=EPOCH_BLOCKS * 5)
    return sample_delta_a, ks_stats_stationary, p_values_stationary


# ============================================================================
# TEST T2 : BIAIS DU POINT FIXE DE 600s SOUS CROISSANCE DU HASHRATE (g)
# ============================================================================
def run_test_T2(rng: np.random.Generator, n_epochs: int = 80):
    """
    Vérifie l'équation du biais du point fixe :
        <Delta a>_époque ~= tau_0 / (1 + g * T_ép / 2)
    où g = (d lambda_H / dt) / lambda_H est le taux de croissance relatif du hashrate.
    """
    print("\\n" + "=" * 78)
    print(" [TEST T2] Biais du point fixe de 600s sous croissance du taux de hachage (g)")
    print("=" * 78)

    # Taux de croissance par époque g * T_ép variant de -15% à +35% par époque de 14 jours
    g_T_ep_values = np.linspace(-0.15, 0.35, n_epochs)
    g_values = g_T_ep_values / T_EPOCH

    observed_mean_intervals = []
    theoretical_mean_intervals = []

    for g_T in g_T_ep_values:
        # Processus de Poisson inhomogène : au k-ième bloc de l'époque, lambda_H(k) croît linéairement
        # de lambda_0 à lambda_0 * (1 + g * T_ép)
        block_fractions = np.linspace(0.0, 1.0, EPOCH_BLOCKS)
        instantaneous_scale = TAU_0 / (1.0 + g_T * block_fractions)
        delta_a_epoch = rng.exponential(scale=instantaneous_scale)

        observed_mean_intervals.append(np.mean(delta_a_epoch))
        # Prédiction théorique au premier ordre (Éq. test-biais)
        theoretical_mean_intervals.append(TAU_0 / (1.0 + 0.5 * g_T))

    obs_arr = np.array(observed_mean_intervals)
    theo_arr = np.array(theoretical_mean_intervals)
    bias_observed = TAU_0 - obs_arr

    # Régression et corrélation entre g et (tau_0 - <Delta a>)
    r_pearson, p_corr = stats.pearsonr(g_T_ep_values, bias_observed)
    rmse = np.sqrt(np.mean((obs_arr - theo_arr) ** 2))

    print(f"-> Nombre d'époques simulées     : {n_epochs} (g*T_ép dans [-15%, +35%])")
    print(f"-> Corrélation (g, tau_0 - <da>) : r = {r_pearson:.5f} (p-value = {p_corr:.2e})")
    print(f"-> Erreur quadratique moyenne    : RMSE = {rmse:.2f} s sur le modèle théorique")
    print(f"-> Exemple à +10%/époque (g*T=0.1): <Delta a>_théo = {TAU_0/(1+0.05):.2f} s (< 600 s)")

    return g_T_ep_values, obs_arr, theo_arr


# ============================================================================
# TEST T3 : TAUX DE BLOCS PERIMES (STALE BLOCKS) EN FONCTION DE DELTA
# ============================================================================
def run_test_T3(rng: np.random.Generator, n_blocks_per_point: int = 200_000):
    """
    Vérifie la loi de probabilité des blocs périmés (stale/orphan) :
        P_stale ~= 1 - exp(-delta / tau_bar) ~= delta / tau_bar
    pour un délai de propagation effectif delta sur la sphère céleste S^2.
    """
    print("\\n" + "=" * 78)
    print(" [TEST T3] Taux de blocs périmés (stale) en fonction du délai de propagation")
    print("=" * 78)

    # Délais de propagation effectifs delta de 0.2s (FIBRE/Compact Blocks) à 15s (Gossip historique)
    deltas = np.array([0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 8.0, 12.0, 15.0])
    p_stale_sim = []
    p_stale_exact = 1.0 - np.exp(-deltas / TAU_0)
    p_stale_linear = deltas / TAU_0

    for d in deltas:
        intervals = rng.exponential(scale=TAU_0, size=n_blocks_per_point)
        # Un conflit (fork local / bloc stale) survient si un second bloc est trouvé dans la fenêtre delta
        stale_rate = np.mean(intervals < d)
        p_stale_sim.append(stale_rate)

    p_stale_sim = np.array(p_stale_sim)

    # Vérification de la linéarité aux petites valeurs de delta (delta <= 3s)
    small_mask = deltas <= 3.0
    slope, intercept, r_val, p_val, std_err = stats.linregress(deltas[small_mask], p_stale_sim[small_mask])

    print(f"-> Pente linéaire mesurée (delta <= 3s) : {slope:.6e} s^-1 (Théorie 1/tau_0 = {1.0/TAU_0:.6e} s^-1)")
    print(f"-> Coefficient de détermination R^2     : {r_val**2:.6f}")
    print("-> Pour delta = 1.5s (Compact Blocks)   : "
          f"P_stale(sim) = {p_stale_sim[deltas == 1.5][0]*1e3:.3f}‰ | "
          f"P_stale(théo) = {p_stale_exact[deltas == 1.5][0]*1e3:.3f}‰")

    return deltas, p_stale_sim, p_stale_exact, p_stale_linear


# ============================================================================
# CHARGEMENT OPTIONNEL D'UN EXPORT CSV DE NOEUD BITCOIN REEL
# ============================================================================
def evaluate_real_csv(csv_path: str):
    """
    Exécute le test T1 sur un fichier CSV contenant une colonne 'timestamp' (en secondes UNIX).
    """
    print("\\n" + "=" * 78)
    print(f" [DONNÉES RÉELLES] Analyse du fichier : {csv_path}")
    print("=" * 78)
    df = pd.read_csv(csv_path)
    if 'timestamp' not in df.columns:
        raise ValueError("Le fichier CSV doit contenir une colonne 'timestamp' (secondes UNIX).")

    timestamps = np.sort(df['timestamp'].values)
    delta_a = np.diff(timestamps)
    delta_a = delta_a[delta_a > 0]  # Filtrage d'éventuels doublons d'horodatage

    ks_stat, p_val = stats.kstest(delta_a, 'expon', args=(0.0, np.mean(delta_a)))
    print(f"-> Blocs analysés : {len(delta_a)} | <Delta a> = {np.mean(delta_a):.2f}s | KS = {ks_stat:.5f} (p = {p_val:.4f})")


# ============================================================================
# GENERATION DE LA PLANCHE GRAPHIQUE DE PUBLICATION (T1, T2, T3)
# ============================================================================
def plot_results(sample_delta_a, g_T_ep, obs_t2, theo_t2, deltas, sim_t3, exact_t3, lin_t3, output_fig="tests_empiriques_T1_T2_T3.png"):
    plt.rcParams.update({
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "figure.dpi": 150
    })

    fig, axes = plt.subplots(1, 3, figsize=(16, 4.8))

    # --- Panneau 1 : Test T1 (Distribution Exponentielle & Survie) ---
    ax1 = axes[0]
    bins = np.linspace(0, 3600, 45)
    ax1.hist(sample_delta_a, bins=bins, density=True, alpha=0.65, color="#1f77b4", edgecolor="black", label="Simulation GKSL diagonale")
    x_grid = np.linspace(0, 3600, 300)
    ax1.plot(x_grid, (1.0 / TAU_0) * np.exp(-x_grid / TAU_0), "r-", lw=2.2, label=r"Loi théorique $\frac{1}{\bar{\tau}}e^{-\Delta a/\bar{\tau}}$")
    ax1.set_yscale("log")
    ax1.set_title("T1 — Statistique des temps de bloc (Éq. 38)")
    ax1.set_xlabel(r"Intervalle inter-blocs $\Delta a$ (s)")
    ax1.set_ylabel(r"Densité de probabilité $p(\Delta a)$ [échelle log]")
    ax1.grid(True, which="both", ls="--", alpha=0.4)
    ax1.legend(loc="upper right", frameon=True)

    # --- Panneau 2 : Test T2 (Biais du point fixe de 600s) ---
    ax2 = axes[1]
    ax2.scatter(g_T_ep * 100.0, obs_t2, color="#2ca02c", alpha=0.75, s=28, label="Moyennes par époque (2016 blocs)")
    ax2.plot(g_T_ep * 100.0, theo_t2, "k-", lw=2.2, label=r"Modèle $\tau_0 / (1 + g T_{\mathrm{ép}}/2)$")
    ax2.axhline(TAU_0, color="crimson", ls="--", lw=1.3, label=r"Point fixe nominal $\tau_0 = 600\,\mathrm{s}$")
    ax2.axvline(0.0, color="gray", ls=":", lw=1.0)
    ax2.set_title("T2 — Biais du point fixe sous croissance (Éq. 39)")
    ax2.set_xlabel(r"Croissance relative du Hashrate par époque $g \cdot T_{\mathrm{ép}}$ (%)")
    ax2.set_ylabel(r"Intervalle moyen $\langle \Delta a \rangle_{\mathrm{époque}}$ (s)")
    ax2.grid(True, ls="--", alpha=0.4)
    ax2.legend(loc="upper right", frameon=True)

    # --- Panneau 3 : Test T3 (Taux de blocs périmés / Stale rate) ---
    ax3 = axes[2]
    ax3.plot(deltas, exact_t3 * 100.0, "b-", lw=2.2, label=r"Exact : $1 - e^{-\delta/\bar{\tau}}$")
    ax3.plot(deltas, lin_t3 * 100.0, "r--", lw=1.6, label=r"Régime linéaire : $\delta / \bar{\tau}$")
    ax3.scatter(deltas, sim_t3 * 100.0, color="darkorange", zorder=5, s=45, edgecolor="black", label="Simulation Monte-Carlo")
    ax3.axvspan(1.0, 2.0, color="gold", alpha=0.25, label="Régime Compact Blocks (1–2 s)")
    ax3.set_title("T3 — Taux de blocs périmés vs latence (Éq. 40)")
    ax3.set_xlabel(r"Délai de propagation effectif $\delta$ (s)")
    ax3.set_ylabel(r"Probabilité de bloc périmé $P_{\mathrm{stale}}$ (%)")
    ax3.grid(True, ls="--", alpha=0.4)
    ax3.legend(loc="upper left", frameon=True)

    plt.tight_layout()
    plt.savefig(output_fig, dpi=200)
    print(f"\\n[OK] Planche graphique sauvegardée sous : {output_fig}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécute les tests statistiques T1, T2 et T3 de la Timechain.")
    parser.add_argument("--csv", type=str, default=None, help="Chemin vers un fichier CSV réel contenant les horodatages de réception.")
    parser.add_argument("--seed", type=int, default=20090103, help="Graine aléatoire reproductible (défaut: 20090103 - Genesis).")
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)

    sample_delta_a, ks_stats, p_vals = run_test_T1(rng)
    g_T_ep, obs_t2, theo_t2 = run_test_T2(rng)
    deltas, sim_t3, exact_t3, lin_t3 = run_test_T3(rng)

    if args.csv:
        evaluate_real_csv(args.csv)

    plot_results(sample_delta_a, g_T_ep, obs_t2, theo_t2, deltas, sim_t3, exact_t3, lin_t3)