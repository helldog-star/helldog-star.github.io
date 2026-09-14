import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

/**
 * 随笔集合。
 * 这是 Astro 相对 Hugo 最实在的优势之一：frontmatter 有 schema，
 * 少写 excerpt、把 date 写成数字，构建时就会直接报错，而不是渲染出一个空标签。
 */
const writing = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/writing' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    excerpt: z.string(),
  }),
});

export const collections = { writing };
