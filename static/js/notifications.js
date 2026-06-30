<!-- static/js/notifications.js -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.css">

<script>
    toastr.options = {
        "closeButton": true,
        "progressBar": true,
        "positionClass": "toast-top-right",
        "timeOut": "10000",
    };

    // Dans votre template, modifiez la fonction checkNotifications
    function checkNotifications() {
        fetch('/api/notifications/unread')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                return response.json();
            })
            .then(notifications => {
                if (notifications && notifications.length > 0) {
                    updateBadge(notifications.length);

                    notifications.forEach(notif => {
                        let icon = '🔔';
                        if (notif.level === 'error') icon = '🚨';
                        else if (notif.level === 'warning') icon = '⚠️';
                        else if (notif.level === 'success') icon = '✅';

                        toastr[notif.level || 'info'](
                            `${notif.message}<br><small>${notif.time || ''}</small>`,
                            `${icon} Notification Admin`
                        );
                    });
                } else {
                    updateBadge(0);
                }
            })
            .catch(error => {
                console.error('Erreur checkNotifications:', error);
                // Ne pas afficher d'alerte, juste logger
                updateBadge(0);
            });
    }

    setInterval(checkNotifications, 15000);
</script>