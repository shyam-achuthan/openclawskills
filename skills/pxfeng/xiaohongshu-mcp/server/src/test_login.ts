import { login } from './xiaohongshu.js';

(async () => {
    console.log("=== 开始测试登录 (Start Login Test) ===");
    try {
        console.log("正在启动浏览器...请在弹出的窗口中扫码登录 / Launching browser... Please scan QR code.");
        const result = await login();
        console.log("登录结果 / Login Result:", result);
    } catch (e) {
        console.error("登录失败 / Login Failed:", e);
    }
})();
