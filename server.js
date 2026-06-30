const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Connexion MongoDB
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/bank_audit', {
    useNewUrlParser: true,
    useUnifiedTopology: true
})
.then(() => console.log('✅ Connecté à MongoDB'))
.catch(err => console.error('❌ Erreur MongoDB:', err));

// Routes
app.use('/admin/audit-acces', require('./routes/audit'));

// Route de test
app.get('/health', (req, res) => {
    res.json({
        status: 'OK',
        timestamp: new Date(),
        service: 'Bank Audit System'
    });
});

// Middleware d'erreur
app.use((err, req, res, next) => {
    console.error('❌ Erreur:', err);
    res.status(500).json({
        success: false,
        message: 'Erreur interne du serveur',
        error: process.env.NODE_ENV === 'development' ? err.message : undefined
    });
});

// Démarrer le serveur
app.listen(PORT, () => {
    console.log(`🚀 Serveur audit démarré sur http://localhost:${PORT}`);
    console.log(`📊 Audit disponible sur: http://localhost:${PORT}/admin/audit-acces`);
});