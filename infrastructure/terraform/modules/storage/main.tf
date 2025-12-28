# Abstracted Blob Storage (S3/Azure Blob/GCS)

variable "provider" { type = string }

resource "null_resource" "storage" {
  # Placeholder for provider-specific logic
  provisioner "local-exec" {
    command = "echo Creating storage for ${var.provider}"
  }
}
