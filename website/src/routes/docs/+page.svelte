<script>
    import NavBar from '../components/NavBar.svelte';
    import Footer from '../components/Footer.svelte';
    import Area from '../components/Area.svelte';

	let { data } = $props();

	function formatDate(dateString) {
		if (!dateString) return '';
		const date = new Date(dateString);
		return new Intl.DateTimeFormat('en-US', {
			year: 'numeric',
			month: 'long',
			day: 'numeric',
			timeZone: 'UTC'
		}).format(date);
	}
</script>

<NavBar />

<Area>
    <h1>Documents</h1>
    <div class="space-y-2">
        {#each data.posts as post}
            <hr class="p-0! m-0! my-6! border-slate-300" />
            <a href="/docs/{post.slug}">
                <div>
                    <h2
                        class="truncate text-base font-semibold text-current group-hover:opacity-80"
                        style="margin: 0 !important; margin-top: 0.25rem !important;"
                    >
                        {post.meta.title}
                    </h2>
                    {#if post.meta?.description}
                        <p
                            class="mt-1 line-clamp-1 text-sm text-current/70"
                            style="margin: 0 !important; margin-top: 0.25rem !important;"
                        >
                            {post.meta.description}
                        </p>
                    {/if}
                    {#if post.meta.date}
                        <time class="self-start text-xs whitespace-nowrap text-current/30 sm:self-center uppercase md:hidden block mt-2">
                            {formatDate(post.meta.date)}
                        </time>
                    {/if}
                </div>
            </a>
        {:else}
            <p>No documents found.</p>
        {/each}
        <hr class="p-0! m-0! my-6! border-slate-300" />
    </div>
</Area>

<Footer />


