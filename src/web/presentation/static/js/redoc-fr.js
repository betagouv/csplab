// Redoc 2 has no i18n: translates its interface labels in place.
(function () {
    "use strict";

    const TEXTS = {
        "required": "obligatoire",
        "Array of": "Tableau de",
        "strings": "chaînes",
        "objects": "objets",
        "integers": "entiers",
        "numbers": "nombres",
        "booleans": "booléens",
        "Items": "Éléments",
        "Enum": "Valeurs possibles",
        "Enum:": "Valeurs possibles :",
        "Content type": "Type de contenu",
        "Copy": "Copier",
        "Copied": "Copié",
        "Authorizations:": "Authentification :",
        "None": "Aucune",
        "Responses": "Réponses",
        "Response Headers": "En-têtes de réponse",
        "Response Schema:": "Schéma de la réponse :",
        "Response samples": "Exemples de réponse",
        "Request samples": "Exemples de requête",
        "Request Body schema:": "Corps de la requête :",
        "Payload": "Corps",
        "Expand all": "Tout déplier",
        "Collapse all": "Tout replier",
        "Default:": "Par défaut :",
        "Example": "Exemple",
        "Example:": "Exemple :",
        "Examples:": "Exemples :",
        "Value:": "Valeur :",
        "non-empty": "non vide",
        "Deprecated": "Obsolète",
        "deprecated": "obsolète",
        "read-only": "lecture seule",
        "write-only": "écriture seule",
        "Recursive": "Récursif",
        "Callbacks": "Callbacks",
        "No results found": "Aucun résultat",
        "API docs by Redocly": "Documentation générée par Redocly",
        "Security Scheme Type:": "Type de schéma de sécurité :",
        "Header parameter name:": "Nom de l'en-tête :",
        "HTTP Authorization Scheme:": "Schéma d'autorisation HTTP :",
        "Bearer format:": "Format du jeton :",
    };
    const PARAMETERS = {
        "query Parameters": "Paramètres de requête",
        "path Parameters": "Paramètres de chemin",
        "header Parameters": "Paramètres d'en-tête",
        "cookie Parameters": "Paramètres de cookie",
    };
    const ITEMS = /^(\[[^\]]*\]) items$/;
    const PLACEHOLDER = "Rechercher…";

    function translateText(node) {
        const raw = node.nodeValue;
        const text = raw.trim();
        if (!text || node.parentElement?.closest(".redoc-markdown, pre, code")) {
            return;
        }
        let translated = TEXTS[text];
        if (translated === undefined) {
            const match = ITEMS.exec(text);
            translated = match ? `${match[1]} éléments` : undefined;
        }
        if (translated !== undefined && translated !== text) {
            node.nodeValue = raw.replace(text, translated);
        }
    }

    function translate(root) {
        const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
        let node;
        while ((node = walker.nextNode())) {
            translateText(node);
        }
        root.querySelectorAll("h5").forEach((heading) => {
            const translated = PARAMETERS[heading.textContent.trim()];
            if (translated) {
                heading.textContent = translated;
            }
        });
        root.querySelectorAll("input[placeholder]").forEach((input) => {
            if (input.placeholder !== PLACEHOLDER) {
                input.placeholder = PLACEHOLDER;
            }
        });
    }

    window.translateRedoc = function (container) {
        let scheduled = false;
        const observer = new MutationObserver(() => {
            if (scheduled) {
                return;
            }
            scheduled = true;
            requestAnimationFrame(() => {
                scheduled = false;
                translate(container);
            });
        });
        observer.observe(container, {
            childList: true,
            subtree: true,
            characterData: true,
        });
        translate(container);
    };
})();
