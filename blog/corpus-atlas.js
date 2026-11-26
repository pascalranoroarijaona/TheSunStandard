/* /blog/corpus-atlas.js — Unified Navigation Atlas & Live Timechain Telemetry */
(function () {
    const CORPUS = [
        // Track 1: The Core Tetralogy
        { track: 'tetralogy', file: 'l-univers-participatif.html', badge: 'ACTE I', fr: "L'Éveil de l'Univers Participatif (It from Bit)", en: 'Awakening of the Participatory Universe (It from Bit)' },
        { track: 'tetralogy', file: 'le-monde-est-complexe.html', badge: 'ACTE II', fr: 'Le Monde est Complexe (z = a + ib)', en: 'The World is Complex (z = a + ib)' },
        { track: 'tetralogy', file: 'nautile-nakamoto.html', badge: 'ACTE III', fr: 'Le Nautile de Nakamoto (Hélice Bimétrique)', en: 'The Nakamoto Nautilus (Bimetric Helix)' },
        { track: 'tetralogy', file: 'matrice-inversee.html', badge: 'ACTE IV', fr: 'La Matrice Inversée (Calcul Régénératif)', en: 'The Inverted Matrix (Regenerative Compute)' },

        // Track 2: Spectral & Complex Time Bridges
        { track: 'math', file: 'nakamoto-riemann.html', badge: 'ZÊTA · 144', fr: "L'Invariant Critique : Riemann & Nakamoto", en: 'The Critical Invariant: Riemann & Nakamoto' },
        { track: 'math', file: 'horloge-cosmo-btc-cadran-mu.html', badge: 'KMS · MU', fr: 'Cadran Mu : Temps Thermique Complexe', en: 'Mu Dial: Complex Thermal Time' },

        // Track 3: Applied Energy & Living Ecology
        { track: 'ecology', file: 'ornoir_ornum.html', badge: 'L0–L5', fr: "De l'Or Noir à l'Or Numérique (2026–2044)", en: 'From Black Gold to Digital Gold (2026–2044)' },
        { track: 'ecology', file: 'wood-wide-web.html', badge: 'MYCÉLIUM', fr: 'The Wood Wide Web : La Blockchain & la Forêt', en: 'The Wood Wide Web: Blockchain & Forest' },
        { track: 'ecology', file: 'weboflife.html', badge: 'MEGA-POD', fr: 'La Toile de la Vie (Web of Life · H3)', en: 'Web of Life: Planetary Mega-POD (H3)' },
        { track: 'ecology', file: 'horizon-zero-2044.html', badge: 'HORIZON 0', fr: 'Horizon Zéro 2044 : Éveil de la Noosphère', en: 'Horizon Zero 2044: Noosphere Awakening' }
    ];

    function injectCorpusAtlas() {
        const article = document.querySelector('article');
        if (!article || document.getElementById('sun-corpus-atlas')) return;

        const currentFile = window.location.pathname.split('/').pop() || 'index.html';
        const style = document.createElement('style');
        style.textContent = `
            #sun-corpus-atlas {
                margin: 3.5rem auto 2.5rem;
                padding: 1.8rem;
                background: linear-gradient(145deg, rgba(8, 12, 20, 0.94), rgba(4, 6, 10, 0.98));
                border: 1px solid rgba(255, 204, 0, 0.28);
                border-top: 3px solid #ffcc00;
                border-radius: 14px;
                font-family: 'Inter', 'Helvetica Neue', sans-serif;
                box-shadow: 0 16px 45px rgba(0, 0, 0, 0.65);
            }
            .atlas-head {
                display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center;
                gap: 10px; margin-bottom: 1.2rem; padding-bottom: 0.8rem;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            }
            .atlas-title {
                color: #ffcc00; font-size: 1rem; font-weight: 800;
                text-transform: uppercase; letter-spacing: 1.5px; margin: 0;
            }
            .atlas-pulse-pill {
                font-family: 'Fira Code', monospace; font-size: 0.74rem;
                padding: 4px 11px; border-radius: 999px;
                background: rgba(0, 229, 255, 0.1); border: 1px solid rgba(0, 229, 255, 0.35);
                color: #00e5ff;
            }
            .atlas-tracks {
                display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem;
            }
            .atlas-col {
                background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.07);
                border-radius: 10px; padding: 1rem;
            }
            .atlas-col h4 {
                font-size: 0.78rem; text-transform: uppercase; letter-spacing: 1.2px;
                margin: 0 0 0.75rem; font-family: 'Fira Code', monospace;
            }
            .atlas-link {
                display: flex; align-items: center; gap: 8px;
                padding: 7px 9px; margin-bottom: 6px; border-radius: 7px;
                text-decoration: none; color: #cbd5e1; font-size: 0.84rem;
                background: rgba(0, 0, 0, 0.35); border: 1px solid transparent;
                transition: 0.2s;
            }
            .atlas-link:hover {
                border-color: rgba(255, 204, 0, 0.45); color: #fff; transform: translateX(3px);
            }
            .atlas-link.is-current {
                background: rgba(255, 204, 0, 0.14); border-color: #ffcc00;
                color: #fff; font-weight: 700;
            }
            .atlas-badge {
                font-family: 'Fira Code', monospace; font-size: 0.67rem; font-weight: 700;
                padding: 2px 6px; border-radius: 4px; background: rgba(255, 255, 255, 0.08);
                color: #ffcc00; white-space: nowrap;
            }
        `;
        document.head.appendChild(style);

        const renderCol = (trackKey, titleFr, titleEn, accentColor) => {
            const links = CORPUS.filter(item => item.track === trackKey).map(item => {
                const active = item.file === currentFile ? ' is-current' : '';
                return `<a href="${item.file}" class="atlas-link${active}">
                    <span class="atlas-badge" style="color:${accentColor}">${item.badge}</span>
                    <span lang="fr">${item.fr}</span>
                    <span lang="en">${item.en}</span>
                </a>`;
            }).join('');
            return `<div class="atlas-col">
                <h4 style="color:${accentColor};"><span lang="fr">${titleFr}</span><span lang="en">${titleEn}</span></h4>
                ${links}
            </div>`;
        };

        const wrapper = document.createElement('section');
        wrapper.id = 'sun-corpus-atlas';
        wrapper.innerHTML = `
            <div class="atlas-head">
                <h3 class="atlas-title">
                    <span lang="fr">🧭 Atlas de Recherche — L'Étalon Solaire & Lemuria Technologies</span>
                    <span lang="en">🧭 Research Atlas — The Sun Standard & Lemuria Technologies</span>
                </h3>
                <div class="atlas-pulse-pill" id="atlas-live-clock">
                    ⏱️ <span lang="fr">Méditation 144 blocs/j · Synchro...</span><span lang="en">144 blocks/day · Syncing...</span>
                </div>
            </div>
            <div class="atlas-tracks">
                ${renderCol('tetralogy', 'I. La Tétralogie Fondatrice', 'I. The Core Tetralogy', '#ffcc00')}
                ${renderCol('math', 'II. Temps Complexe & Spectre', 'II. Complex Time & Spectrum', '#00e5ff')}
                ${renderCol('ecology', 'III. Énergie, Forêt & Mega-POD', 'III. Energy, Forest & Mega-POD', '#44ee77')}
            </div>
        `;

        const navBlock = article.querySelector('.article-navigation');
        if (navBlock) {
            navBlock.parentNode.insertBefore(wrapper, navBlock);
        } else {
            article.appendChild(wrapper);
        }

        // Live Mempool Heartbeat sync
        fetch('https://mempool.space/api/v1/blocks')
            .then(r => r.ok ? r.json() : null)
            .then(blocks => {
                const pill = document.getElementById('atlas-live-clock');
                if (!pill || !Array.isArray(blocks) || blocks.length < 10) return;
                const h = blocks[0].height;
                const dt = (blocks[0].timestamp - blocks[blocks.length - 1].timestamp) / (blocks.length - 1);
                const pace = (86400 / Math.max(60, dt)).toFixed(1);
                pill.innerHTML = `⛓️ #${h.toLocaleString()} · <span lang="fr">${pace} blocs/j (Cible 144)</span><span lang="en">${pace} blocks/d (Target 144)</span>`;
            })
            .catch(() => {});
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectCorpusAtlas);
    } else {
        injectCorpusAtlas();
    }
})();