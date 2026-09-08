import {defineConfig} from '@playwright/test';
export default defineConfig({testDir:'tests/browser',workers:1,use:{baseURL:'http://127.0.0.1:8016',headless:true},webServer:{command:'.venv/bin/python -m uvicorn intrinsiclab.api:app --host 127.0.0.1 --port 8016',url:'http://127.0.0.1:8016/api/health',reuseExistingServer:!process.env.CI}});
