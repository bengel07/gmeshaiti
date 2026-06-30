const jwt = require('jsonwebtoken');

// Middleware pour vérifier l'authentification
exports.authenticate = (req, res, next) => {
    try {
        const token = req.headers.authorization?.split(' ')[1];

        if (!token) {
            return res.status(401).json({
                success: false,
                message: 'Accès non autorisé. Token manquant.'
            });
        }

        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        req.user = decoded;
        next();
    } catch (error) {
        return res.status(401).json({
            success: false,
            message: 'Token invalide ou expiré'
        });
    }
};

// Middleware pour vérifier les rôles
exports.authorize = (...roles) => {
    return (req, res, next) => {
        if (!req.user || !roles.includes(req.user.role)) {
            return res.status(403).json({
                success: false,
                message: 'Accès interdit. Permissions insuffisantes.'
            });
        }
        next();
    };
};

// Middleware de logging d'audit
exports.auditMiddleware = async (req, res, next) => {
    const startTime = Date.now();

    // Sauvegarder la fonction originale send
    const originalSend = res.send;

    res.send = function(data) {
        const duration = Date.now() - startTime;

        // Journaliser après l'envoi de la réponse
        setTimeout(async () => {
            try {
                const AuditLog = require('../models/AuditLog');

                const auditData = {
                    userId: req.user?.id,
                    username: req.user?.username || 'anonymous',
                    userRole: req.user?.role,
                    eventType: getEventType(req),
                    description: `${req.method} ${req.originalUrl} - ${res.statusCode}`,
                    ipAddress: req.ip || req.connection.remoteAddress,
                    userAgent: req.get('User-Agent'),
                    status: res.statusCode >= 400 ? 'failed' : 'success',
                    severity: res.statusCode >= 500 ? 'high' : 'medium',
                    succursale: req.query.succursale || req.body.succursale || 'unknown',
                    details: {
                        method: req.method,
                        url: req.originalUrl,
                        statusCode: res.statusCode,
                        duration: `${duration}ms`,
                        query: req.query,
                        body: sanitizeBody(req.body)
                    }
                };

                await AuditLog.create(auditData);
            } catch (error) {
                console.error('Erreur logging audit:', error);
            }
        }, 0);

        // Appeler la fonction originale
        return originalSend.call(this, data);
    };

    next();
};

// Helper functions
function getEventType(req) {
    if (req.originalUrl.includes('/login')) return 'connexion';
    if (req.originalUrl.includes('/logout')) return 'deconnexion';
    if (req.method === 'POST') return 'creation';
    if (req.method === 'PUT' || req.method === 'PATCH') return 'modification';
    if (req.method === 'DELETE') return 'suppression';
    if (req.originalUrl.includes('/permissions')) return 'permission';
    return 'consultation';
}

function sanitizeBody(body) {
    const sanitized = { ...body };
    // Supprimer les données sensibles
    delete sanitized.password;
    delete sanitized.token;
    delete sanitized.creditCard;
    delete sanitized.cvv;
    return sanitized;
}