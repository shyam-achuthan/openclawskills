const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// [2026-02-03] WRAPPER REFACTOR: PURE PROXY
// This wrapper now correctly delegates to the core 'evolver' plugin.

async function run() {
    console.log('🚀 Launching Feishu Evolver Wrapper (Proxy Mode)...');
    
    const args = process.argv.slice(2);
    
    // 1. Force Feishu Card Reporting
    process.env.EVOLVE_REPORT_TOOL = 'feishu-card';
    
    // 2. Resolve Core Evolver Path
    // Try 'evolver' or 'capability-evolver' (they are the same)
    let evolverDir = path.resolve(__dirname, '../evolver');
    if (!fs.existsSync(evolverDir)) {
        evolverDir = path.resolve(__dirname, '../capability-evolver');
    }
    
    if (!fs.existsSync(evolverDir)) {
        console.error("❌ Critical Error: Core 'evolver' plugin not found!");
        process.exit(1);
    }

    const mainScript = path.join(evolverDir, 'index.js');
    const lifecycleLog = path.resolve(__dirname, '../../logs/wrapper_lifecycle.log');
    
    // Ensure logs dir
    if (!fs.existsSync(path.dirname(lifecycleLog))) {
        fs.mkdirSync(path.dirname(lifecycleLog), { recursive: true });
    }
    
    const startTime = Date.now();
    fs.appendFileSync(lifecycleLog, `[${new Date(startTime).toISOString()}] START Wrapper Proxy PID=${process.pid}\n`);
    
    try {
        // 3. Inject Reporting Directive (Feishu Specific)
        process.env.EVOLVE_REPORT_DIRECTIVE = `3.  **📝 REPORT (FEISHU WRAPPER)**:
    - You **MUST** use the \`feishu-evolver-wrapper/report.js\` tool.
    - **Frequency**: Report EVERY cycle.
    - **Command**:
      \`\`\`bash
      node skills/feishu-evolver-wrapper/report.js --cycle "__CYCLE_ID__" --status "Status: [WRAPPED] Step Complete."
      \`\`\`
    - **Target**: Auto-detects context (Group 🧬 or Master).`;

        // 4. Inject Atomic Mode Rule (Cron Compatibility)
        process.env.EVOLVE_EXTRA_MODES = `- **Mode A (Atomic/Cron)**: 🔗 **MANDATORY**: You are running in **Cron Mode**. 
      - **Action**: Do NOT spawn a new loop. Do NOT call sessions_spawn.
      - **Goal**: Complete ONE generation, update state, and EXIT gracefully.`;

        // Pass clean args (remove wrapper flags if any)
        let childArgsArr = args.filter(a => a !== '--once' && a !== '--loop');
        
        // Default to 'run' if no command provided
        if (childArgsArr.length === 0) {
            childArgsArr.push('run');
        }
        
        const childArgs = childArgsArr.join(' ');

        // Execute Core Evolver
        console.log(`▶️ Delegating to Core: ${mainScript}`);
        const output = execSync(`node "${mainScript}" ${childArgs}`, { 
            stdio: 'pipe', 
            maxBuffer: 1024 * 1024 * 50, 
            timeout: 900000, // 15 min max
            encoding: 'utf8'
        }); 

        // Output Handling
        const lines = output.split('\n');
        if (lines.length > 1500) {
            console.log(lines.slice(0, 500).join('\n'));
            console.log(`\n... [TRUNCATED ${lines.length - 1000} LINES] ...\n`);
            console.log(lines.slice(-500).join('\n'));
        } else {
            console.log(output);
        }

        const duration = ((Date.now() - startTime) / 1000).toFixed(2);
        fs.appendFileSync(lifecycleLog, `[${new Date().toISOString()}] SUCCESS Wrapper PID=${process.pid} Duration=${duration}s\n`);
        console.log("\n✅ Wrapper Proxy Complete.");

    } catch (e) {
        const duration = ((Date.now() - startTime) / 1000).toFixed(2);
        fs.appendFileSync(lifecycleLog, `[${new Date().toISOString()}] ERROR Wrapper PID=${process.pid} Duration=${duration}s: ${e.message}\n`);
        console.error("Wrapper Proxy Failed:", e.message);
        console.log("\n❌ Wrapper Failed.");
        process.exit(1);
    }
}

run();
