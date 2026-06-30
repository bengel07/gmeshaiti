import 'dart:async';
import 'package:geolocator/geolocator.dart';

Timer? trackingTimer;
int interval = 10;
Position? lastPosition;

void startTracking(Function sendToAPI) {
  trackingTimer?.cancel();

  trackingTimer = Timer.periodic(Duration(seconds: interval), (timer) async {

    Position pos = await Geolocator.getCurrentPosition();

    bool moving = false;

    if (lastPosition != null) {
      double distance = Geolocator.distanceBetween(
        lastPosition!.latitude,
        lastPosition!.longitude,
        pos.latitude,
        pos.longitude,
      );

      moving = distance > 5; // 5 mètres
    }

    lastPosition = pos;

    // 🔥 ADAPTATION INTERVAL
    if (moving) {
      interval = 5;
    } else {
      interval = 60;
    }

    // 🔥 RESTART TIMER avec nouvel interval
    startTracking(sendToAPI);

    // 📡 envoyer au backend
    sendToAPI({
      "lat": pos.latitude,
      "lon": pos.longitude,
    });

  });
}