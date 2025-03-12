import 'package:flutter/material.dart';
import 'dart:developer' as dev;
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import '../logic/bluetooth.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final BluetoothManager bluetoothManager = BluetoothManager();
  List<ScanResult> foundDevices = [];

  @override
  void initState() {
    super.initState();
    bluetoothManager.initializeBluetooth();
    dev.log('Bluetooth initialized');
  }

  void _startScanning() async {
    await bluetoothManager.scanForDevices();
    setState(() {
      foundDevices = List.from(bluetoothManager.foundDevices);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Devices',
          style: TextStyle(color: Colors.white),
        ),
        backgroundColor: Colors.black,
        centerTitle: true,
      ),
      body: ListView.builder(
        itemCount: foundDevices.length,
        itemBuilder: (context, index) {
          final device = foundDevices[index];
          return ListTile(
            title: Text(device.advertisementData.advName.isNotEmpty
                ? device.advertisementData.advName
                : "Unknown Device"),
            subtitle: Text(device.device.remoteId.toString()),
          );
        },
      ),
      floatingActionButton: Column(
        mainAxisAlignment: MainAxisAlignment.end,
        children: [
          FloatingActionButton(
            onPressed: _startScanning,
            child: const Icon(Icons.bluetooth_searching),
          ),
        ],
      ),
    );
  }
}
