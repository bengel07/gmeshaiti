@override
void initState() {
  super.initState();

  startTracking(sendToAPI);
}

void sendToAPI(data) {
  print(data);

  // appeler FastAPI ici
}