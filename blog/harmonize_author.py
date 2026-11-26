import os
import re
import shutil

UNIFIED_AUTHOR_HTML = """<!-- SECTION AUTEUR & RESSOURCES OPEN-SOURCE UNIFIÉE (CORPUS L'ÉTALON SOLAIRE) -->
<section class="author-section unified-author-card" aria-label="À propos de l'auteur et ressources">
    <style>
        .unified-author-card {
            margin: 4rem auto 3rem;
            padding: 2.2rem;
            background: linear-gradient(145deg, rgba(12, 16, 26, 0.94), rgba(5, 7, 12, 0.98));
            border: 1px solid rgba(255, 204, 0, 0.28);
            border-top: 4px solid var(--sun-yellow, #ffcc00);
            border-radius: 14px;
            box-shadow: 0 18px 48px rgba(0, 0, 0, 0.65);
            font-family: var(--font-ui, 'Inter', 'Helvetica Neue', sans-serif);
            max-width: 1020px;
        }
        .unified-author-header {
            display: flex;
            align-items: center;
            gap: 1.4rem;
            padding-bottom: 1.5rem;
            margin-bottom: 1.6rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        .unified-author-emblem {
            font-size: 2.6rem;
            line-height: 1;
            padding: 0.85rem;
            border-radius: 14px;
            background: radial-gradient(circle, rgba(255, 204, 0, 0.14) 0%, rgba(0, 229, 255, 0.06) 100%);
            border: 1px solid rgba(255, 204, 0, 0.32);
            box-shadow: 0 0 24px rgba(255, 204, 0, 0.14);
            flex-shrink: 0;
        }
        .unified-author-info h3 {
            color: #ffffff;
            margin: 0 0 0.4rem 0;
            font-size: 1.28rem;
            font-weight: 800;
            letter-spacing: 0.6px;
            text-transform: uppercase;
        }
        .unified-author-role {
            color: var(--sun-yellow, #ffcc00);
            font-family: var(--font-mono, 'Fira Code', monospace);
            font-size: 0.78rem;
            font-weight: 600;
            margin-bottom: 0.55rem;
            display: block;
        }
        .unified-author-info p {
            color: #cbd5e1;
            font-size: 0.92rem;
            line-height: 1.62;
            margin: 0;
            text-align: left;
        }
        .unified-author-links {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin-top: 0.85rem;
        }
        .unified-social-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 11px;
            border-radius: 999px;
            font-family: var(--font-mono, 'Fira Code', monospace);
            font-size: 0.72rem;
            font-weight: 600;
            text-decoration: none;
            color: #e2e8f0;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.14);
            transition: all 0.22s ease;
        }
        .unified-social-pill:hover {
            border-color: var(--sun-yellow, #ffcc00);
            color: var(--sun-yellow, #ffcc00);
            transform: translateY(-1px);
        }
        .unified-author-video {
            margin: 1.5rem auto 1.8rem;
            max-width: 680px;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(255, 204, 0, 0.25);
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.6);
            aspect-ratio: 16 / 9;
            background: #000;
        }
        .unified-author-video iframe {
            width: 100%;
            height: 100%;
            border: 0;
            display: block;
        }
        .unified-resources-heading {
            color: var(--sun-yellow, #ffcc00);
            font-family: var(--font-mono, 'Fira Code', monospace);
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 1rem;
        }
        .unified-resources-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.1rem;
        }
        .unified-res-card {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 1.2rem;
            background: rgba(255, 255, 255, 0.025);
            border: 1px solid rgba(255, 255, 255, 0.09);
            border-top: 3px solid var(--card-accent, #ffcc00);
            border-radius: 12px;
            text-decoration: none;
            transition: transform 0.24s ease, border-color 0.24s ease, background 0.24s ease, box-shadow 0.24s ease;
        }
        .unified-res-card:hover {
            transform: translateY(-4px);
            background: rgba(255, 255, 255, 0.048);
            border-color: var(--card-accent, #ffcc00);
            box-shadow: 0 12px 28px rgba(0, 0, 0, 0.55);
        }
        .unified-card-head {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            gap: 0.75rem;
            margin-bottom: 0.75rem;
        }
        .unified-card-logo {
            width: 176px;
            height: 176px;
            border-radius: 14px;
            object-fit: cover;
            background: #060911;
            border: 1px solid rgba(255, 255, 255, 0.16);
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.55);
            transition: transform 0.28s ease, border-color 0.28s ease;
        }
        .unified-res-card:hover .unified-card-logo {
            transform: scale(1.06);
            border-color: var(--card-accent, #ffcc00);
        }
        .unified-card-logo-dual {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        .unified-card-logo-dual img {
            width: 76px;
            height: 76px;
            border-radius: 12px;
            object-fit: cover;
            background: #060911;
            border: 1px solid rgba(255, 255, 255, 0.16);
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.55);
            transition: transform 0.28s ease, border-color 0.28s ease;
        }
        .unified-res-card:hover .unified-card-logo-dual img {
            transform: scale(1.05);
            border-color: var(--card-accent, #ffcc00);
        }
        .unified-res-card h4 {
            color: var(--card-accent, #ffcc00);
            font-size: 0.98rem;
            font-weight: 700;
            margin: 0;
            line-height: 1.35;
            text-align: center;
        }
        .unified-res-card h4 a {
            color: inherit;
            text-decoration: none;
        }
        .unified-res-card h4 a:hover {
            text-decoration: underline;
        }
        .unified-res-card p {
            color: #94a3b8;
            font-size: 0.82rem;
            line-height: 1.52;
            margin: 0;
            text-align: left;
        }
        .unified-card-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
            margin-top: 0.85rem;
            padding-top: 0.6rem;
            border-top: 1px dashed rgba(255, 255, 255, 0.08);
        }
        .unified-repo-tag {
            display: inline-block;
            font-family: var(--font-mono, 'Fira Code', monospace);
            font-size: 0.71rem;
            font-weight: 600;
            color: var(--card-accent, #ffcc00);
            text-decoration: none;
            opacity: 0.92;
        }
        .unified-repo-tag:hover {
            opacity: 1;
            text-decoration: underline;
        }
        @media (max-width: 860px) {
            .unified-resources-grid { grid-template-columns: repeat(2, 1fr); }
        }
        @media (max-width: 580px) {
            .unified-author-header { flex-direction: column; text-align: center; }
            .unified-author-info p { text-align: center; }
            .unified-author-links { justify-content: center; }
            .unified-resources-grid { grid-template-columns: 1fr; }
        }
    </style>

    <div class="unified-author-header">
        <div class="unified-author-emblem" aria-hidden="true">☀️🌱🐚</div>
        <div class="unified-author-info">
            <h3>Pascal Ranoroarijaona (Ranaora)</h3>
            <span class="unified-author-role">
                <span lang="fr">Ingénieur en Informatique (HPC) &amp; Chercheur Indépendant · Information Physics Institute (Sydney)</span>
                <span lang="en">Computer Engineer (HPC) &amp; Independent Researcher · Information Physics Institute (Sydney)</span>
            </span>
            <p lang="fr">
                Fondateur de <strong>Lemuria Technologies</strong> et de l'ONG <strong>Angovo</strong> (Madagascar), auteur de <em>L'Étalon Solaire</em>, de <a href="https://www.livre-bitcoin.fr/" target="_blank" rel="noopener" style="color:var(--sun-yellow, #ffcc00);"><em>Le Livre Bitcoin</em></a> et des ouvrages libres <a href="https://www.thesunstandard.net/HomoBiodiversitas.pdf" target="_blank" rel="noopener" style="color:#44ee77;"><em>Homo Biodiversitas</em></a> &amp; <a href="https://www.sufficiencyprotocol.org/HorizonZero.pdf" target="_blank" rel="noopener" style="color:#00e5ff;"><em>Horizon Zéro</em></a>. Ses travaux unifient physique statistique hors d'équilibre, temps thermique modulaire, preuves formelles Lean 4 et calcul régénératif.
            </p>
            <p lang="en">
                Founder of <strong>Lemuria Technologies</strong> and the <strong>Angovo</strong> NGO (Madagascar), author of <em>The Sun Standard</em>, <a href="https://www.livre-bitcoin.fr/" target="_blank" rel="noopener" style="color:var(--sun-yellow, #ffcc00);"><em>The Bitcoin Book</em></a>, and free online books <a href="https://www.thesunstandard.net/HomoBiodiversitas.pdf" target="_blank" rel="noopener" style="color:#44ee77;"><em>Homo Biodiversitas</em></a> &amp; <a href="https://www.sufficiencyprotocol.org/HorizonZero.pdf" target="_blank" rel="noopener" style="color:#00e5ff;"><em>Horizon Zero</em></a>. His work unifies non-equilibrium statistical physics, modular thermal time, Lean 4 formal proofs, and regenerative compute.
            </p>
            <div class="unified-author-links">
                <a href="https://github.com/pascalranoroarijaona/" target="_blank" rel="noopener" class="unified-social-pill">🐙 GitHub</a>
                <a href="https://www.thesunstandard.net/" target="_blank" rel="noopener" class="unified-social-pill">☀️ TheSunStandard.net</a>
                <a href="https://www.regenerativecompute.io/" target="_blank" rel="noopener" class="unified-social-pill">🌱 RegenerativeCompute.io</a>
                <a href="https://www.livre-bitcoin.fr/" target="_blank" rel="noopener" class="unified-social-pill">📘 Livre-Bitcoin.fr</a>
                <a href="https://www.simulateur-bitcoin.fr/" target="_blank" rel="noopener" class="unified-social-pill">⛏️ Simulateur-Bitcoin.fr</a>
                <a href="https://www.compteur-bitcoin.fr/" target="_blank" rel="noopener" class="unified-social-pill">📈 Compteur-Bitcoin.fr</a>
                <span class="unified-social-pill" style="cursor:default; color:#44ee77; border-color:rgba(68,238,119,0.3);">📍 French/Australian/Madagascan located Sydney/Antsirabe, Lemuria - Born in Nairobi Kenya, Married to China/Indonesia/Malaysia, Middle-Earth Human · Fihavanana</span>
            </div>
        </div>
    </div>

    <div class="unified-author-video">
        <iframe width="560" height="315" src="https://www.youtube.com/embed/hpMTGpB0zM0?si=PRPLvFPxi1Krexno" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
    </div>

    <div class="unified-resources-heading">
        <span lang="fr">🧭 Explorez mon Univers : Écosystème de Recherche, Livres, ONG &amp; Dépôts Open-Source</span>
        <span lang="en">🧭 Explore my Universe: Research Ecosystem, Books, NGO &amp; Open-Source Repositories</span>
    </div>

    <div class="unified-resources-grid">
        <!-- 1 : The Sun Standard -->
        <a href="https://www.thesunstandard.net/" target="_blank" rel="noopener" class="unified-res-card" style="--card-accent: #ffcc00;">
            <div>
                <div class="unified-card-head">
                    <img src="img/logo-sunstandard.jpg" alt="The Sun Standard" class="unified-card-logo" onerror="this.style.display='none'">
                    <h4>☀️ The Sun Standard</h4>
                </div>
                <p>
                    <span lang="fr">Portail théorique bilingue : temps thermique KMS, preuves formelles Lean 4 et éconophysique solaire post-PIB.</span>
                    <span lang="en">Bilingual theoretical portal: KMS thermal time, Lean 4 formal proofs, and post-GDP solar econophysics.</span>
                </p>
            </div>
            <div class="unified-card-footer">
                <span class="unified-repo-tag">🌐 www.thesunstandard.net</span>
            </div>
        </a>

        <!-- 2 : Regenerative Compute -->
        <a href="https://www.regenerativecompute.io/" target="_blank" rel="noopener" class="unified-res-card" style="--card-accent: #44ee77;">
            <div>
                <div class="unified-card-head">
                    <img src="img/logo-lemuriatech.jpg" alt="Lemuria Technologies" class="unified-card-logo" onerror="if(!this.dataset.fb){this.dataset.fb='1';this.src='img/logo-lemuriatech.jpg';}else{this.style.display='none';}">
                    <h4>🌱 Regenerative Compute</h4>
                </div>
                <p>
                    <span lang="fr">Ingénierie matérielle (Lemuria Tech) : du BitTerrarium™ de bureau (17 W) aux mines Brownfield mégawatt &amp; MOF-303.</span>
                    <span lang="en">Hardware execution (Lemuria Tech): from 17 W desktop BitTerrarium™ units to megawatt Brownfield mines &amp; MOF-303.</span>
                </p>
            </div>
            <div class="unified-card-footer">
                <span class="unified-repo-tag">🌐 www.regenerativecompute.io</span>
            </div>
        </a>

        <!-- 3 : Protocole Trinité -->
        <a href="https://github.com/pascalranoroarijaona/Trinity" target="_blank" rel="noopener" class="unified-res-card" style="--card-accent: #00e5ff;">
            <div>
                <div class="unified-card-head">
                    <img src="img/logo-trinity.png" alt="Protocole Trinité" class="unified-card-logo" onerror="this.style.display='none'">
                    <h4>👁️ Protocole Trinité</h4>
                </div>
                <p>
                    <span lang="fr">Comme dans <em>Matrix</em>, il faut toujours <strong>Trinity</strong> pour nous sauver de la folie des hallucinations synthétiques et nous ouvrir l'accès direct à <strong>la Source</strong> : intégrité prouvée par le triplet <strong>Qui · Quoi · Quand</strong> (Nostr + SHA-256 + OpenTimestamps).</span>
                    <span lang="en">Just like in <em>The Matrix</em>, it takes <strong>Trinity</strong> to rescue us from the madness of synthetic hallucinations and guide us straight back to <strong>the Source</strong>: integrity anchored via the <strong>Who · What · When</strong> triplet (Nostr + SHA-256 + OpenTimestamps).</span>
                </p>
            </div>
            <div class="unified-card-footer">
                <span class="unified-repo-tag">🕶️ Qui · Quoi · Quand → La Source</span>
            </div>
        </a>

        <!-- 4 : Web of Life (Mega-POD) -->
        <a href="https://github.com/pascalranoroarijaona/WebOfLife" target="_blank" rel="noopener" class="unified-res-card" style="--card-accent: #34d399;">
            <div>
                <div class="unified-card-head">
                    <img src="img/weboflife.jpg" alt="Web of Life" class="unified-card-logo" onerror="this.style.display='none'">
                    <h4>🕸️ Web of Life (Mega-POD)</h4>
                </div>
                <p>
                    <span lang="fr">Jumeau numérique planétaire open-source en TypeScript sur grille hexagonale H3 couplant PoW, PoEW et cogénération MARL.</span>
                    <span lang="en">Open-source planetary TypeScript digital twin on Uber H3 hexagonal grid coupling PoW, PoEW, and MARL cogeneration.</span>
                </p>
            </div>
            <div class="unified-card-footer">
                <span class="unified-repo-tag">🐙 Open-Source Repo →</span>
            </div>
        </a>

        <!-- 5 : Wellbeing Framework (WU) -->
        <a href="https://github.com/pascalranoroarijaona/wellbeing-framework" target="_blank" rel="noopener" class="unified-res-card" style="--card-accent: #fb923c;">
            <div>
                <div class="unified-card-head">
                    <img src="img/logo-wellbeingframework.png" alt="Wellbeing Framework" class="unified-card-logo" onerror="this.style.display='none'">
                    <h4>🌿 Wellbeing Framework (WU)</h4>
                </div>
                <p>
                    <span lang="fr">Comptabilité biophysique open-source en Unités de Bien-Être (WU/kWh) pour transcender les limites destructrices du PIB.</span>
                    <span lang="en">Open-source biophysical accounting in Wellbeing Units (WU/kWh) designed to transcend destructive GDP metrics.</span>
                </p>
            </div>
            <div class="unified-card-footer">
                <span class="unified-repo-tag">🐙 Open-Source Repo →</span>
            </div>
        </a>

        <!-- 6 : Sufficiency Protocol -->
        <a href="https://github.com/pascalranoroarijaona/sufficiency-protocol" target="_blank" rel="noopener" class="unified-res-card" style="--card-accent: #c084fc;">
            <div>
                <div class="unified-card-head">
                    <img src="img/logo-sufficiencyprotocol.png" alt="Sufficiency Protocol" class="unified-card-logo" onerror="this.style.display='none'">
                    <h4>⚙️ Sufficiency Protocol</h4>
                </div>
                <p>
                    <span lang="fr">Limites planétaires, budgets exergétiques et gouvernance écologique open-source auditables par Preuve de Travail.</span>
                    <span lang="en">Open-source planetary boundaries, exergy budgets, and ecological governance auditable via Proof-of-Work.</span>
                </p>
            </div>
            <div class="unified-card-footer">
                <span class="unified-repo-tag">🐙 Open-Source Repo →</span>
            </div>
        </a>

        <!-- 7 : Kaya Wellbeing Identity -->
        <a href="https://github.com/pascalranoroarijaona/wellbeing-identity" target="_blank" rel="noopener" class="unified-res-card" style="--card-accent: #22d3ee;">
            <div>
                <div class="unified-card-head">
                    <img src="img/logo-kayawellbeing.png" alt="Kaya Wellbeing Identity" class="unified-card-logo" onerror="this.style.display='none'">
                    <h4>🪪 Kaya Wellbeing Identity</h4>
                </div>
                <p>
                    <span lang="fr">Identité souveraine open-source (Solid PODs &amp; Preuve d'Humanité) reliant la couverture de Markov de l'individu à son empreinte biophysique.</span>
                    <span lang="en">Open-source sovereign identity (Solid PODs &amp; Proof-of-Personhood) linking an individual's Markov blanket to their biophysical footprint.</span>
                </p>
            </div>
            <div class="unified-card-footer">
                <span class="unified-repo-tag">🐙 wellbeing-identity →</span>
            </div>
        </a>

        <!-- 8 : Homo Biodiversitas & Horizon Zéro (Livres Gratuits en Ligne) -->
        <div class="unified-res-card" style="--card-accent: #a3e635;">
            <div>
                <div class="unified-card-head">
                    <div class="unified-card-logo-dual">
                        <img src="img/logo-homobiodiversitas.png" alt="Homo Biodiversitas" onerror="this.style.display='none'">
                        <img src="img/HorizonZero.png" alt="Horizon Zéro" onerror="this.style.display='none'">
                    </div>
                    <h4>📚 Homo Biodiversitas &amp; Horizon Zéro</h4>
                </div>
                <p>
                    <span lang="fr">Mes deux livres gratuits en accès libre : la symbiose entre la Noosphère et le vivant (<em>Homo Biodiversitas</em>) et l'ingénierie régénérative (<em>Horizon Zéro</em>).</span>
                    <span lang="en">My two free open-access books: symbiosis between the Noosphere and living ecosystems (<em>Homo Biodiversitas</em>) and regenerative engineering (<em>Horizon Zero</em>).</span>
                </p>
            </div>
            <div class="unified-card-footer">
                <a href="https://www.thesunstandard.net/HomoBiodiversitas.pdf" target="_blank" rel="noopener" class="unified-repo-tag">📄 HomoBiodiversitas.pdf</a>
                <a href="https://www.sufficiencyprotocol.org/HorizonZero.pdf" target="_blank" rel="noopener" class="unified-repo-tag">📄 HorizonZero.pdf</a>
            </div>
        </div>

        <!-- 9 : Angovo (Projet ONG Madagascar — IA & Énergie) -->
        <div class="unified-res-card" style="--card-accent: #10b981;">
            <div>
                <div class="unified-card-head">
                    <img src="img/logo-angovo.png" alt="Projet ONG Angovo Madagascar" class="unified-card-logo" onerror="this.style.display='none'">
                    <h4>🇲🇬 Angovo · ONG Madagascar</h4>
                </div>
                <p>
                    <span lang="fr">Projet d'ONG dédié à Madagascar pour développer l'accès souverain à l'énergie décarbonée et l'éducation à l'Intelligence Artificielle au service des communautés locales.</span>
                    <span lang="en">NGO initiative dedicated to Madagascar to develop sovereign clean energy access and local Artificial Intelligence education empowering Malagasy communities.</span>
                </p>
            </div>
            <div class="unified-card-footer">
                <span class="unified-repo-tag">🌱 Énergie &amp; IA · Antsirabe / Madagascar</span>
            </div>
        </div>

        <!-- 10 : Le Livre Bitcoin (édition publiée / dépôt privé) -->
        <a href="https://www.livre-bitcoin.fr/" target="_blank" rel="noopener" class="unified-res-card" style="--card-accent: #f7931a;">
            <div>
                <div class="unified-card-head">
                    <img src="img/JohnNashPoW.png" alt="Le Livre Bitcoin" class="unified-card-logo" onerror="this.style.display='none'">
                    <h4>📘 Le Livre Bitcoin</h4>
                </div>
                <p>
                    <span lang="fr">Ouvrage de référence accessible sur la souveraineté monétaire, la thermodynamique de la rareté et l'histoire de Bitcoin (édition publiée, dépôt privé).</span>
                    <span lang="en">Comprehensive French reference book on monetary sovereignty, thermodynamics of scarcity, and Bitcoin's foundations (published edition, private repo).</span>
                </p>
            </div>
            <div class="unified-card-footer">
                <span class="unified-repo-tag">📖 www.livre-bitcoin.fr</span>
            </div>
        </a>

        <!-- 11 : Simulateur Bitcoin (simulateur de minage + code open-source) -->
        <div class="unified-res-card" style="--card-accent: #fbbf24;">
            <div>
                <div class="unified-card-head">
                    <img src="img/logo-simbtc.png" alt="Simulateur Bitcoin" class="unified-card-logo" onerror="this.style.display='none'">
                    <h4><a href="https://www.simulateur-bitcoin.fr/" target="_blank" rel="noopener">⛏️ Simulateur Bitcoin</a></h4>
                </div>
                <p>
                    <span lang="fr">Simulateur open-source de minage Bitcoin : modélisation du hashrate, de la consommation électrique, de la difficulté réseau et de la rentabilité des ASICs.</span>
                    <span lang="en">Open-source Bitcoin mining simulator: modeling hashrate, power consumption, network difficulty adjustments, and ASIC profitability.</span>
                </p>
            </div>
            <div class="unified-card-footer">
                <a href="https://www.simulateur-bitcoin.fr/" target="_blank" rel="noopener" class="unified-repo-tag">🌐 App</a>
                <a href="https://github.com/pascalranoroarijaona/simulateur-bitcoin" target="_blank" rel="noopener" class="unified-repo-tag">🐙 Inspecter le code →</a>
            </div>
        </div>

        <!-- 12 : Compteur Bitcoin (trajectoire & rendement possible + code open-source) -->
        <div class="unified-res-card" style="--card-accent: #38bdf8;">
            <div>
                <div class="unified-card-head">
                    <img src="img/logo-countbtc.png" alt="Compteur Bitcoin" class="unified-card-logo" onerror="this.style.display='none'">
                    <h4><a href="https://www.compteur-bitcoin.fr/" target="_blank" rel="noopener">📈 Compteur Bitcoin</a></h4>
                </div>
                <p>
                    <span lang="fr">Observatoire open-source en temps réel de la trajectoire du réseau Bitcoin, des cycles de Halving et des projections de rendement possible.</span>
                    <span lang="en">Open-source real-time observatory tracking Bitcoin's network trajectory, Halving cycles, and potential yield projections.</span>
                </p>
            </div>
            <div class="unified-card-footer">
                <a href="https://www.compteur-bitcoin.fr/" target="_blank" rel="noopener" class="unified-repo-tag">🌐 Live</a>
                <a href="https://github.com/pascalranoroarijaona/compteur-bitcoin" target="_blank" rel="noopener" class="unified-repo-tag">🐙 Inspecter le code →</a>
            </div>
        </div>
    </div>
</section>"""


def replace_author_block(html_text):
    """Trouve le bloc <section class="...unified-author-card"> ou <div class="...author-section"> et le remplace."""
    sec_pattern = re.compile(
        r'(?:<!--[^\n]*AUTEUR[^\n]*-->\s*)?<section\s+class=["\'][^"\']*\bunified-author-card\b[^"\']*["\'][^>]*>.*?</section>',
        re.IGNORECASE | re.DOTALL
    )
    if sec_pattern.search(html_text):
        return sec_pattern.sub(lambda _: UNIFIED_AUTHOR_HTML, html_text, count=1), True

    match = re.search(r'<div\s+class=["\'][^"\']*\bauthor-section\b[^"\']*["\'][^>]*>', html_text)
    if not match:
        return html_text, False

    start_idx = match.start()
    pos = match.end()
    depth = 1
    tag_pattern = re.compile(r'<(/?)div\b[^>]*>', re.IGNORECASE)

    while depth > 0:
        tag_match = tag_pattern.search(html_text, pos)
        if not tag_match:
            return html_text, False
        if tag_match.group(1) == '/':
            depth -= 1
        else:
            depth += 1
        pos = tag_match.end()

    prefix = html_text[:start_idx]
    prefix = re.sub(r'<!--[^\n]*AUTEUR[^\n]*-->\s*$', '', prefix, flags=re.IGNORECASE)

    new_html = prefix + UNIFIED_AUTHOR_HTML + html_text[pos:]
    return new_html, True


def insert_if_missing(html_text):
    """Insère la section auteur avant le formulaire de feedback ou avant le footer si absente."""
    for anchor in ['<div class="feedback-container">', '<div class="article-navigation">', '<footer>']:
        idx = html_text.find(anchor)
        if idx != -1:
            return html_text[:idx] + UNIFIED_AUTHOR_HTML + "\n\n    " + html_text[idx:], True
    return html_text, False


def main():
    articles = [
        "focker-planck.html",
        "HailMary.html",
        "horizon-zero-2044.html",
        "HorizonZeroArchitecture.html",
        "horloge-cosmo-btc-cadran-mu.html",
        "index.html",
        "l-univers-participatif.html",
        "le-monde-est-complexe.html",
        "matrice-inversee.html",
        "nakamoto-riemann.html",
        "nautile-nakamoto.html",
        "ornoir_ornum.html",
        "starship_arche_thermodynamique_c_ur_vibrant.html",
        "weboflife.html",
        "wood-wide-web.html"
    ]

    for fname in articles:
        if not os.path.exists(fname):
            print(f"[IGNORÉ] Fichier introuvable : {fname}")
            continue

        with open(fname, "r", encoding="utf-8") as f:
            content = f.read()

        updated_content, replaced = replace_author_block(content)
        action = "Mis à jour"

        if not replaced:
            updated_content, replaced = insert_if_missing(content)
            action = "Inséré (était absent)"

        if replaced:
            if not os.path.exists(fname + ".bak"):
                shutil.copyfile(fname, fname + ".bak")
            with open(fname, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print(f"[OK - {action}] {fname}")
        else:
            print(f"[ERREUR] Impossible de localiser l'emplacement dans {fname}")


if __name__ == "__main__":
    main()