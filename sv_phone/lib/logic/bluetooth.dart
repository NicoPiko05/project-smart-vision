import 'dart:async';
import 'dart:io';
import 'dart:developer' as dev;
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:permission_handler/permission_handler.dart';


class BluetoothManager {
  final List<ScanResult> foundDevices = [];

  Future<void> initializeBluetooth() async {
    dev.log('BluetoothManager loaded');
    // Request permissions
    if (await Permission.bluetoothScan.request().isGranted &&
        await Permission.bluetoothConnect.request().isGranted &&
        await Permission.location.request().isGranted) {
      dev.log('Bluetooth permissions granted');
    } else {
      dev.log('Bluetooth permissions denied');
      return;
    }
      // Permissions granted, proceed with initialization
    // if your terminal doesn't support color you'll see annoying logs like `\x1B[1;35m`
    //FlutterBluePlus.setLogLevel(LogLevel.verbose, color: false);

    // first, check if bluetooth is supported by your hardware
    // Note: The platform is initialized on the first call to any FlutterBluePlus method.
    if (await FlutterBluePlus.isSupported == false) {
      dev.log("Bluetooth not supported by this device");
      return;
    }


    // handle bluetooth on & off
    // note: for iOS the initial state is typically BluetoothAdapterState.unknown
    // note: if you have permissions issues you will get stuck at BluetoothAdapterState.unauthorized
    var subscription = FlutterBluePlus.adapterState.listen((BluetoothAdapterState state) {
      dev.log(state as String);
      if (state == BluetoothAdapterState.on) {
        scanForDevices();
      }
    });

    // turn on bluetooth ourself if we can
    // for iOS, the user controls bluetooth enable/disable
    if (!kIsWeb && Platform.isAndroid) {
      await FlutterBluePlus.turnOn();
    }

    // cancel to prevent duplicate listeners
    subscription.cancel();
  }

  Future<void> scanForDevices() async {
    Set<ScanResult> foundDevices = {};
    dev.log('Scanning for devices');
    // listen to scan results
    // Note: `onScanResults` clears the results between scans. You should use
    //  `scanResults` if you want the current scan results *or* the results from the previous scan.
    var subscription = FlutterBluePlus.onScanResults.listen((results) {
      for (var result in results) {
        String deviceId = result.device.remoteId.toString();
        String deviceName = result.advertisementData.advName ?? "Unknown";

        if (deviceName != "Unknown" && !foundDevices.contains(deviceId)) {
          foundDevices.add(result); // Add to the set to avoid duplicates
          dev.log('Device found: $deviceName ($deviceId)');
        }
      }
    }, onError: (e) => dev.log(e));

    // cleanup: cancel subscription when scanning stops
    FlutterBluePlus.cancelWhenScanComplete(subscription);

    // Wait for Bluetooth enabled & permission granted
    // In your real app you should use `FlutterBluePlus.adapterState.listen` to handle all states
    await FlutterBluePlus.adapterState.where((val) => val == BluetoothAdapterState.on).first;

    // Start scanning w/ timeout
    // Optional: use `stopScan()` as an alternative to timeout
    dev.log('Starting scan');
    await FlutterBluePlus.startScan(
      //withServices: [Guid("180D")], // match any of the specified services
      //withNames: ["Bluno"], // *or* any of the specified names
      timeout: const Duration(seconds: 15),
      androidScanMode: AndroidScanMode.balanced,
    );

    // wait for scanning to stop
    await FlutterBluePlus.isScanning.where((val) => val == false).first;
    for (var device in foundDevices) {
      dev.log('${device.device.remoteId}: "${device.advertisementData.advName}"');
    }
  }
}
