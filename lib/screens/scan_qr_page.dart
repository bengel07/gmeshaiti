class ScanQRPage extends StatelessWidget {

  void loginWithQR(String code) async {
    var res = await http.get(
      Uri.parse("https://ton-api.com/login-qr/$code"),
    );

    print(res.body);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Scanner QR")),
      body: MobileScanner(
        onDetect: (barcode, args) {
          final String? code = barcode.rawValue;

          if (code != null) {
            loginWithQR(code);
          }
        },
      ),
    );
  }
}