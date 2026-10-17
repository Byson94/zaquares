<script>
    import { onMount } from 'svelte';
    import NavBar from '../components/NavBar.svelte';
    import Footer from '../components/Footer.svelte';
    import Area from '../components/Area.svelte';
    import { loadModel } from '@bubblyworld/xgboost-ts';

    const PARAMS = [
        'potential of Hydrogen (pH)',
        'Dissolved Oxygen (mg/L)',
        'Nitrate N (mgN/L)',
        'Ammonia N (mgN/L)',
        'Chloride (mg/L)',
        'Turbidity (NTU)',
        'Electric Conductivity (μS/cm)',
        'Temperature (ºC)',
    ];
    const DEFAULTS = [7, 7, 0.47, 0.05, 6, 1.1, 52.1, 26];

    let model = $state(null);
    let cal = $state(null);
    let loading = $state(true);
    let loadError = $state('');

    let values = $state([...DEFAULTS]);
    let hide = $state(PARAMS.map(() => false));

    let predicted = $state(null);
    let qHat = $state(null);
    let predictError = $state('');

    onMount(async () => {
        try {
            const [modelRes, calRes] = await Promise.all([
                fetch('/zape.ubj'),
                fetch('/zape_q.json'),
            ]);
            const buffer = new Uint8Array(await modelRes.arrayBuffer());
            model = await loadModel(buffer);
            cal = await calRes.json();
        } catch (e) {
            loadError = String(e);
        } finally {
            loading = false;
        }
    });

    function computeQHat(hiddenIndices) {
        if (hiddenIndices.length === 0) return cal.q_empty;
        const sumSq = hiddenIndices.reduce(
            (acc, p) => acc + cal.q_by_param[String(p)] ** 2,
            0,
        );
        return Math.sqrt(sumSq);
    }

    async function runPredict() {
        predictError = '';
        if (!model || !cal) {
            predictError = 'Model not loaded yet.';
            return;
        }

        const hiddenIndices = [];
        const inputs = values.map((v, i) => {
            if (hide[i]) {
                hiddenIndices.push(i);
                return NaN;
            }
            return Number(v);
        });

        try {
            const result = await model.predict([inputs]);
            predicted = result.values[0];
            qHat = computeQHat(hiddenIndices);
        } catch (e) {
            predictError = String(e);
        }
    }

    function reset() {
        values = [...DEFAULTS];
        hide = PARAMS.map(() => false);
        predicted = null;
        qHat = null;
        predictError = '';
    }
</script>

<NavBar />

<Area>
    <h1>Calculate WPI</h1>
    <p class="mb-8 leading-relaxed">
        Calculate WPI from any available parameters using our Machine Learning model,
        Zape. It predicts the WPI score based on the provided, unhidden parameters and displays
        a 90% confidence range <span class="font-mono">[x, y]</span>. The larger the
        range is, the less accurate the model will be. The model prioritizes parameters in the descending
        order of Nitrate N, Ammonia N, Chloride, Electric Conductivity, Dissolved Oxygen, Turbidity, Temperature,
        and potential of Hydrogen (pH). Therfore, target the first few parameters for ideal result.
    </p>

    {#if loading}
        <div class="flex items-center gap-3 text-slate-500 text-sm">
            <span class="inline-block w-4 h-4 border-2 border-slate-300 border-t-slate-500 rounded-full animate-spin"></span>
            Loading model…
        </div>
    {:else if loadError}
        <div class="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">
            <span class="font-semibold">Failed to load:</span>
            {loadError}
        </div>
    {:else}
        <div class="border border-[var(--accent3)] bg-white divide-y divide-slate-300">
            {#each PARAMS as name, i}
                <div class="flex items-center gap-4 px-4 py-3">
                    <label class="flex-1 text-sm font-medium text-slate-700" for="p-{i}">
                        {name}
                    </label>
                    <input
                        id="p-{i}"
                        type="number"
                        step="any"
                        bind:value={values[i]}
                        disabled={hide[i]}
                        class="w-28 rounded-md border border-[var(--accent3)] px-3 py-1.5 text-sm text-left font-mono
                               focus:border-[var(--accent2)] focus:outline-none focus:ring-1 focus:ring-slate-500
                               disabled:bg-slate-100 disabled:text-slate-400"
                    />
                    <label class="flex items-center gap-2 text-xs text-slate-500 cursor-pointer select-none">
                        <input
                            type="checkbox"
                            bind:checked={hide[i]}
                            class="h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-slate-500"
                        />
                        Hide
                    </label>
                </div>
            {/each}
        </div>

        <div class="flex items-center gap-3 mt-6">
            <button
                onclick={runPredict}
                class="rounded-md bg-[var(--accent2)] px-4 py-2 text-sm font-medium text-white
                       hover:bg-[var(--accent)] active:bg-[var(--accent2)] transition-colors"
            >
                Predict
            </button>
            <button
                onclick={reset}
                class="rounded-md border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700
                       hover:bg-slate-50 active:bg-slate-100 transition-colors"
            >
                Reset
            </button>
        </div>

        {#if predictError}
            <div class="mt-6 rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">
                {predictError}
            </div>
        {/if}

        {#if predicted !== null}
            <div class="mt-8 border border-[var(--accent3)] bg-gradient-to-br from-slate-50 to-white p-6 shadow-sm">
                <div class="text-xs uppercase tracking-wider text-slate-500 mb-1">
                    Predicted WPI
                </div>
                <div class="text-4xl font-bold tabular-nums text-slate-900">
                    {predicted.toFixed(2)}
                </div>
                {#if qHat !== null}
                    <div class="mt-3 text-sm text-slate-600">
                        <span class="font-medium">90% confidence:</span>
                        <span class="font-mono tabular-nums ml-1">
                            [{Math.max(predicted - qHat, 0).toFixed(2)},
                            {Math.min(predicted + qHat, 100).toFixed(2)}]
                        </span>
                    </div>
                {/if}
            </div>
        {/if}
    {/if}
</Area>

<Footer />
