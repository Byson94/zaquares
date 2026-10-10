<script>
    import NavBar from '../../components/NavBar.svelte';
    import Footer from '../../components/Footer.svelte';
    import Area from '../../components/Area.svelte';

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
    <div class="mt-10 flex" id="page"> 
        <article class="prose w-full max-w-none p-2">
            {#if data.meta}
                <h1 class="mb-0!">{data.meta.title}</h1>
                <p>{data.meta.description}</p>

                <div class="text-current/70 mb-4 flex items-center space-x-2 text-sm">
                    {#if data.meta.date}
                        <time datetime={data.meta.date}>{formatDate(data.meta.date)}</time>
                    {/if}

                    {#if data.meta.date && data.readingTime}
                        <span>-</span>
                    {/if}

                    {#if data.readingTime}
                        <span>{data.readingTime} minute read</span>
                    {/if}
                </div>

                <hr class="border-dark/10" />
            {/if}

            <data.content />
        </article>

        <aside class="toc-sidebar min-w-[200px] pl-6 md:block hidden">
            <nav class="sticky top-18">
                <h3 class="font-bold">On This Page</h3>
                <ul class="list-none not-prose p-0">
                    {#each data.headings as { id, text, tag }}
                        <li class={tag === 'H3' ? 'pl-4' : ''}>
                            <a href="#{id}" class="no-underline text-current/70 hover:text-current">{text}</a>
                        </li>
                    {:else}
                        <li>
                            <a href="#page" class="no-underline text-current/70 hover:text-current">This Page</a>
                        </li>
                    {/each}
                </ul>
            </nav>
        </aside>
    </div>
</Area>

<Footer />


