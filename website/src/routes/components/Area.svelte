<script lang="ts">
	let { children } = $props();
</script>

<div class="prose mx-auto max-w-[95vw] md:max-w-[75vw]">
    {@render children()}
</div>
