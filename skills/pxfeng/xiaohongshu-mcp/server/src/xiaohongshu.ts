import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

// Define path for cookies relative to the package workspace
const COOKIE_PATH = path.resolve(process.cwd(), 'cookies.json');

export async function login() {
    console.error("Launching browser for login...");
    const browser = await chromium.launch({ headless: false });
    const context = await browser.newContext();
    const page = await context.newPage();

    try {
        await page.goto('https://creator.xiaohongshu.com/login');

        console.error("Please log in. Waiting for 'Publish Note' button to appear...");

        // Wait for the "Publish Note" button to appear, which confirms we are logged in
        try {
            await page.getByText('发布笔记', { exact: true }).or(page.locator('.publish-btn')).first().waitFor({ state: 'visible', timeout: 300000 }); // 5 minutes wait
        } catch (e) {
            console.error("Warning: 'Publish Note' button not found. Checking URL...");
            await page.waitForURL('**/creator/home**', { timeout: 30000 });
        }

        await context.storageState({ path: COOKIE_PATH });
        console.error(`Saved cookies to ${COOKIE_PATH}`);
        return "Login successful! Session saved.";

    } catch (error) {
        throw error;
    } finally {
        await browser.close();
    }
}

export async function upload(args: {
    title: string;
    content: string;
    files: string[];
    publishTime?: string
}) {
    if (!fs.existsSync(COOKIE_PATH)) {
        throw new Error("Not logged in. Please run xiaohongshu_login first.");
    }

    console.error("Launching browser for upload...");
    const browser = await chromium.launch({ headless: false });
    const context = await browser.newContext({ storageState: COOKIE_PATH });
    const page = await context.newPage();

    try {
        await page.goto('https://creator.xiaohongshu.com/creator/home');

        // 1. Click "发布笔记" (Publish Note)
        const publishNoteBtn = page.getByText('发布笔记', { exact: true }).or(page.locator('.publish-btn'));
        await publishNoteBtn.first().click();

        // 2. Click "上传图文" (Upload Image/Text)
        const uploadImageTextBtn = page.getByText('上传图文').first();
        await uploadImageTextBtn.waitFor({ state: 'visible' });
        await uploadImageTextBtn.click();

        // 3. Upload Files
        // The input[type=file] might be hidden, so we look for it but don't require visibility
        const fileInput = page.locator('input[type="file"]');

        // Wait for input to be attached
        await fileInput.waitFor({ state: 'attached', timeout: 10000 });
        await fileInput.setInputFiles(args.files);

        // Wait for upload processing
        console.error("Files set, waiting for upload processing...");
        await page.waitForTimeout(5000);

        // 4. Fill Title
        const titleInput = page.getByPlaceholder('填写标题', { exact: false });
        await titleInput.fill(args.title);

        // 3. Fill Content
        const contentInput = page.getByPlaceholder('填写正文', { exact: false });
        // It might be a contenteditable div
        if (await contentInput.isVisible()) {
            await contentInput.fill(args.content);
        } else {
            // Fallback for rich text editors
            const editor = page.locator('.ql-editor').or(page.locator('#post-textarea')); // Hypothetical selectors
            if (await editor.isVisible()) {
                await editor.fill(args.content);
            } else {
                // Try clicking into the area and typing
                await page.locator('.content-input-area').first().click(); // Generic guess
                await page.keyboard.type(args.content);
            }
        }

        // 4. Publish
        const publishButton = page.locator('button').filter({ hasText: '发布' });
        await publishButton.click();

        // 5. Verification
        await page.getByText('发布成功').waitFor({ state: 'visible', timeout: 30000 });

        console.error("Success detected. Waiting 15 seconds for manual observation...");
        await page.waitForTimeout(15000);
        return "Upload successful!";
    } catch (e: any) {
        const screenshotPath = path.resolve(process.cwd(), 'error_screenshot.png');
        await page.screenshot({ path: screenshotPath });
        console.error(`Upload failed. Screenshot saved to ${screenshotPath}`);
        throw e;
    } finally {
        await browser.close();
    }
}
