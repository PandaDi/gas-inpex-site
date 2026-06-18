#!/usr/bin/env python3
"""Extract content from HTML pages and generate Jinja2 templates."""
import re, os

BASE_DIR = "/home/alexagent/projects/gas-inpex-site"
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

# Page metadata
PAGES = {
    "index.html": {
        "title": "Gas Inpex — Инжиниринг, автоматизация и поставка газового оборудования",
        "description": "ТОО «Gas Inpex» — инжиниринг, автоматизация (АСУ ТП), поставка промышленного газового оборудования, проектирование систем Умный дом. г. Темиртау.",
        "canonical": "https://pandadi.github.io/gas-inpex-site/",
        "og_url": "https://pandadi.github.io/gas-inpex-site/",
        "og_image": "https://pandadi.github.io/gas-inpex-site/images/og-preview.webp",
        "route": "/",
    },
    "services.html": {
        "title": "Услуги — Gas Inpex",
        "description": "Полный перечень услуг ТОО «Gas Inpex»: инжиниринг, автоматизация АСУ ТП, поставка газового оборудования, проектирование Умный дом, СМР и ПНР.",
        "canonical": "https://pandadi.github.io/gas-inpex-site/services.html",
        "og_url": "https://pandadi.github.io/gas-inpex-site/services.html",
        "og_image": "https://pandadi.github.io/gas-inpex-site/images/og-preview.webp",
        "route": "/services.html",
    },
    "contacts.html": {
        "title": "Контакты — Gas Inpex",
        "description": "Контакты ТОО «Gas Inpex»: г. Темиртау, ул. Амангельды, 112. Телефон, email, форма обратной связи.",
        "canonical": "https://pandadi.github.io/gas-inpex-site/contacts.html",
        "og_url": "https://pandadi.github.io/gas-inpex-site/contacts.html",
        "og_image": "https://pandadi.github.io/gas-inpex-site/images/og-preview.webp",
        "route": "/contacts.html",
    },
    "objects.html": {
        "title": "Объекты — Gas Inpex",
        "description": "Портфолио выполненных проектов ТОО «Gas Inpex»: промышленные котельные, автоматизация заводов, Умный дом, газопроводы.",
        "canonical": "https://pandadi.github.io/gas-inpex-site/objects.html",
        "og_url": "https://pandadi.github.io/gas-inpex-site/objects.html",
        "og_image": "https://pandadi.github.io/gas-inpex-site/images/og-preview.webp",
        "route": "/objects.html",
    },
    "partners.html": {
        "title": "Партнеры и клиенты — Gas Inpex",
        "description": "Партнеры и клиенты ТОО «Gas Inpex»: Hitachi, Toyota Tsusho, Caterpillar, Ariston, Qarmet, Siemens, Baxi, Vaillant, Grundfos, Kiturami.",
        "canonical": "https://pandadi.github.io/gas-inpex-site/partners.html",
        "og_url": "https://pandadi.github.io/gas-inpex-site/partners.html",
        "og_image": "https://pandadi.github.io/gas-inpex-site/images/og-preview.webp",
        "route": "/partners.html",
    },
    "certificates.html": {
        "title": "Сертификаты и лицензии — Gas Inpex",
        "description": "Лицензии и сертификаты ТОО «Gas Inpex»: ISO 9001, лицензия ГСЛ, разрешения на монтаж, свидетельство СРО.",
        "canonical": "https://pandadi.github.io/gas-inpex-site/certificates.html",
        "og_url": "https://pandadi.github.io/gas-inpex-site/certificates.html",
        "og_image": "https://pandadi.github.io/gas-inpex-site/images/og-preview.webp",
        "route": "/certificates.html",
    },
    "service-detail.html": {
        "title": "Услуги Gas Inpex — Подробное описание",
        "description": "Подробное описание услуг ТОО «Gas Inpex»: проектирование АСУ ТП, системы Умный дом, СМР и ПНР, промышленные котельные, бытовые котлы, датчики утечки газа.",
        "canonical": "https://pandadi.github.io/gas-inpex-site/service-detail.html",
        "og_url": "https://pandadi.github.io/gas-inpex-site/service-detail.html",
        "og_image": "https://pandadi.github.io/gas-inpex-site/images/og-preview.webp",
        "route": "/service-detail.html",
    },
    "catalog-boilers.html": {
        "title": "Бытовые котлы — Каталог Gas Inpex",
        "description": "Каталог бытовых газовых котлов от Gas Inpex: настенные, напольные, двухконтурные модели Ariston, Baxi, Vaillant.",
        "canonical": "https://pandadi.github.io/gas-inpex-site/catalog-boilers.html",
        "og_url": "https://pandadi.github.io/gas-inpex-site/catalog-boilers.html",
        "og_image": "https://pandadi.github.io/gas-inpex-site/images/og-preview.webp",
        "route": "/catalog-boilers.html",
    },
    "catalog-industrial.html": {
        "title": "Промышленное газовое оборудование — Каталог Gas Inpex",
        "description": "Каталог промышленного газового оборудования от Gas Inpex: газовые горелки, клапаны, регуляторы давления, газоанализаторы.",
        "canonical": "https://pandadi.github.io/gas-inpex-site/catalog-industrial.html",
        "og_url": "https://pandadi.github.io/gas-inpex-site/catalog-industrial.html",
        "og_image": "https://pandadi.github.io/gas-inpex-site/images/og-preview.webp",
        "route": "/catalog-industrial.html",
    },
    "catalog-kipia.html": {
        "title": "Оборудование КИПиА — Каталог Gas Inpex",
        "description": "Каталог оборудования КИПиА от Gas Inpex: датчики давления, температуры, расхода, уровня, контроллеры, панели оператора.",
        "canonical": "https://pandadi.github.io/gas-inpex-site/catalog-kipia.html",
        "og_url": "https://pandadi.github.io/gas-inpex-site/catalog-kipia.html",
        "og_image": "https://pandadi.github.io/gas-inpex-site/images/og-preview.webp",
        "route": "/catalog-kipia.html",
    },
    "catalog-smarthome.html": {
        "title": "Системы «Умный дом» — Каталог Gas Inpex",
        "description": "Каталог систем «Умный дом» от Gas Inpex: контроллеры, датчики, исполнительные устройства, сценарии автоматизации.",
        "canonical": "https://pandadi.github.io/gas-inpex-site/catalog-smarthome.html",
        "og_url": "https://pandadi.github.io/gas-inpex-site/catalog-smarthome.html",
        "og_image": "https://pandadi.github.io/gas-inpex-site/images/og-preview.webp",
        "route": "/catalog-smarthome.html",
    },
}


def extract_content(html_path):
    """Extract content between </header> and <footer."""
    with open(html_path, "r") as f:
        html = f.read()

    # Find the end of the header (after the mobile menu closing div)
    # Pattern: end of header mobile menu, before content starts
    # We look for </header> and then take everything until <footer
    header_end = html.find("</header>")
    if header_end == -1:
        print(f"WARNING: no </header> found in {html_path}")
        return ""

    footer_start = html.find("<footer", header_end)
    if footer_start == -1:
        print(f"WARNING: no <footer found in {html_path}")
        return ""

    content = html[header_end + len("</header>"):footer_start]

    # Fix image paths: images/xxx.webp -> /static/images/xxx.webp
    # But only for relative paths, not absolute URLs
    # Fix url() references in styles
    content = re.sub(
        r'images/([a-zA-Z0-9_\-/]+\.(?:webp|svg|png|jpg|jpeg))',
        r'/static/images/\1',
        content
    )

    return content.strip()


template_header = """{% extends "base.html" %}
{% block title %}TITLE_PLACEHOLDER{% endblock %}
{% block description %}DESC_PLACEHOLDER{% endblock %}
{% block canonical %}CANONICAL_PLACEHOLDER{% endblock %}
{% block og_url %}OG_URL_PLACEHOLDER{% endblock %}
{% block og_image %}OG_IMAGE_PLACEHOLDER{% endblock %}

{% block content %}
"""

template_footer = """
{% endblock %}
"""

for filename, meta in PAGES.items():
    html_path = os.path.join(BASE_DIR, filename)
    content = extract_content(html_path)

    templ = template_header
    templ = templ.replace("TITLE_PLACEHOLDER", meta["title"])
    templ = templ.replace("DESC_PLACEHOLDER", meta["description"])
    templ = templ.replace("CANONICAL_PLACEHOLDER", meta["canonical"])
    templ = templ.replace("OG_URL_PLACEHOLDER", meta["og_url"])
    templ = templ.replace("OG_IMAGE_PLACEHOLDER", meta["og_image"])

    out_path = os.path.join(TEMPLATE_DIR, filename)
    with open(out_path, "w") as f:
        f.write(templ + content + template_footer)

    print(f"Created {out_path} ({len(content)} chars of content)")

print("\nDone!")
