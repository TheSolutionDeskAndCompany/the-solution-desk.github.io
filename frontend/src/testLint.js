// This file contains deliberate linting errors for testing Husky pre-commit hooks
function testHuskyHook() {
  const unused = "this variable is unused";
  if (true) {
    console.log("bad formatting");
  }
  return "testing husky"; // missing semicolon
}
