import { mdsvex } from 'mdsvex';
import rehypeSlug from 'rehype-slug';
import remarkHeadings from '@vcarl/remark-headings';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex-svelte';
import tailwindcss from '@tailwindcss/vite';
import adapter from '@sveltejs/adapter-static';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import path from 'node:path';
import GithubSlugger from 'github-slugger';

const pnpmStore = path.resolve('node_modules/.pnpm');

/** Plugin to expose extracted headings inside mdsvex metadata */
function attachHeadingsToMeta() {
    return (tree, vfile) => {
        vfile.data.fm = vfile.data.fm || {};
        if (vfile.data.headings) {
            const slugger = new GithubSlugger();

            vfile.data.fm.headings = vfile.data.headings.map((h) => ({
                id: slugger.slug(h.value),
                text: h.value,
                depth: h.depth
            }));
        }
    };
}

export default defineConfig({
	plugins: [
		tailwindcss(),
		sveltekit({
			compilerOptions: {
				// Force runes mode for the project, except for libraries. Can be removed in svelte 6.
				runes: ({ filename }) =>
					filename.split(/[/\\]/).includes('node_modules') ? undefined : true
			},
			adapter: adapter({ pages: 'build', assets: 'build', strict: true }),
			preprocess: [mdsvex({ 
                remarkPlugins: [remarkHeadings, attachHeadingsToMeta, remarkMath],
                rehypePlugins: [rehypeKatex, rehypeSlug],
                extensions: ['.svx', '.md'] 
            })],
			extensions: ['.svelte', '.svx', '.md']
		})
	],
    server: {
        fs: {
            allow: [pnpmStore],
        },
    },
});
