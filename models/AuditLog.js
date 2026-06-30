const mongoose = require('mongoose');

const auditLogSchema = new mongoose.Schema({
    timestamp: {
        type: Date,
        default: Date.now,
        required: true
    },
    userId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User'
    },
    username: {
        type: String,
        required: true
    },
    userRole: {
        type: String,
        enum: ['admin', 'directeur', 'gestionnaire', 'caissier', 'conseiller', 'externe']
    },
    eventType: {
        type: String,
        required: true,
        enum: ['connexion', 'deconnexion', 'creation', 'modification', 'suppression', 'permission', 'transaction', 'consultation']
    },
    description: {
        type: String,
        required: true
    },
    ipAddress: {
        type: String,
        required: true
    },
    userAgent: String,
    status: {
        type: String,
        enum: ['success', 'failed', 'warning'],
        default: 'success'
    },
    severity: {
        type: String,
        enum: ['low', 'medium', 'high', 'critical'],
        default: 'medium'
    },
    succursale: {
        type: String,
        required: true
    },
    details: {
        type: mongoose.Schema.Types.Mixed
    },
    metadata: {
        type: mongoose.Schema.Types.Mixed
    }
}, {
    timestamps: true
});

// Index pour les recherches rapides
auditLogSchema.index({ timestamp: -1 });
auditLogSchema.index({ succursale: 1, timestamp: -1 });
auditLogSchema.index({ eventType: 1, timestamp: -1 });
auditLogSchema.index({ username: 1, timestamp: -1 });

module.exports = mongoose.model('AuditLog', auditLogSchema);