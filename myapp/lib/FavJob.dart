import 'package:flutter/material.dart';

class FavoriteJobsScreen extends StatelessWidget {
  final List<dynamic> favoriteJobs;

  const FavoriteJobsScreen({super.key, required this.favoriteJobs});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        iconTheme: const IconThemeData(color: Colors.deepPurple),
        title: const Text(
          "Favorite Jobs",
          style: TextStyle(
            fontFamily: 'Roboto',
            fontWeight: FontWeight.bold,
            color: Colors.deepPurple,
          ),
        ),
      ),
      body: favoriteJobs.isEmpty
          ? const Center(
              child: Text(
                "No favorite jobs yet",
                style: TextStyle(
                  fontFamily: 'Roboto',
                  fontSize: 16,
                  color: Colors.deepPurple,
                ),
              ),
            )
          : ListView.builder(
              itemCount: favoriteJobs.length,
              itemBuilder: (context, index) {
                final job = favoriteJobs[index];

                return Card(
                  margin: const EdgeInsets.symmetric(
                    horizontal: 16,
                    vertical: 8,
                  ),
                  child: ListTile(
                    title: Text(
                      job['title'] ?? 'No Title',
                      style: const TextStyle(
                        fontFamily: 'Roboto',
                        fontWeight: FontWeight.w600,
                        color: Colors.deepPurple,
                      ),
                    ),
                    subtitle: Text("Match: ${job['match_percentage']}%"),
                  ),
                );
              },
            ),
    );
  }
}
