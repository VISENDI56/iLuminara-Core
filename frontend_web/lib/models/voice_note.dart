import 'dart:typed_data';

/// Voice note model with location tagging
class VoiceNote {
  final String id;
  final String userId;
  final Uint8List audioData;
  final double latitude;
  final double longitude;
  final String? patientId;
  final Map<String, dynamic> metadata;
  final DateTime timestamp;
  bool isSynced;
  String? cloudUrl;

  VoiceNote({
    required this.id,
    required this.userId,
    required this.audioData,
    required this.latitude,
    required this.longitude,
    this.patientId,
    required this.metadata,
    required this.timestamp,
    this.isSynced = false,
    this.cloudUrl,
  });

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'userId': userId,
      'audioData': audioData,
      'latitude': latitude,
      'longitude': longitude,
      'patientId': patientId,
      'metadata': metadata,
      'timestamp': timestamp.toIso8601String(),
      'isSynced': isSynced,
      'cloudUrl': cloudUrl,
    };
  }

  factory VoiceNote.fromJson(Map<String, dynamic> json) {
    return VoiceNote(
      id: json['id'] as String,
      userId: json['userId'] as String,
      audioData: json['audioData'] as Uint8List,
      latitude: (json['latitude'] as num).toDouble(),
      longitude: (json['longitude'] as num).toDouble(),
      patientId: json['patientId'] as String?,
      metadata: Map<String, dynamic>.from(json['metadata'] as Map),
      timestamp: DateTime.parse(json['timestamp'] as String),
      isSynced: json['isSynced'] as bool? ?? false,
      cloudUrl: json['cloudUrl'] as String?,
    );
  }

  /// Get location as formatted string
  String get locationString {
    return '${latitude.toStringAsFixed(6)}, ${longitude.toStringAsFixed(6)}';
  }

  /// Get relative time description
  String get relativeTime {
    final now = DateTime.now();
    final difference = now.difference(timestamp);

    if (difference.inMinutes < 1) {
      return 'Just now';
    } else if (difference.inMinutes < 60) {
      return '${difference.inMinutes} minutes ago';
    } else if (difference.inHours < 24) {
      return '${difference.inHours} hours ago';
    } else if (difference.inDays < 7) {
      return '${difference.inDays} days ago';
    } else {
      return '${(difference.inDays / 7).floor()} weeks ago';
    }
  }
}
