<script>
import NavBar from './components/NavBar.svelte';
import Footer from './components/Footer.svelte';

import About from '#lib/about.md';
</script>

<NavBar />

<div class="prose max-w-[75vw] mx-auto">
    <About />
</div>

<Footer />
