import { error } from '@sveltejs/kit';

export async function load({ params }) {
	try {
		const post = await import(`#lib/docs/${params.slug}.md`);
		const rawPost = await import(`#lib/docs/${params.slug}.md?raw`);

		const bodyText = rawPost.default.replace(/^---[\s\S]*?---/, '').trim();
		const wordCount = bodyText ? bodyText.split(/\s+/).length : 0;
		const readingTime = Math.ceil(wordCount / 200);

		return {
			content: post.default,
			meta: post.metadata,
            headings: post.metadata.headings || [],
			readingTime
		};
	} catch (e) {
		error(404, `Could not find document: ${params.slug}`);
	}
}

