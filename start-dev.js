const { spawn } = require("child_process");

const startBackend = spawn("uvicorn", ["main:app", "--reload"], { stdio: "inherit" });
const startFrontend = spawn("pnpm", ["--dir", "frontend", "start"], { stdio: "inherit" });

startBackend.on("close", (code) => {
  console.log(`Backend process exited with code ${code}`);
});

startFrontend.on("close", (code) => {
  console.log(`Frontend process exited with code ${code}`);
});
