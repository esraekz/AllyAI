import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  final String baseUrl = 'https://allyai-1.onrender.com';  // Replace with your FastAPI URL

  // Method to get restaurant suggestions
  Future<List<String>> getRestaurantSuggestions(String query) async {
    try {
      print('Sending request to API with query: $query');
      final response = await http.post(
        Uri.parse('$baseUrl/suggest_restaurant'),
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode({'query': query}),
      );

      print('Response status code: ${response.statusCode}');
      print('Response body: ${response.body}');

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);

        // Check if the suggestions exist and are not null
        if (data != null && data['suggestions'] != null) {
          return List<String>.from(data['suggestions']);
        } else {
          print('No suggestions found in the response.');
          return ["No suggestions found"];
        }
      } else {
        print('Error: Received ${response.statusCode} status code from the API.');
        throw Exception('Failed to load suggestions');
      }
    } catch (e) {
      print('Error occurred while fetching suggestions: $e');
      throw Exception('Failed to load suggestions: $e');
    }
  }
}
