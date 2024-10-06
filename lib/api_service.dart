import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  final String baseUrl = 'http://127.0.0.1:8000';  // Replace with your FastAPI URL if deployed

  Future<List<String>> getRestaurantSuggestions(String query) async {
    final response = await http.post(
      Uri.parse('$baseUrl/suggest_restaurant'),
      headers: {
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'query': query,
      }),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return List<String>.from(data['suggestions']);
    } else {
      throw Exception('Failed to load suggestions');
    }
  }
}
