<script>
    import { onMount } from 'svelte';
    import NavBar from '../../components/NavBar.svelte';
    import Footer from '../../components/Footer.svelte';
    import Area from '../../components/Area.svelte';

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

    let cal = $state(null);
    let values = $state([...DEFAULTS]);

    let calculated = $state(null);
    let calculateError = $state('');

    const WEIGHTS = [
        0.08571428571428572, // pH
        0.22857142857142856, // DO
        0.2,                 // NO3
        0.17142857142857143, // NH3
        0.11428571428571428, // Cl
        0.05714285714285714, // Tur
        0.14285714285714285, // EC
    ];

    function validate(name, val, lo, hi) {
        if (typeof val !== 'number' || Number.isNaN(val))
            throw new Error(`${name} is empty or invalid`);
        if (val < lo || val > hi)
            throw new Error(`${name} out of [${lo}, ${hi}] bounds`);
        return val;
    }

    const scorePH = (x) => 100 * (1 - Math.abs((x - 7.5) / 7.5) ** 2) ** 4;

    function doSat(t) {
        const tk = t + 273.15;
        return Math.exp(
            -139.34411 + 1.575701e5 / tk
            - 6.642308e7 / tk ** 2
            + 1.2438e10 / tk ** 3
            - 8.621949e11 / tk ** 4
        );
    }

    function scoreDO(x, t) {
        const sat = doSat(t);
        if (x >= 2 * sat) return 0;
        return 100 * (1 - ((x - sat) / sat) ** 2) ** 4;
    }

    const scoreNH3 = (x) => (x <= 0 ? 100 : x >= 1 ? 0 : 100 * (1 - x ** 2) ** 30);

    // generic body
    const ramp = (lo, hi, pow) => (x) =>
        x <= lo ? 100 : x >= hi ? 0 : 100 * (1 - ((x - lo) / (hi - lo)) ** 2) ** pow;

    const scoreNO3 = ramp(0.47, 1.5, 4);
    const scoreCl = ramp(6, 19, 4);
    const scoreTur = ramp(1.1, 23, 1.54);
    const scoreEC = ramp(52.1, 151.2, 6);

    function computeWPI([pH, DO, NO3, NH3, Cl, Tur, EC, T]) {
        const q = [
            scorePH(validate('pH', pH, 0, 14)),
            scoreDO(validate('DO', DO, 0, 25), validate('Temperature', T, 0, 40)),
            scoreNO3(validate('Nitrate N', NO3, 0, 50)),
            scoreNH3(validate('Ammonia N', NH3, 0, 20)),
            scoreCl(validate('Chloride', Cl, 0, 1000)),
            scoreTur(validate('Turbidity', Tur, 0, 10000)),
            scoreEC(validate('Conductivity', EC, 0, 5000)),
        ];
        return 100 - q.reduce((acc, qp, i) => acc * Math.max(qp, 1) ** WEIGHTS[i], 1);
    }

    async function runCalculation() {
        calculateError = '';
        calculated = null;
        try {
            calculated = computeWPI(values);
        } catch (e) {
            calculateError = e.message;
        }
    }

    function reset() {
        values = [...DEFAULTS];
        calculated = null;
        calculateError = '';
    }
</script>

<NavBar />

<Area>
    <h1>WPI Calculation</h1>
    <p class="mb-8 leading-relaxed">
        Calculate a determinisitic WPI using the Zaquares WPI (ZPI) model from a full list of parameters, including potential of Hydrogen (pH), Dissolved Oyxgen, Nitrate N, Ammonia N, Chloride, Turbidity, Electric Conductivity, and Temperature.
    </p>

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
                    class="w-28 rounded-md border border-[var(--accent3)] px-3 py-1.5 text-sm text-left font-mono
                           focus:border-[var(--accent2)] focus:outline-none focus:ring-1 focus:ring-slate-500
                           disabled:bg-slate-100 disabled:text-slate-400"
                />
            </div>
        {/each}
    </div>

    <div class="flex items-center gap-3 mt-6">
        <button
            onclick={runCalculation}
            class="rounded-md bg-[var(--accent2)] px-4 py-2 text-sm font-medium text-white
                   hover:bg-[var(--accent)] active:bg-[var(--accent2)] transition-colors"
        >
            Calculate
        </button>
        <button
            onclick={reset}
            class="rounded-md border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700
                   hover:bg-slate-50 active:bg-slate-100 transition-colors"
        >
            Reset
        </button>
    </div>

    {#if calculateError}
        <div class="mt-6 rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">
            {calculateError}
        </div>
    {/if}

    {#if calculated !== null}
        <div class="mt-8 border border-[var(--accent3)] bg-gradient-to-br from-slate-50 to-white p-6 shadow-sm">
            <div class="text-xs uppercase tracking-wider text-slate-500 mb-1">
                Calculated WPI
            </div>
            <div class="text-4xl font-bold tabular-nums text-slate-900">
                {calculated.toFixed(2)}
            </div>
        </div>
    {/if}
</Area>

<Footer />


