// main.dart
import 'package:flutter/material.dart';
import 'screens/home_page.dart'; // Import the HomePage widget from home_page.dart

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Restaurant Chat Assistant',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const HomePage(), // Set HomePage as the initial screen
    );
  }
}
