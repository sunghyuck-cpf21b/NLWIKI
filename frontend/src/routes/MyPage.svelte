<script>
    import {fastapi} from "../lib/api";
    import CalendarComp from "../components/Calendar_comp.svelte";
    import GraphComp from "../components/Graph_comp.svelte";
    import { username, is_login } from "../lib/store";

    /*
    params
    username : url로 받음

    */
    export let params = {year: year, month: month}
    let p_username = params.username

    let today = new Date()
    let year = today.getFullYear()
    let month = today.getMonth() + 1
    $: if(year, month) {
        params.year = year
        params.month = month
    }
    console.log('test page')
</script>


<div class='date_control'>
    <div class='date_select'> 
        <select bind:value={year}>
            {#each Array.from({length:5}) as _, i}
                <option>{i+2023}</option>
            {/each}
        </select>
        <select bind:value={month}>
            {#each Array.from({length:12}) as _, i}
                <option>{i+1}</option>
            {/each}
        </select>
    </div>
    <h1>{year}.{month}</h1>
</div>



<CalendarComp params={params}/>
<GraphComp params={params}/>




<style>

    .date_control {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 300px;
        margin: 50px auto;
    }
    
</style>