// @ts-check
import { defineConfig } from 'astro/config';

export default defineConfig({
  // 用户主页仓库 helldog-star.github.io —— 部署在根路径，不需要设 base
  site: 'https://helldog-star.github.io',

  // 目录式 URL：/writing/xxx/ 而不是 /writing/xxx.html
  build: { format: 'directory' },

  devToolbar: { enabled: false },

  // 代码块沿用站点自己的浅灰样式，不引入 Shiki 配色，
  // 与亮色学术极简的整体调性一致。
  // 想开语法高亮：删掉这一行，或改成
  //   markdown: { shikiConfig: { theme: 'github-light' } }
  markdown: { syntaxHighlight: false },
});
