import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:flutter_bluetooth_serial/flutter_bluetooth_serial.dart';
import 'package:permission_handler/permission_handler.dart';

var address;

Future<List<BluetoothDiscoveryResult>> discoverDevices() async {
  if (await Permission.bluetoothScan.request().isGranted &&
      await Permission.bluetoothConnect.request().isGranted) {
    // Permissions granted → proceed with discovery/connection
  }
  List<BluetoothDiscoveryResult> results = [];
  // Start discovery
  await for (var result
  in FlutterBluetoothSerial.instance.startDiscovery()) {
    results.add(result);
  }
  return results;
}

Future<BluetoothConnection> connectToDevice(String address) async {
  // Opens an RFCOMM connection to the given MAC address
  final connection =
  await BluetoothConnection.toAddress(address);
  print('Connected to $address');
  return connection;
}

// Sending & receiving a single message
void communicate(BluetoothConnection conn) {
  const msg = 'Hello, Pi!';
  conn.output.add(utf8.encode(msg + '\n'));
  conn.output.allSent.then((_) => print('Sent: $msg'));

  conn.input!.listen((data) {
    final response = utf8.decode(data);
    print('Received: $response');
    conn.finish(); // close socket after one message
  });
}



