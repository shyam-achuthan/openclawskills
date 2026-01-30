import { upload } from './xiaohongshu.js';
import path from 'path';
import fs from 'fs';

(async () => {
    console.log("=== 开始测试上传 (Start Upload Test) ===");

    // 请在这里替换为你想要测试的图片路径
    // Replace this with the absolute path to your test image
    const imagePath = path.resolve(process.cwd(), 'test_image.jpg');

    if (!fs.existsSync(imagePath)) {
        console.error(`错误: 找不到测试图片 (Error: Test image not found at ${imagePath})`);
        console.error("请在项目根目录放一张名为 'test_image.jpg' 的图片，或者修改脚本中的路径。");
        console.error("Please place a file named 'test_image.jpg' in the project root or edit this script.");
        process.exit(1);
    }

    try {
        const result = await upload({
            title: "脚本测试标题 (Test Title)",
            content: "这是通过脚本自动上传的测试内容。\nThis is a test content uploaded via script.",
            files: [imagePath]
        });
        console.log("上传结果 / Upload Result:", result);
    } catch (e) {
        console.error("上传失败 / Upload Failed:", e);
    }
})();
