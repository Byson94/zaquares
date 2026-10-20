<script>
    import NavBar from '../components/NavBar.svelte';
    import Footer from '../components/Footer.svelte';
    import Area from '../components/Area.svelte';

    const RESULTS = {
        "Ranked Stations, Rivers, and Tributaries, in Kerala": ["https://raw.githubusercontent.com/byson94/zaquares/main/data/wpi/ranked-dataset.pdf", "PDF"],
        "ML Model accuracy": ["https://raw.githubusercontent.com/byson94/zaquares/main/data/zape/headline.pdf", "PDF"],
        "Mean Average Error Rise": ["https://raw.githubusercontent.com/byson94/zaquares/main/data/zape/mae-rise.pdf", "PDF"],
        "Parameters ML Model Consideres Important": ["https://raw.githubusercontent.com/byson94/zaquares/main/data/zape/param-importance.pdf", "PDF"],
        "Best and Worst Params to Hide from ML model": ["https://raw.githubusercontent.com/byson94/zaquares/main/data/zape/best-worst-params.pdf", "PDF"],
        
    }
</script>

<NavBar />

<Area>
    <h1>Results</h1>
    <p>For full result data including the .csv's see the <a href="https://github.com/byson94/zaquares">GitHub repository</a> /data/ directory.</p>

    <div class="flex flex-col gap-2">
        {#each Object.entries(RESULTS) as [name, info]}
        <a href={info[0]} class="p-5 border flex justify-between">
            <span class="font-medium text-zinc-900">{name}</span>
            <span class="text-sm text-zinc-500">{info[1]}</span>
        </a>
        {/each}
    </div>
</Area>

<Footer />


