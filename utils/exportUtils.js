const PDFDocument = require('pdfkit');
const ExcelJS = require('exceljs');

// Générer PDF
exports.generatePDF = async (logs, filters) => {
    return new Promise((resolve, reject) => {
        try {
            const doc = new PDFDocument({ margin: 50 });
            const chunks = [];

            doc.on('data', chunk => chunks.push(chunk));
            doc.on('end', () => resolve(Buffer.concat(chunks)));

            // En-tête
            doc.fontSize(20).text('Rapport d\'Audit des Accès', { align: 'center' });
            doc.moveDown();

            // Informations
            doc.fontSize(12)
                .text(`Date de génération: ${new Date().toLocaleDateString('fr-FR')}`)
                .text(`Total logs: ${logs.length}`);

            if (filters.succursale) {
                doc.text(`Succursale: ${filters.succursale}`);
            }
            if (filters.start || filters.end) {
                doc.text(`Période: ${filters.start || 'Début'} à ${filters.end || 'Fin'}`);
            }

            doc.moveDown();

            // Tableau des logs
            const tableTop = doc.y;
            const headers = ['Date', 'Utilisateur', 'Événement', 'IP', 'Statut', 'Sévérité'];
            const colWidths = [80, 100, 150, 100, 80, 80];

            // En-têtes du tableau
            let x = 50;
            headers.forEach((header, i) => {
                doc.fontSize(10).font('Helvetica-Bold')
                    .text(header, x, tableTop, { width: colWidths[i] });
                x += colWidths[i];
            });

            // Ligne de séparation
            doc.moveTo(50, tableTop + 20).lineTo(590, tableTop + 20).stroke();

            // Données
            let y = tableTop + 30;
            logs.forEach((log, index) => {
                if (y > 700) { // Nouvelle page si nécessaire
                    doc.addPage();
                    y = 50;
                }

                x = 50;
                const rowData = [
                    new Date(log.timestamp).toLocaleDateString('fr-FR'),
                    log.username,
                    log.description.length > 40 ? log.description.substring(0, 40) + '...' : log.description,
                    log.ipAddress,
                    log.status,
                    log.severity
                ];

                rowData.forEach((cell, i) => {
                    doc.fontSize(9).font('Helvetica')
                        .text(cell || '-', x, y, { width: colWidths[i] });
                    x += colWidths[i];
                });

                y += 20;
            });

            // Pied de page
            doc.addPage();
            doc.fontSize(12).text('Résumé et Conformité', { align: 'center' });
            doc.moveDown();

            const stats = {
                total: logs.length,
                success: logs.filter(l => l.status === 'success').length,
                failed: logs.filter(l => l.status === 'failed').length,
                critical: logs.filter(l => l.severity === 'critical').length
            };

            doc.text(`Événements total: ${stats.total}`);
            doc.text(`Réussis: ${stats.success} (${((stats.success/stats.total)*100).toFixed(1)}%)`);
            doc.text(`Échoués: ${stats.failed} (${((stats.failed/stats.total)*100).toFixed(1)}%)`);
            doc.text(`Critiques: ${stats.critical}`);

            doc.moveDown();
            doc.text('Signature responsable:');
            doc.moveDown(3);
            doc.text('________________________');
            doc.text('Directeur d\'agence');

            doc.end();

        } catch (error) {
            reject(error);
        }
    });
};

// Générer CSV
exports.generateCSV = (logs) => {
    const headers = ['Date', 'Heure', 'Utilisateur', 'Rôle', 'Événement', 'Description', 'IP', 'Statut', 'Sévérité', 'Succursale'];

    let csv = headers.join(';') + '\n';

    logs.forEach(log => {
        const row = [
            new Date(log.timestamp).toLocaleDateString('fr-FR'),
            new Date(log.timestamp).toLocaleTimeString('fr-FR'),
            log.username,
            log.userRole,
            log.eventType,
            `"${log.description.replace(/"/g, '""')}"`,
            log.ipAddress,
            log.status,
            log.severity,
            log.succursale
        ];
        csv += row.join(';') + '\n';
    });

    // Ajouter BOM pour Excel
    return '\ufeff' + csv;
};

// Générer Excel
exports.generateExcel = async (logs) => {
    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet('Audit des Accès');

    // En-têtes
    worksheet.columns = [
        { header: 'Date', key: 'date', width: 15 },
        { header: 'Heure', key: 'time', width: 12 },
        { header: 'Utilisateur', key: 'username', width: 20 },
        { header: 'Rôle', key: 'role', width: 15 },
        { header: 'Type Événement', key: 'eventType', width: 15 },
        { header: 'Description', key: 'description', width: 40 },
        { header: 'Adresse IP', key: 'ip', width: 15 },
        { header: 'Statut', key: 'status', width: 10 },
        { header: 'Sévérité', key: 'severity', width: 10 },
        { header: 'Succursale', key: 'succursale', width: 15 }
    ];

    // Style des en-têtes
    worksheet.getRow(1).font = { bold: true };
    worksheet.getRow(1).fill = {
        type: 'pattern',
        pattern: 'solid',
        fgColor: { argb: 'FF1a237e' }
    };
    worksheet.getRow(1).font = { color: { argb: 'FFFFFFFF' }, bold: true };

    // Données
    logs.forEach(log => {
        worksheet.addRow({
            date: new Date(log.timestamp).toLocaleDateString('fr-FR'),
            time: new Date(log.timestamp).toLocaleTimeString('fr-FR'),
            username: log.username,
            role: log.userRole,
            eventType: log.eventType,
            description: log.description,
            ip: log.ipAddress,
            status: log.status,
            severity: log.severity,
            succursale: log.succursale
        });
    });

    // Statistiques dans une deuxième feuille
    const statsSheet = workbook.addWorksheet('Statistiques');

    const stats = {
        total: logs.length,
        success: logs.filter(l => l.status === 'success').length,
        failed: logs.filter(l => l.status === 'failed').length,
        critical: logs.filter(l => l.severity === 'critical').length
    };

    statsSheet.addRow(['Statistiques d\'Audit']);
    statsSheet.addRow(['Total événements', stats.total]);
    statsSheet.addRow(['Réussis', stats.success]);
    statsSheet.addRow(['Échoués', stats.failed]);
    statsSheet.addRow(['Critiques', stats.critical]);
    statsSheet.addRow(['Taux de réussite', `${((stats.success/stats.total)*100).toFixed(1)}%`]);

    // Générer le buffer
    return await workbook.xlsx.writeBuffer();
};