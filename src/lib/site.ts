import { parse } from 'yaml';
import { z } from 'astro/zod';
// 通过 Vite 的 ?raw 把 YAML 当字符串导入。
// 不能用 node:fs 读 —— 构建阶段模块被搬到 dist/ 下执行，
// import.meta.url 不再指向 src/lib，路径会断。
import rawYaml from '../data/site.yaml?raw';

/**
 * 站点数据。源文件是 YAML（便于手写与加注释），
 * 读进来之后过一遍 Zod —— 字段写错、漏字段，构建时就报错。
 *
 * 例如把 role 写成 first_author（下划线），构建会直接失败并指出位置，
 * 而不是安静地渲染出一个空标签。
 */
const Link = z.object({
  label: z.string(),
  url: z.string(),
});

const Site = z.object({
  author: z.object({
    name_zh: z.string(),
    name_en: z.string(),
    role: z.string(),
    affil: z.string(),
    bio: z.string(),
    links: z.array(Link),
  }),
  news: z.array(z.object({ when: z.string(), what: z.string() })),
  publications: z.array(
    z.object({
      title: z.string(),
      authors: z.string(),
      venue: z.string(),
      year: z.number(),
      role: z.enum(['first-author', 'co-author']),
      status: z.enum(['published', 'review']),
      link: z.string(),
    })
  ),
  projects: z.array(
    z.object({
      name: z.string(),
      repo: z.string(),
      lang: z.string(),
      stars: z.number(),
      body: z.string(),
    })
  ),
  timeline: z.array(z.object({ year: z.string(), what: z.string(), place: z.string() })),
});

export const site = Site.parse(parse(rawYaml));

/** 在作者串里把自己加粗，学术主页的常规做法。 */
export function highlightSelf(authors: string): string {
  return authors.replaceAll(site.author.name_en, `<strong>${site.author.name_en}</strong>`);
}

export type Publication = z.infer<typeof Site>['publications'][number];
export type Project = z.infer<typeof Site>['projects'][number];
