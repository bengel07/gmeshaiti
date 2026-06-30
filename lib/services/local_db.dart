Future saveOffline(data) async {
  await localDB.insert("pointages", {
    "user_id": data["user_id"],
    "time": DateTime.now().toString(),
    "lat": data["lat"],
    "lon": data["lon"],
    "synced": 0
  });
}
void syncData() async {
  var data = await localDB.getUnsynced();

  for (var item in data) {
    var res = await sendToAPI(item);

    if (res.success) {
      await localDB.markSynced(item["id"]);
    }
  }
}