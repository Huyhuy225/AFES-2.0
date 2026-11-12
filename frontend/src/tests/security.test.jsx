import { describe, it, expect } from 'vitest';
import apiService from '../api/sensorApi';
import fs from 'node:fs';
import path from 'node:path';

describe('Security & Zero CoreIOT Credential Invariant Tests', () => {
  it('throws security error if CoreIOT token header is injected', async () => {
    apiService.setMockMode(false);

    await expect(
      apiService._fetch('/zones/summary', {
        headers: { 'X-CoreIOT-Token': 'illegal-admin-token' },
      })
    ).rejects.toThrow(/SECURITY VIOLATION/);
  });

  it('verifies that frontend source files contain NO hardcoded CoreIOT secrets, tokens, or credentials', () => {
    const srcDir = path.resolve(__dirname, '..');
    const filesToScan = [];

    const walkSync = (dir) => {
      const list = fs.readdirSync(dir);
      list.forEach((file) => {
        const fullPath = path.join(dir, file);
        const stat = fs.statSync(fullPath);
        if (stat.isDirectory()) {
          if (file !== 'node_modules' && file !== 'dist') walkSync(fullPath);
        } else if (file.endsWith('.js') || file.endsWith('.jsx') || file.endsWith('.json') || file.endsWith('.html')) {
          filesToScan.push(fullPath);
        }
      });
    };

    walkSync(srcDir);
    expect(filesToScan.length).toBeGreaterThan(5);

    // Look for actual credential assignment patterns or platform secrets
    const forbiddenPatterns = [
      /coreiot[._-]token\s*[:=]\s*['"][a-zA-Z0-9_-]{8,}['"]/i,
      /coreiot[._-]secret\s*[:=]\s*['"][a-zA-Z0-9_-]{8,}['"]/i,
      /device[._-]access[._-]token\s*[:=]\s*['"][a-zA-Z0-9_-]{8,}['"]/i,
      /api[._-]key\s*[:=]\s*['"][a-zA-Z0-9_-]{16,}['"]/i,
      /thingsboard[._-]token\s*[:=]\s*['"][a-zA-Z0-9_-]{8,}['"]/i,
      /password\s*[:=]\s*['"](?!<PASSWORD_PLACEHOLDER>)[a-zA-Z0-9_!@#$%^&*]{6,}['"]/i,
    ];

    filesToScan.forEach((filePath) => {
      if (filePath.endsWith('security.test.jsx')) return;

      const content = fs.readFileSync(filePath, 'utf-8');
      forbiddenPatterns.forEach((pattern) => {
        const match = content.match(pattern);
        expect(
          match,
          `Security Invariant Violation: Found forbidden secret pattern '${pattern}' in file: ${filePath}`
        ).toBeNull();
      });
    });
  });
});
