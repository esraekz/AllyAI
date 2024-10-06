// main.dart
import 'package:flutter/material.dart';
import 'screens/home_page.dart';  // Import HomePage

void main() {
  runApp(RestaurantChatApp());
}

class RestaurantChatApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Restaurant Chat Assistant',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: HomePage(),  // Set HomePage as the home
    );
  }
}
