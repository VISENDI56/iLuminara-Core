# iLuminara Constitutional Build System
all: verify_sovereignty build_nuclear_stack

verify_sovereignty:
	@python3 core/compiler_gate/shl_compiler.py

build_nuclear_stack:
	@echo "[*] RSA: Building Blackwell-Optimized Kernels..."
		@# Standard build commands proceed only if verify_sovereignty passes
		@python3 -m build

clean:
	@rm -rf build/ dist/ *.egg-info