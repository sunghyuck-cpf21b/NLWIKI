<script>
    import { Chart, registerables } from 'chart.js'
    import { onMount } from 'svelte';
    import fastapi from '../lib/api';
    import * as my_func from "../lib/my_func";

    import { findBestMatch } from 'string-similarity';

    // 공백없는 길이가 동일하고 유사도가 높은 종목 이어주는 기능 만들기
    // 알림으로 띄우거나 사이드에 보여주는 식으로?
    
    // 외부 입력 변수
    export let params = {}
    

    Chart.register(...registerables)

    // 그래프를 위한 초기 데이터 생성
    let data = {}
    let options = {
        responsive: true,
        scales: {
            x: {
                type: 'category',
                stacked: true,
                offset: true,
                grid: {
                    display: false,
                }
            },
            y1: {
                stacked: true,
                beginAtZero: true,
                position: 'left',
                grid: {
                    display: false,
                },
            },
            y2: {
                beginAtZero: true,
                position: 'right',
                grid: {
                    display: false
                },
                
            }
        },
        plugins: {
            legend: {display: false},
            tooltip: {
                enable: true,
                callbacks: {
                    label: function(context) {
                        let dataset = data['datasets'][context.datasetIndex]
                        let tooltip = dataset.tooltips 
                        return tooltip || context.raw
                    },   
                    footer: function(tooltipitems) {
                        if (tooltipitems[0].dataset.type === 'bar') {
                            let y_value_list = Object.values(tooltipitems[0].parsed._stacks.y._visualValues)
                            let total = 0 
                            y_value_list.forEach(y => {
                                total += y
                            })
                            return '    Total = ' + total
                        }
                    }  
                }
            }
            
        }
    }
    
    let chartConfig = {
        //type: 'bar',
        data: {},
        options: options 
    }
    let canvas;
    let chart;
    onMount(()=>{
        const ctx = canvas.getContext('2d')
        chart = new Chart(ctx, chartConfig)
    })

    let name_list = []
    $: selected_name_list = [...name_list]

    function init_data_maker(DS, WR) { // DS: datasets, WR: weight_range // 백엔드 데이터를 chartjs에서 사용 가능한 형태로 가공

        let color_dict = {}
        name_list.forEach((n, i)=>{
            color_dict[n] = (360/name_list.length)*i
        })
        let bar_result = []
        let sct_result = []
        let B_range = [20, 80]
        const seen_points = new Map // 겹치는 scatter를 판단하기 위한 Map 객체
        const duplicate_weight = new Map // sct 에서 불필요한 중복을 방지하기 위함 Map 객체
        const Max_value = new Map // 누적 최대값을 찾기 위한 Map 객체
        for (const d of DS) {
            let weight_range = WR[d['tooltip'][0]]
            let BR = 50
            if (weight_range[0] !== weight_range[1]) {
                BR = B_range[1] - 
                Math.abs((weight_range[0]-d['color']) / (weight_range[0]-weight_range[1]))*(B_range[1]-B_range[0])
            }
            const dv_key = d['x']
            let dataset_bar = { // bar 그래프 데이터셋
                type: 'bar',
                label: d['tooltip'][0],
                data: [{x: d['x'], y: d['y']}],
                xAxisID: 'x',
                yAxisID: 'y1',
                barPercentage: 0.8,
                categoryPercentage: 1.0,
                backgroundColor: `hsl(${color_dict[d['tooltip'][0]]}, 100%, ${BR}%, 50%)`,
                borderColor: `hsl(${color_dict[d['tooltip'][0]]}, 100%, ${BR}%, 70%)`,
                borderWidth: 2,
                order: 2,
                tooltips: d['tooltip'],
                hidden: data_type_hidden['bar'],
            }
            bar_result.push(dataset_bar)


            const sct_rad_key = `${d['x']}-${d['color']}`
            let point_rad = 3
            if (seen_points.has(sct_rad_key)) {
                const count = seen_points.get(sct_rad_key)
                seen_points.set(sct_rad_key, count+2)
                point_rad = point_rad + count
                console.log('sct', count)
            } else {
                seen_points.set(sct_rad_key, 2) // 겹치는 포인트는 2px만큼 커짐
            }
            const dup_key = `${d['x']}-${d['tooltip'][0]}-${d['color']}`
            if (!duplicate_weight.has(dup_key)) { // 날짜, 종목, 중량이 다른 경우에만 sct 데이터를 추가
                // 중량별로 횟수나 세트가 다른 경우에, 서로 다른 볼륨으로 인식하도록 만들었기 때문에 이 조건을 제외시키면 겹치는 sct point가 많아짐
                duplicate_weight.set(dup_key, 'exist!')
                let dataset_sct = { // scatter 그래프
                    type: 'scatter',
                    label: d['tooltip'][0],
                    data: [{x: d['x'], y: d['color']}],
                    xAxisID: 'x',
                    yAxisID: 'y2',
                    backgroundColor: `hsl(${color_dict[d['tooltip'][0]]}, 100%, 50%, 70%)`,
                    borderColor: `hsl(${color_dict[d['tooltip'][0]]}, 100%, 0%, 100%)`,
                    borderWidth: 0.5,
                    pointRadius: point_rad,
                    order: 1,
                    tooltips: [d['tooltip'][0], d['tooltip'][1].split('x ')[2]],
                    hidden: data_type_hidden['scatter'],
                }
                sct_result.push(dataset_sct)
            }

            const Max_value_key = d['x']
            if (Max_value.has(Max_value_key)) {
                const value = Max_value.get(Max_value_key)
                Max_value.set(Max_value_key, value + d['y'])
            } else {
                Max_value.set(Max_value_key, d['y'])
            }


        }
        let max_volume = Math.max(...Max_value.values())
        if (chart) { // volume 최대값에 맞춰서 y1축 상한을 5000단위로 올림
            //chart.options.scales.y1.max = Math.ceil(max_volume/5000)*5000
            //chart.update()
        }
        return [bar_result, sct_result]
    }

    let labels = []
    let datasets_bar = []
    let datasets_sct = []
    let data_check = false 
    async function get_overload_data({name_list, date_limit, weight_limit, wk_list, username}) { // api 통신 
        const url = '/api/sep_program/overload_data'
        const params = new URLSearchParams()
        // 리스트형 정보를 전송할 때 필요한 url 변환방식인데
        // api.js에 포함시킬지 고민해보기 
        /*
        const params = {
            key_1 : value_1,
        }
        => 
        api_params.append(String(Object.keys(params)), Object.values(params))
        이런식으로 변환해서 사용하기
        */
        if (!name_list.length) {name_list = ['']}
        name_list.forEach(n =>{
            params.append('name_list', n)
        })
        date_limit.forEach(d =>{
            params.append('date_limit', d)
        })
        weight_limit.forEach(d =>{
            params.append('weight_limit', d)
        }) 
        wk_list.forEach(wk =>{
            params.append('wk_list', wk)
        })
        params.append('username', username)
        const tt = params.toString() // temp_url
        const ff = tt ? `${url}?${tt}` : url // full_url

        await fastapi('get', ff, {},
            (json)=>{
                labels = json.labels 
                const total_datasets = init_data_maker(json.data, json.weight_range)
                datasets_bar = total_datasets[0]
                datasets_sct = total_datasets[1]
                data_check = true
            }
        )
    }



    let weight_limit = [0, 10000]
    let date_limit = ['2000-01-01', '2030-01-01']
    let wk_list = ['kg', 'kg']

    $: get_overload_data({name_list:selected_name_list, date_limit: date_limit, 
        weight_limit: weight_limit, wk_list: wk_list, username: params.username})






    let all_ex = []
    function get_all_ex() {
        const url = '/api/sep_program/all_ex'
        fastapi('get', url, {},
            (json)=>{
                all_ex = json
            }
        )
    }
    get_all_ex()

 

    $: if(data_check) { // 초기 데이터 생성
        data = {
            labels: labels,
            datasets: [...datasets_bar, ...datasets_sct],
        }
        if (chart) {
            chart.data = data 
            chart.update()
        }
        data_check = false
    }

    let exercise_select = {}
    $: if (name_list.length) { // 토글버튼을 위한 딕셔너리 생성
        name_list.forEach((n)=>{
            
            exercise_select[n] = false
        })
    }
    function name_list_push(value) {
        let name = ''
        let input_tag = document.getElementById('name_list_element')
        if (!value) {
            name = input_tag.value
        } else {
            name = value
        }
        input_tag.value = ''
        exercise_similar_list = []
        similar_list_show = false
        if (name.length && all_ex.includes(name) && !name_list.includes(name)) {
            if (!name_list.length) {
                name_list[0] = name
                name_list = [...name_list]
            } else {
                name_list.push(name)
                name_list = [...name_list]
                date_limit = [...date_limit, ...['2000-01-01','2030-01-01']]
                weight_limit = [...weight_limit, ...[0, 10000]]
                wk_list = [...wk_list, ...['kg','kg']]
            }
        }
    }
    function name_list_delete(name, i) {
        name_list.splice(i, 1)
        name_list = [...name_list]
    }

    function weight_limit_push(i) {
        const lower = document.getElementById(`weight_lower_${i}`).value
        const upper = document.getElementById(`weight_upper_${i}`).value
        const lower_wk = document.getElementById(`wk_lower_${i}`).value
        const upper_wk = document.getElementById(`wk_upper_${i}`).value
        if (lower) {weight_limit[2*i]=lower} else {weight_limit[2*i]=0}
        if (upper) {weight_limit[2*i+1]=upper} else {weight_limit[2*i+1]=10000}
        weight_limit = [...weight_limit] 
        wk_list[2*i] = lower_wk; wk_list[2*i+1] = upper_wk;
        wk_list = [...wk_list]
        console.log(weight_limit, wk_list)
    }
    function date_limit_push(i) {
        const lower = document.getElementById(`date_lower_${i}`).value
        const upper = document.getElementById(`date_upper_${i}`).value
        if (lower) {date_limit[2*i]=lower}
        if (upper) {date_limit[2*i+1]=upper}
        date_limit = [...date_limit]
        console.log(date_limit)
    }

    function name_list_reconstruct(name, i) { // 토글기능에 반응하여 datasets을 재구성하는 함수
        if (exercise_select[name]) {
            selected_name_list[i] = ''
        } else {
            selected_name_list[i] = name
        }
    }


    let data_type_hidden = {'bar': false, 'scatter': false} // hidden: false 로 해야 보임
    function change_hidden(key) {
        data_type_hidden[key] = !data_type_hidden[key]
        data.datasets.forEach(d=>{
            if (d.type===key) {
                d.hidden = data_type_hidden[key]
            }
        })
        chart.update()
    }

    
    let exercise_similar_list = []
    let similar_list_show = false 
    function make_similar_start(event) { // 유사한 운동 이름 
        let text = event.target.value
        let MS_list = my_func.make_similar(text, all_ex)
        console.log(MS_list)
        exercise_similar_list = MS_list[0]
        similar_list_show = MS_list[1]
    }

</script>

<div class='graph_comp'>
    <div class='graph_buttons'>
        <button on:click={()=>{change_hidden('bar')}} 
            style='{data_type_hidden['bar'] ? 'opacity:0.1':'opacity:1'}'>bar</button>
        <button on:click={()=>{change_hidden('scatter')}}
            style='{data_type_hidden['scatter'] ? 'opacity:0.1':'opacity:1'}'>sct</button>


        {#each name_list as name, i}
        <button 
        on:click={()=>{exercise_select[name] = !exercise_select[name]; name_list_reconstruct(name, i)}}
        style='
        background-color: hsl({(360/name_list.length)*i}, 100%, 50%, 30%);
        border: 3px solid hsl({(360/name_list.length)*i}, 100%, 50%, 70%);
        {exercise_select[name] ? 'opacity:0.1':'opacity:1'}'>
            {name}
        </button>
        {/each}

        <div class='exercises_list'>
            {#each name_list as name, i}
                <p>
                    {name}
                    <a href='/' on:click|preventDefault={()=>{name_list_delete(name, i)}}>x</a>
                </p>
            {/each}
        </div>
    </div>



    <div class='chart_box'>
        <!-- 그래프 -->
        <canvas id='chart' width='1200' height='600' bind:this={canvas}></canvas>
    </div>
    <!-- 그래프 정보 -->
    <div class='graph_info_box'>
        <div class='appended_list'>
            {#each name_list as name, i}
            <div class='info_box'>
                <div class='name_control_box'>
                    <a href='/' on:click|preventDefault={()=>{name_list_delete(name, i)}}>x</a>
                    {name}<br>
                    {weight_limit[2*i]} {wk_list[2*i]} ~ {weight_limit[2*i+1]} {wk_list[2*i+1]} <br>
                    {date_limit[2*i]} ~ {date_limit[2*i+1]}
                </div>
                <div class='limit_box'>
                        <div class='weight_limit_input_box'>
                            <input type='number' id='weight_lower_{i}' class='limit_input' placeholder="lower">
                            <input type='number' id='weight_upper_{i}' class='limit_input' placeholder="upper">
                        </div>
                        <div class='limit_wk_box'>
                            <select id='wk_lower_{i}' class='limit_wk'><option>kg</option><option>lbs</option></select>
                            <select id='wk_upper_{i}' class='limit_wk'><option>kg</option><option>lbs</option></select>
                        </div>
                        <button class='weight_apply' on:click={()=>{weight_limit_push(i)}}>적용</button>

                        <div class='date_limit_input_box'>
                            <input type='date' id='date_lower_{i}' class='limit_input' placeholder="date lower">
                            <input type='date' id='date_upper_{i}' class='limit_input' placeholder="date upper">
                        </div>
                        <button class='date_apply' on:click={()=>{date_limit_push(i)}}>적용</button>

                </div>
            </div>
            {/each}
        </div>

        <div class='graph_info'>
            <!-- 나중에 이거를 각 운동마다 적용해보기 -->
            <div class='name_list'>
                <input id='name_list_element'
                autocomplete="off"
                on:input={()=>{make_similar_start(event)}}> 
                <br>
                <button on:click={()=>{name_list_push()}}>추가</button>
            </div>
            <div class='similar_list'>
                {#if similar_list_show}
                <ul>
                    {#each exercise_similar_list as e}
                    <li>
                        <a href='/' on:click|preventDefault={()=>{name_list_push(e)}}>{e}</a>
                    </li>
                    {/each}
                </ul>
                {/if}
            </div>
        </div>
    </div>
</div>




<style>
    /* calc() => 변수명을 넣어도 됨*/
        :root {
        --limit-margin: 1px;
    }

    .graph_comp {
        display: grid;
        grid-template-areas: 
        'btns .'
        'chart info';
        gap: 30px;
        width: 80%;
        margin: 50px;
    }
    .graph_buttons {
        grid-area: btns;
    }
    .chart_box {
        grid-area: chart;
    }
    .graph_info_box {
        grid-area: info;
        margin-left: 10px;
        width: 400px;
        padding: 5px;
        border: 1px solid #ffffff;
        display: flex;
        flex-direction: column;
        justify-content: space-between;

    }
    .exercises_list > p {
        display: inline-block;
        border: 1px solid #ffffff;
        font-size: 10px;
        padding: 2px 3px;
        padding-right: 15px;
    }
    .info_box {
        display: grid;
        grid-template-columns: 1.6fr 1fr;
        grid-template-areas: 
        'name_box limit_box';
        border: 1px solid #ffffff;
    }
    .graph_info {
        border: 1px solid #ffffff;
        height: 150px;
        display: flex;
        justify-content: space-around;
        align-items: center;
    }
    .name_list {
        border: 1px solid #ffffff;
        width: 40%;
        height: 90%;
    }
    #name_list_element {
        width: 100px;
    }
    .name_control_box {
        grid-area: name_box;
        font-size: 15px;
    }
	.limit_box {
		border: 1px solid;
		margin: 5px;
		display: grid;
        grid-auto-columns: 70px 60px 60px;
		grid-template-areas: 
			'weight wk wa'
			'date date da';
	}
	.limit_box > div {
		display: flex;
		flex-direction: column;
	}
	.weight_limit_input_box {
		grid-area: weight;
	}
	.date_limit_input_box {
		grid-area: date;
	}
	.limit_wk_box {
		grid-area: wk;
	}
    .weight_limit_input_box > *, .date_limit_input_box > *, .limit_wk_box > * {
        margin: var(--limit-margin);
    }
    .weight_limit_input_box, .date_limit_input_box, .limit_wk_box {
        /*border: 1px solid;*/
		margin: calc(var(--limit-margin)*2);
        display: flex;
        flex-direction: column;
        justify-content: space-around;
    }
	.weight_apply {
		grid-area: wa;
	}
	.date_apply {
		grid-area: da;
	}
    .weight_apply, .date_apply {
        /*border: 1px solid;*/
		margin: calc(var(--limit-margin)*2);
    }
    .weight_apply, .date_apply {
        font-size: 12px;
    }

    .similar_list {
        border: 1px solid #ffffff;
        display: inline-block;
        width: 55%;
        height: 90%;
        font-size: 13px;
        text-align: left;
        overflow: auto;
    }
    .similar_list > ul {
        margin: 0 auto;
        padding: 0;
    }
    .similar_list li {
        border: 1px solid #ffffff;
        list-style-type: none;
        height: 22px;
    }
    .similar_list a {
        color: #ffffff;
    }
    
</style>