const AuditLog = require('../models/AuditLog');
const exportUtils = require('../utils/exportUtils');

// GET /admin/audit-acces - Page principale avec filtres
exports.getAuditLogs = async (req, res) => {
    try {
        const {
            type,
            status,
            user,
            start,
            end,
            succursale,
            severity,
            page = 1,
            limit = 20
        } = req.query;

        // Construction des filtres
        const filter = {};

        if (type) filter.eventType = type;
        if (status) filter.status = status;
        if (severity) filter.severity = severity;
        if (succursale) filter.succursale = succursale;

        if (user) {
            filter.$or = [
                { username: { $regex: user, $options: 'i' } },
                { 'details.email': { $regex: user, $options: 'i' } }
            ];
        }

        // Filtrage par date
        if (start || end) {
            filter.timestamp = {};
            if (start) filter.timestamp.$gte = new Date(start);
            if (end) filter.timestamp.$lte = new Date(end);
        }

        // Calcul de la pagination
        const skip = (page - 1) * limit;

        // Récupération des logs avec pagination
        const logs = await AuditLog.find(filter)
            .sort({ timestamp: -1 })
            .skip(skip)
            .limit(parseInt(limit))
            .lean();

        // Total pour la pagination
        const total = await AuditLog.countDocuments(filter);

        // Statistiques
        const stats = await AuditLog.aggregate([
            { $match: filter },
            {
                $group: {
                    _id: null,
                    total: { $sum: 1 },
                    success: { $sum: { $cond: [{ $eq: ["$status", "success"] }, 1, 0] } },
                    failed: { $sum: { $cond: [{ $eq: ["$status", "failed"] }, 1, 0] } },
                    critical: { $sum: { $cond: [{ $eq: ["$severity", "critical"] }, 1, 0] } }
                }
            }
        ]);

        // Formatage des dates pour l'affichage
        const formattedLogs = logs.map(log => ({
            ...log,
            date: log.timestamp.toLocaleDateString('fr-FR'),
            time: log.timestamp.toLocaleTimeString('fr-FR'),
            formattedTimestamp: log.timestamp.toISOString()
        }));

        res.json({
            success: true,
            data: formattedLogs,
            pagination: {
                page: parseInt(page),
                limit: parseInt(limit),
                total,
                pages: Math.ceil(total / limit)
            },
            stats: stats[0] || { total: 0, success: 0, failed: 0, critical: 0 },
            filters: req.query
        });

    } catch (error) {
        console.error('Erreur récupération logs audit:', error);
        res.status(500).json({
            success: false,
            message: 'Erreur serveur',
            error: error.message
        });
    }
};

// GET /admin/audit-acces/export - Export des logs
exports.exportAuditLogs = async (req, res) => {
    try {
        const { format = 'pdf', ...filters } = req.query;

        // Mêmes filtres que pour l'affichage
        const filter = buildFilter(filters);

        // Récupération de tous les logs (sans pagination)
        const logs = await AuditLog.find(filter)
            .sort({ timestamp: -1 })
            .lean();

        if (logs.length === 0) {
            return res.status(404).json({
                success: false,
                message: 'Aucun log à exporter'
            });
        }

        // Génération du fichier selon le format
        switch (format.toLowerCase()) {
            case 'pdf':
                const pdfBuffer = await exportUtils.generatePDF(logs, filters);
                res.setHeader('Content-Type', 'application/pdf');
                res.setHeader('Content-Disposition', `attachment; filename=audit-${Date.now()}.pdf`);
                return res.send(pdfBuffer);

            case 'csv':
                const csvData = exportUtils.generateCSV(logs);
                res.setHeader('Content-Type', 'text/csv');
                res.setHeader('Content-Disposition', `attachment; filename=audit-${Date.now()}.csv`);
                return res.send(csvData);

            case 'excel':
                const excelBuffer = await exportUtils.generateExcel(logs);
                res.setHeader('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
                res.setHeader('Content-Disposition', `attachment; filename=audit-${Date.now()}.xlsx`);
                return res.send(excelBuffer);

            default:
                return res.status(400).json({
                    success: false,
                    message: 'Format non supporté. Utilisez pdf, csv ou excel.'
                });
        }

    } catch (error) {
        console.error('Erreur export logs audit:', error);
        res.status(500).json({
            success: false,
            message: 'Erreur lors de l\'export',
            error: error.message
        });
    }
};

// POST /admin/audit-acces/log - Créer un log d'audit (interne)
exports.createAuditLog = async (data) => {
    try {
        const auditLog = new AuditLog(data);
        await auditLog.save();
        return auditLog;
    } catch (error) {
        console.error('Erreur création log audit:', error);
        throw error;
    }
};

// GET /admin/audit-acces/stats - Statistiques détaillées
exports.getAuditStats = async (req, res) => {
    try {
        const { succursale, start, end } = req.query;

        const filter = {};
        if (succursale) filter.succursale = succursale;
        if (start || end) {
            filter.timestamp = {};
            if (start) filter.timestamp.$gte = new Date(start);
            if (end) filter.timestamp.$lte = new Date(end);
        }

        const stats = await AuditLog.aggregate([
            { $match: filter },
            {
                $facet: {
                    byEventType: [
                        { $group: { _id: "$eventType", count: { $sum: 1 } } },
                        { $sort: { count: -1 } }
                    ],
                    byStatus: [
                        { $group: { _id: "$status", count: { $sum: 1 } } }
                    ],
                    bySeverity: [
                        { $group: { _id: "$severity", count: { $sum: 1 } } }
                    ],
                    byHour: [
                        {
                            $group: {
                                _id: { $hour: "$timestamp" },
                                count: { $sum: 1 }
                            }
                        },
                        { $sort: { _id: 1 } }
                    ],
                    recentActivity: [
                        { $sort: { timestamp: -1 } },
                        { $limit: 10 },
                        {
                            $project: {
                                username: 1,
                                eventType: 1,
                                description: 1,
                                timestamp: 1,
                                status: 1
                            }
                        }
                    ]
                }
            }
        ]);

        res.json({
            success: true,
            data: stats[0]
        });

    } catch (error) {
        console.error('Erreur récupération stats audit:', error);
        res.status(500).json({
            success: false,
            message: 'Erreur serveur',
            error: error.message
        });
    }
};

// Helper function pour construire les filtres
function buildFilter(query) {
    const filter = {};

    if (query.type) filter.eventType = query.type;
    if (query.status) filter.status = query.status;
    if (query.severity) filter.severity = query.severity;
    if (query.succursale) filter.succursale = query.succursale;

    if (query.user) {
        filter.$or = [
            { username: { $regex: query.user, $options: 'i' } },
            { 'details.email': { $regex: query.user, $options: 'i' } }
        ];
    }

    if (query.start || query.end) {
        filter.timestamp = {};
        if (query.start) filter.timestamp.$gte = new Date(query.start);
        if (query.end) filter.timestamp.$lte = new Date(query.end);
    }

    return filter;
}