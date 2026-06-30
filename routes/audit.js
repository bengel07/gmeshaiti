const express = require('express');
const router = express.Router();
const auditController = require('../controllers/auditController');
const { authenticate, authorize, auditMiddleware } = require('../middleware/auth');

// Appliquer l'authentification et l'audit à toutes les routes
router.use(authenticate);
router.use(auditMiddleware);

// GET /admin/audit-acces - Page principale avec filtres
router.get('/', authorize('admin', 'directeur', 'compliance'), auditController.getAuditLogs);

// GET /admin/audit-acces/export - Export des logs
router.get('/export', authorize('admin', 'directeur', 'compliance'), auditController.exportAuditLogs);

// GET /admin/audit-acces/stats - Statistiques détaillées
router.get('/stats', authorize('admin', 'directeur', 'compliance'), auditController.getAuditStats);

// GET /admin/audit-acces/types - Types d'événements disponibles
router.get('/types', authenticate, (req, res) => {
    res.json({
        success: true,
        types: [
            { value: 'connexion', label: 'Connexion/Déconnexion' },
            { value: 'creation', label: 'Création' },
            { value: 'modification', label: 'Modification' },
            { value: 'suppression', label: 'Suppression' },
            { value: 'permission', label: 'Changement permission' },
            { value: 'transaction', label: 'Transaction sensible' },
            { value: 'consultation', label: 'Consultation' }
        ],
        statuses: [
            { value: 'success', label: 'Réussi' },
            { value: 'failed', label: 'Échoué' },
            { value: 'warning', label: 'Avertissement' }
        ],
        severities: [
            { value: 'low', label: 'Faible' },
            { value: 'medium', label: 'Moyenne' },
            { value: 'high', label: 'Élevée' },
            { value: 'critical', label: 'Critique' }
        ]
    });
});

// GET /admin/audit-acces/recent - Activité récente
router.get('/recent', authenticate, async (req, res) => {
    try {
        const AuditLog = require('../models/AuditLog');
        const logs = await AuditLog.find({ succursale: req.query.succursale })
            .sort({ timestamp: -1 })
            .limit(10)
            .lean();

        res.json({
            success: true,
            data: logs
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: 'Erreur serveur'
        });
    }
});

module.exports = router;