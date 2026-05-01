import 'dart:convert';
import 'dart:io';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:url_launcher/url_launcher.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

Future<void> openJobLink(BuildContext context, String? urlString) async {
  if (urlString == null || urlString.isEmpty) {
    if (context.mounted) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text("No link available")));
    }
    return;
  }
  String url = urlString;
  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    url = 'https://$url';
  }
  final uri = Uri.tryParse(url);
  if (uri == null) {
    if (context.mounted) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text("Invalid link")));
    }
    return;
  }
  debugPrint('Opening URL: $url');
  try {
    bool launched = await launchUrl(uri, mode: LaunchMode.externalApplication);
    if (!launched) {
      launched = await launchUrl(uri);
    }
    if (!launched && context.mounted) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text("Could not open: $url")));
    }
  } catch (e) {
    debugPrint('launchUrl error: $e');
    if (context.mounted) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text("Error: $e")));
    }
  }
}

class MainDashboard extends StatefulWidget {
  const MainDashboard({super.key});

  @override
  State<MainDashboard> createState() => _MainDashboardState();
}

// Separate Favorites Page
class FavoriteJobsScreen extends StatelessWidget {
  final List<dynamic> favoriteJobs;

  const FavoriteJobsScreen({super.key, required this.favoriteJobs});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          "Favorite Jobs",
          style: TextStyle(fontFamily: 'Roboto', color: Colors.deepPurple),
        ),
        backgroundColor: Colors.white,
        elevation: 0,
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
                  child: ListTile(
                    title: Text(
                      job['title'] ?? 'No Title',
                      style: const TextStyle(
                        fontFamily: 'Roboto',
                        fontWeight: FontWeight.w600,
                        color: Colors.deepPurple,
                      ),
                    ),
                    subtitle: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text("Match: ${job['match_percentage']}%"),
                        InkWell(
                          onTap: () => openJobLink(context, job['link']),
                          child: Text(
                            job['link'] ?? 'No link',
                            style: const TextStyle(
                              color: Colors.blue,
                              decoration: TextDecoration.underline,
                            ),
                          ),
                        ),
                      ],
                    ),
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => JobDetailScreen(job: job),
                        ),
                      );
                    },
                  ),
                );
              },
            ),
    );
  }
}

class JobDetailScreen extends StatelessWidget {
  final Map<String, dynamic> job;

  const JobDetailScreen({super.key, required this.job});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Job Details")),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              job['title'] ?? 'No Title',
              style: const TextStyle(
                fontSize: 32,
                fontWeight: FontWeight.bold,
                color: Colors.deepPurple,
                fontFamily: 'Roboto',
              ),
            ),
            const SizedBox(height: 12),
            const Text(
              "Description",
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                fontFamily: 'Roboto',
                color: Colors.deepPurple,
              ),
            ),
            const SizedBox(height: 16),
            Text(
              job['description'] ?? 'No description available',
              style: const TextStyle(fontSize: 15),
            ),
            const SizedBox(height: 20),
            InkWell(
              onTap: () => openJobLink(context, job['link']),
              child: Text(
                job['link'] ?? 'No application link available',
                style: const TextStyle(
                  color: Colors.blue,
                  decoration: TextDecoration.underline,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _MainDashboardState extends State<MainDashboard> {
  File? selectedFile;
  bool isLoading = false;
  List<dynamic> topMatches = [];
  List<dynamic> topDomains = [];
  List<dynamic> favoriteJobs = [];

  bool showAnalysis = false;
  double atsScore = 0;
  List<String> suggestions = [];

  final String baseUrl = "http://10.0.2.2:8000";

  @override
  void initState() {
    super.initState();
    _loadFavorites();
  }

  Future<void> _loadFavorites() async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return;
    final doc = await FirebaseFirestore.instance
        .collection('users')
        .doc(user.uid)
        .get();
    if (doc.exists && doc.data() != null) {
      final data = doc.data()!;
      if (data.containsKey('favorites')) {
        setState(() {
          favoriteJobs = List<dynamic>.from(data['favorites']);
        });
      }
    }
  }

  Future<void> _saveFavorites() async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return;
    await FirebaseFirestore.instance.collection('users').doc(user.uid).set({
      'favorites': favoriteJobs,
    }, SetOptions(merge: true));
  }

  bool isFavorite(Map<String, dynamic> job) {
    return favoriteJobs.any((item) => item['title'] == job['title']);
  }

  void toggleFavorite(Map<String, dynamic> job) {
    setState(() {
      if (isFavorite(job)) {
        favoriteJobs.removeWhere((item) => item['title'] == job['title']);
      } else {
        favoriteJobs.add(job);
      }
    });
    _saveFavorites();
  }

  Future<void> pickResume() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf'],
    );

    if (result != null) {
      setState(() {
        selectedFile = File(result.files.single.path!);
      });
    }
  }

  Future<void> analyzeResume() async {
    if (selectedFile == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Please select a PDF first")),
      );
      return;
    }

    setState(() {
      isLoading = true;
      topMatches = [];
    });

    try {
      var request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/analyze-resume'),
      );

      request.files.add(
        await http.MultipartFile.fromPath('file', selectedFile!.path),
      );

      var streamedResponse = await request.send();
      var response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);

        setState(() {
          topDomains = data['top_domains'] ?? [];
          topMatches = data['top_matches'] ?? [];
          atsScore = (data['ats_score'] ?? 0).toDouble();
          suggestions = List<String>.from(data['suggestions'] ?? []);
        });
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("Server Error: ${response.statusCode}")),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text("Error: $e")));
    }

    setState(() {
      isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        automaticallyImplyLeading: false,
        backgroundColor: Colors.white,
        elevation: 0,
        iconTheme: const IconThemeData(color: Colors.deepPurple),
        actions: [
          PopupMenuButton<String>(
            icon: const Icon(Icons.more_vert),
            onSelected: (value) {
              if (value == 'favorites') {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) =>
                        FavoriteJobsScreen(favoriteJobs: favoriteJobs),
                  ),
                );
              } else if (value == 'logout') {
                Navigator.pop(context);
              }
            },
            itemBuilder: (context) => const [
              PopupMenuItem(
                value: 'favorites',
                child: Text(
                  'Favorite Jobs',
                  style: TextStyle(fontFamily: 'Roboto'),
                ),
              ),
              PopupMenuItem(
                value: 'logout',
                child: Text('Logout', style: TextStyle(fontFamily: 'Roboto')),
              ),
            ],
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const SizedBox(height: 50),
              const Text(
                "welcome to your",
                style: TextStyle(
                  fontSize: 18,
                  fontFamily: 'Roboto',
                  fontWeight: FontWeight.w400,
                  color: Colors.deepPurple,
                ),
              ),
              const Text(
                "Dashboard",
                style: TextStyle(
                  fontSize: 62,
                  fontFamily: 'Roboto',
                  fontWeight: FontWeight.w900,
                  color: Colors.deepPurple,
                ),
              ),
              const SizedBox(height: 20),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  ElevatedButton(
                    onPressed: pickResume,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.deepPurple,
                      padding: const EdgeInsets.symmetric(
                        horizontal: 24,
                        vertical: 16,
                      ),
                    ),
                    child: const Text(
                      "Upload Resume PDF",
                      style: TextStyle(fontSize: 13, color: Colors.white),
                    ),
                  ),
                  const SizedBox(width: 12),
                  ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 36,
                        vertical: 14,
                      ),
                    ),
                    onPressed: isLoading ? null : analyzeResume,
                    child: Text(isLoading ? "Analyzing..." : "Analyze Resume"),
                  ),
                ],
              ),
              const SizedBox(height: 12),
              Text(
                selectedFile != null ? "Resume Selected" : "No file selected",
              ),
              const SizedBox(height: 50),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 2),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    GestureDetector(
                      onTap: () {
                        setState(() => showAnalysis = false);
                      },
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            "Recommended Jobs",
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                              color: showAnalysis
                                  ? Colors.grey
                                  : Colors.deepPurple,
                              fontFamily: 'Roboto',
                            ),
                          ),
                          if (!showAnalysis)
                            Container(
                              margin: const EdgeInsets.only(top: 4),
                              height: 3,
                              width: 160,
                              color: Colors.deepPurple,
                            ),
                        ],
                      ),
                    ),
                    GestureDetector(
                      onTap: () {
                        setState(() => showAnalysis = true);
                      },
                      child: Column(
                        children: [
                          Text(
                            "Resume Analysis",
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                              color: showAnalysis
                                  ? Colors.deepPurple
                                  : Colors.grey,
                              fontFamily: 'Roboto',
                            ),
                          ),
                          if (showAnalysis)
                            Container(
                              margin: const EdgeInsets.only(top: 4),
                              height: 3,
                              width: 140,
                              color: Colors.deepPurple,
                            ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 10),
              Expanded(
                child: showAnalysis
                    ? SingleChildScrollView(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            // 🔥 ATS CARD
                            Container(
                              width: double.maxFinite,
                              padding: const EdgeInsets.all(17),
                              margin: const EdgeInsets.only(
                                bottom: 20,
                                top: 10,
                              ),
                              decoration: BoxDecoration(
                                color: Colors.deepPurple,
                                borderRadius: BorderRadius.circular(16),
                              ),
                              child: Column(
                                children: [
                                  const Text(
                                    "ATS Score",
                                    style: TextStyle(
                                      fontSize: 14,
                                      letterSpacing: 2,
                                      color: Colors.white70,
                                      fontFamily: 'Roboto',
                                    ),
                                  ),

                                  Text(
                                    "${atsScore.toStringAsFixed(1)}%",
                                    style: const TextStyle(
                                      fontSize: 42,
                                      fontWeight: FontWeight(1000),
                                      color: Colors.white,
                                      fontFamily: 'Roboto',
                                    ),
                                  ),
                                ],
                              ),
                            ),

                            // 🔥 Suggestions Title
                            const Text(
                              "Improvement Suggestions",
                              style: TextStyle(
                                fontSize: 22,
                                fontWeight: FontWeight.bold,
                                color: Colors.deepPurple,
                                fontFamily: 'Roboto',
                              ),
                            ),
                            const SizedBox(height: 5),

                            // 🔥 Suggestions List
                            suggestions.isEmpty
                                ? const Text("No suggestions available")
                                : Column(
                                    children: suggestions.map((s) {
                                      return Container(
                                        width: double.infinity,
                                        margin: const EdgeInsets.symmetric(
                                          vertical: 5,
                                        ),

                                        padding: const EdgeInsets.all(12),
                                        decoration: BoxDecoration(
                                          boxShadow: [
                                            BoxShadow(
                                              color: Colors.grey.shade400,
                                              blurRadius: 2,
                                              offset: const Offset(0, 2),
                                            ),
                                          ],

                                          color: Colors.grey.shade100,
                                          borderRadius: BorderRadius.circular(
                                            10,
                                          ),
                                        ),

                                        child: Text(
                                          "• $s",
                                          style: const TextStyle(
                                            fontSize: 15,
                                            fontFamily: 'Roboto',
                                          ),
                                        ),
                                      );
                                    }).toList(),
                                  ),
                          ],
                        ),
                      )
                    : (topMatches.isEmpty
                          ? const Center(child: Text("No recommendations yet"))
                          : ListView.builder(
                              itemCount: topMatches.length,
                              itemBuilder: (context, index) {
                                final job = topMatches[index];

                                return Card(
                                  child: ListTile(
                                    leading: IconButton(
                                      icon: Icon(
                                        isFavorite(job)
                                            ? Icons.favorite
                                            : Icons.favorite_border,
                                        color: Colors.deepPurple,
                                      ),
                                      onPressed: () {
                                        toggleFavorite(job);
                                      },
                                    ),
                                    title: Text(
                                      job['title'] ?? 'No Title',
                                      style: const TextStyle(
                                        fontSize: 14,
                                        color: Colors.deepPurple,
                                        fontFamily: 'Roboto',
                                      ),
                                    ),
                                    trailing: Text(
                                      "${job['match_percentage']}%",
                                    ),
                                    onTap: () {
                                      Navigator.push(
                                        context,
                                        MaterialPageRoute(
                                          builder: (context) =>
                                              JobDetailScreen(job: job),
                                        ),
                                      );
                                    },
                                  ),
                                );
                              },
                            )),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
