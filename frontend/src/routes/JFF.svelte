<script>
    import { fastapi } from "../lib/api";


    let img_data
    let data_ready = false
    let x_limit
    let y_limit
    const dp_ratio = 5

    function b64_to_data(b64) {
        return 'data:image/png;base64,'+b64
    }

    function get_dp_image() {
        const url = '/api/jff/dp_image'
        
        fastapi('get', url, {}, 
            (json)=>{
                img_data = b64_to_data(json.image_data)
                data_ready = true
                x_limit = json.x_limit
                y_limit = json.y_limit
            }
        )
    }
    get_dp_image()

    async function create_dot(x, y, color) {
        const url = '/api/jff/create_dot'
        const params = {
            x: x,
            y: y,
            color: color,
        }
        console.log(params)
        await fastapi('post', url, params, 
            (json)=>{
                get_dp_image()
            }
        )
    }

/*
    {#if data_ready}
    <img class='dp_image'
    src={img_data} alt='' style='width: 500px; height: 500px;'>
    {/if}

*/
// table 방식 렌더링하는데 시간이 좀 걸리는듯
// 좌표 변수를 정하고 div 태그를 움직이는 방식으로 바꿔야할 수도
    let dp_mouse_hover = [-1,-1]
    let dp_position = [-1,-1]
    $: console.log(dp_position)

    let dp_control_ready = false

    function dp_click() {
        if (event.target.closest('.jff_box')) {
            dp_control_ready = true

        } else {
            dp_control_ready = false
            return
        }
        const jff_box_pos = event.target.closest('.jff_box').getBoundingClientRect()
        const click_tag = event.target
        const click_tag_pos = click_tag.getBoundingClientRect()
        const x_pos = Math.floor((click_tag_pos.x - jff_box_pos.x)/dp_ratio)*dp_ratio
        const y_pos = Math.floor((click_tag_pos.y - jff_box_pos.y)/dp_ratio)*dp_ratio

        dp_position = [x_pos, y_pos]
    }
    function dp_keydown() {
        if (!dp_control_ready) {
            return
        }
        event.preventDefault()
        const key = event.key 
        if (key == 'ArrowUp') {
            if (dp_position[1] >= dp_ratio) {
                dp_position[1] = dp_position[1]-dp_ratio
            }
        }
        if (key == 'ArrowDown') {
            if (dp_position[1] <= (y_limit-2)*dp_ratio) {
                dp_position[1] = dp_position[1]+dp_ratio
            }
        }
        if (key == 'ArrowLeft') {
            if (dp_position[0] >= dp_ratio) {
                dp_position[0] = dp_position[0]-dp_ratio
            }
        }
        if (key == 'ArrowRight') {
            if (dp_position[0] <= (y_limit-2)*dp_ratio) {
                dp_position[0] = dp_position[0]+dp_ratio
            }
        }

        if (key == 'q') {
            const x = parseInt(dp_position[0]/dp_ratio)
            const y = parseInt(dp_position[1]/dp_ratio)
            const color = 'ffffff'
            create_dot(x, y, color)
        }
    }

    

//

</script>

<svelte:window 
on:click={()=>{dp_click()}} 
on:keydown={()=>{dp_keydown()}}/>



<div class='jff_box' 
style='background-image: url({img_data}); width:{x_limit*dp_ratio}px; height:{y_limit*dp_ratio}px;
background-size: cover;
image-rendering: pixelated;'>
    <div class='hover_box' style='left: {dp_position[0]}px; top: {dp_position[1]}px'></div>
    <table class='dp_pixel_table'>
        <tbody>
            {#each Array.from({length:y_limit}) as _, i}
            <tr class='dp_pixel_tr'>
                {#each Array.from({length:x_limit}) as _, j}
                <!-- svelte-ignore a11y-mouse-events-have-key-events -->
                <td class='dp_pixel_td' 
                style='
                width: {dp_ratio}px;
                height: {dp_ratio}px;
                '
                on:mouseover={()=>{dp_mouse_hover=[j, i]}}
                on:click={()=>{dp_position=[j, i]}}></td>
                {/each}
            </tr>
            {/each}
        </tbody>
    </table>

</div>

<style>
    :root {
        --jff-dp-size: 500px;
    }
    .jff_box {
        margin: auto;
        position: relative;
    }
    .hover_box {
        position: absolute;
        width: 4px;
        height: 4px;
        border: 1px solid #ffffff;
    }
    .dp_pixel_tr {
        
    }
    .dp_pixel_td {
    }
</style>