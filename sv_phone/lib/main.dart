import 'dart:async';
import 'package:flutter/material.dart';
import 'package:sv_phone/pages/home.dart';
import 'logic/bluetooth.dart';

void main() {
  runApp(const MyApp());
}
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: HomePage(),
    );

  }
}