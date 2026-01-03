import torch
import torch.nn as nn
import math

class SpatiotemporalTensor(nn.Module):
    """
        The HSTPU Core. 
            Handles 4D Data: (Latitude, Longitude, Time, Severity).
                Implements the '72-hour Decision Window' via temporal convolution.
                    """
                        def __init__(self, input_dim=128, hidden_dim=256):
                                super().__init__()
                                        # Spatiotemporal Graph Convolution (Simulated logic)
                                                self.spatial_conv = nn.Conv2d(input_dim, hidden_dim, kernel_size=3, padding=1)
                                                        self.temporal_conv = nn.Conv1d(hidden_dim, hidden_dim, kernel_size=72) # 72-hour window
                                                                
                                                                    def forward(self, x_map):
                                                                            # x_map: [Batch, Channels, Lat, Lon, Time]
                                                                                    # 1. Spatial Aggregation (Local Outbreaks)
                                                                                            s_out = self.spatial_conv(x_map)
                                                                                                    
                                                                                                            # 2. Temporal Projection (Crisis Evolution)
                                                                                                                    # Collapsing spatial dims to focus on time dynamics
                                                                                                                            t_in = s_out.mean(dim=[2, 3]) 
                                                                                                                                    t_out = self.temporal_conv(t_in.unsqueeze(2))
                                                                                                                                            
                                                                                                                                            return t_out

                                                                                                                                            class FristonFreeEnergyLoss(nn.Module):
                                                                                                                                                """
                                                                                                                                                    Uncertainty Minimization (Friston's Free Energy).
                                                                                                                                                        F = Energy - Entropy
                                                                                                                                                            Used to drive the 'Active Inference' of the system.
                                                                                                                                                                """
                                                                                                                                                                    def forward(self, observation, prediction, model_uncertainty):
                                                                                                                                                                            # Surprise (Prediction Error)
                                                                                                                                                                                    energy = torch.mean((observation - prediction) ** 2)
                                                                                                                                                                                            
                                                                                                                                                                                                    # Entropy (Model Uncertainty)
                                                                                                                                                                                                            entropy = -torch.mean(model_uncertainty * torch.log(model_uncertainty + 1e-6))
                                                                                                                                                                                                                    
                                                                                                                                                                                                                    # Free Energy to Minimize
                                                                                                                                                                                                                            # We want to minimize Surprise AND minimize Uncertainty
                                                                                                                                                                                                                                    F = energy + entropy 
                                                                                                                                                                                                                                            return F