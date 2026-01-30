import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
    CallToolRequestSchema,
    ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { login, upload } from "./xiaohongshu.js";

const server = new Server(
    {
        name: "xiaohongshu-mcp",
        version: "0.1.0",
    },
    {
        capabilities: {
            tools: {},
        },
    }
);

server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
        tools: [
            {
                name: "xiaohongshu_login",
                description: "Opens a browser for the user to log in to Xiaohongshu Creator Platform. Saves cookies for future use.",
                inputSchema: {
                    type: "object",
                    properties: {},
                },
            },
            {
                name: "xiaohongshu_upload",
                description: "Uploads a post (image/video) to Xiaohongshu.",
                inputSchema: {
                    type: "object",
                    properties: {
                        title: {
                            type: "string",
                            description: "Title of the post (max 20 chars usually recommended)",
                        },
                        content: {
                            type: "string",
                            description: "Description/Body of the post",
                        },
                        files: {
                            type: "array",
                            items: { type: "string" },
                            description: "Absolute paths to images or videos to upload",
                        },
                        publishTime: {
                            type: "string",
                            description: "Optional ISO timestamp to schedule publish",
                        },
                    },
                    required: ["title", "content", "files"],
                },
            },
        ],
    };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
    try {
        if (request.params.name === "xiaohongshu_login") {
            const result = await login();
            return {
                content: [{ type: "text", text: result }],
            };
        }

        if (request.params.name === "xiaohongshu_upload") {
            const args = request.params.arguments as any;
            const result = await upload(args);
            return {
                content: [{ type: "text", text: result }],
            };
        }

        throw new Error(`Tool not found: ${request.params.name}`);
    } catch (error: any) {
        return {
            content: [{ type: "text", text: `Error: ${error.message}` }],
            isError: true,
        };
    }
});

const transport = new StdioServerTransport();
await server.connect(transport);
