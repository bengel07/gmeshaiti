import 'package:nfc_manager/nfc_manager.dart';

void startNFC() {
  NfcManager.instance.startSession(
    onDiscovered: (NfcTag tag) async {
      var uid = tag.data["nfca"]["identifier"].toString();

      loginWithNFC(uid);
    },
  );
}

final auth = LocalAuthentication();

bool authenticated = await auth.authenticate(
  localizedReason: 'Scanner empreinte',
);

if (authenticated) {
  // ouvrir QR ou NFC
}