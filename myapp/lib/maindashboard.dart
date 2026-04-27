import 'dart:convert';
import 'dart:io';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:url_launcher/url_launcher.dart';

class MainDashboard extends StatefulWidget {
  const MainDashboard({super.key});

  @override
  State<MainDashboard> createState() => _MainDashboardState();
}

class JobDetailScreen extends StatelessWidget {
  final Map<String, dynamic> job;

  const JobDetailScreen({super.key, required this.job});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Job Details")),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              "${job['title']}" ?? 'No Title',
              style: TextStyle(
                fontSize: 32,
                fontWeight: FontWeight.bold,
                color: Colors.deepPurple,
                fontFamily: 'Roboto',
              ),
            ),

            const SizedBox(height: 12),
            Text(
              "Description",
              style: const TextStyle(
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
              onTap: () async {
                final urlString = job['link'];
                if (urlString != null && urlString.isNotEmpty) {
                  final uri = Uri.parse(urlString);
                  if (await canLaunchUrl(uri)) {
                    await launchUrl(uri, mode: LaunchMode.externalApplication);
                  }
                }
              },
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

  // IMPORTANT:
  // For Android emulator use: http://10.0.2.2:8000
  // For real mobile use your PC IP like: http://192.168.1.5:8000
  final String baseUrl = "http://10.0.2.2:8000";

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
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const SizedBox(height: 100),
              Text(
                "welcome to your",
                style: TextStyle(
                  fontSize: 18,
                  fontFamily: 'Roboto',
                  fontWeight: FontWeight.w400,

                  color: Colors.deepPurple,
                ),
              ),
              Text(
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
              const SizedBox(height: 30),
              Align(
                alignment: Alignment.centerLeft,

                child: Text(
                  "Recommended Jobs",
                  textAlign: TextAlign.left,
                  style: TextStyle(
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                    color: Colors.deepPurple,
                    fontFamily: 'Roboto',
                  ),
                ),
              ),
              const SizedBox(height: 10),
              Expanded(
                child: topMatches.isEmpty
                    ? const Center(child: Text("No recommendations yet"))
                    : ListView.builder(
                        itemCount: topMatches.length,
                        itemBuilder: (context, index) {
                          final job = topMatches[index];

                          return Card(
                            child: ListTile(
                              title: Text(
                                job['title'] ?? 'No Title',
                                style: TextStyle(
                                  fontSize: 14,

                                  color: Colors.deepPurple,
                                  fontFamily: 'Roboto',
                                ),
                              ),
                              trailing: Text("${job['match_percentage']}%"),
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
                      ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
