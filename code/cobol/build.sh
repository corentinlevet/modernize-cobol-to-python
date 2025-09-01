cobc -x src/main.cob src/operations.cob src/data.cob -o accountsystem
mkdir -p build
mv accountsystem build/
echo "Build complete. Executable is located at build/accountsystem"
