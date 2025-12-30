import torch
import torch.nn as nn

class RetinaInputLayer(nn.Module):
    """
        Pixel-First Tokenizer.
            Replaces fragile text tokenization with visual embeddings.
                Based on DeepSeek-OCR / Karpathy's 'Pixel-Input' thesis.
                    """
                        def __init__(self, patch_size=16, embed_dim=768):
                                super().__init__()
                                        # A simple Vision Transformer (ViT) style patch embedder
                                                # In prod, this wraps SigLIP or a specialized OCR encoder
                                                        self.patch_embed = nn.Conv2d(3, embed_dim, kernel_size=patch_size, stride=patch_size)
                                                                self.flatten = nn.Flatten(2)

                                                                    def forward(self, image_tensor):
                                                                            """
                                                                                    Input: Raw pixels of a doctor's note (B, C, H, W)
                                                                                            Output: Visual Embeddings sequence (B, Seq_Len, Dim)
                                                                                                    """
                                                                                                            # Bypasses Unicode/Byte-Pair Encoding issues entirely.
                                                                                                                    # "Smiling Emoji" is processed as pixels, not a weird token ID.
                                                                                                                            x = self.patch_embed(image_tensor)
                                                                                                                                    x = self.flatten(x).transpose(1, 2)
                                                                                                                                            return x