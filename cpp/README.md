# cpp-sandbox

A minimal C++ sandbox for trying out language features and libraries. Every
`.cpp` file in `src/` is built as its own standalone executable, so you can
have a dozen unrelated experiments living side by side without them
interfering with each other.

## Requirements
- `gcc`/`g++` (or clang, if you'd rather — see below) supporting C++23
- `cmake` (3.20+)
- `clang-format` (optional, for formatting)

## Project layout
```
cpp-sandbox/
├── CMakeLists.txt      # build config — one executable per file in src/
├── .clang-format       # formatting rules
├── src/                # your source files go here
│   └── main.cpp
└── build/               # created by cmake, gitignored
```

## Building
From the project root:
```bash
cmake -S . -B build
cmake --build build
```
This produces one binary per `.cpp` file in `src/`, named after the file —
e.g. `src/main.cpp` becomes `build/main`, `src/threads_test.cpp` would
become `build/threads_test`.

## Running
```bash
./build/main
```

## Adding a new experiment
1. Create a new file in `src/`, e.g. `src/coroutines_test.cpp`.
2. Reconfigure so CMake picks it up:
   ```bash
   cmake -S . -B build
   ```
3. Build and run it:
   ```bash
   cmake --build build
   ./build/coroutines_test
   ```
Editing an *existing* file doesn't need a reconfigure — just
`cmake --build build` again.

## Formatting
```bash
clang-format -i src/*.cpp
```
Or format a single file: `clang-format -i src/main.cpp`.

## Choosing the compiler
CMake picks up your system default (usually gcc on Linux). To use a specific
compiler, set it at configure time:
```bash
cmake -S . -B build -DCMAKE_CXX_COMPILER=g++-13
# or
cmake -S . -B build -DCMAKE_CXX_COMPILER=clang++
```

## Adding dependencies
There are two common ways to pull in a library:

**1. System packages (simplest, for well-known libraries)**
Install via your package manager, then locate it with `find_package`:
```bash
sudo apt install libfmt-dev
```
```cmake
find_package(fmt REQUIRED)
# then, per-target:
target_link_libraries(main PRIVATE fmt::fmt)
```

**2. FetchContent (no system install, pulled straight from source)**
Add near the top of `CMakeLists.txt`:
```cmake
include(FetchContent)
FetchContent_Declare(
  fmt
  GIT_REPOSITORY https://github.com/fmtlib/fmt.git
  GIT_TAG        11.0.2
)
FetchContent_MakeAvailable(fmt)
```
Then link it against whichever executable needs it:
```cmake
target_link_libraries(main PRIVATE fmt::fmt)
```
Since executables are created in a `foreach` loop from the source glob,
`target_link_libraries(main ...)` calls should go **after** that loop, once
the `main` target actually exists.

## Cleaning
```bash
rm -rf build
```

## What the CMakeLists.txt does

```cmake
cmake_minimum_required(VERSION 3.20)
project(sandbox LANGUAGES CXX)
```
Declares the minimum CMake version this file relies on, and names the
project `sandbox` (this name is mostly cosmetic — it shows up in IDE
integrations, not in the binaries themselves).

```cmake
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
```
Targets C++23. `REQUIRED ON` means CMake errors out instead of silently
falling back to an older standard if your compiler doesn't support it.
`EXTENSIONS OFF` disables compiler-specific extensions (e.g. GNU extensions
in gcc), keeping the code portable/standards-conformant.

```cmake
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
```
Generates `build/compile_commands.json`, a file editors/language servers
(clangd, VS Code, etc.) use to get accurate autocomplete and diagnostics
for your exact compiler flags.

```cmake
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Debug)
endif()
```
If you don't pass `-DCMAKE_BUILD_TYPE=...` explicitly, default to a `Debug`
build (includes debug symbols, no optimization — good for learning/
stepping through code). Override with `Release` for optimized builds:
```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
```

```cmake
file(GLOB APP_SOURCES CONFIGURE_DEPENDS "${CMAKE_SOURCE_DIR}/src/*.cpp")
```
Finds every `.cpp` file directly inside `src/` and stores the list in
`APP_SOURCES`. `CONFIGURE_DEPENDS` tells CMake to re-scan this glob on
every build (not just on manual reconfigure) on generators that support
it — in practice you should still reconfigure manually after adding a
file, since glob-based sourcing isn't guaranteed to pick up new files on
every generator/CMake version.

```cmake
foreach(src ${APP_SOURCES})
  get_filename_component(name ${src} NAME_WE)
  add_executable(${name} ${src})
endforeach()
```
Loops over each source file found above. `get_filename_component(... NAME_WE)`
strips the directory and extension, leaving just the base filename (e.g.
`src/coroutines_test.cpp` → `coroutines_test`). `add_executable` then
creates a build target with that name, compiled from just that one file —
this is what gives you an independent binary per experiment.