#!/usr/bin/env python3
"""
Script d'automatisation d'ajout de blogpost avec intelligence Gemini pour TheSunStandard.
Déplace les fichiers source de la racine vers leurs sous-dossiers respectifs (blog/ et blog/img/).
Usage : python add_blog.py <fichier_html> <chemin_image>
Exemple : python add_blog.py weboflife.html weboflife.jpg
"""

import os
import sys

# =============================================================================
# BUGFIX: Windows SSL [ASN1: NOT_ENOUGH_DATA] Bypass
# Doit être exécuté AVANT d'importer google.genai ou aiohttp
# =============================================================================
import ssl
import certifi

_orig_create_default_context = ssl.create_default_context

def _custom_create_default_context(purpose=ssl.Purpose.SERVER_AUTH, *, cafile=None, capath=None, cadata=None):
    if cafile is None:
        cafile = certifi.where()
    return _orig_create_default_context(purpose=purpose, cafile=cafile, capath=capath, cadata=cadata)

ssl.create_default_context = _custom_create_default_context
# =============================================================================

import shutil
import re
from pathlib import Path
from datetime import datetime
from google import genai

def generate_metadata_with_gemini(html_content: str) -> dict:
    """
    Fait appel à Gemini pour analyser le contenu brut du blogpost et générer 
    les métadonnées bilingues (titres, résumés, tags) de manière intelligente.
    """
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("⚠️ Erreur : Clé GEMINI_API_KEY manquante. Utilisation des métadonnées par défaut.")
        return {
            "title_en": "New Architecture Essay",
            "title_fr": "Nouvel Essai d'Architecture",
            "desc_fr": "Un article explorant l'ingénierie systémique et la thermodynamique.",
            "desc_en": "An article exploring systemic engineering and thermodynamics.",
            "tags_fr": "Thermodynamique & Architecture",
            "tags_en": "Thermodynamics & Architecture"
        }

    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    Analyse ce contenu de blog HTML et génère un objet JSON strict (sans markdown autour, juste le JSON brut) contenant les clés suivantes :
    - "title_en": Titre accrocheur en anglais (max 10 mots)
    - "title_fr": Titre accrocheur en français (max 10 mots)
    - "desc_fr": Un résumé percutant en français pour la carte du blog (1-2 phrases)
    - "desc_en": Un résumé percutant en anglais pour la carte du blog (1-2 phrases)
    - "tags_fr": Tags de catégorie en français (ex: "Thermodynamique, Biosphère & Bitcoin")
    - "tags_en": Tags de catégorie en anglais (ex: "Thermodynamics, Biosphere & Bitcoin")

    Contenu HTML brut :
    {html_content[:4000]}
    """

    print("🧠 Analyse du blogpost par Gemini pour extraction des métadonnées...")
    try:
        response = client.models.generate_content(
            model='gemini-flash-lite-latest',
            contents=prompt,
        )
        text_response = response.text.strip()
        text_response = re.sub(r"^```json\s*", "", text_response)
        text_response = re.sub(r"^```\s*", "", text_response)
        text_response = re.sub(r"\s*```$", "", text_response)
        
        import json
        return json.loads(text_response)
    except Exception as e:
        print(f"⚠️ Échec de l'appel Gemini ({e}), utilisation de valeurs de repli.")
        return {
            "title_en": "The Web of Life: Open Source Reality",
            "title_fr": "La Toile de la Vie : La Réalité Open Source",
            "desc_fr": "Où la thermodynamique rencontre la conscience planétaire et les blockchains fractales.",
            "desc_en": "Where thermodynamics meets planetary consciousness and fractal blockchains.",
            "tags_fr": "Thermodynamique & Systèmes",
            "tags_en": "Thermodynamics & Systems"
        }

def main():
    if len(sys.argv) < 3:
        print("❌ Utilisation incorrecte.")
        print("Exemple : python add_blog.py weboflife.html weboflife.jpg")
        sys.exit(1)

    html_arg = sys.argv[1]
    img_arg = sys.argv[2]

    repo_root = Path(__file__).parent.resolve()
    blog_dir = repo_root / "blog"
    img_dir = blog_dir / "img"
    img_dir.mkdir(parents=True, exist_ok=True)

    src_html = repo_root / html_arg
    if not src_html.exists():
        src_html = Path(html_arg)
    
    if not src_html.exists():
        print(f"❌ Erreur : Fichier HTML source introuvable ({html_arg}).")
        sys.exit(1)

    src_img = repo_root / img_arg
    if not src_img.exists():
        src_img = Path(img_arg)

    if not src_img.exists():
        print(f"❌ Erreur : Fichier image source introuvable ({img_arg}).")
        sys.exit(1)

    # Lecture du HTML pour analyse IA avant déplacement
    raw_html_content = src_html.read_text(encoding="utf-8")
    meta = generate_metadata_with_gemini(raw_html_content)

    # 1. Déplacement du fichier HTML vers blog/
    target_html_name = src_html.name
    target_html_path = blog_dir / target_html_name
    shutil.move(src_html, target_html_path)
    print(f"📄 Déplacé : {src_html.name} -> blog/{target_html_name}")

    # 2. Déplacement de l'image vers blog/img/
    target_img_name = src_img.name
    target_img_path = img_dir / target_img_name
    shutil.move(src_img, target_img_path)
    print(f"🖼️ Déplacé : {src_img.name} -> blog/img/{target_img_name}")

    # Dates et formats
    now = datetime.now()
    date_en = now.strftime("%B %d, %Y") + f" · {meta['tags_en']}"
    date_fr = now.strftime("%d %B %Y") + f" · {meta['tags_fr']}"
    timeline_date = now.strftime("Blog Post - %B %dth, %Y — ") + meta['tags_en']

    # 3. Mise à jour de blog/index.html
    blog_index_path = blog_dir / "index.html"
    if not blog_index_path.exists():
        print("❌ Erreur : blog/index.html est introuvable.")
        sys.exit(1)

    blog_index_content = blog_index_path.read_text(encoding="utf-8")

    match_first_href = re.search(r'<main class="blog-grid">\s*<a href="([^"]+\.html)"', blog_index_content)
    old_top_blog = match_first_href.group(1) if match_first_href else None
    print(f"🔍 Ancien article de tête identifié : {old_top_blog}")

    new_article_card = f"""    <!-- NOUVEAU POST : AUTOMATISÉ VIA GEMINI -->
    <a href="{target_html_name}" class="article-card" style="border-color: rgba(0, 225, 255, 0.35); box-shadow: 0 0 25px rgba(0, 225, 255, 0.08);">
        <span class="article-date" style="color: var(--human-cyan);">
            <span lang="en">{date_en}</span>
            <span lang="fr">{date_fr}</span>
        </span>
        
        <img src="img/{target_img_name}" alt="{meta['title_en']}" style="width: 50%; max-width: 900px; height: auto; border-radius: 8px; border: 1px solid rgba(0, 225, 255, 0.3); margin-bottom: 1.5rem;">
        
        <h2 lang="en">{meta['title_en']}</h2>
        <h2 lang="fr">{meta['title_fr']}</h2>
        
        <p lang="fr">{meta['desc_fr']}</p>
        <p lang="en">{meta['desc_en']}</p>

        <span class="read-more" style="color: var(--human-cyan);">
            <span lang="en">Read architecture essay →</span>
            <span lang="fr">Lire l'essai architectural →</span>
        </span>
    </a>
"""

    grid_marker = '<main class="blog-grid">'
    if grid_marker in blog_index_content:
        blog_index_content = blog_index_content.replace(grid_marker, f"{grid_marker}\n{new_article_card}")
        blog_index_path.write_text(blog_index_content, encoding="utf-8")
        print("✅ blog/index.html mis à jour avec le nouveau post généré par l'IA.")
    else:
        print("⚠️ Avertissement : Marqueur <main class='blog-grid'> introuvable dans blog/index.html.")

    # 4. Mise à jour du lien "Article Suivant" dans l'ancien dernier article
    if old_top_blog:
        old_blog_path = blog_dir / old_top_blog
        if old_blog_path.exists():
            old_blog_content = old_blog_path.read_text(encoding="utf-8")
            nav_marker = '<div class="article-navigation">'
            
            nav_card_injection = f"""    <div class="article-navigation">
        <a href="{target_html_name}" class="nav-card">
            <div class="nav-direction"><span lang="fr">Article Suivant →</span><span lang="en">Next Article →</span></div>
            <div class="nav-title"><span lang="fr">{meta['title_fr']}</span><span lang="en">{meta['title_en']}</span></div>
            <img src="img/{target_img_name}" alt="Article Image" style="width:100%; max-width:280px; border-radius:6px;">
        </a>
"""
            if nav_marker in old_blog_content:
                old_blog_content = old_blog_content.replace(nav_marker, nav_card_injection)
                old_blog_path.write_text(old_blog_content, encoding="utf-8")
                print(f"✅ Lien 'Article Suivant' ajouté dynamiquement dans l'ancien article ({old_top_blog}).")

    # 5. Mise à jour de la timeline dans index.html à la racine (ajout à la FIN du bloc timeline)
    root_index_path = repo_root / "index.html"
    if root_index_path.exists():
        root_index_content = root_index_path.read_text(encoding="utf-8")
        
        timeline_item = f"""        <div class="timeline-item">
            <p class="timeline-date">{timeline_date}</p>
            <h4 class="timeline-title">
                <a href="blog/{target_html_name}" target="_blank">
                    <span lang="en">{meta['title_en']}</span>
                    <span lang="fr">{meta['title_fr']}</span>
                </a>
            </h4>
            <div>
                <img src="blog/img/{target_img_name}" alt="{meta['title_en']}" style="width: 50%; max-width: 900px; height: auto; border-radius: 8px; border: 1px solid rgba(0, 225, 255, 0.2);">
            </div>
            <p class="timeline-text">
                <span lang="fr">{meta['desc_fr']}</span>
                <span lang="en">{meta['desc_en']}</span>
            </p>
        </div>"""

        # On cherche la balise <div class="timeline"> et on insère l'élément juste avant la fermeture du conteneur div de la timeline
        # Hypothèse structurelle classique : la timeline se ferme par un </div> correspondant. 
        # Pour être robuste, on peut localiser la balise de fin de la timeline ou insérer juste avant le dernier </div> de la section timeline.
        if '<div class="timeline">' in root_index_content:
            # On découpe à partir de <div class="timeline">
            parts = root_index_content.split('<div class="timeline">')
            timeline_inner = parts[1]
            
            # On cherche où se ferme la timeline (le prochain gros conteneur ou la fin des timeline-items)
            # En général, les items sont imbriqués. On peut insérer le nouvel item tout à la fin juste avant la fermeture du bloc timeline.
            # Cherchons le premier "</div>\s*</section>" ou une structure similaire après les items, ou remplaçons simplement la balise fermante de fin de timeline.
            # Approche sécurisée : trouver la fin du bloc timeline. Si la structure utilise un </div> fermant la div timeline, on peut insérer l'item juste avant.
            
            # Recherchons l'index du dernier "</div>" du bloc timeline ou insérons avant le premier tag suivant de niveau supérieur (ex: </section> ou <footer)
            end_markers = ['</section>', '<footer>', '<div class="footer">', '<div class="container">']
            inserted = False
            for marker in end_markers:
                if marker in timeline_inner:
                    # On insère juste avant ce marqueur dans la partie 1
                    sub_parts = timeline_inner.split(marker)
                    sub_parts[0] = sub_parts[0] + "\n" + timeline_item + "\n"
                    parts[1] = marker.join(sub_parts)
                    inserted = True
                    break
            
            if not inserted:
                # Fallback : remplacement simple de la balise de fin de timeline si elle est identifiable, 
                # ou ajout avant la fin du fichier si non trouvé.
                parts[1] = timeline_inner + "\n" + timeline_item + "\n"

            root_index_content = '<div class="timeline">'.join(parts)
            root_index_path.write_text(root_index_content, encoding="utf-8")
            print("✅ index.html (racine) mis à jour avec le nouvel élément à la FIN de la timeline.")
        else:
            print("⚠️ Avertissement : Conteneur <div class=\"timeline\"> introuvable dans index.html (racine).")
    else:
        print("⚠️ Avertissement : index.html à la racine introuvable.")

    print("\n🎉 Processus de déplacement et d'automatisation par Gemini terminé avec succès !")

if __name__ == "__main__":
    main()