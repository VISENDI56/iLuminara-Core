import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'dart:typed_data';
import '../services/storage_service.dart';
import '../services/auth_service.dart';

/// Voice recorder widget with compassionate UI
class VoiceRecorderWidget extends StatefulWidget {
  const VoiceRecorderWidget({super.key});

  @override
  State<VoiceRecorderWidget> createState() => _VoiceRecorderWidgetState();
}

class _VoiceRecorderWidgetState extends State<VoiceRecorderWidget> {
  bool _isRecording = false;
  bool _isProcessing = false;
  final _patientIdController = TextEditingController();
  final _notesController = TextEditingController();

  @override
  void dispose() {
    _patientIdController.dispose();
    _notesController.dispose();
    super.dispose();
  }

  Future<void> _toggleRecording() async {
    if (_isRecording) {
      // Stop recording
      setState(() {
        _isProcessing = true;
      });

      // Simulate recording stop and save
      // In a real implementation, use the record package
      await _saveRecording();

      setState(() {
        _isRecording = false;
        _isProcessing = false;
      });
    } else {
      // Start recording
      // In a real implementation, request microphone permissions
      // and start recording using the record package
      setState(() {
        _isRecording = true;
      });
    }
  }

  Future<void> _saveRecording() async {
    try {
      final storageService = context.read<StorageService>();
      final authService = context.read<AuthService>();

      // Simulate audio data (in real app, get from recorder)
      final audioData = Uint8List.fromList([1, 2, 3, 4, 5]);
      
      // Simulate GPS coordinates (in real app, use geolocator)
      const latitude = -1.2921;  // Nairobi coordinates as example
      const longitude = 36.8219;

      final metadata = {
        'notes': _notesController.text.trim(),
        if (_patientIdController.text.trim().isNotEmpty)
          'patient_id': _patientIdController.text.trim(),
      };

      await storageService.uploadVoiceNote(
        audioData: audioData,
        userId: authService.currentUser!.uid,
        latitude: latitude,
        longitude: longitude,
        patientId: _patientIdController.text.trim().isEmpty 
            ? null 
            : _patientIdController.text.trim(),
        metadata: metadata,
      );

      // Clear form
      _patientIdController.clear();
      _notesController.clear();

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: const Row(
              children: [
                Icon(Icons.check_circle_outline, color: Colors.white),
                SizedBox(width: 8),
                Text('Voice note saved successfully'),
              ],
            ),
            backgroundColor: Colors.green.shade600,
            behavior: SnackBarBehavior.floating,
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error saving recording: $e'),
            backgroundColor: Colors.red.shade600,
            behavior: SnackBarBehavior.floating,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Patient ID field
            TextField(
              controller: _patientIdController,
              decoration: const InputDecoration(
                labelText: 'Patient ID (Optional)',
                hintText: 'Enter patient identifier',
                prefixIcon: Icon(Icons.badge_outlined),
              ),
              enabled: !_isRecording && !_isProcessing,
            ),
            const SizedBox(height: 16),

            // Notes field
            TextField(
              controller: _notesController,
              decoration: const InputDecoration(
                labelText: 'Notes (Optional)',
                hintText: 'Add any additional notes',
                prefixIcon: Icon(Icons.notes_outlined),
              ),
              maxLines: 3,
              enabled: !_isRecording && !_isProcessing,
            ),
            const SizedBox(height: 32),

            // Recording status
            if (_isRecording)
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.red.shade50,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.red.shade200),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    _PulsingDot(),
                    const SizedBox(width: 12),
                    Text(
                      'Recording in progress...',
                      style: TextStyle(
                        color: Colors.red.shade700,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ],
                ),
              ),

            if (_isRecording) const SizedBox(height: 24),

            // Record button
            ElevatedButton.icon(
              onPressed: _isProcessing ? null : _toggleRecording,
              style: ElevatedButton.styleFrom(
                backgroundColor: _isRecording
                    ? Colors.red.shade600
                    : Theme.of(context).colorScheme.primary,
                foregroundColor: Colors.white,
                minimumSize: const Size.fromHeight(56),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              icon: _isProcessing
                  ? const SizedBox(
                      width: 24,
                      height: 24,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                      ),
                    )
                  : Icon(
                      _isRecording ? Icons.stop_rounded : Icons.mic_rounded,
                      size: 28,
                    ),
              label: Text(
                _isProcessing
                    ? 'Saving...'
                    : _isRecording
                        ? 'Stop Recording'
                        : 'Start Recording',
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),

            // Location indicator
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  Icons.location_on_outlined,
                  size: 16,
                  color: Colors.grey[600],
                ),
                const SizedBox(width: 4),
                Text(
                  'Location will be captured automatically',
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.grey[600],
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

/// Pulsing dot animation for recording indicator
class _PulsingDot extends StatefulWidget {
  @override
  State<_PulsingDot> createState() => _PulsingDotState();
}

class _PulsingDotState extends State<_PulsingDot> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 1000),
      vsync: this,
    )..repeat(reverse: true);
    _animation = Tween<double>(begin: 0.5, end: 1.0).animate(_controller);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FadeTransition(
      opacity: _animation,
      child: Container(
        width: 12,
        height: 12,
        decoration: BoxDecoration(
          color: Colors.red.shade600,
          shape: BoxShape.circle,
        ),
      ),
    );
  }
}
