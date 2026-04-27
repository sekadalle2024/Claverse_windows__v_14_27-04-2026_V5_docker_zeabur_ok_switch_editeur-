/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * PAPIER DE TRAVAIL - CROSS RÉFÉRENCE HORIZONTALE
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * Ce module gère l'ajout automatique d'une table "Cross référence horizontale"
 * au-dessus des tables principales de test (Modelised_table) dans le chat.
 * 
 * Fonctionnalités:
 * - Détection automatique de la "Nature de test" dans la table 2 de la div
 * - Génération des références selon la nature de test (même structure que Schéma de calcul)
 * - Indexation des références selon le cycle comptable
 * - Sauvegarde persistante avec localStorage
 * - Édition des cellules de cross référence
 * 
 * @version 1.0
 * @date 2026-04-24
 */

(function () {
  "use strict";

  console.log("📎 [Cross Ref] Module chargé");

  // Configuration
  const CONFIG = {
    storageKey: "claraverse_cross_ref_data",
    autoSaveDelay: 500,
    debugMode: true,
  };

  // Utilitaires de debug
  const debug = {
    log: (...args) => CONFIG.debugMode && console.log("📎 [Cross Ref]", ...args),
    error: (...args) => console.error("❌ [Cross Ref]", ...args),
    warn: (...args) => console.warn("⚠️ [Cross Ref]", ...args),
  };

  /**
   * Classe principale pour gérer les cross références horizontales
   */
  class CrossRefHorizontaleManager {
    constructor() {
      this.processedTables = new WeakSet();
      this.saveTimeout = null;
      this.isInitialized = false;
      this.storageKey = CONFIG.storageKey;
      this.autoSaveDelay = CONFIG.autoSaveDelay;
    }

    init() {
      if (this.isInitialized) return;
      
      debug.log("Initialisation du gestionnaire de cross références horizontales");
      
      // Attendre que le DOM soit prêt
      if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", () => this.start());
      } else {
        this.start();
      }
    }

    start() {
      this.testLocalStorage();
      this.startMonitoring();
      this.restoreAllCrossRefs();
      this.isInitialized = true;
      
      debug.log("✅ Gestionnaire initialisé avec succès");
    }

    /**
     * Tester la disponibilité de localStorage
     */
    testLocalStorage() {
      try {
        if (typeof localStorage === "undefined") {
          debug.warn("localStorage n'est pas disponible");
          return false;
        }

        const testKey = "claraverse_crossref_test";
        localStorage.setItem(testKey, "test");
        const testValue = localStorage.getItem(testKey);
        localStorage.removeItem(testKey);

        if (testValue === "test") {
          debug.log("✅ localStorage fonctionne correctement");
          
          const existingData = this.loadAllData();
          const crossRefCount = Object.keys(existingData).length;
          debug.log(`📦 ${crossRefCount} cross référence(s) trouvée(s) dans le stockage`);
          
          return true;
        }
      } catch (error) {
        debug.error("Erreur de test localStorage:", error.message);
        return false;
      }
    }

    /**
     * Démarrer la surveillance des tables
     */
    startMonitoring() {
      // Traitement initial
      this.processAllTables();

      // Surveillance continue avec MutationObserver
      this.setupMutationObserver();

      // Fallback avec setInterval
      this.intervalId = setInterval(() => {
        this.processAllTables();
      }, 2000);

      debug.log("Surveillance des tables démarrée");
    }

    /**
     * Configurer le MutationObserver
     */
    setupMutationObserver() {
      if (this.observer) {
        this.observer.disconnect();
      }

      this.observer = new MutationObserver((mutations) => {
        let shouldProcess = false;

        mutations.forEach((mutation) => {
          if (mutation.type === "childList") {
            mutation.addedNodes.forEach((node) => {
              if (node.nodeType === Node.ELEMENT_NODE) {
                if (
                  node.tagName === "TABLE" ||
                  (node.querySelector && node.querySelector("table"))
                ) {
                  shouldProcess = true;
                }
              }
            });
          }
        });

        if (shouldProcess) {
          debug.log("Changement DOM détecté, retraitement des tables");
          setTimeout(() => this.processAllTables(), 500);
        }
      });

      this.observer.observe(document.body, {
        childList: true,
        subtree: true,
        attributes: false,
      });
    }

    /**
     * Traiter toutes les tables du document
     */
    processAllTables() {
      // Rechercher toutes les divs contenant des tables
      const chatDivs = document.querySelectorAll('div.prose, div[class*="prose"]');
      
      chatDivs.forEach((div) => {
        this.processDivTables(div);
      });
    }

    /**
     * Traiter les tables dans une div spécifique
     */
    processDivTables(div) {
      debug.log("🔍 [DEBUT] Traitement d'une div pour cross références");
      
      const tables = div.querySelectorAll("table");
      debug.log(`📊 Nombre de tables trouvées: ${tables.length}`);
      
      if (tables.length < 2) {
        debug.warn(`⚠️ Pas assez de tables (besoin de 2 minimum, trouvé ${tables.length})`);
        return;
      }

      // Identifier la table 2 (contient "Nature de test")
      let table2 = null;
      let natureDeTest = null;

      debug.log("🔍 Recherche de la table avec 'Nature de test'...");
      for (let i = 0; i < tables.length; i++) {
        const table = tables[i];
        const result = this.extractNatureDeTest(table);
        debug.log(`  Table ${i + 1}: ${result ? `✅ Nature trouvée: "${result}"` : "❌ Pas de nature"}`);
        if (result) {
          table2 = table;
          natureDeTest = result;
          break;
        }
      }

      if (!table2 || !natureDeTest) {
        debug.error("❌ Aucune table avec 'Nature de test' trouvée");
        return;
      }

      debug.log(`✅ Nature de test détectée: "${natureDeTest}"`);

      // Trouver la table principale (Modelised_table)
      let tablePrincipale = null;
      
      debug.log("🔍 Recherche de la table principale...");
      for (let i = 0; i < tables.length; i++) {
        const table = tables[i];
        if (table === table2) {
          debug.log(`  Table ${i + 1}: ⏭️ Ignorée (c'est la table 2)`);
          continue;
        }
        
        if (this.isModelizedTable(table)) {
          tablePrincipale = table;
          debug.log(`  Table ${i + 1}: ✅ C'est la table principale!`);
          break;
        }
      }

      if (!tablePrincipale) {
        debug.error("❌ Aucune table principale trouvée");
        return;
      }

      // Vérifier si une cross référence existe déjà
      if (this.processedTables.has(tablePrincipale)) {
        debug.warn("⚠️ Cross référence déjà créée pour cette table");
        return;
      }

      // Créer la cross référence horizontale
      debug.log("🎯 Création de la cross référence horizontale...");
      this.createCrossRefHorizontale(tablePrincipale, natureDeTest, div);
      this.processedTables.add(tablePrincipale);
      debug.log("✅ [FIN] Cross référence créée avec succès!");
    }

    /**
     * Extraire la "Nature de test" de la table 2
     */
    extractNatureDeTest(table) {
      const rows = table.querySelectorAll("tr");
      
      // CAS 1: Recherche horizontale
      for (let rowIdx = 0; rowIdx < rows.length; rowIdx++) {
        const row = rows[rowIdx];
        const cells = row.querySelectorAll("td, th");
        
        for (let i = 0; i < cells.length - 1; i++) {
          const cellText = cells[i].textContent.trim().toLowerCase();
          
          if (cellText.includes("nature") && cellText.includes("test")) {
            const valueCell = cells[i + 1];
            if (valueCell && valueCell.textContent.trim() !== "") {
              return valueCell.textContent.trim();
            }
          }
        }
      }
      
      // CAS 2: Recherche verticale
      for (let rowIdx = 0; rowIdx < rows.length; rowIdx++) {
        const row = rows[rowIdx];
        const cells = row.querySelectorAll("td, th");
        
        for (let colIdx = 0; colIdx < cells.length; colIdx++) {
          const cellText = cells[colIdx].textContent.trim().toLowerCase();
          
          if (cellText.includes("nature") && cellText.includes("test")) {
            for (let nextRowIdx = rowIdx + 1; nextRowIdx < rows.length; nextRowIdx++) {
              const nextRow = rows[nextRowIdx];
              const nextCells = nextRow.querySelectorAll("td, th");
              
              if (nextCells[colIdx]) {
                const value = nextCells[colIdx].textContent.trim();
                if (value !== "" && !value.toLowerCase().includes("nature")) {
                  return value;
                }
              }
            }
            
            // CAS 3: Cellule adjacente
            if (colIdx + 1 < cells.length) {
              const adjacentCell = cells[colIdx + 1];
              if (adjacentCell && adjacentCell.textContent.trim() !== "") {
                const value = adjacentCell.textContent.trim();
                if (!value.toLowerCase().includes("nature")) {
                  return value;
                }
              }
            }
          }
        }
      }
      
      return null;
    }

    /**
     * Vérifier si une table est une table modelisée
     */
    isModelizedTable(table) {
      const headers = this.getTableHeaders(table);
      
      return headers.some(header => {
        const h = header.toLowerCase().trim();
        if (h === "conclusion") return true;
        if (h === "assertion") return true;
        if (/^ctr\d*$/i.test(h)) return true;
        if (h.includes("ecart") || h.includes("écart") || h.includes("montant")) return true;
        
        return false;
      });
    }

    /**
     * Obtenir les en-têtes d'une table
     */
    getTableHeaders(table) {
      const headerSelectors = [
        "thead th",
        "thead td",
        "tr:first-child th",
        "tr:first-child td",
      ];

      for (const selector of headerSelectors) {
        const headers = table.querySelectorAll(selector);
        if (headers.length > 0) {
          return Array.from(headers).map((cell) => cell.textContent.trim());
        }
      }

      return [];
    }

    /**
     * Trouver l'index de la colonne "Ecart" dans une table
     */
    findEcartColumnIndex(table) {
      const headers = this.getTableHeaders(table);
      
      for (let i = 0; i < headers.length; i++) {
        const h = headers[i].toLowerCase().trim();
        if (h.includes("ecart") || h.includes("écart") || h.includes("montant")) {
          debug.log(`📎 [Alignement] Colonne "Ecart" trouvée à l'index ${i}`);
          return i;
        }
      }
      
      debug.warn("📎 [Alignement] Colonne 'Ecart' non trouvée");
      return -1;
    }

    /**
     * Calculer le nombre de colonnes vides à ajouter avant les références
     */
    calculateEmptyColumnsCount(tablePrincipale, nbColonnes) {
      const totalColumns = this.getTableHeaders(tablePrincipale).length;
      const ecartIndex = this.findEcartColumnIndex(tablePrincipale);
      
      debug.log(`📎 [Alignement] Total colonnes table: ${totalColumns}`);
      debug.log(`📎 [Alignement] Index colonne Ecart: ${ecartIndex}`);
      debug.log(`📎 [Alignement] Nombre de références: ${nbColonnes}`);
      
      if (ecartIndex === -1) {
        // Pas de colonne Ecart, aligner à droite
        const emptyColumns = totalColumns - nbColonnes;
        debug.log(`📎 [Alignement] Pas d'Ecart, alignement à droite: ${emptyColumns} colonnes vides`);
        return Math.max(0, emptyColumns);
      }
      
      // Aligner pour que la dernière référence soit sur la colonne Ecart
      const emptyColumns = ecartIndex - nbColonnes + 1;
      
      debug.log(`📎 [Alignement] Formule: ${ecartIndex} - ${nbColonnes} + 1 = ${emptyColumns}`);
      
      return Math.max(0, emptyColumns);
    }

    /**
     * Créer la cross référence horizontale selon la nature de test
     */
    createCrossRefHorizontale(tablePrincipale, natureDeTest, parentDiv) {
      debug.log(`Création de la cross référence pour: ${natureDeTest}`);

      // Déterminer le modèle (même logique que Schéma de calcul)
      const modele = this.determinerModele(natureDeTest);
      
      if (!modele) {
        debug.warn(`Aucun modèle trouvé pour: ${natureDeTest}`);
        return;
      }

      // Vérifier si une cross référence existe déjà
      const existingCrossRef = this.findExistingCrossRef(tablePrincipale);
      if (existingCrossRef) {
        debug.log("Cross référence déjà existante");
        return;
      }

      // Créer la table de cross référence avec alignement
      const crossRefTable = this.buildCrossRefTable(modele, natureDeTest, tablePrincipale);
      
      // Générer un ID unique
      const crossRefId = this.generateCrossRefId(tablePrincipale);
      crossRefTable.dataset.crossRefId = crossRefId;
      crossRefTable.dataset.forTable = tablePrincipale.dataset.tableId || this.generateTableId(tablePrincipale);

      // Insérer EN DESSOUS de la table principale
      if (tablePrincipale.nextSibling) {
        tablePrincipale.parentNode.insertBefore(crossRefTable, tablePrincipale.nextSibling);
      } else {
        tablePrincipale.parentNode.appendChild(crossRefTable);
      }

      // Rendre les cellules éditables
      this.makeCrossRefEditable(crossRefTable);

      // Installer le détecteur de changements
      this.setupCrossRefChangeDetection(crossRefTable);

      debug.log(`✅ Cross référence créée avec ID: ${crossRefId}`);
    }

    /**
     * Déterminer le modèle selon la nature de test
     * Retourne le nombre de colonnes basé sur le schéma de calcul
     */
    determinerModele(natureDeTest) {
      const nature = natureDeTest.toLowerCase();

      // Validation: 5 colonnes
      if (nature.includes("validation")) {
        return {
          type: "Validation",
          nbColonnes: 5,
        };
      }

      // Mouvement: 6 colonnes
      if (nature.includes("mouvement")) {
        return {
          type: "Mouvement",
          nbColonnes: 6,
        };
      }

      // Rapprochement: 3 colonnes
      if (nature.includes("rapprochement")) {
        return {
          type: "Rapprochement",
          nbColonnes: 3,
        };
      }

      // Séparation: 3 colonnes
      if (nature.includes("separation") || nature.includes("séparation")) {
        return {
          type: "Séparation",
          nbColonnes: 3,
        };
      }

      // Estimation: 5 colonnes
      if (nature.includes("estimation")) {
        return {
          type: "Estimation",
          nbColonnes: 5,
        };
      }

      // Revue analytique: 3 colonnes
      if (nature.includes("revue") && nature.includes("analytique")) {
        return {
          type: "Revue analytique",
          nbColonnes: 3,
        };
      }

      // Cadrage TVA: 6 colonnes
      if (nature.includes("cadrage") && nature.includes("tva")) {
        return {
          type: "Cadrage TVA",
          nbColonnes: 6,
        };
      }

      // Cotisations sociales: 4 colonnes
      if (nature.includes("cotisation") && nature.includes("sociale")) {
        return {
          type: "Cotisations sociales",
          nbColonnes: 4,
        };
      }

      // Vierge: 0 colonnes
      if (nature.includes("vierge")) {
        return {
          type: "Vierge",
          nbColonnes: 0,
        };
      }

      // Modélisation: détection automatique
      if (nature.includes("modelisation") || nature.includes("modélisation")) {
        const variables = this.extractVariablesFromNature(natureDeTest);
        return {
          type: "Modélisation",
          nbColonnes: variables.length,
        };
      }

      // Par défaut
      if (natureDeTest.trim() !== "") {
        const variables = this.extractVariablesFromNature(natureDeTest);
        if (variables.length > 0) {
          return {
            type: "Modélisation (auto-détecté)",
            nbColonnes: variables.length,
          };
        }
      }

      return null;
    }

    /**
     * Extraire les variables d'une formule
     */
    extractVariablesFromNature(natureDeTest) {
      const variablePattern = /\([A-Z]\)/g;
      const matches = natureDeTest.match(variablePattern);
      
      if (!matches) return [];

      return [...new Set(matches)];
    }

    /**
     * Construire la table HTML de cross référence horizontale
     */
    buildCrossRefTable(modele, natureDeTest, tablePrincipale) {
      const table = document.createElement("table");
      table.className = "min-w-full border border-gray-200 dark:border-gray-700 rounded-lg claraverse-cross-ref-horizontale";
      table.style.cssText = `
        margin-bottom: 1rem;
        border-collapse: separate;
        border-spacing: 0;
        background: #f0f9ff;
      `;

      // Calculer l'alignement
      const totalColumns = this.getTableHeaders(tablePrincipale).length;
      const emptyColumnsCount = this.calculateEmptyColumnsCount(tablePrincipale, modele.nbColonnes);
      
      debug.log(`📎 [Build] Total colonnes: ${totalColumns}`);
      debug.log(`📎 [Build] Colonnes vides avant: ${emptyColumnsCount}`);

      // Créer le tbody
      const tbody = document.createElement("tbody");

      // Ligne unique avec les colonnes
      const row = document.createElement("tr");

      // Ajouter les colonnes vides AVANT les références (fusionnées)
      if (emptyColumnsCount > 0) {
        const td = document.createElement("td");
        td.className = "px-4 py-3 border border-gray-200 dark:border-gray-700";
        td.style.cssText = `
          background: #f0f9ff;
          min-width: 80px;
        `;
        td.colSpan = emptyColumnsCount;
        td.textContent = "";
        row.appendChild(td);
      }

      // Créer les cellules de référence selon le nombre de colonnes
      for (let i = 0; i < modele.nbColonnes; i++) {
        const td = document.createElement("td");
        td.className = "px-4 py-3 text-sm text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-gray-700";
        td.style.cssText = `
          background: #e0f2fe;
          font-weight: 500;
          text-align: center;
          min-width: 80px;
        `;
        // Placeholder pour la cross référence
        td.textContent = `[  ]`;
        td.contentEditable = "true";
        row.appendChild(td);
      }

      // Compléter avec des colonnes vides APRÈS les références si nécessaire (fusionnées)
      const remainingColumns = totalColumns - emptyColumnsCount - modele.nbColonnes;
      debug.log(`📎 [Build] Colonnes vides après: ${remainingColumns}`);
      
      if (remainingColumns > 0) {
        const td = document.createElement("td");
        td.className = "px-4 py-3 border border-gray-200 dark:border-gray-700";
        td.style.cssText = `
          background: #f0f9ff;
          min-width: 80px;
        `;
        td.colSpan = remainingColumns;
        td.textContent = "";
        row.appendChild(td);
      }

      tbody.appendChild(row);
      table.appendChild(tbody);

      return table;
    }

    /**
     * Rendre la cross référence éditable
     */
    makeCrossRefEditable(crossRefTable) {
      const cells = crossRefTable.querySelectorAll("td");
      
      cells.forEach((cell) => {
        cell.contentEditable = "true";
        cell.style.cursor = "text";
        
        cell.addEventListener("blur", () => {
          this.saveCrossRefData(crossRefTable);
        });

        cell.addEventListener("keydown", (e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            cell.blur();
          }
        });
      });
    }

    /**
     * Installer le détecteur de changements
     */
    setupCrossRefChangeDetection(crossRefTable) {
      if (crossRefTable.dataset.observerInstalled === "true") {
        return;
      }

      const crossRefId = crossRefTable.dataset.crossRefId;
      debug.log(`🔍 Installation détecteur sur cross référence ${crossRefId}`);

      const crossRefObserver = new MutationObserver((mutations) => {
        let hasChanges = false;

        mutations.forEach((mutation) => {
          if (
            mutation.type === "characterData" ||
            mutation.type === "childList"
          ) {
            hasChanges = true;
          }
        });

        if (hasChanges) {
          debug.log(`📝 Changement détecté dans cross référence ${crossRefId}`);
          this.saveCrossRefData(crossRefTable);
        }
      });

      crossRefObserver.observe(crossRefTable, {
        childList: true,
        subtree: true,
        characterData: true,
        characterDataOldValue: false,
      });

      crossRefTable.dataset.observerInstalled = "true";

      if (!this.crossRefObservers) {
        this.crossRefObservers = new Map();
      }
      this.crossRefObservers.set(crossRefTable, crossRefObserver);

      debug.log(`✅ Détecteur installé sur cross référence ${crossRefId}`);
    }

    /**
     * Trouver une cross référence existante
     */
    findExistingCrossRef(tablePrincipale) {
      const tableId = tablePrincipale.dataset.tableId || this.generateTableId(tablePrincipale);
      return document.querySelector(`table.claraverse-cross-ref-horizontale[data-for-table="${tableId}"]`);
    }

    /**
     * Générer un ID unique pour la cross référence
     */
    generateCrossRefId(tablePrincipale) {
      const tableId = tablePrincipale.dataset.tableId || this.generateTableId(tablePrincipale);
      return `crossref_${tableId}_${Date.now()}`;
    }

    /**
     * Générer un ID pour une table
     */
    generateTableId(table) {
      if (table.dataset.tableId) {
        return table.dataset.tableId;
      }

      const headers = this.getTableHeaders(table);
      const headerText = headers.join("__").replace(/\s+/g, "_");
      const hash = this.hashCode(headerText);
      const uniqueId = `table_${hash}`;
      
      table.dataset.tableId = uniqueId;
      return uniqueId;
    }

    /**
     * Fonction de hachage simple
     */
    hashCode(str) {
      let hash = 0;
      for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = (hash << 5) - hash + char;
        hash = hash & hash;
      }
      return Math.abs(hash).toString(36);
    }

    /**
     * Sauvegarder les données avec debounce
     */
    saveCrossRefData(crossRefTable) {
      if (!crossRefTable) {
        debug.warn("crossRefTable est null");
        return;
      }

      debug.log("⏳ Sauvegarde programmée dans", this.autoSaveDelay, "ms");

      if (this.saveTimeout) {
        clearTimeout(this.saveTimeout);
      }

      this.saveTimeout = setTimeout(() => {
        this.saveCrossRefDataNow(crossRefTable);
      }, this.autoSaveDelay);
    }

    /**
     * Sauvegarder immédiatement
     */
    saveCrossRefDataNow(crossRefTable) {
      if (!crossRefTable) {
        debug.warn("crossRefTable est null");
        return;
      }

      debug.log("💾 Début de sauvegarde immédiate");

      const crossRefId = crossRefTable.dataset.crossRefId;
      debug.log("🆔 ID pour sauvegarde:", crossRefId);

      const allData = this.loadAllData();

      const crossRefData = {
        timestamp: Date.now(),
        forTable: crossRefTable.dataset.forTable,
        cells: [],
      };

      const rows = crossRefTable.querySelectorAll("tbody tr");
      rows.forEach((row, rowIndex) => {
        const cells = row.querySelectorAll("td");
        cells.forEach((cell, colIndex) => {
          crossRefData.cells.push({
            row: rowIndex,
            col: colIndex,
            value: cell.textContent.trim(),
          });
        });
      });

      allData[crossRefId] = crossRefData;
      this.saveAllData(allData);

      debug.log(`✅ Cross référence ${crossRefId} sauvegardée`);
    }

    /**
     * Charger toutes les données
     */
    loadAllData() {
      try {
        const data = localStorage.getItem(this.storageKey);
        return data ? JSON.parse(data) : {};
      } catch (error) {
        debug.error("Erreur lors du chargement:", error);
        return {};
      }
    }

    /**
     * Sauvegarder toutes les données
     */
    saveAllData(data) {
      try {
        localStorage.setItem(this.storageKey, JSON.stringify(data));
        debug.log("💾 Données sauvegardées dans localStorage");
      } catch (error) {
        debug.error("❌ Erreur lors de la sauvegarde:", error);
        if (error.name === "QuotaExceededError") {
          debug.warn("⚠️ Quota localStorage dépassé");
        }
      }
    }

    /**
     * Restaurer toutes les cross références
     */
    restoreAllCrossRefs() {
      debug.log("🔄 Restauration des cross références");

      const allData = this.loadAllData();
      const crossRefIds = Object.keys(allData);

      if (crossRefIds.length === 0) {
        debug.log("Aucune cross référence à restaurer");
        return;
      }

      debug.log(`📦 ${crossRefIds.length} cross référence(s) à restaurer`);

      crossRefIds.forEach((crossRefId) => {
        const crossRefData = allData[crossRefId];
        const forTableId = crossRefData.forTable;

        const tablePrincipale = document.querySelector(`table[data-table-id="${forTableId}"]`);
        
        if (!tablePrincipale) {
          debug.warn(`Table principale ${forTableId} non trouvée`);
          return;
        }

        const existingCrossRef = document.querySelector(`table[data-cross-ref-id="${crossRefId}"]`);
        
        if (existingCrossRef) {
          this.restoreCrossRefValues(existingCrossRef, crossRefData);
        } else {
          debug.log(`Cross référence ${crossRefId} non trouvée dans le DOM`);
        }
      });

      debug.log("✅ Restauration terminée");
    }

    /**
     * Restaurer les valeurs
     */
    restoreCrossRefValues(crossRefTable, crossRefData) {
      const rows = crossRefTable.querySelectorAll("tbody tr");
      
      crossRefData.cells.forEach((cellData) => {
        const row = rows[cellData.row];
        if (!row) return;

        const cells = row.querySelectorAll("td");
        const cell = cells[cellData.col];
        
        if (cell && cellData.value) {
          cell.textContent = cellData.value;
        }
      });

      debug.log(`✅ Valeurs restaurées pour ${crossRefTable.dataset.crossRefId}`);
    }

    /**
     * Nettoyer les ressources
     */
    cleanup() {
      if (this.observer) {
        this.observer.disconnect();
      }

      if (this.intervalId) {
        clearInterval(this.intervalId);
      }

      if (this.saveTimeout) {
        clearTimeout(this.saveTimeout);
      }

      if (this.crossRefObservers) {
        this.crossRefObservers.forEach((observer) => observer.disconnect());
        this.crossRefObservers.clear();
      }

      debug.log("🧹 Ressources nettoyées");
    }
  }

  // Initialiser le gestionnaire
  const manager = new CrossRefHorizontaleManager();
  manager.init();

  // Exposer globalement
  window.CrossRefHorizontaleManager = manager;

  // Commandes de debug
  window.crossRefCommands = {
    processAll: () => manager.processAllTables(),
    showStorage: () => {
      const data = manager.loadAllData();
      console.log("📦 Contenu du localStorage (cross références):");
      console.log(JSON.stringify(data, null, 2));
    },
    clearStorage: () => {
      if (confirm("Effacer toutes les cross références sauvegardées ?")) {
        localStorage.removeItem(CONFIG.storageKey);
        console.log("🗑️ Cross références effacées");
      }
    },
    restoreAll: () => manager.restoreAllCrossRefs(),
  };

  debug.log("✅ Module Cross Référence Horizontale initialisé");
  debug.log("💡 Commandes disponibles: crossRefCommands");

})();
