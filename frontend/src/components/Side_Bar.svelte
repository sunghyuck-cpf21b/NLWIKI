<script>
    import {fastapi} from "../lib/api";
    import { username, is_login } from '../lib/store'

    let personal_memo
    let isit_memo = false
    async function get_personal_memo() {
        const url = '/api/memo/personal/detail'
        await fastapi('get', url, {},
            (json)=>{
                if (json) {
                    isit_memo = true
                    personal_memo = json.content
                }
            }
        )
    }
    if ($is_login) {get_personal_memo()}

    async function post_personal_memo(content) {
        const url = '/api/memo/personal/create'
        const params = {
            content: content,
        }
        await fastapi('post', url, params, 
            (json)=>{}
        )
    }
    
    async function update_personal_memo(content) {
        const url = '/api/memo/personal/update'
        const params = {
            content: content,
        }
        await fastapi('put', url, params, 
            (json)=>{}
        )
    }
    async function on_BL() {
        const content = event.target.innerHTML
        if (isit_memo) {await update_personal_memo(content)}
        else {await post_personal_memo(content)}
        await get_personal_memo()
    }
    async function input_enter() {
        if (event.key === 'Enter') {
            const content = event.target.innerHTML
        if (isit_memo) {await update_personal_memo(content)}
        else {await post_personal_memo(content)}
        }
    }
</script>


<div class='sidebar'>
    <img src="https://noonnucc-production.sfo2.cdn.digitaloceanspaces.com/202308/1692878523978236.jpeg" 
    alt='' style='width: 100%;'>
    {#if isit_memo}
    <!--svelte-ignore a11y-no-static-element-interactions-->
    <div class='personal_memo' contenteditable="true"
    on:blur={()=>{on_BL()}} on:keydown={()=>{input_enter()}}>
        {@html personal_memo}
    </div>
    {:else}
    <!--svelte-ignore a11y-no-static-element-interactions-->
    <div class='personal_memo' contenteditable="true"
    on:blur={()=>{on_BL()}} on:keydown={()=>{input_enter()}}>
    </div>
    {/if}
</div> 

<style>
    .sidebar {
        border: 1px solid; 
        height: 500px;
        overflow: scroll;
    }
    .personal_memo {
        width: 100%;
        min-height: 100%;
        padding: 5px;
        font-size: 14px;
    }
</style>