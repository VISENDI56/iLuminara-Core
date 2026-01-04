{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python3
    pkgs.python3Packages.numpy
    pkgs.python3Packages.pandas
    pkgs.python3Packages.plotly
    pkgs.python3Packages.cryptography
  ];

  shellHook = ''
    echo "🦁 Nairobi-Nexus Environment Active"
    echo "Running Master Audit..."
    python3 governance/compliance_oracle.py
  '';
}
