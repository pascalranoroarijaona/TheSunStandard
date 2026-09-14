#!/usr/bin/env python3
"""
Script d'automatisation de suppression de blogpost robuste pour TheSunStandard.
Utilise un découpage par blocs pour éviter les erreurs de regex sur les balises imbriquées.
Usage : python remove_blog.py <fichier_html> <chemin_image>
Exemple : python remove_blog.py weboflife.html weboflife.jpg
"""

import os
import sys
from pathlib import Path

def main():
    if len(sys.argv) < 3:
        print("❌ Utilisation incorrecte.")
        print("Exemple : python remove_blog.py weboflife.html weboflife.jpg")
        sys.exit(1)

    html_name = sys.argv[1]
    img_name = sys.argv[2]

    repo_root = Path(__file__).parent.resolve()
    blog_dir = repo_root / "blog"
    img_dir = blog_dir / "img"

    target_html_path = blog_dir / html_name
    target_img_path = img_dir / img_name

    # 1. Suppression physique des fichiers dans les sous-dossiers
    if target_html_path.exists():
        target_html_path.unlink()
        print(f"🗑️ Supprimé : blog/{html_name}")
    else:
        print(f"⚠️ Avertissement : Le fichier blog/{html_name} n'existe pas.")

    if target_img_path.exists():
        target_img_path.unlink()
        print(f"🗑️ Supprimé : blog/img/{img_name}")
    else:
        print(f"⚠️ Avertissement : Le fichier blog/img/{img_name} n'existe pas.")

    # 2. Nettoyage sécurisé dans blog/index.html (Découpage par blocs d'articles)
    blog_index_path = blog_dir / "index.html"
    if blog_index_path.exists():
        blog_index_content = blog_index_path.read_text(encoding="utf-8")
        
        if '<a href="' in blog_index_content:
            parts = blog_index_content.split('<a href="')
            header = parts[0]
            cards = parts[1:]
            
            new_cards = []
            removed_card = False
            for card in cards:
                if card.startswith(f'{html_name}"'):
                    removed_card = True
                    print(f"✅ Carte article pour {html_name} retirée de blog/index.html.")
                else:
                    new_cards.append(card)
            
            if removed_card:
                blog_index_content = header + '<a href="'.join([''] + new_cards)
                blog_index_path.write_text(blog_index_content, encoding="utf-8")
            else:
                print("⚠️ Avertissement : Aucune carte correspondante trouvée dans blog/index.html.")

    # 3. Nettoyage des liens "Article Suivant" dans les autres fichiers du blog
    for f in blog_dir.glob("*.html"):
        if f.name == "index.html":
            continue
        content = f.read_text(encoding="utf-8")
        if html_name in content:
            if '<a href="' in content:
                parts = content.split('<a href="')
                header = parts[0]
                links = parts[1:]
                new_links = []
                cleaned = False
                for link in links:
                    if link.startswith(f'{html_name}"'):
                        cleaned = True
                    else:
                        new_links.append(link)
                if cleaned:
                    content = header + '<a href="'.join([''] + new_links)
                    f.write_text(content, encoding="utf-8")
                    print(f"✅ Lien de navigation vers {html_name} retiré de {f.name}.")

    # 4. Nettoyage sécurisé dans index.html à la racine (Découpage par timeline-item)
    root_index_path = repo_root / "index.html"
    if root_index_path.exists():
        root_index_content = root_index_path.read_text(encoding="utf-8")
        
        if '<div class="timeline">' in root_index_content:
            parts = root_index_content.split('<div class="timeline-item">')
            header = parts[0]
            items = parts[1:]
            
            new_items = []
            removed_timeline = False
            for item in items:
                # On cible uniquement l'élément qui contient le lien vers ce blog spécifique
                if f"blog/{html_name}" in item:
                    removed_timeline = True
                    print(f"✅ Élément de timeline correspondant à blog/{html_name} retiré.")
                else:
                    new_items.append(item)
            
            if removed_timeline:
                root_index_content = header + '<div class="timeline-item">'.join([''] + new_items)
                root_index_path.write_text(root_index_content, encoding="utf-8")
                print("✅ index.html (racine) nettoyé : l'élément de la timeline a été retiré avec succès.")
            else:
                print("⚠️ Avertissement : Aucun élément de timeline ne correspond à ce blog dans index.html.")

    print("\n🎉 Processus de suppression et de nettoyage ciblé terminé avec succès !")

if __name__ == "__main__":
    main()