import 'package:flutter/foundation.dart';
import 'package:firebase_storage/firebase_storage.dart';
import 'package:hive/hive.dart';
import 'dart:typed_data';
import '../models/voice_note.dart';

/// Storage service for voice notes and location-tagged data
/// Implements offline-first storage with Cloud Storage sync
class StorageService extends ChangeNotifier {
  final FirebaseStorage _storage = FirebaseStorage.instance;
  late Box _offlineStorageBox;
  late Box _pendingSyncBox;
  bool _isInitialized = false;
  bool _isSyncing = false;
  int _pendingUploads = 0;

  bool get isInitialized => _isInitialized;
  bool get isSyncing => _isSyncing;
  int get pendingUploads => _pendingUploads;

  StorageService() {
    _initializeService();
  }

  Future<void> _initializeService() async {
    try {
      _offlineStorageBox = await Hive.openBox('offline_storage');
      _pendingSyncBox = await Hive.openBox('pending_sync');
      _pendingUploads = _pendingSyncBox.length;
      _isInitialized = true;
      notifyListeners();
      
      // Auto-sync if online
      _syncPendingUploads();
    } catch (e) {
      debugPrint('Storage service initialization error: $e');
    }
  }

  /// Upload voice note with location data
  /// Stores offline-first, syncs when connection available
  Future<String?> uploadVoiceNote({
    required Uint8List audioData,
    required String userId,
    required double latitude,
    required double longitude,
    String? patientId,
    Map<String, dynamic>? metadata,
  }) async {
    try {
      final voiceNote = VoiceNote(
        id: DateTime.now().toUtc().millisecondsSinceEpoch.toString(),
        userId: userId,
        audioData: audioData,
        latitude: latitude,
        longitude: longitude,
        patientId: patientId,
        metadata: metadata ?? {},
        timestamp: DateTime.now().toUtc(), // Use UTC for consistency across regions
        isSynced: false,
      );

      // Save to offline storage first
      await _saveOffline(voiceNote);
      
      // Try to upload immediately if online
      try {
        final uploadedUrl = await _uploadToCloud(voiceNote);
        if (uploadedUrl != null) {
          // Mark as synced
          await _markAsSynced(voiceNote.id);
          voiceNote.isSynced = true;
          voiceNote.cloudUrl = uploadedUrl;
        }
      } catch (e) {
        debugPrint('Cloud upload failed, will retry when online: $e');
        // Add to pending sync queue
        await _addToPendingSync(voiceNote);
        _pendingUploads++;
        notifyListeners();
      }

      return voiceNote.id;
    } catch (e) {
      debugPrint('Error saving voice note: $e');
      return null;
    }
  }

  /// Save voice note to offline storage
  Future<void> _saveOffline(VoiceNote voiceNote) async {
    await _offlineStorageBox.put(voiceNote.id, voiceNote.toJson());
  }

  /// Upload to Firebase Cloud Storage
  Future<String?> _uploadToCloud(VoiceNote voiceNote) async {
    try {
      final path = 'voice_notes/${voiceNote.userId}/${voiceNote.id}.m4a';
      final ref = _storage.ref().child(path);
      
      // Set metadata including location
      final metadata = SettableMetadata(
        contentType: 'audio/m4a',
        customMetadata: {
          'userId': voiceNote.userId,
          'latitude': voiceNote.latitude.toString(),
          'longitude': voiceNote.longitude.toString(),
          'timestamp': voiceNote.timestamp.toIso8601String(),
          if (voiceNote.patientId != null) 'patientId': voiceNote.patientId!,
          ...voiceNote.metadata.map((key, value) => MapEntry(key, value.toString())),
        },
      );

      // Upload
      final uploadTask = ref.putData(voiceNote.audioData, metadata);
      final snapshot = await uploadTask;
      
      // Get download URL
      final downloadUrl = await snapshot.ref.getDownloadURL();
      return downloadUrl;
    } catch (e) {
      debugPrint('Cloud upload error: $e');
      rethrow;
    }
  }

  /// Add to pending sync queue
  Future<void> _addToPendingSync(VoiceNote voiceNote) async {
    await _pendingSyncBox.put(voiceNote.id, voiceNote.toJson());
  }

  /// Mark voice note as synced
  Future<void> _markAsSynced(String id) async {
    final voiceNoteJson = _offlineStorageBox.get(id);
    if (voiceNoteJson != null) {
      final updated = Map<String, dynamic>.from(voiceNoteJson as Map);
      updated['isSynced'] = true;
      await _offlineStorageBox.put(id, updated);
    }
    
    // Remove from pending sync
    await _pendingSyncBox.delete(id);
    _pendingUploads = _pendingSyncBox.length;
    notifyListeners();
  }

  /// Sync all pending uploads
  Future<void> _syncPendingUploads() async {
    if (_isSyncing || _pendingSyncBox.isEmpty) return;

    _isSyncing = true;
    notifyListeners();

    try {
      final keys = _pendingSyncBox.keys.toList();
      for (final key in keys) {
        try {
          final voiceNoteJson = _pendingSyncBox.get(key);
          if (voiceNoteJson != null) {
            final voiceNote = VoiceNote.fromJson(
              Map<String, dynamic>.from(voiceNoteJson as Map),
            );
            
            final uploadedUrl = await _uploadToCloud(voiceNote);
            if (uploadedUrl != null) {
              await _markAsSynced(voiceNote.id);
            }
          }
        } catch (e) {
          debugPrint('Error syncing voice note $key: $e');
          // Continue with next item
        }
      }
    } finally {
      _isSyncing = false;
      notifyListeners();
    }
  }

  /// Manually trigger sync
  Future<void> syncNow() async {
    await _syncPendingUploads();
  }

  /// Get all voice notes (offline storage)
  List<VoiceNote> getAllVoiceNotes() {
    try {
      return _offlineStorageBox.values
          .map((e) => VoiceNote.fromJson(Map<String, dynamic>.from(e as Map)))
          .toList()
        ..sort((a, b) => b.timestamp.compareTo(a.timestamp));
    } catch (e) {
      debugPrint('Error getting voice notes: $e');
      return [];
    }
  }

  /// Get voice note by ID
  VoiceNote? getVoiceNote(String id) {
    try {
      final voiceNoteJson = _offlineStorageBox.get(id);
      if (voiceNoteJson != null) {
        return VoiceNote.fromJson(Map<String, dynamic>.from(voiceNoteJson as Map));
      }
      return null;
    } catch (e) {
      debugPrint('Error getting voice note $id: $e');
      return null;
    }
  }

  /// Delete voice note
  Future<bool> deleteVoiceNote(String id) async {
    try {
      // Delete from cloud if synced
      final voiceNote = getVoiceNote(id);
      if (voiceNote?.isSynced == true && voiceNote?.cloudUrl != null) {
        try {
          final ref = _storage.refFromURL(voiceNote!.cloudUrl!);
          await ref.delete();
        } catch (e) {
          debugPrint('Error deleting from cloud: $e');
        }
      }

      // Delete from offline storage
      await _offlineStorageBox.delete(id);
      await _pendingSyncBox.delete(id);
      _pendingUploads = _pendingSyncBox.length;
      notifyListeners();
      
      return true;
    } catch (e) {
      debugPrint('Error deleting voice note: $e');
      return false;
    }
  }
}
