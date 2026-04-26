プロジェクト: モデルガン分解組み立てシミュレーター（プロトタイプ）
方針: B — React Three Fiber + TypeScript + @react-spring（拡張性重視）
目的: 今回は各LLMのコーディング出力性能を評価するための実装雛形を自動生成します。

セットアップ:
1. cd prototype/bootstrap
2. npm install
3. npm run dev

生成物:
- package.json
- tsconfig.json
- vite.config.ts
- index.html
- src/main.tsx
- src/App.tsx
- src/components/SceneCanvas.tsx
- src/components/GunPlaceholder.tsx
- src/styles.css

注記: これは最小限のブートストラップです。ボクセルガンモデル等は含みません。テスト目的でのコード生成品質と互換性を早期に確認するための雛形です。