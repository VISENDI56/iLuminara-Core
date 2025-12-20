import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/storage_service.dart';
import '../models/voice_note.dart';

/// List of voice notes with compassionate UI
class VoiceNotesList extends StatelessWidget {
  const VoiceNotesList({super.key});

  @override
  Widget build(BuildContext context) {
    final storageService = context.watch<StorageService>();
    final voiceNotes = storageService.getAllVoiceNotes();

    if (voiceNotes.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.mic_none_rounded,
              size: 80,
              color: Colors.grey[300],
            ),
            const SizedBox(height: 16),
            Text(
              'No voice notes yet',
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                color: Colors.grey[600],
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Start recording to create your first note',
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                color: Colors.grey[500],
              ),
            ),
          ],
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: () async {
        await storageService.syncNow();
      },
      child: ListView.builder(
        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 8),
        itemCount: voiceNotes.length,
        itemBuilder: (context, index) {
          final voiceNote = voiceNotes[index];
          return _VoiceNoteCard(voiceNote: voiceNote);
        },
      ),
    );
  }
}

/// Voice note card widget
class _VoiceNoteCard extends StatelessWidget {
  final VoiceNote voiceNote;

  const _VoiceNoteCard({required this.voiceNote});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: InkWell(
        onTap: () => _showVoiceNoteDetails(context),
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header with sync status
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: Theme.of(context).colorScheme.primary.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Icon(
                      Icons.mic_rounded,
                      color: Theme.of(context).colorScheme.primary,
                      size: 20,
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          voiceNote.relativeTime,
                          style: const TextStyle(
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          voiceNote.timestamp.toString().substring(0, 16),
                          style: TextStyle(
                            fontSize: 12,
                            color: Colors.grey[600],
                          ),
                        ),
                      ],
                    ),
                  ),
                  // Sync status badge
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 8,
                      vertical: 4,
                    ),
                    decoration: BoxDecoration(
                      color: voiceNote.isSynced
                          ? Colors.green.shade50
                          : Colors.orange.shade50,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(
                        color: voiceNote.isSynced
                            ? Colors.green.shade200
                            : Colors.orange.shade200,
                      ),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(
                          voiceNote.isSynced
                              ? Icons.cloud_done_rounded
                              : Icons.cloud_upload_outlined,
                          size: 14,
                          color: voiceNote.isSynced
                              ? Colors.green.shade700
                              : Colors.orange.shade700,
                        ),
                        const SizedBox(width: 4),
                        Text(
                          voiceNote.isSynced ? 'Synced' : 'Pending',
                          style: TextStyle(
                            fontSize: 11,
                            color: voiceNote.isSynced
                                ? Colors.green.shade700
                                : Colors.orange.shade700,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 12),
              
              // Patient ID if available
              if (voiceNote.patientId != null) ...[
                Row(
                  children: [
                    Icon(
                      Icons.badge_outlined,
                      size: 16,
                      color: Colors.grey[600],
                    ),
                    const SizedBox(width: 8),
                    Text(
                      'Patient: ${voiceNote.patientId}',
                      style: TextStyle(
                        fontSize: 13,
                        color: Colors.grey[700],
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
              ],
              
              // Location
              Row(
                children: [
                  Icon(
                    Icons.location_on_outlined,
                    size: 16,
                    color: Colors.grey[600],
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      voiceNote.locationString,
                      style: TextStyle(
                        fontSize: 13,
                        color: Colors.grey[700],
                      ),
                    ),
                  ),
                ],
              ),
              
              // Notes if available
              if (voiceNote.metadata['notes'] != null &&
                  (voiceNote.metadata['notes'] as String).isNotEmpty) ...[
                const SizedBox(height: 8),
                Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Icon(
                      Icons.notes_outlined,
                      size: 16,
                      color: Colors.grey[600],
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        voiceNote.metadata['notes'] as String,
                        style: TextStyle(
                          fontSize: 13,
                          color: Colors.grey[700],
                        ),
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                  ],
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }

  void _showVoiceNoteDetails(BuildContext context) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) => DraggableScrollableSheet(
        initialChildSize: 0.7,
        minChildSize: 0.5,
        maxChildSize: 0.95,
        expand: false,
        builder: (context, scrollController) => _VoiceNoteDetails(
          voiceNote: voiceNote,
          scrollController: scrollController,
        ),
      ),
    );
  }
}

/// Voice note details bottom sheet
class _VoiceNoteDetails extends StatelessWidget {
  final VoiceNote voiceNote;
  final ScrollController scrollController;

  const _VoiceNoteDetails({
    required this.voiceNote,
    required this.scrollController,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(24),
      child: ListView(
        controller: scrollController,
        children: [
          // Handle bar
          Center(
            child: Container(
              width: 40,
              height: 4,
              decoration: BoxDecoration(
                color: Colors.grey[300],
                borderRadius: BorderRadius.circular(2),
              ),
            ),
          ),
          const SizedBox(height: 24),
          
          // Title
          Text(
            'Voice Note Details',
            style: Theme.of(context).textTheme.headlineSmall,
          ),
          const SizedBox(height: 24),
          
          // Timestamp
          _DetailRow(
            icon: Icons.access_time_rounded,
            label: 'Recorded',
            value: voiceNote.timestamp.toString().substring(0, 16),
          ),
          const Divider(height: 32),
          
          // Patient ID
          if (voiceNote.patientId != null) ...[
            _DetailRow(
              icon: Icons.badge_outlined,
              label: 'Patient ID',
              value: voiceNote.patientId!,
            ),
            const Divider(height: 32),
          ],
          
          // Location
          _DetailRow(
            icon: Icons.location_on_outlined,
            label: 'Location',
            value: voiceNote.locationString,
          ),
          const Divider(height: 32),
          
          // Sync status
          _DetailRow(
            icon: voiceNote.isSynced
                ? Icons.cloud_done_rounded
                : Icons.cloud_upload_outlined,
            label: 'Sync Status',
            value: voiceNote.isSynced ? 'Synced to cloud' : 'Pending sync',
            valueColor: voiceNote.isSynced
                ? Colors.green.shade700
                : Colors.orange.shade700,
          ),
          
          // Notes
          if (voiceNote.metadata['notes'] != null &&
              (voiceNote.metadata['notes'] as String).isNotEmpty) ...[
            const Divider(height: 32),
            _DetailRow(
              icon: Icons.notes_outlined,
              label: 'Notes',
              value: voiceNote.metadata['notes'] as String,
            ),
          ],
          
          const SizedBox(height: 32),
          
          // Delete button
          ElevatedButton.icon(
            onPressed: () => _deleteVoiceNote(context),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.red.shade50,
              foregroundColor: Colors.red.shade700,
              elevation: 0,
              minimumSize: const Size.fromHeight(50),
            ),
            icon: const Icon(Icons.delete_outline_rounded),
            label: const Text('Delete Voice Note'),
          ),
        ],
      ),
    );
  }

  Future<void> _deleteVoiceNote(BuildContext context) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Delete Voice Note'),
        content: const Text(
          'Are you sure you want to delete this voice note? This action cannot be undone.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () => Navigator.pop(context, true),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.red.shade600,
            ),
            child: const Text('Delete'),
          ),
        ],
      ),
    );

    if (confirmed == true && context.mounted) {
      final storageService = context.read<StorageService>();
      final success = await storageService.deleteVoiceNote(voiceNote.id);
      
      if (context.mounted) {
        Navigator.pop(context); // Close bottom sheet
        
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              success
                  ? 'Voice note deleted successfully'
                  : 'Failed to delete voice note',
            ),
            backgroundColor: success
                ? Colors.green.shade600
                : Colors.red.shade600,
            behavior: SnackBarBehavior.floating,
          ),
        );
      }
    }
  }
}

/// Detail row widget
class _DetailRow extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;
  final Color? valueColor;

  const _DetailRow({
    required this.icon,
    required this.label,
    required this.value,
    this.valueColor,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Icon(
          icon,
          size: 24,
          color: Theme.of(context).colorScheme.primary,
        ),
        const SizedBox(width: 16),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                label,
                style: TextStyle(
                  fontSize: 13,
                  color: Colors.grey[600],
                  fontWeight: FontWeight.w500,
                ),
              ),
              const SizedBox(height: 4),
              Text(
                value,
                style: TextStyle(
                  fontSize: 16,
                  color: valueColor ?? Colors.grey[900],
                  fontWeight: FontWeight.w600,
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
