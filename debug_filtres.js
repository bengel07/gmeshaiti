// debug_filtres.js
// Exécutez ce script dans la console F12 de votre navigateur

console.clear();
console.log("%c🔍 DIAGNOSTIC DES FILTRES - GMES", "background: #003366; color: white; padding: 10px; font-size: 16px;");
console.log("==========================================");

// 1. VÉRIFIER LES ÉLÉMENTS
console.log("\n1️⃣ ÉLÉMENTS DU FILTRE:");
const elements = {
    statut: document.getElementById('filtre_statut'),
    role: document.getElementById('filtre_role'),
    succursale: document.getElementById('filtre_succursale'),
    search: document.getElementById('searchInput')
};

for (let [name, el] of Object.entries(elements)) {
    console.log(`   ${name}: ${el ? '✅' : '❌'}`, el || '');
}

// 2. VÉRIFIER LE TABLEAU
console.log("\n2️⃣ TABLEAU:");
const table = document.querySelector('table');
console.log("   Existe:", table ? '✅' : '❌');

const tbody = document.querySelector('tbody');
const rows = tbody ? tbody.querySelectorAll('tr') : [];
console.log("   Lignes:", rows.length);

// 3. ANALYSER LES COLONNES
if (rows.length > 0) {
    console.log("\n3️⃣ COLONNES DISPONIBLES:");
    const firstRow = rows[0];
    const cells = firstRow.querySelectorAll('td');

    console.log(`   Nombre de colonnes: ${cells.length}`);
    console.log("   ");

    cells.forEach((cell, i) => {
        let content = cell.textContent.trim().replace(/\s+/g, ' ').substring(0, 40);
        let type = '';

        if (cell.innerHTML.includes('btn-success')) type = '🔘 (bouton Approuver)';
        else if (cell.innerHTML.includes('text-muted')) type = 'ℹ️ (info)';

        console.log(`   [${i}] "${content}" ${type}`);
    });
}

// 4. TESTER LA FONCTION
console.log("\n4️⃣ FONCTION FILTRE:");
if (typeof filterTable === 'function') {
    console.log("   ✅ filterTable() existe");

    // Tester chaque filtre
    console.log("\n   TEST - Filtrer 'en_attente':");
    if (elements.statut) {
        elements.statut.value = 'en_attente';
        filterTable();

        const visible = Array.from(rows).filter(r => r.style.display !== 'none');
        console.log(`   ➤ Lignes visibles: ${visible.length}/${rows.length}`);

        // Afficher les employés en attente trouvés
        visible.forEach((row, i) => {
            const nom = row.cells[0]?.textContent.trim();
            const role = row.cells[2]?.textContent.trim();
            console.log(`     ${i+1}. ${nom} (${role})`);
        });

        elements.statut.value = '';
        filterTable();
    }
} else {
    console.log("   ❌ filterTable() n'existe pas!");
}

// 5. VÉRIFIER LES ÉVÉNEMENTS
console.log("\n5️⃣ ÉVÉNEMENTS:");
const statutSelect = elements.statut;
if (statutSelect) {
    const events = getEventListeners ? getEventListeners(statutSelect) : 'N/A';
    console.log("   Écouteurs sur filtre_statut:",
                typeof events === 'string' ? 'Vérifiez avec Chrome DevTools' :
                Object.keys(events).length > 0 ? '✅' : '❌');
}

console.log("\n%c📋 RAPPORT:", "font-weight: bold;");
console.log("   Si des ❌ apparaissent, voici les solutions:");
console.log("   - Éléments manquants: Les IDs dans le HTML ne correspondent pas");
console.log("   - Pas de lignes: La variable 'employes' est vide dans Flask");
console.log("   - Mauvaises colonnes: Ajustez les indexes dans filterTable()");
console.log("   - filterTable manquante: Le script n'est pas chargé");