
echo "Cleaning .raw-wasm build files..."
make clean SUFFIX=.raw-wasm -s

echo "Cleaning .mems-wasm build files..."
make clean SUFFIX=.mems-wasm -s

echo "Cleaning .native build files..."
make clean SUFFIX=.native -s

echo "Building native with clang from /usr..."
make native CC_PATH=/usr -j8 -s    # here is your native clang, ${CC_PATH}/bin/clang

echo "Building with custom LLVM supporting MemS-Wasm..."
make CC_PATH=../llvm-project-memswasm/build WASI_LIBC_PATH=../ms-wasi-libc/sysroot SUFFIX=.mems-wasm -j8 -s    

echo "Building with WASI SDK for raw WebAssembly..."
make CC_PATH=../wasi-sdk/build/install/opt/wasi-sdk/ WASI_LIBC_PATH=../wasi-sdk/build/install/opt/wasi-sdk/share/wasi-sysroot SUFFIX=.raw-wasm -j8 -s


echo "Running benchmarks and logging to output.log, the result is in result.log..."
python3 benchmark.py --wasmtime /home/hh/wasmtime/target/debug/wasmtime --log output.log --suffix=.mems-wasm

echo "Drawing bar graph and the result is res.png..."
python3 drawBarGraph.py
