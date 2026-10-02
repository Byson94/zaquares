<script>
    import NavBar from './components/NavBar.svelte';
    import Footer from './components/Footer.svelte';
    import Area from './components/Area.svelte';

    import About from '#lib/about.md';
</script>

<NavBar />

<Area>
    <About />
</Area>

<Footer />
